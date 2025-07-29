import os
from lesson_watcher.config import load_config


def test_load_config(monkeypatch):
    monkeypatch.setenv('SCHEDDY', '  "http://example.com"   ')
    monkeypatch.setenv('Coach', '“Jane Doe” ')
    cfg = load_config()
    assert cfg.url == 'http://example.com'
    assert cfg.coach == 'Jane Doe'
