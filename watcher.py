from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import yaml
import shutil
from pathlib import Path
from os import environ


def compile():
    subprocess.run(["python3", "blog.py", "build"], cwd="/repo")

    # copy
    with open("/repo/config.yaml") as f:
        output_dir = Path("/repo") / yaml.safe_load(f)["artifacts_dir"]
    try:
        shutil.rmtree("/site")
    except:
        pass
    shutil.copytree(output_dir, "/site")


class Handler(FileSystemEventHandler):
    def on_created(self, event):
        # pull
        cnt = 0
        while True:
            result = subprocess.run(["git", "-C", "/repo", "pull"])
            if result.returncode == 0:
                break
            cnt += 1
            if cnt > 5:
                return

        # compile
        compile()
        try:
            Path("/flags/reload").unlink()
        except:
            pass


subprocess.run(["git", "clone", environ.get("REPO"), "/repo"])
compile()

# start webhook service
subprocess.Popen(["gunicorn", "app:app", "-w", "4", "-b", "0.0.0.0:81", "-k", "gevent"])
subprocess.Popen(["caddy", "run"])

event_handler = Handler()
observer = Observer()
observer.schedule(event_handler, "/flags/")
observer.start()

try:
    while True:
        sleep(60)
        Path("/flags/reload").touch()
except KeyboardInterrupt:
    observer.stop()
observer.join()
