import webview
from webview import windows

from app.api import API

if __name__ == '__main__':
    api = API()
    api._window = webview.create_window(
        'dev',
        'http://localhost:5173/',
        frameless=True,
        easy_drag=False,
        resizable=True,
        js_api=api,
    )
    webview.start(debug=True)