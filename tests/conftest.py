from __future__ import annotations

import os

import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "integration: opt-in tests that touch live Decimal nodes")


def pytest_collection_modifyitems(config, items):
    if os.getenv("DECIMAL_SDK_RUN_INTEGRATION") == "1":
        return
    skip = pytest.mark.skip(reason="Set DECIMAL_SDK_RUN_INTEGRATION=1 to run live-node tests")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip)

