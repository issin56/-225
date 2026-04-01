from __future__ import annotations

import json
from dataclasses import dataclass

import requests


class Notifier:
    def send_info(self, message: str) -> None:
        raise NotImplementedError

    def send_alert(self, message: str) -> None:
        raise NotImplementedError


@dataclass(slots=True)
class DiscordNotifier(Notifier):
    webhook_url: str | None

    def _send(self, content: str) -> None:
        if not self.webhook_url:
            return
        response = requests.post(
            self.webhook_url,
            data=json.dumps({"content": content}),
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        response.raise_for_status()

    def send_info(self, message: str) -> None:
        self._send(f"[INFO] {message}")

    def send_alert(self, message: str) -> None:
        self._send(f"[ALERT] {message}")
