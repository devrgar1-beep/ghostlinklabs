import os
import importlib


def test_maximized_profile_values(monkeypatch):
    monkeypatch.setenv('GHOSTLINK_PERF_PROFILE', 'maximized')
    pc = importlib.import_module('ghostlinklabs.utils.perf_config')

    assert pc.is_maximized()
    # request timeout should be a small number (default 0.5)
    assert pc.request_timeout_seconds() == int(float(os.getenv('GHOSTLINK_REQUEST_TIMEOUT', '0.5')))
    # max_workers should be at least cpu_count
    assert pc.max_workers() >= 1
