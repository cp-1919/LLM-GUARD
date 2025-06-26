import signal
import os
import sys
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
        try:
            os.kill(self.llm._pipe.pid, signal.CTRL_C_EVENT)
        except Exception:
            pass
        try:
            os.kill(os.getpid(), signal.SIGTERM)
        except Exception:
            pass
        sys.exit(0)

    def is_new(self):
        return self.config._is_new
