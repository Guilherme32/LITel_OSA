from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import numpy as np
from time import sleep
import os


class FileLoader(PatternMatchingEventHandler, Observer):
    def __init__(self, load_callback, path=None, patterns=('*', )):
        PatternMatchingEventHandler.__init__(self, patterns)
        Observer.__init__(self)

        self.next = None
        self.ready = False
        self.load_callback = load_callback

        self.path = path or '.'

        if os.path.exists(self.path):
            self.schedule(self, path=self.path)
            self.start()
        else:
            print('Caminho não encontrado, por favor atualize')

        self.set_ready()

    def reset_config(self, load_callback=None, path=None):
        self.next = None
        self.ready = False
        self.unschedule_all()

        self.load_callback = load_callback or self.load_callback
        self.path = path or self.path

        if os.path.exists(self.path):
            self.schedule(self, path=self.path)
        else:
            print('Caminho não encontrado, por favor atualize')

        self.set_ready()

    def set_ready(self):
        self.ready = True
        self.try_send()

    def on_created(self, event):
        path = event.src_path
        sleep(0.01)     # garantir que o arquivo já foi fechado
        self.next = path
        self.try_send()

    def try_send(self):
        if self.ready and (self.next is not None):
            spectrum = np.loadtxt(self.next, delimiter=';', dtype=np.float64)

            if spectrum[0, 0] > 100:
                spectrum[::, 0] *= 1e-9

            self.ready = False
            self.next = None
            self.load_callback(spectrum)
            self.set_ready()
