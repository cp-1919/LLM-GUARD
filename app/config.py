import os
import sys
import json

class Config:
    def __init__(self):
        if getattr(sys, 'frozen', False):
            self.base_path = sys._MEIPASS
        else:
            self.base_path = os.path.dirname(__file__)
        with open(os.path.join(self.base_path, 'config.json'), 'r', encoding='utf-8') as file:
            self._data = json.load(file)
        print(self._data)
        if self._data['local_model'] == '':
            self._is_new = True
        else:
            self._is_new = False

        # config environment vars
        os.environ["TIKTOKEN_CACHE_DIR"] = os.path.join(self.base_path, 'tiktoken_resource')

    def update(self, data):
        for item in data:
            if item in self._data:
                self._data[item] = data[item]
        with open(os.path.join(self.base_path, 'config.json'), mode='w', encoding='utf-8') as f:
            f.write(json.dumps(self._data, ensure_ascii=False))

    def gets(self):
        return self._data