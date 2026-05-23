#property copyright "OpenAI Codex"
#property link      "https://openai.com"
#property version   "1.04"
#property strict

#include <Trade/Trade.mqh>

input bool   EnableTrading                  = true;
input bool   NewsStopMode                   = false;
input int    JSTOffsetHours                 = 7;
input bool   RequireJPYAccount              = true;
input long   MagicNumber                    = 25052101;
input double LotSize                        = 0.01;
input double StopLossPips                   = 15.0;
input double TakeProfitPips                 = 22.0;
input double MaxSpreadPips                  = 0.5;
input int    SpreadCooldownMinutes          = 15;
input int    MaxTradesPerDay                = 2;
input int    MaxConsecutiveLossesPerDay     = 2;
input double DailyLossLimitJPY              = 1000.0;
input double WeeklyLossLimitJPY             = 3000.0;
input double MonthlyLossLimitJPY            = 8000.0;
input double EmergencyFloatingLossLimitJPY  = 1000.0;
input int    MaxHoldingMinutes              = 180;
input int    TradeStartHourJST              = 21;
input int    TradeEndHourJST                = 24;
input int    FridayNoEntryAfterHourJST      = 23;
input bool   ClosePositionsOnFriday         = true;
input int    FridayCloseHourJST             = 23;
input double PullbackTolerancePips          = 3.0;
input double MinATRPips                     = 4.0;
input double MaxStrategyStopLossPips        = 15.0;
input int    SlippagePoints                 = 20;
input int    ManagementTimerSeconds         = 30;
input string OrderComment                   = "USDJPY_EMA_RiskGuard";

const string TARGET_SYMBOL = "USDJPY";

CTrade   g_trade;
bool     g_symbol_allowed       = true;
datetime g_last_m15_bar_time    = 0;
datetime g_last_spread_block_time = 0;

int g_handle_h1_ema20 = INVALID_HANDLE;
int g_handle_h1_ema50 = INVALID_HANDLE;
int g_handle_m15_ema20 = INVALID_HANDLE;
int g_handle_m15_atr14 = INVALID_HANDLE;

struct RiskSnapshot
{
   int    trades_today;
   int    consecutive_losses_today;
   int    max_consecutive_losses_today;
   double daily_pnl;
   double weekly_pnl;
   double monthly_pnl;
   bool   daily_loss_limit_hit;
   bool   weekly_loss_limit_hit;
   bool   monthly_loss_limit_hit;
   bool   consecutive_loss_limit_hit;
};

struct MarketSnapshot
{
   MqlRates m15_bar_1;
   MqlRates m15_bar_2;
   double   h1_close;
   double   h1_ema20;
   double   h1_ema50;
   double   m15_ema20;
   double   m15_atr14;
   double   spread_pips;
};

struct ClosedDealSnapshot
{
   datetime deal_time_jst;
   ulong    position_id;
   double   net_profit;
   bool     closed_today;
};

double PipSize();
datetime ToJst(const datetime server_time);
int DayKey(const datetime jst_time);
int WeekKey(const datetime jst_time);
int MonthKey(const datetime jst_time);
int MinutesOfDay(const datetime jst_time);
int ClampInt(const int value, const int min_value, const int max_value);
int VolumeDigitsFromStep(const double step);
string AccountCurrencyLabel();
bool GetCurrentTick(MqlTick &tick, string &reason);
bool IsWithinTradeWindow(const datetime jst_time);
bool IsFridayEntryBlocked(const datetime jst_time);
bool ShouldForceFridayClose(const datetime jst_time);
bool SelectManagedPosition(ulong &ticket);
int CountManagedPositions();
int CountSymbolPositions();
bool BuildRiskSnapshot(RiskSnapshot &snapshot);
bool LoadMarketSnapshot(MarketSnapshot &snapshot, string &reason);
bool CanOpenNewTrade(const MarketSnapshot &snapshot, RiskSnapshot &risk, string &reason);
bool EvaluateBuySignal(const MarketSnapshot &snapshot, string &reason);
bool EvaluateSellSignal(const MarketSnapshot &snapshot, string &reason);
bool ValidateVolume(double &volume, string &reason);
bool PrepareOrderPrices(const ENUM_ORDER_TYPE order_type, double &entry_price, double &stop_loss, double &take_profit, string &reason);
bool PlaceEntryOrder(const ENUM_ORDER_TYPE order_type, const string entry_reason, const MarketSnapshot &snapshot);
void ManageManagedPosition();
bool CloseManagedPosition(const string close_reason);
void CloseAllManagedPositions(const string close_reason);
void ProcessNewM15Bar();
double NetDealProfit(const ulong deal_ticket);
void LogBlock(const string reason);
string FormatIndicatorSummary(const MarketSnapshot &snapshot);
bool ValidateInputs(string &reason);

int OnInit()
{
   string validation_reason = "";
   if(!ValidateInputs(validation_reason))
   {
      PrintFormat("[INIT] Parameter validation failed: %s", validation_reason);
      return(INIT_PARAMETERS_INCORRECT);
   }

   g_trade.SetExpertMagicNumber((ulong)MagicNumber);
   g_trade.SetDeviationInPoints(SlippagePoints);
   g_trade.SetTypeFillingBySymbol(_Symbol);

   if(_Symbol != TARGET_SYMBOL)
   {
      g_symbol_allowed = false;
      PrintFormat("[INIT] Safety lock: %s is not supported. Attach this EA only to %s.", _Symbol, TARGET_SYMBOL);
      return(INIT_SUCCEEDED);
   }

   g_handle_h1_ema20 = iMA(_Symbol, PERIOD_H1, 20, 0, MODE_EMA, PRICE_CLOSE);
   g_handle_h1_ema50 = iMA(_Symbol, PERIOD_H1, 50, 0, MODE_EMA, PRICE_CLOSE);
   g_handle_m15_ema20 = iMA(_Symbol, PERIOD_M15, 20, 0, MODE_EMA, PRICE_CLOSE);
   g_handle_m15_atr14 = iATR(_Symbol, PERIOD_M15, 14);

   if(g_handle_h1_ema20 == INVALID_HANDLE ||
      g_handle_h1_ema50 == INVALID_HANDLE ||
      g_handle_m15_ema20 == INVALID_HANDLE ||
      g_handle_m15_atr14 == INVALID_HANDLE)
   {
      PrintFormat("[INIT] Indicator handle creation failed. h1ema20=%d h1ema50=%d m15ema20=%d m15atr14=%d",
                  g_handle_h1_ema20,
                  g_handle_h1_ema50,
                  g_handle_m15_ema20,
                  g_handle_m15_atr14);
      return(INIT_FAILED);
   }

   if(!EventSetTimer(ManagementTimerSeconds))
   {
      PrintFormat("[INIT] EventSetTimer failed. error=%d. Position management will still run on ticks.", GetLastError());
   }

   PrintFormat("[INIT] %s started on %s. PipSize=%.5f JSTOffsetHours=%d MagicNumber=%I64d",
               OrderComment,
               _Symbol,
               PipSize(),
               JSTOffsetHours,
               MagicNumber);

   string account_currency = AccountInfoString(ACCOUNT_CURRENCY);
   if(account_currency != "JPY")
   {
      if(RequireJPYAccount)
      {
         PrintFormat("[INIT] Safety: account currency is %s. New entries will be blocked because RequireJPYAccount is true.",
                     account_currency);
      }
      else
      {
         PrintFormat("[INIT] Warning: account currency is %s. Loss limit inputs are named JPY and are evaluated in account currency.",
                     account_currency);
      }
   }

   return(INIT_SUCCEEDED);
}

void OnDeinit(const int reason)
{
   EventKillTimer();

   if(g_handle_h1_ema20 != INVALID_HANDLE)
      IndicatorRelease(g_handle_h1_ema20);
   if(g_handle_h1_ema50 != INVALID_HANDLE)
      IndicatorRelease(g_handle_h1_ema50);
   if(g_handle_m15_ema20 != INVALID_HANDLE)
      IndicatorRelease(g_handle_m15_ema20);
   if(g_handle_m15_atr14 != INVALID_HANDLE)
      IndicatorRelease(g_handle_m15_atr14);

   PrintFormat("[DEINIT] %s stopped. reason=%d", OrderComment, reason);
}

void OnTimer()
{
   if(!g_symbol_allowed)
      return;

   ManageManagedPosition();
}

void OnTick()
{
   if(!g_symbol_allowed)
      return;

   ManageManagedPosition();

   datetime current_m15_bar_time = iTime(_Symbol, PERIOD_M15, 0);
   if(current_m15_bar_time == 0)
      return;

   if(current_m15_bar_time == g_last_m15_bar_time)
      return;

   g_last_m15_bar_time = current_m15_bar_time;
   ProcessNewM15Bar();
}

void ProcessNewM15Bar()
{
   MarketSnapshot snapshot;
   string market_reason = "";
   if(!LoadMarketSnapshot(snapshot, market_reason))
   {
      LogBlock(market_reason);
      return;
   }

   RiskSnapshot risk;
   string gate_reason = "";
   if(!CanOpenNewTrade(snapshot, risk, gate_reason))
   {
      LogBlock(gate_reason);
      return;
   }

   string buy_reason = "";
   if(EvaluateBuySignal(snapshot, buy_reason))
   {
      PlaceEntryOrder(ORDER_TYPE_BUY, buy_reason, snapshot);
      return;
   }

   string sell_reason = "";
   if(EvaluateSellSignal(snapshot, sell_reason))
   {
      PlaceEntryOrder(ORDER_TYPE_SELL, sell_reason, snapshot);
      return;
   }

   PrintFormat("[NO_ENTRY] No valid setup. buy_check=%s | sell_check=%s | %s",
               buy_reason,
               sell_reason,
               FormatIndicatorSummary(snapshot));
}

double PipSize()
{
   if(_Digits == 3 || _Digits == 5)
      return(_Point * 10.0);
   return(_Point);
}

datetime ToJst(const datetime server_time)
{
   return(server_time + JSTOffsetHours * 3600);
}

int DayKey(const datetime jst_time)
{
   MqlDateTime parts;
   TimeToStruct(jst_time, parts);
   return(parts.year * 10000 + parts.mon * 100 + parts.day);
}

int MonthKey(const datetime jst_time)
{
   MqlDateTime parts;
   TimeToStruct(jst_time, parts);
   return(parts.year * 100 + parts.mon);
}

int WeekKey(const datetime jst_time)
{
   MqlDateTime parts;
   TimeToStruct(jst_time, parts);

   datetime start_of_day = jst_time - (parts.hour * 3600 + parts.min * 60 + parts.sec);
   int monday_based_offset = (parts.day_of_week + 6) % 7;
   datetime start_of_week = start_of_day - monday_based_offset * 86400;
   return(DayKey(start_of_week));
}

int MinutesOfDay(const datetime jst_time)
{
   MqlDateTime parts;
   TimeToStruct(jst_time, parts);
   return(parts.hour * 60 + parts.min);
}

int ClampInt(const int value, const int min_value, const int max_value)
{
   if(value < min_value)
      return(min_value);
   if(value > max_value)
      return(max_value);
   return(value);
}

int VolumeDigitsFromStep(const double step)
{
   double scaled_step = step;
   int digits = 0;

   while(digits < 8 && MathAbs(scaled_step - MathRound(scaled_step)) > 0.00000001)
   {
      scaled_step *= 10.0;
      digits++;
   }

   return(digits);
}

string AccountCurrencyLabel()
{
   string currency = AccountInfoString(ACCOUNT_CURRENCY);
   if(currency == "")
      return("account currency");
   return(currency);
}

bool GetCurrentTick(MqlTick &tick, string &reason)
{
   reason = "";

   if(!SymbolInfoTick(_Symbol, tick))
   {
      reason = "Market tick data is unavailable.";
      return(false);
   }

   if(tick.bid <= 0.0 || tick.ask <= 0.0 || tick.ask < tick.bid)
   {
      reason = StringFormat("Invalid tick data. bid=%.5f ask=%.5f.", tick.bid, tick.ask);
      return(false);
   }

   return(true);
}

bool IsWithinTradeWindow(const datetime jst_time)
{
   int start_minutes = ClampInt(TradeStartHourJST, 0, 23) * 60;
   int end_minutes = ClampInt(TradeEndHourJST, 1, 24) * 60;
   int current_minutes = MinutesOfDay(jst_time);

   if(end_minutes == start_minutes)
      return(false);

   if(end_minutes > start_minutes)
      return(current_minutes >= start_minutes && current_minutes < end_minutes);

   return(current_minutes >= start_minutes || current_minutes < end_minutes);
}

bool IsFridayEntryBlocked(const datetime jst_time)
{
   MqlDateTime parts;
   TimeToStruct(jst_time, parts);
   if(parts.day_of_week != 5)
      return(false);

   return(MinutesOfDay(jst_time) >= ClampInt(FridayNoEntryAfterHourJST, 0, 23) * 60);
}

bool ShouldForceFridayClose(const datetime jst_time)
{
   if(!ClosePositionsOnFriday)
      return(false);

   MqlDateTime parts;
   TimeToStruct(jst_time, parts);
   if(parts.day_of_week != 5)
      return(false);

   return(MinutesOfDay(jst_time) >= ClampInt(FridayCloseHourJST, 0, 23) * 60);
}

int CountManagedPositions()
{
   int count = 0;
   for(int index = PositionsTotal() - 1; index >= 0; --index)
   {
      ulong ticket = PositionGetTicket(index);
      if(ticket == 0 || !PositionSelectByTicket(ticket))
         continue;

      string symbol = PositionGetString(POSITION_SYMBOL);
      long magic = PositionGetInteger(POSITION_MAGIC);
      if(symbol == TARGET_SYMBOL && magic == MagicNumber)
         count++;
   }
   return(count);
}

int CountSymbolPositions()
{
   int count = 0;
   for(int index = PositionsTotal() - 1; index >= 0; --index)
   {
      ulong ticket = PositionGetTicket(index);
      if(ticket == 0 || !PositionSelectByTicket(ticket))
         continue;

      string symbol = PositionGetString(POSITION_SYMBOL);
      if(symbol == TARGET_SYMBOL)
         count++;
   }
   return(count);
}

bool SelectManagedPosition(ulong &ticket)
{
   ticket = 0;

   for(int index = PositionsTotal() - 1; index >= 0; --index)
   {
      ulong candidate = PositionGetTicket(index);
      if(candidate == 0 || !PositionSelectByTicket(candidate))
         continue;

      string symbol = PositionGetString(POSITION_SYMBOL);
      long magic = PositionGetInteger(POSITION_MAGIC);
      if(symbol == TARGET_SYMBOL && magic == MagicNumber)
      {
         ticket = candidate;
         return(true);
      }
   }
   return(false);
}

double NetDealProfit(const ulong deal_ticket)
{
   return(HistoryDealGetDouble(deal_ticket, DEAL_PROFIT) +
          HistoryDealGetDouble(deal_ticket, DEAL_SWAP) +
          HistoryDealGetDouble(deal_ticket, DEAL_COMMISSION));
}

bool BuildRiskSnapshot(RiskSnapshot &snapshot)
{
   ZeroMemory(snapshot);

   // Rebuild limits from account history so the EA remains safe after restart.
   ulong counted_entry_orders[];
   int counted_entry_order_count = 0;
   ClosedDealSnapshot todays_closed_deals[];
   int todays_closed_deal_count = 0;

   datetime now_server = TimeCurrent();
   if(!HistorySelect(0, now_server))
   {
      PrintFormat("[RISK] HistorySelect failed. error=%d", GetLastError());
      return(false);
   }

   datetime now_jst = ToJst(now_server);
   int today_key = DayKey(now_jst);
   int week_key = WeekKey(now_jst);
   int month_key = MonthKey(now_jst);

   int total_deals = HistoryDealsTotal();
   for(int index = 0; index < total_deals; ++index)
   {
      ulong deal_ticket = HistoryDealGetTicket(index);
      if(deal_ticket == 0)
         continue;

      string symbol = HistoryDealGetString(deal_ticket, DEAL_SYMBOL);
      long magic = HistoryDealGetInteger(deal_ticket, DEAL_MAGIC);
      if(symbol != TARGET_SYMBOL || magic != MagicNumber)
         continue;

      datetime deal_jst = ToJst((datetime)HistoryDealGetInteger(deal_ticket, DEAL_TIME));
      int deal_day_key = DayKey(deal_jst);
      int deal_week_key = WeekKey(deal_jst);
      int deal_month_key = MonthKey(deal_jst);
      ENUM_DEAL_ENTRY entry = (ENUM_DEAL_ENTRY)HistoryDealGetInteger(deal_ticket, DEAL_ENTRY);

      if(entry == DEAL_ENTRY_IN && deal_day_key == today_key)
      {
         // Count a partially filled entry order as one trade.
         ulong order_ticket = (ulong)HistoryDealGetInteger(deal_ticket, DEAL_ORDER);
         if(order_ticket == 0)
            order_ticket = deal_ticket;

         bool already_counted = false;
         for(int order_index = 0; order_index < counted_entry_order_count; ++order_index)
         {
            if(counted_entry_orders[order_index] == order_ticket)
            {
               already_counted = true;
               break;
            }
         }

         if(!already_counted)
         {
            ArrayResize(counted_entry_orders, counted_entry_order_count + 1);
            counted_entry_orders[counted_entry_order_count] = order_ticket;
            counted_entry_order_count++;
            snapshot.trades_today++;
         }
      }

      double net_profit = NetDealProfit(deal_ticket);
      if(deal_day_key == today_key)
         snapshot.daily_pnl += net_profit;
      if(deal_week_key == week_key)
         snapshot.weekly_pnl += net_profit;
      if(deal_month_key == month_key)
         snapshot.monthly_pnl += net_profit;

      ulong position_id = (ulong)HistoryDealGetInteger(deal_ticket, DEAL_POSITION_ID);
      if(position_id == 0)
         position_id = (ulong)HistoryDealGetInteger(deal_ticket, DEAL_ORDER);
      if(position_id == 0)
         position_id = deal_ticket;

      bool is_today_close = ((entry == DEAL_ENTRY_OUT || entry == DEAL_ENTRY_OUT_BY) && deal_day_key == today_key);

      // Aggregate all deal costs by position so entry-side commissions affect loss streaks.
      bool existing_closed_position = false;
      for(int close_index = 0; close_index < todays_closed_deal_count; ++close_index)
      {
         if(todays_closed_deals[close_index].position_id == position_id)
         {
            todays_closed_deals[close_index].net_profit += net_profit;
            if(is_today_close)
            {
               todays_closed_deals[close_index].closed_today = true;
               if(deal_jst > todays_closed_deals[close_index].deal_time_jst)
                  todays_closed_deals[close_index].deal_time_jst = deal_jst;
            }
            existing_closed_position = true;
            break;
         }
      }

      if(!existing_closed_position)
      {
         ArrayResize(todays_closed_deals, todays_closed_deal_count + 1);
         todays_closed_deals[todays_closed_deal_count].deal_time_jst = (is_today_close ? deal_jst : (datetime)0);
         todays_closed_deals[todays_closed_deal_count].position_id = position_id;
         todays_closed_deals[todays_closed_deal_count].net_profit = net_profit;
         todays_closed_deals[todays_closed_deal_count].closed_today = is_today_close;
         todays_closed_deal_count++;
      }
   }

   // Sort today's closed trades before calculating consecutive losses.
   for(int index = 1; index < todays_closed_deal_count; ++index)
   {
      ClosedDealSnapshot current = todays_closed_deals[index];
      int sort_index = index - 1;

      while(sort_index >= 0 && todays_closed_deals[sort_index].deal_time_jst > current.deal_time_jst)
      {
         todays_closed_deals[sort_index + 1] = todays_closed_deals[sort_index];
         sort_index--;
      }

      todays_closed_deals[sort_index + 1] = current;
   }

   int current_loss_streak = 0;
   for(int index = 0; index < todays_closed_deal_count; ++index)
   {
      if(!todays_closed_deals[index].closed_today)
         continue;

      if(todays_closed_deals[index].net_profit < 0.0)
      {
         current_loss_streak++;
         snapshot.consecutive_losses_today = current_loss_streak;
         if(current_loss_streak > snapshot.max_consecutive_losses_today)
            snapshot.max_consecutive_losses_today = current_loss_streak;
      }
      else
      {
         current_loss_streak = 0;
         snapshot.consecutive_losses_today = 0;
      }
   }

   snapshot.daily_loss_limit_hit = (snapshot.daily_pnl <= -MathAbs(DailyLossLimitJPY));
   snapshot.weekly_loss_limit_hit = (snapshot.weekly_pnl <= -MathAbs(WeeklyLossLimitJPY));
   snapshot.monthly_loss_limit_hit = (snapshot.monthly_pnl <= -MathAbs(MonthlyLossLimitJPY));
   snapshot.consecutive_loss_limit_hit = (snapshot.max_consecutive_losses_today >= MaxConsecutiveLossesPerDay);
   return(true);
}

bool LoadMarketSnapshot(MarketSnapshot &snapshot, string &reason)
{
   ZeroMemory(snapshot);
   reason = "";

   MqlTick tick;
   if(!GetCurrentTick(tick, reason))
      return(false);
   snapshot.spread_pips = (tick.ask - tick.bid) / PipSize();

   MqlRates m15_rates[3];
   MqlRates h1_rates[3];
   ArraySetAsSeries(m15_rates, true);
   ArraySetAsSeries(h1_rates, true);
   if(CopyRates(_Symbol, PERIOD_M15, 0, 3, m15_rates) < 3)
   {
      reason = "Not enough M15 bars for signal evaluation.";
      return(false);
   }
   if(CopyRates(_Symbol, PERIOD_H1, 0, 3, h1_rates) < 3)
   {
      reason = "Not enough H1 bars for trend evaluation.";
      return(false);
   }

   double h1_ema20[3];
   double h1_ema50[3];
   double m15_ema20[3];
   double m15_atr14[3];
   ArraySetAsSeries(h1_ema20, true);
   ArraySetAsSeries(h1_ema50, true);
   ArraySetAsSeries(m15_ema20, true);
   ArraySetAsSeries(m15_atr14, true);

   if(CopyBuffer(g_handle_h1_ema20, 0, 0, 3, h1_ema20) < 3 ||
      CopyBuffer(g_handle_h1_ema50, 0, 0, 3, h1_ema50) < 3 ||
      CopyBuffer(g_handle_m15_ema20, 0, 0, 3, m15_ema20) < 3 ||
      CopyBuffer(g_handle_m15_atr14, 0, 0, 3, m15_atr14) < 3)
   {
      reason = "Indicator data is unavailable.";
      return(false);
   }

   snapshot.m15_bar_1 = m15_rates[1];
   snapshot.m15_bar_2 = m15_rates[2];
   snapshot.h1_close = h1_rates[1].close;
   snapshot.h1_ema20 = h1_ema20[1];
   snapshot.h1_ema50 = h1_ema50[1];
   snapshot.m15_ema20 = m15_ema20[1];
   snapshot.m15_atr14 = m15_atr14[1];
   return(true);
}

bool CanOpenNewTrade(const MarketSnapshot &snapshot, RiskSnapshot &risk, string &reason)
{
   reason = "";

   if(!EnableTrading)
   {
      reason = "EnableTrading is false.";
      return(false);
   }

   if(!MQLInfoInteger(MQL_TRADE_ALLOWED) ||
      !TerminalInfoInteger(TERMINAL_TRADE_ALLOWED) ||
      !AccountInfoInteger(ACCOUNT_TRADE_ALLOWED))
   {
      reason = "Trading is not allowed by terminal or account settings.";
      return(false);
   }

   if(NewsStopMode)
   {
      reason = "NewsStopMode is true.";
      return(false);
   }

   if(_Symbol != TARGET_SYMBOL)
   {
      reason = "This EA is locked to USDJPY only.";
      return(false);
   }

   if(RequireJPYAccount && AccountInfoString(ACCOUNT_CURRENCY) != "JPY")
   {
      reason = StringFormat("Account currency must be JPY when RequireJPYAccount is true. Current=%s.",
                            AccountCurrencyLabel());
      return(false);
   }

   datetime now_jst = ToJst(TimeCurrent());
   if(!IsWithinTradeWindow(now_jst))
   {
      reason = "Outside the configured trading window.";
      return(false);
   }

   if(IsFridayEntryBlocked(now_jst))
   {
      reason = "Friday late-session new entries are blocked.";
      return(false);
   }

   if(ShouldForceFridayClose(now_jst))
   {
      reason = "Friday close protection is active.";
      return(false);
   }

   if(snapshot.spread_pips > MaxSpreadPips)
   {
      g_last_spread_block_time = TimeCurrent();
      reason = StringFormat("Spread is too wide: %.2f pips > %.2f pips.", snapshot.spread_pips, MaxSpreadPips);
      return(false);
   }

   if(SpreadCooldownMinutes > 0 && g_last_spread_block_time > 0)
   {
      int cooldown_seconds = SpreadCooldownMinutes * 60;
      int elapsed_seconds = (int)(TimeCurrent() - g_last_spread_block_time);
      if(elapsed_seconds < cooldown_seconds)
      {
         reason = StringFormat("Spread cooldown is active: %d seconds remaining after a wide-spread event.",
                               cooldown_seconds - elapsed_seconds);
         return(false);
      }
   }

   if(CountSymbolPositions() > 0)
   {
      reason = "A USDJPY position already exists. Only one position is allowed.";
      return(false);
   }

   if(!BuildRiskSnapshot(risk))
   {
      reason = "Risk snapshot could not be built from account history.";
      return(false);
   }

   if(risk.trades_today >= MaxTradesPerDay)
   {
      reason = StringFormat("Daily trade limit reached: %d / %d.", risk.trades_today, MaxTradesPerDay);
      return(false);
   }

   if(risk.consecutive_loss_limit_hit)
   {
      reason = StringFormat("Daily consecutive loss limit reached: %d / %d.",
                            risk.max_consecutive_losses_today,
                            MaxConsecutiveLossesPerDay);
      return(false);
   }

   if(risk.daily_loss_limit_hit)
   {
      reason = StringFormat("Daily loss limit reached: %.2f %s <= -%.2f %s.",
                            risk.daily_pnl,
                            AccountCurrencyLabel(),
                            DailyLossLimitJPY,
                            AccountCurrencyLabel());
      return(false);
   }

   if(risk.weekly_loss_limit_hit)
   {
      reason = StringFormat("Weekly loss limit reached: %.2f %s <= -%.2f %s.",
                            risk.weekly_pnl,
                            AccountCurrencyLabel(),
                            WeeklyLossLimitJPY,
                            AccountCurrencyLabel());
      return(false);
   }

   if(risk.monthly_loss_limit_hit)
   {
      reason = StringFormat("Monthly loss limit reached: %.2f %s <= -%.2f %s.",
                            risk.monthly_pnl,
                            AccountCurrencyLabel(),
                            MonthlyLossLimitJPY,
                            AccountCurrencyLabel());
      return(false);
   }

   if(StopLossPips > MaxStrategyStopLossPips)
   {
      reason = StringFormat("StopLossPips %.2f exceeds the strategy safety cap %.2f.",
                            StopLossPips,
                            MaxStrategyStopLossPips);
      return(false);
   }

   if(snapshot.m15_atr14 / PipSize() < MinATRPips)
   {
      reason = StringFormat("ATR is too low: %.2f pips < %.2f pips.",
                            snapshot.m15_atr14 / PipSize(),
                            MinATRPips);
      return(false);
   }

   return(true);
}

bool EvaluateBuySignal(const MarketSnapshot &snapshot, string &reason)
{
   double tolerance = PullbackTolerancePips * PipSize();
   bool bullish_rebound = (snapshot.m15_bar_1.close > snapshot.m15_bar_1.open);
   bool near_ema_pullback = (MathAbs(snapshot.m15_bar_1.low - snapshot.m15_ema20) <= tolerance);
   bool close_back_above_ema = (snapshot.m15_bar_1.close >= snapshot.m15_ema20);

   if(snapshot.h1_close <= snapshot.h1_ema50)
   {
      reason = "Buy rejected: H1 close is not above EMA50.";
      return(false);
   }

   if(snapshot.h1_ema20 <= snapshot.h1_ema50)
   {
      reason = "Buy rejected: H1 EMA20 is not above EMA50.";
      return(false);
   }

   if(!near_ema_pullback)
   {
      reason = "Buy rejected: M15 pullback did not reach the EMA20 area.";
      return(false);
   }

   if(!bullish_rebound)
   {
      reason = "Buy rejected: M15 bar did not close as a bullish rebound candle.";
      return(false);
   }

   if(!close_back_above_ema)
   {
      reason = "Buy rejected: M15 close did not recover above EMA20.";
      return(false);
   }

   reason = StringFormat("BUY setup confirmed. H1 close %.3f > EMA50 %.3f, H1 EMA20 %.3f > EMA50 %.3f, M15 low %.3f near EMA20 %.3f, ATR %.2f pips.",
                         snapshot.h1_close,
                         snapshot.h1_ema50,
                         snapshot.h1_ema20,
                         snapshot.h1_ema50,
                         snapshot.m15_bar_1.low,
                         snapshot.m15_ema20,
                         snapshot.m15_atr14 / PipSize());
   return(true);
}

bool EvaluateSellSignal(const MarketSnapshot &snapshot, string &reason)
{
   double tolerance = PullbackTolerancePips * PipSize();
   bool bearish_rebound = (snapshot.m15_bar_1.close < snapshot.m15_bar_1.open);
   bool near_ema_pullback = (MathAbs(snapshot.m15_bar_1.high - snapshot.m15_ema20) <= tolerance);
   bool close_back_below_ema = (snapshot.m15_bar_1.close <= snapshot.m15_ema20);

   if(snapshot.h1_close >= snapshot.h1_ema50)
   {
      reason = "Sell rejected: H1 close is not below EMA50.";
      return(false);
   }

   if(snapshot.h1_ema20 >= snapshot.h1_ema50)
   {
      reason = "Sell rejected: H1 EMA20 is not below EMA50.";
      return(false);
   }

   if(!near_ema_pullback)
   {
      reason = "Sell rejected: M15 rebound did not reach the EMA20 area.";
      return(false);
   }

   if(!bearish_rebound)
   {
      reason = "Sell rejected: M15 bar did not close as a bearish rejection candle.";
      return(false);
   }

   if(!close_back_below_ema)
   {
      reason = "Sell rejected: M15 close did not settle below EMA20.";
      return(false);
   }

   reason = StringFormat("SELL setup confirmed. H1 close %.3f < EMA50 %.3f, H1 EMA20 %.3f < EMA50 %.3f, M15 high %.3f near EMA20 %.3f, ATR %.2f pips.",
                         snapshot.h1_close,
                         snapshot.h1_ema50,
                         snapshot.h1_ema20,
                         snapshot.h1_ema50,
                         snapshot.m15_bar_1.high,
                         snapshot.m15_ema20,
                         snapshot.m15_atr14 / PipSize());
   return(true);
}

bool ValidateVolume(double &volume, string &reason)
{
   reason = "";

   double min_volume = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
   double max_volume = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);
   double step = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
   if(min_volume <= 0.0 || max_volume <= 0.0 || step <= 0.0 || max_volume < min_volume)
   {
      reason = StringFormat("Broker volume settings are invalid. min=%.4f max=%.4f step=%.4f.",
                            min_volume,
                            max_volume,
                            step);
      return(false);
   }

   if(volume < min_volume)
   {
      reason = StringFormat("LotSize %.4f is smaller than broker minimum %.4f.", volume, min_volume);
      return(false);
   }

   if(volume > max_volume)
   {
      reason = StringFormat("LotSize %.4f is larger than broker maximum %.4f.", volume, max_volume);
      return(false);
   }

   double steps = MathFloor((volume + 1e-8) / step);
   double normalized = steps * step;
   normalized = NormalizeDouble(normalized, VolumeDigitsFromStep(step));

   if(normalized <= 0.0)
   {
      reason = "Normalized volume became zero.";
      return(false);
   }

   if(normalized > volume + 1e-8)
   {
      reason = "Volume normalization would increase risk. Adjust LotSize manually.";
      return(false);
   }

   volume = normalized;
   return(true);
}

bool PrepareOrderPrices(const ENUM_ORDER_TYPE order_type, double &entry_price, double &stop_loss, double &take_profit, string &reason)
{
   reason = "";

   MqlTick tick;
   if(!GetCurrentTick(tick, reason))
      return(false);

   double pip = PipSize();
   double stop_distance = StopLossPips * pip;
   double take_distance = TakeProfitPips * pip;

   if(order_type == ORDER_TYPE_BUY)
   {
      entry_price = tick.ask;
      stop_loss = NormalizeDouble(entry_price - stop_distance, _Digits);
      take_profit = NormalizeDouble(entry_price + take_distance, _Digits);
   }
   else if(order_type == ORDER_TYPE_SELL)
   {
      entry_price = tick.bid;
      stop_loss = NormalizeDouble(entry_price + stop_distance, _Digits);
      take_profit = NormalizeDouble(entry_price - take_distance, _Digits);
   }
   else
   {
      reason = "Unsupported order type.";
      return(false);
   }

   int stops_level_points = (int)SymbolInfoInteger(_Symbol, SYMBOL_TRADE_STOPS_LEVEL);
   double min_stop_distance = stops_level_points * _Point;

   if(min_stop_distance > 0.0)
   {
      double actual_stop_distance = MathAbs(entry_price - stop_loss);
      double actual_take_distance = MathAbs(take_profit - entry_price);
      if(actual_stop_distance < min_stop_distance || actual_take_distance < min_stop_distance)
      {
         reason = StringFormat("Broker stop level blocks the configured SL/TP distances. stop_level=%.5f actual_sl=%.5f actual_tp=%.5f",
                               min_stop_distance,
                               actual_stop_distance,
                               actual_take_distance);
         return(false);
      }
   }

   return(true);
}

bool PlaceEntryOrder(const ENUM_ORDER_TYPE order_type, const string entry_reason, const MarketSnapshot &snapshot)
{
   double volume = LotSize;
   string volume_reason = "";
   if(!ValidateVolume(volume, volume_reason))
   {
      LogBlock(volume_reason);
      return(false);
   }

   double entry_price = 0.0;
   double stop_loss = 0.0;
   double take_profit = 0.0;
   string price_reason = "";
   if(!PrepareOrderPrices(order_type, entry_price, stop_loss, take_profit, price_reason))
   {
      LogBlock(price_reason);
      return(false);
   }

   bool result = false;
   if(order_type == ORDER_TYPE_BUY)
      result = g_trade.Buy(volume, _Symbol, 0.0, stop_loss, take_profit, OrderComment);
   else if(order_type == ORDER_TYPE_SELL)
      result = g_trade.Sell(volume, _Symbol, 0.0, stop_loss, take_profit, OrderComment);

   if(!result)
   {
      PrintFormat("[ORDER_FAIL] type=%s retcode=%u description=%s last_error=%d reason=%s",
                  EnumToString(order_type),
                  g_trade.ResultRetcode(),
                  g_trade.ResultRetcodeDescription(),
                  GetLastError(),
                  entry_reason);
      return(false);
   }

   PrintFormat("[ENTRY] type=%s volume=%.4f price=%.3f sl=%.3f tp=%.3f ticket=%I64u reason=%s | %s",
               EnumToString(order_type),
               volume,
               entry_price,
               stop_loss,
               take_profit,
               g_trade.ResultOrder(),
               entry_reason,
               FormatIndicatorSummary(snapshot));
   return(true);
}

bool CloseManagedPosition(const string close_reason)
{
   ulong ticket = 0;
   if(!SelectManagedPosition(ticket))
      return(false);

   if(!PositionSelectByTicket(ticket))
      return(false);

   double volume = PositionGetDouble(POSITION_VOLUME);
   double price_open = PositionGetDouble(POSITION_PRICE_OPEN);
   ENUM_POSITION_TYPE position_type = (ENUM_POSITION_TYPE)PositionGetInteger(POSITION_TYPE);

   if(!g_trade.PositionClose(ticket, SlippagePoints))
   {
      PrintFormat("[CLOSE_FAIL] ticket=%I64u type=%s retcode=%u description=%s last_error=%d reason=%s",
                  ticket,
                  EnumToString(position_type),
                  g_trade.ResultRetcode(),
                  g_trade.ResultRetcodeDescription(),
                  GetLastError(),
                  close_reason);
      return(false);
   }

   PrintFormat("[CLOSE] ticket=%I64u type=%s volume=%.4f open_price=%.3f reason=%s",
               ticket,
               EnumToString(position_type),
               volume,
               price_open,
               close_reason);
   return(true);
}

void ManageManagedPosition()
{
   ulong ticket = 0;
   if(!SelectManagedPosition(ticket))
      return;

   if(CountManagedPositions() > 1)
   {
      PrintFormat("[SAFETY] More than one managed position detected for %s. Manual intervention is recommended.", TARGET_SYMBOL);
      CloseAllManagedPositions("Multiple managed positions detected.");
      return;
   }

   if(!PositionSelectByTicket(ticket))
      return;

   if(EmergencyFloatingLossLimitJPY > 0.0)
   {
      double floating_pnl = PositionGetDouble(POSITION_PROFIT) + PositionGetDouble(POSITION_SWAP);
      if(floating_pnl <= -MathAbs(EmergencyFloatingLossLimitJPY))
      {
         CloseManagedPosition(StringFormat("Emergency floating loss limit reached: %.2f %s.",
                                           floating_pnl,
                                           AccountCurrencyLabel()));
         return;
      }
   }

   datetime now_jst = ToJst(TimeCurrent());
   if(ShouldForceFridayClose(now_jst))
   {
      CloseAllManagedPositions("Friday close protection.");
      return;
   }

   datetime open_time = (datetime)PositionGetInteger(POSITION_TIME);
   if(MaxHoldingMinutes > 0 && (TimeCurrent() - open_time) >= MaxHoldingMinutes * 60)
   {
      CloseManagedPosition("MaxHoldingMinutes exceeded.");
      return;
   }
}

void LogBlock(const string reason)
{
   PrintFormat("[BLOCK] %s", reason);
}

void CloseAllManagedPositions(const string close_reason)
{
   bool closed_any = false;

   for(int index = PositionsTotal() - 1; index >= 0; --index)
   {
      ulong ticket = PositionGetTicket(index);
      if(ticket == 0 || !PositionSelectByTicket(ticket))
         continue;

      string symbol = PositionGetString(POSITION_SYMBOL);
      long magic = PositionGetInteger(POSITION_MAGIC);
      if(symbol != TARGET_SYMBOL || magic != MagicNumber)
         continue;

      closed_any = true;
      if(!g_trade.PositionClose(ticket, SlippagePoints))
      {
         PrintFormat("[CLOSE_FAIL] ticket=%I64u retcode=%u description=%s last_error=%d reason=%s",
                     ticket,
                     g_trade.ResultRetcode(),
                     g_trade.ResultRetcodeDescription(),
                     GetLastError(),
                     close_reason);
      }
      else
      {
         PrintFormat("[CLOSE] ticket=%I64u reason=%s", ticket, close_reason);
      }
   }

   if(!closed_any)
      PrintFormat("[CLOSE_SKIP] No managed positions were found for reason=%s", close_reason);
}

string FormatIndicatorSummary(const MarketSnapshot &snapshot)
{
   return(StringFormat("spread=%.2f ATR=%.2f H1Close=%.3f H1EMA20=%.3f H1EMA50=%.3f M15EMA20=%.3f",
                       snapshot.spread_pips,
                       snapshot.m15_atr14 / PipSize(),
                       snapshot.h1_close,
                       snapshot.h1_ema20,
                       snapshot.h1_ema50,
                       snapshot.m15_ema20));
}

bool ValidateInputs(string &reason)
{
   reason = "";

   if(MagicNumber <= 0)
   {
      reason = "MagicNumber must be greater than zero.";
      return(false);
   }

   if(LotSize <= 0.0)
   {
      reason = "LotSize must be greater than zero.";
      return(false);
   }

   if(StopLossPips <= 0.0 || TakeProfitPips <= 0.0)
   {
      reason = "StopLossPips and TakeProfitPips must be greater than zero.";
      return(false);
   }

   if(StopLossPips > MaxStrategyStopLossPips)
   {
      reason = "StopLossPips must not exceed MaxStrategyStopLossPips.";
      return(false);
   }

   if(MaxSpreadPips <= 0.0)
   {
      reason = "MaxSpreadPips must be greater than zero.";
      return(false);
   }

   if(SpreadCooldownMinutes < 0 || SpreadCooldownMinutes > 1440)
   {
      reason = "SpreadCooldownMinutes must be between 0 and 1440.";
      return(false);
   }

   if(MaxTradesPerDay < 1 || MaxConsecutiveLossesPerDay < 1)
   {
      reason = "MaxTradesPerDay and MaxConsecutiveLossesPerDay must be at least 1.";
      return(false);
   }

   if(DailyLossLimitJPY <= 0.0 || WeeklyLossLimitJPY <= 0.0 || MonthlyLossLimitJPY <= 0.0)
   {
      reason = "Daily, weekly, and monthly loss limits must be greater than zero.";
      return(false);
   }

   if(EmergencyFloatingLossLimitJPY < 0.0)
   {
      reason = "EmergencyFloatingLossLimitJPY must be zero or greater.";
      return(false);
   }

   if(MaxHoldingMinutes < 1)
   {
      reason = "MaxHoldingMinutes must be at least 1.";
      return(false);
   }

   if(TradeStartHourJST < 0 || TradeStartHourJST > 23)
   {
      reason = "TradeStartHourJST must be between 0 and 23.";
      return(false);
   }

   if(TradeEndHourJST < 1 || TradeEndHourJST > 24)
   {
      reason = "TradeEndHourJST must be between 1 and 24.";
      return(false);
   }

   if(TradeStartHourJST == TradeEndHourJST)
   {
      reason = "TradeStartHourJST and TradeEndHourJST must not be the same.";
      return(false);
   }

   if(FridayNoEntryAfterHourJST < 0 || FridayNoEntryAfterHourJST > 23)
   {
      reason = "FridayNoEntryAfterHourJST must be between 0 and 23.";
      return(false);
   }

   if(FridayCloseHourJST < 0 || FridayCloseHourJST > 23)
   {
      reason = "FridayCloseHourJST must be between 0 and 23.";
      return(false);
   }

   if(PullbackTolerancePips < 0.0 || MinATRPips < 0.0 || MaxStrategyStopLossPips <= 0.0)
   {
      reason = "PullbackTolerancePips, MinATRPips, and MaxStrategyStopLossPips must be valid positive values.";
      return(false);
   }

   if(JSTOffsetHours < -24 || JSTOffsetHours > 24)
   {
      reason = "JSTOffsetHours must be between -24 and 24.";
      return(false);
   }

   if(SlippagePoints < 0)
   {
      reason = "SlippagePoints must be zero or greater.";
      return(false);
   }

   if(ManagementTimerSeconds < 1 || ManagementTimerSeconds > 3600)
   {
      reason = "ManagementTimerSeconds must be between 1 and 3600.";
      return(false);
   }

   if(OrderComment == "")
   {
      reason = "OrderComment must not be empty.";
      return(false);
   }

   return(true);
}
