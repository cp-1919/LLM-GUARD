from app.apis.file import File
import webview
from dataclasses import dataclass
from typing import Any

@dataclass
class Test:
    _window: Any

if __name__ == '__main__':
    window = webview.create_window('Open file dialog example', 'https://baidu.com/')
    test = Test(window)
    file = File(test)
    webview.start(lambda w:file.create(), window)