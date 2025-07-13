def test_prompt_build(capsys):
    from rag_cli_interface import build_prompt
    prompt = build_prompt("Shaky and low glucose")
    out, _ = capsys.readouterr()
    assert "User Question" in prompt