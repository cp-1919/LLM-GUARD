import os

class Window:
    def __init__(self, api):
        self._api = api
    def restore(self):
        self._api._window.restore()

    def maximize(self):
        self._api._window.maximize()

    def minimize(self):
        self._api._window.minimize()
