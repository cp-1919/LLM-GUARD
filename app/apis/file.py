import asyncio
import os
import json
import webview
from openai import OpenAI
from uuid import uuid4
from markitdown import MarkItDown
import chromadb
from pytesseract import pytesseract

guard_file_types = ('Guard Data File (*.guard.json)',)
supported_file_types = (
    'Supported Files (*.docx;*.pptx;*.xlsx;*.pdf;*.jpg;*.jpeg;*.png;*.bmp;'
    '*.html;*.htm;*.csv;*.json;*.xml;*.txt)',
)
export_file_types = ('Markdown File (*.md)', 'Text File (*.txt)')

class File:
    def __init__(self, api):
        self._api = api
        self._base_path = None
        self._conf_path = None
        self._resource_path = None
        self._state = 'done'
        self._data = {}
        self._vdb = None
        pytesseract.tesseract_cmd = os.path.join(api.config.base_path, r'tesseract/tesseract.exe')
        print(pytesseract.tesseract_cmd)

    def _chroma_init(self):
        self._vdb = chromadb.PersistentClient(path=self._resource_path)

    def create(self, name):
        self._base_path = None
        self._data = {
            'name': name['value'],
            'files': {},
            'strategies': {},
            'history': [],
        }
        self.save()

    def save(self):
        if self._base_path is None:
            base_path = self._api._window.create_file_dialog(
                webview.FOLDER_DIALOG, directory='', file_types=()
            )[0]
            if base_path is None:
                return False
            self._base_path = base_path
            self._conf_path = os.path.join(base_path, self._data['name']+'.guard.json')
            self._resource_path = os.path.join(base_path, self._data['name']+'_resource')
            if os.path.exists(self._conf_path):
                return False
            if os.path.exists(self._resource_path):
                return False
            os.mkdir(self._resource_path)
            self._chroma_init()
        with open(self._conf_path, mode='w', encoding='utf-8') as f:
            f.write(json.dumps(self._data, ensure_ascii=False))
        return True

    def open(self):
        conf_path = self._api._window.create_file_dialog(
            webview.OPEN_DIALOG, allow_multiple=False, file_types=guard_file_types
        )[0]
        if conf_path is None:
            return False
        try:
            with (open(conf_path, 'r', encoding='utf-8') as file):
                data = json.load(file)
                if (
                    'name' not in data or
                    'files' not in data or
                    'strategies' not in data or
                    'history' not in data
                ):
                    return False
                self._data = data
        except Exception:
            return False
        self._base_path = os.path.dirname(conf_path)
        self._conf_path = conf_path
        self._resource_path = os.path.join(self._base_path, self._data['name']+'_resource')
        self._chroma_init()
        return True

    def list(self):
        return [{
            'name': item,
            'from': self._data['files'][item]['from'],
            'tag': self._data['files'][item]['tag'],
        } for item in self._data['files']]

    def _create_file_idx(self, file_name, from_file = '-'):
        tail = ''
        i = 0
        while file_name+tail in self._data['files']:
            tail = '_'+str(i)
            i += 1
        file_name += tail
        file_uuid = str(uuid4())
        dest_path = os.path.join(self._resource_path, file_uuid)
        while os.path.exists(dest_path):
            file_uuid = str(uuid4())
            dest_path = os.path.join(self._resource_path, file_uuid)
        self._data['files'][file_name] = {
            'name': file_name,
            'from': from_file,
            'file': file_uuid,
            'tag': 'common',
            'meta': {},
        }
        return file_name, dest_path

    def add(self):
        self._state = 'loading'
        md = MarkItDown()
        file_paths = self._api._window.create_file_dialog(
            webview.OPEN_DIALOG, allow_multiple=True, file_types=supported_file_types
        )
        if file_paths is None:
            return False
        batch_size = int(self._api.config._data['thread_number'])
        chunk_size = int(self._api.config._data['chunk_size'])
        errors = []
        finished = 0
        for file_path in file_paths:
            self._state = '{}/{}'.format(finished, len(file_paths))
            file_name, dest_path = self._create_file_idx(os.path.basename(file_path))
            if file_name.split('.')[-1].lower() in ['jpg', 'png', 'jpeg', 'bmp']:
                content = pytesseract.image_to_string(file_path, lang='chi_sim+equ')
            else:
                try:
                    content = md.convert(file_path).text_content
                except Exception as e:
                    errors.append(str(e))
                    continue
            with open(dest_path, mode='w', encoding='utf-8') as f:
                f.write(content)
            print('size:', os.path.getsize(dest_path))
            if os.path.getsize(dest_path) > 50000:
                self._data['files'][file_name]['tag'] = 'large'
                asyncio.run(self._api.llm.embedding_large_file(
                    source_path=dest_path,
                    name=self._data['files'][file_name]['file'],
                    chunk_size=chunk_size,
                    batch_size=batch_size,
                    display_name=file_name
                ))
            finished += 1
        self.save()
        self._state = 'done'
        return errors

    def get(self, name, context=None):
        if name not in self._data['files']:
            return {
                'content': '# 404',
                'state': 'not found',
            }
        if self._data['files'][name]['tag'] == 'large':
            if context is None:
                return {
                    'content': '文件过大，无法查看',
                    'state': 'file too large'
                }
            else:
                return {
                    'state': 'success',
                    'content': self._api.llm.get_chunk_from_large_file(name, context)
                }
        else:
            try:
                with open(
                    os.path.join(self._resource_path, self._data['files'][name]['file']),
                    mode='r',
                    encoding='utf-8'
                ) as f:
                    return {
                        #'name': self._data['files'][name]['name'],
                        #'from': self._data['files'][name]['from'],
                        'content': f.read(),
                        'state': 'success',
                    }
            except Exception as e:
                return {
                    'content': '文件不存在',
                    'state': 'not found'
                }

    def remove(self, name):
        if name not in self._data['files']:
            return False
        if self._data['files'][name]['tag'] != 'large' or self._data['files'][name]['from'] == '-':
            print('remove file')
            path = os.path.join(self._resource_path, self._data['files'][name]['file'])
            try:
                os.remove(path)
            except Exception:
                pass
        if self._data['files'][name]['tag'] == 'large ' and self._data['files'][name]['from'] == '-':
            print('remove vdb')
            self._vdb.delete_collection(name=self._data['files'][name]['file'])
        del self._data['files'][name]
        self.save()

    def rename(self, name, new_name):
        if new_name in self._data['files']:
            return False
        if name in self._data['files']:
            self._data['files'][new_name] = self._data['files'].pop(name)
            self._data['files'][new_name]['name'] = new_name
            self.save()
        return True

    def export(self, name):
        if name not in self._data['files']:
            return
        path = self._api._window.create_file_dialog(
            webview.SAVE_DIALOG, directory='/', save_filename=name+'.md',
            file_types=export_file_types
        )
        if path is None:
            return
        with open(os.path.join(self._resource_path, self._data['files'][name]['file']), 'r', encoding='utf-8') as resource_file:
            with open(path, mode='w', encoding='utf-8') as dest_file:
                dest_file.write(resource_file.read())

    def get_state(self):
        return self._state

    def get_strategies(self):
        return list(self._data['strategies'].values())

    def remove_strategy(self, name):
        if name in self._data['strategies']:
            del self._data['strategies'][name]
        self.save()

    def list_history(self):
        return [
            item[1]['content'][:20:] if len(item)!=1 else 'new chat'
            for item in self._data['history']
        ]

    def get_history(self, idx):
        return self._data['history'][idx]

    def create_history(self, context):
        print('created')
        self._data['history'].insert(0, context)
        self.save()

    def update_history(self, idx, value):
        if idx >= len(self._data['history']):
            return False
        self._data['history'][idx] = value
        self.save()
        return True

    def remove_history(self, idx):
        if idx >= len(self._data['history']):
            return False
        del self._data['history'][idx]
        self.save()
        return True
