from operator_gates.cli import main


def test_check_nogo_exit_code():
    assert main(["check", "mail_send", "--phrase"]) == 1


def test_check_go_exit_code():
    assert main(["check", "mail_send", "--mirror-ok", "--phrase"]) == 0


def test_replay_001(capsys):
    assert main(["replay", "001"]) == 0
    out = capsys.readouterr().out
    assert "NO-GO" in out
    assert "GO" in out


def test_scars_list(capsys):
    assert main(["scars"]) == 0
    assert "001" in capsys.readouterr().out
