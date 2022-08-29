from prompt_toolkit.shortcuts import radiolist_dialog

result = radiolist_dialog(
    title="Hi Medium!",
    text="What's your favorite IDE?",
    values=[
        ("pycharm", "PyCharm"),
        ("vscode", "Vistual Studio Code"),
        ("wingide", "WingIDE")
    ]
).run()
