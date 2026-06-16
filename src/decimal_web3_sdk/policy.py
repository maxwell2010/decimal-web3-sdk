from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TransactionPolicy:
    target_total_seconds: float = 5.0
    build_timeout_seconds: float = 1.0
    estimate_timeout_seconds: float = 1.5
    broadcast_timeout_seconds: float = 1.5
    receipt_poll_seconds: float = 1.0
    max_rpc_attempts: int = 2

    def validate(self) -> None:
        if self.target_total_seconds <= 0:
            raise ValueError("target_total_seconds must be positive")
        stage_budget = (
            self.build_timeout_seconds
            + self.estimate_timeout_seconds
            + self.broadcast_timeout_seconds
            + self.receipt_poll_seconds
        )
        if stage_budget > self.target_total_seconds:
            raise ValueError("Stage timeouts exceed target_total_seconds")

    @classmethod
    def fast(cls) -> "TransactionPolicy":
        return cls()

