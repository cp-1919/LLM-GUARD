import sys
import os
import subprocess

base_path = ''
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

print(base_path)

cmd = [os.path.join(base_path, 'Ollama/ollama.exe'), 'pull', 'deepseek-r1:7b']
pipe = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
pipe.wait()