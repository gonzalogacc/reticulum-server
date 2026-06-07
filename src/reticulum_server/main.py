from pathlib import Path

from watchfiles import run_process

from .config import settings
from .custom_rutes import routes
from .server import Server


def run_server(config):
    server = Server(config)
    server.add_router(routes)
    server()


def main():
    config_file = Path(settings.CONFIG_FILE)
    src_dir = Path(__file__).parent.parent
    run_process(src_dir, target=run_server, args=(str(config_file),))


if __name__ == "__main__":
    main()
