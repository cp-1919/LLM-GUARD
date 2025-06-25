import subprocess
import os
import signal
import time
import ollama

# 执行外部命令

os.environ['OLLAMA_MODELS'] = os.path.abspath('../app/models')
cmd = [os.path.abspath('../app/ollama/ollama.exe'), 'serve']

p = subprocess.Popen(cmd)
time.sleep(10)

def download():
    complete = 0
    for progress in ollama.pull('qwen2.5:0.5b', stream=True):
        #print(progress.get('digest',''))
        #print(progress.get('status'))
        if progress.get('completed') is None:
            continue
        if complete := progress.get('completed'):
            print(complete / progress.total)


def chat(quest):
    message = [
        {'role': 'user', 'content': quest}
    ]
    for part in ollama.chat('deepseek-r1:7b', message, stream=True):
        print(part['message']['content'], end='', flush=True)

def total_exit():
    time.sleep(10)
    os.kill(os.getpid(), signal.SIGTERM)

if __name__ == '__main__':
    total_exit()