"""Serve files via reticulum, but mine."""

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import RNS

from config import settings
from identity import announce_destination, create_identity

from router import Router
from utils import client_connected


class Server:
    
    def __init__(self, config_path: Path | None = None):

        # A reference to the latest client link that connected
        self.latest_client_link = None
        self.config_path = config_path

        self.reticulum = RNS.Reticulum(self.config_path)

        self.server_destination = RNS.Destination(
            create_identity(settings.IDENTITY_PATH),
            RNS.Destination.IN,
            RNS.Destination.SINGLE,
            settings.APP_NAME,
            "requestexample"
        ) 

        self.set_server()

    def __call__(self):
        self.server_loop(self.server_destination)
    
    def set_server(self):
        # We must first initialise Reticulum
        self.server_destination.set_link_established_callback(client_connected)


    def add_router(self, router: Router):
        for router_inst in router.ROUTES_REGISTRY:
            self.server_destination.register_request_handler(
                router_inst.url,
                response_generator = router_inst.callback,
                allow = RNS.Destination.ALLOW_ALL
            )

    def server_loop(self, destination):
        # Let the user know that everything is ready
        RNS.log(
            "Request example "+
            RNS.prettyhexrep(destination.hash)+
            " running, waiting for a connection."
        )

        RNS.log("Hit enter to manually send an announce (Ctrl-C to quit)")

        # Send the destination 
        with ThreadPoolExecutor(max_workers=1) as executor:
            executor.submit(announce_destination, destination)