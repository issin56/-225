from kanekasegi.sbi_adapter import SbiApiProfile, SbiFuturesAdapter
import pytest


def test_sbi_connectivity_check_reports_profile_state():
    adapter = SbiFuturesAdapter(
        SbiApiProfile(
            api_key="key",
            api_secret="secret",
            endpoint="https://example.invalid",
            tool_name="SBI API Tool",
        )
    )
    summary = adapter.connectivity_check("NK225MICRO")
    assert summary["broker"] == "sbi"
    assert summary["api_key_present"] is True
    assert summary["api_secret_present"] is True
    assert summary["endpoint_present"] is True


def test_sbi_trading_methods_are_explicitly_unimplemented():
    adapter = SbiFuturesAdapter(SbiApiProfile(api_key="key", api_secret="secret", endpoint=None, tool_name=None))
    with pytest.raises(NotImplementedError):
        adapter.get_ticker("NK225MICRO")
    with pytest.raises(NotImplementedError):
        adapter.place_order(None)  # type: ignore[arg-type]
    with pytest.raises(NotImplementedError):
        adapter.get_position("NK225MICRO")
