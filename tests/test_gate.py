from operator_gates import Posture, check


def test_mail_nogo_without_phrase():
    c = check("mail_send", Posture(mirror_ok=True, phrase=False))
    assert c.go is False
    assert "NO-GO" in str(c)


def test_mail_go():
    c = check("mail_send", Posture(mirror_ok=True, phrase=True, note="ops"))
    assert c.go is True
    assert str(c).startswith("ARMED-CHECK: GO")


def test_money_requires_phrase():
    assert check("money", Posture()).go is False
    assert check("money", Posture(phrase=True)).go is True


def test_outreach_paused():
    c = check("outreach", Posture(phrase=True, outreach_live=False, outreach_paused=True))
    assert c.go is False


def test_other_requires_host_pin():
    assert check("other", Posture()).go is False
    assert check("other", Posture(host_pinned=True)).go is True
