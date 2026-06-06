import argparse
from functools import partial
from pathlib import Path
import sys
from watchfiles import run_process
from server import Server
from custom_rutes import routes


def run_server(config):
    server = Server(config)
    server.add_router(routes)
    server() # This calls the __call__ method defined in server.py


if __name__ == "__main__":
    
    try:
        parser = argparse.ArgumentParser(description="Simple request/response example")

        parser.add_argument(
            "--config",
            action="store",
            default=None,
            help="path to alternative Reticulum config directory",
            type=str
        )

        args = parser.parse_args()
        if args.config:
            configarg = args.config
        else:
            configarg = None

        run_process(Path.cwd(), target=run_server, args=(configarg,))

    except KeyboardInterrupt:
        print("")
        sys.exit(0)