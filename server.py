"""Serve files via reticulum, but mine."""

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import threading
from time import sleep
import RNS

from config import settings
from identity import create_identity

from router import Router
from utils import client_connected


class Server:
    
    def __init__(self, config_path: Path):

        # A reference to the latest client link that connected
        self.latest_client_link = None
        self.config_path = config_path

        self.reticulum = RNS.Reticulum(self.config_path)

        identity = create_identity(Path(settings.IDENTITY_PATH))
        self.server_destination = RNS.Destination(
            identity,
            RNS.Destination.IN,
            RNS.Destination.SINGLE,
            settings.APP_NAME,
            "requestexample"
        ) 

        # Set callbacks.
        # TODO (Gonza): move this to a function later for easier configuration
        self.server_destination.set_link_established_callback(client_connected)

    def __call__(self):
        RNS.log(f"Running server.")
        self.server_loop(self.server_destination)
    
    def announce_destination(self, destination):
        destination.announce()
        RNS.log(f"Sent announce from {RNS.prettyhexrep(destination.hash)}")

    def add_router(self, router: Router):
        for router_inst in router.ROUTES_REGISTRY:
            self.server_destination.register_request_handler(
                router_inst.url,
                response_generator = router_inst.callback,
                allow = RNS.Destination.ALLOW_ALL
            )

    def server_loop(self, destination):
        RNS.log(f"Request example {RNS.prettyhexrep(destination.hash)} running, waiting for a connection.")

        # This look keeps the server alive and annouces the server every N seconds
        while True:
            self.announce_destination(destination)
            sleep(settings.ANNOUNCE_INTERVAL_SECONDS)