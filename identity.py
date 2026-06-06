
import time

import RNS
from pathlib import Path

def create_identity(identity_path: Path) -> RNS.Identity:
    identity = RNS.Identity.from_file(identity_path)
    RNS.log(f"Using {identity=} from file {identity_path=}")
    if identity is None:
        raise Exception("Could not generate identity.")
    return identity

def announce_destination(destination) -> None:
    for _ in range(3):
        destination.announce()
        RNS.log("Sent announce from "+RNS.prettyhexrep(destination.hash))
        time.sleep(5)
