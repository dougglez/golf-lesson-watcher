import importlib
from lesson_watcher import notifier as original_notifier


def test_notify(monkeypatch):
    monkeypatch.setenv('NTFY_TOPIC', 'unit-test-topic')
    notifier = importlib.reload(original_notifier)

    called = {}

    def fake_post(url, data, timeout):
        called['url'] = url
        called['data'] = data
        class Resp:
            def raise_for_status(self):
                pass
        return Resp()

    monkeypatch.setattr(notifier.requests, 'post', fake_post)
    notifier.notify('hello')
    assert called['url'].endswith('unit-test-topic')
    assert called['data'] == b'hello'
