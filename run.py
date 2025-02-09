import os
import subprocess
from multiprocessing import Process

from app.config import config


def start_api(path='.'):
    PORT = config.FASTAPI_PORT
    HOST = config.FASTAPI_HOST
    subprocess.call(['uvicorn', 'app.main:app', '--port', PORT, '--host', HOST], cwd=path)

def start_frontend(path='.'):
    PORT = config.STREAMLIT_PORT
    subprocess.call(['streamlit', 'run', 'Home.py', '--server.port', PORT], cwd=path)


if __name__ == '__main__':
    try:
        path = os.path.realpath(os.path.dirname(__file__))
        api = Process(target=start_api, kwargs={'path': path})
        frontend = Process(target=start_frontend, kwargs={'path': path})
        api.start()
        frontend.start()
        api.join()
        frontend.join()
    except KeyboardInterrupt:
        api.terminate()
        frontend.terminate()
