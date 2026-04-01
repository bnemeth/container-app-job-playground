from vscode_single_library_template.__main__ import main


def test_main_prints_sum_and_greeting(capsys):
    main()
    captured = capsys.readouterr()

    assert captured.out == "7\nHello, World!\n"
