from app import USERS, app


def test_win_rate():
    assert USERS["brian"].games == 13
    assert round(USERS["brian"].win_rate, 2) == 0.92


def test_health():
    assert app.test_client().get("/health").get_json() == {"status": "ok"}


def test_login_redirects_when_anonymous():
    resp = app.test_client().get("/")
    assert resp.status_code == 302 and "/login" in resp.headers["Location"]
