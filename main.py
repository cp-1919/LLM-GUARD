import webview
import sys
import io
import os
from app.api import API

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    api = API()
    api._window = webview.create_window(
        'LLM-GUARD',
        str(os.path.join(api.config.base_path, 'front/index.html')),
        #'front/dist/index.html',
        frameless=True,
        easy_drag=False,
        resizable=True,
        js_api=api,
    )
    webview.start(debug=False, ssl=True)