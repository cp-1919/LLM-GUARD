import signal
import os
from .apis.window import Window
from .apis.llm import LLM
from .apis.file import File
from .config import Config

class API:
    def __init__(self):
        self.config = Config()
        self.window = Window(self)
        self.file = File(self)
        self.llm = LLM(self)

    def exit(self):
        self.file._vdb = None
        os.kill(self.llm._pipe.pid, signal.CTRL_C_EVENT)
        os.kill(os.getpid(), signal.SIGTERM)
        exit()

    def is_new(self):
        return self.config._is_new
