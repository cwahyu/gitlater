# tests/test_api.py


from gitlater import allow, guard, status


def test_allow_true(monkeypatch):
    monkeypatch.setattr(
        "gitlater.check_allowed",
        lambda: (True, ""),
    )

    assert allow() is True


def test_allow_false(monkeypatch):
    monkeypatch.setattr(
        "gitlater.check_allowed",
        lambda: (False, "blocked"),
    )

    assert allow() is False


def test_status(monkeypatch):
    monkeypatch.setattr(
        "gitlater.check_allowed",
        lambda: (False, "message"),
    )

    allowed, message = status()

    assert allowed is False
    assert message == "message"


def test_guard_allowed(monkeypatch):
    monkeypatch.setattr(
        "gitlater.check_allowed",
        lambda: (True, ""),
    )

    # should NOT exit
    guard()


def test_guard_blocked(monkeypatch, capsys):
    monkeypatch.setattr(
        "gitlater.check_allowed",
        lambda: (False, "blocked message"),
    )

    try:
        guard()
    except SystemExit as e:
        assert e.code == 1

    captured = capsys.readouterr()
    assert "blocked message" in captured.out
