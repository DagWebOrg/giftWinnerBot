import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class PythonFileHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.py'):
            print(f'Обнаружено изменение в файле {event.src_path}')
            self.restart_script()

    def restart_script(self):
        # Завершаем предыдущий процесс, если он еще работает
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()

        # Запускаем новый процесс
        self.process = subprocess.Popen(['python3', "bot.py"])

if __name__ == "__main__":
    event_handler = PythonFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)  # Отслеживаем изменения в текущей директории и поддиректориях
    observer.start()

    try:
        while True:
            time.sleep(4)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()