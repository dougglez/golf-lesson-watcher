from datetime import datetime, timedelta

import pytest

from lesson_watcher.config import Config
from lesson_watcher.scheduler import ScheddyClient


class DummyClient(ScheddyClient):
    def __init__(self):
        super().__init__(Config(url='http://example.com', coach='coach'))

    def fetch_schedule(self) -> str:
        dt = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d %I:%M %p')
        return f"<div>Open: {dt}</div>"


def test_find_openings():
    client = DummyClient()
    openings = client.find_openings(days_ahead=2)
    assert len(openings) == 1


def test_login(monkeypatch):
    html = '''<form action="/login" method="post">
        <input name="__RequestVerificationToken" value="token" />
        <input name="Alias" value="alias" />
    </form>'''
    posted = {}

    class LoginClient(ScheddyClient):
        def __init__(self):
            super().__init__(Config(url='http://example.com', coach='c', username='u', password='p'))

    client = LoginClient()

    def fake_get(url, timeout):
        class Resp:
            text = html

            def raise_for_status(self):
                pass

        return Resp()

    def fake_post(url, data, timeout):
        posted['url'] = url
        posted['data'] = data

        class Resp:
            def raise_for_status(self):
                pass

        return Resp()

    monkeypatch.setattr(client.session, 'get', fake_get)
    monkeypatch.setattr(client.session, 'post', fake_post)
    client.login()
    assert posted['url'].endswith('/login')
    assert posted['data']['UserName'] == 'u'


def test_fetch_schedule_login_failure(monkeypatch):
    client = ScheddyClient(
        Config(url='http://example.com', coach='c', username='u', password='p')
    )
    called = {}

    def fake_login():
        called['login'] = True

    class Resp:
        text = '<html>Login <input type="Password" /></html>'

        def raise_for_status(self):
            pass

    monkeypatch.setattr(client, 'login', fake_login)
    monkeypatch.setattr(client.session, 'get', lambda url, timeout: Resp())

    with pytest.raises(RuntimeError, match='Login failed'):
        client.fetch_schedule()
    assert called.get('login')

