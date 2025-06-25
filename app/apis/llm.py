import ollama
import openai
from openai import OpenAI
import os
import subprocess as sp
import asyncio

from .. import utils
from . import prompt

class LLM:
    def __init__(self, api):
        self._state = 'done'
        self._total_word = 0
        self._strategy_gen_state = 'done'
        self._api = api
        os.environ['OLLAMA_MODELS'] = os.path.join(self._api.config.base_path, 'models')
        os.environ['OLLAMA_FLASH_ATTENTION'] = '1'
        cmd = [os.path.join(self._api.config.base_path, 'ollama/ollama.exe'), 'serve']
        self._pipe = sp.Popen(cmd, shell=True)

    def list(self):
        return [i.model for i in ollama.list().models]

    def pull(self, name):
        self._state = '0%'
        try:
            print('pulling:',name)
            for progress in ollama.pull(name, stream=True):
                if progress.get('completed') is None:
                    continue
                if complete := progress.get('completed'):
                    self._state = '%.2f'%(100 * complete / progress.total)+'%'
        except Exception as e:
            return str(e)
        finally:
            self._state = 'done'
            return 'complete'

    def get_state(self):
        return self._state

    def generate_strategy(self, message, name):
        self._strategy_gen_state = 'generating'
        client = OpenAI(
            api_key=self._api.config._data['api_key'],
            base_url=self._api.config._data['online_base_url']
        )
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "user", "content": prompt.strategy_generate_system},
                {"role": "assistant", "content":""},
                {"role": "user", "content": message},
            ],
            stream=False
        )
        self._api.file._data['strategies'][name] = {
            'name': name,
            'prompt': response.choices[0].message.content,
        }
        self._strategy_gen_state = 'done'
        self._api.file.save()

    def get_strategy_gen_state(self):
        return self._strategy_gen_state

    def process_files(self, file_list, strategy, template):
        self._state = 'initializing'
        system = prompt.file_process_system.format(self._api.file._data['strategies'][strategy]['prompt'])
        batch_size = int(self._api.config._data['thread_number'])
        chunk_size = int(self._api.config._data['chunk_size'])
        model = self._api.config._data['online_model']
        i = 0
        for file in file_list:
            if template == '{}':
                new_name = file
                dest_path = os.path.join(
                    self._api.file._base_path,
                    self._api.file._data['files'][file]['file']
                )
            else:
                new_name, dest_path = self._api.file._create_file_idx(template.format(file), file)
            self._state = '{}/{}'.format(i, len(file_list))
            i += 1
            file_obj = self._api.file._data['files'][file]
            source_path = os.path.join(self._api.file._resource_path, self._api.file._data['files'][file]['file'])
            if file_obj['tag'] == 'large':
                dest_obj = self._api.file._data['files'][new_name]
                dest_obj['file'] = file_obj['file']
                dest_obj['tag'] = file_obj['tag']
                dest_obj['meta']['strategy'] = strategy
            else:
                asyncio.run(
                    self.__process_file(
                        source_path=source_path,
                        dest_path=dest_path,
                        model=model,
                        system=system,
                        chunk_size=chunk_size,
                        batch_size=batch_size
                    )
                )
            self._api.file.save()
        self._total_word = 0
        self._state = 'done'

    async def __process_file(self, source_path, dest_path, model, system, chunk_size, batch_size):
        with open(source_path,'r', encoding='utf-8') as f:
            file = f.read()
        chunks = [file[i:i+chunk_size] for i in range(0, len(file), chunk_size)]
        results = []
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            # 每组最多 batch_size 个并发
            batch_results = await asyncio.gather(
                *[self.__process_chunk(chunk, system, model) for chunk in batch]
            )
            results.extend(batch_results)
        print(results)
        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(''.join(results))

    async def embedding_large_file(self, source_path, name, chunk_size, batch_size, display_name):
        collection = self._api.file._vdb.create_collection(name=name)
        total = os.path.getsize(source_path)
        progress = 0
        with (open(source_path, 'r', encoding='utf-8') as f):
            i = 0
            overlap = ''
            while True:
                self._api.file._state = '{}: {}%'.format(display_name, '%.2f'%(progress / total * 100))
                chunks = []
                for current_batch_size in range(batch_size):
                    chunk = f.read(chunk_size-len(overlap))
                    if not chunk:
                        if current_batch_size == 0:
                            f.close()
                            return
                        break
                    chunks.append(overlap+chunk)
                    overlap = chunk[-64 if len(chunk)>=64 else 0::]
                    progress += len(chunk.encode('utf-8'))
                vectors = (await ollama.AsyncClient().embed(
                    model=self._api.config._data['local_model'],
                    input=chunks,
                ))['embeddings']
                print(
                    'embedding datas',
                    chunks,
                    vectors,
                    len(vectors)
                )
                collection.add(
                    ids=[str(i) for i in range(i*batch_size, i*batch_size+len(chunks))],
                    embeddings=vectors,
                    documents=chunks
                )
                i += 1

    def get_chunk_from_large_file(self, name, query):
        uuid = self._api.file._data['files'][name]['file']
        vector = ollama.embed(
            model=self._api.config._data['local_model'],
            input=query,
        )["embeddings"]
        try:
            collection = self._api.file._vdb.get_collection(name=uuid)
        except Exception as e:
            return '--not found--'
        res = collection.query(
            query_embeddings=vector,
            n_results=3,
        )['documents'][0]
        print(res)
        origin = ''.join([
            prompt.file_chunk_result.format(idx, item)
            for idx, item in enumerate(res)
        ])
        if 'strategy' in self._api.file._data['files'][name]['meta']:
            return asyncio.run(self.__process_chunk(
                origin,
                prompt.file_process_system.format(
                    self._api.file._data['strategies'][self._api.file._data['files'][name]['meta']['strategy']]
                ),
                model=self._api.config._data['online_model']
            ))
        return origin

    def purify_prompt(self, content, exception):
        message = [{'role': 'user', 'content': prompt.prompt_purify_system.format(content,exception)}]
        return utils.extract_result(asyncio.run(self.__chat(message, self._api.config._data['online_model'])))

    async def __process_chunk(self, chunk, system, model):
        message = [
            {'role': 'user', 'content': system+chunk}
        ]
        replacement = utils.extract_results(
            utils.deepseek_modify(await self.__chat(message, model))
        )
        return utils.replace_by_dict(chunk, replacement)

    async def __chat(self, message, model):
        client = openai.AsyncOpenAI(
            api_key=self._api.config._data['api_key'],
            base_url=self._api.config._data['online_base_url']
        )
        res = await client.chat.completions.create(
            model=model,
            messages=message,
        )
        return res.choices[0].message.content

    def encrypt(self, content):
        print(content)
        client = openai.OpenAI(
            api_key=self._api.config._data['api_key'],
            base_url=self._api.config._data['online_base_url']
        )
        model = self._api.config._data['online_model']
        message1 = [{'role': 'user', 'content':prompt.translate.format(content)}]
        res1 = client.chat.completions.create(
            model=model,
            messages=message1,
        ).choices[0].message.content
        res1 = utils.extract_result(res1)
        print(res1)
        res2 = utils.blur(res1)
        print(res2)
        return res2

