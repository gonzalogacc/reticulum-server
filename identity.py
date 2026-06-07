
import time
import threading

import RNS
from pathlib import Path

       
def create_identity(identity_path: Path) -> RNS.Identity:
    identity = RNS.Identity.from_file(identity_path)
    RNS.log(f"Using {identity=} from file {identity_path=}")
    if identity is None:
        raise Exception("Could not generate identity.")
    return identity

