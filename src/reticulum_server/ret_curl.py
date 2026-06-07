import argparse
import sys
import time

import RNS

from .config import settings

##########################################################
#### Client Part #########################################
##########################################################

# A reference to the server link
server_link = None


# This initialisation is executed when the users chooses
# to run as a client
def client(destination_hexhash, configpath, path, payload, *args, **kwargs):
    global server_link

    # We need a binary representation of the destination
    # hash that was entered on the command line
    try:
        dest_len = (RNS.Reticulum.TRUNCATED_HASHLENGTH // 8) * 2
        if len(destination_hexhash) != dest_len:
            raise ValueError(
                f"Destination length is invalid, must be \
                    {dest_len=} hexadecimal characters ({dest_len//2=} bytes)."
            )

        destination_hash = bytes.fromhex(destination_hexhash)
    except:  # noqa: E722
        RNS.log("Invalid destination entered. Check your input!\n")
        sys.exit(0)

    # We must first initialise Reticulum
    RNS.Reticulum(configpath)

    # Check if we know a path to the destination
    if not RNS.Transport.has_path(destination_hash):
        RNS.log(
            "Destination is not yet known. \
            Requesting path and waiting for announce to arrive..."
        )
        RNS.Transport.request_path(destination_hash)
        while not RNS.Transport.has_path(destination_hash):
            time.sleep(0.1)

    # Recall the server identity
    server_identity = RNS.Identity.recall(destination_hash)

    # Inform the user that we'll begin connecting
    RNS.log("Establishing link with server...")

    # When the server identity is known, we set
    # up a destination
    server_destination = RNS.Destination(
        server_identity,
        RNS.Destination.OUT,
        RNS.Destination.SINGLE,
        settings.APP_NAME,
        "requestexample",
    )

    # And create a link
    link = RNS.Link(server_destination)

    # We'll set up functions to inform the
    # user when the link is established or closed
    link.set_link_established_callback(link_established)
    link.set_link_closed_callback(link_closed)

    while not server_link:
        time.sleep(0.1)

    response = server_link.request(
        path,
        data=payload,
    )

    while response.get_status() == RNS.RequestReceipt.SENT:
        ...

    response = response.get_response()
    print(response)
    # sys.stdout.write(response.get_response())

    server_link.teardown()


# This function is called when a link
# has been established with the server
def link_established(link):
    # We store a reference to the link
    # instance for later use
    global server_link
    server_link = link

    # Inform the user that the server is
    # connected
    RNS.log(
        'Link established with server, \
        hit enter to perform a request, or type in "quit" to quit'
    )


# When a link is closed, we'll inform the
# user, and exit the program
def link_closed(link):
    if link.teardown_reason == RNS.Link.TIMEOUT:
        RNS.log("The link timed out, exiting now")
    elif link.teardown_reason == RNS.Link.DESTINATION_CLOSED:
        RNS.log("The link was closed by the server, exiting now")
    else:
        RNS.log("Link closed, exiting now")


##########################################################
#### Program Startup #####################################
##########################################################


def main():
    try:
        parser = argparse.ArgumentParser(description="Simple request/response example")

        parser.add_argument(
            "--config",
            action="store",
            default=None,
            help="path to alternative Reticulum config directory",
            type=str,
        )

        parser.add_argument(
            "destination",
            nargs="?",
            default=None,
            help="hexadecimal hash of the server destination",
            type=str,
        )

        parser.add_argument(
            "path",
            nargs="?",
            default=None,
            help="hexadecimal hash of the server destination",
            type=str,
        )

        parser.add_argument(
            "--payload",
            nargs="?",
            default="",
            help="Json paylod for the server",
            type=str,
        )

        args = parser.parse_args()

        if args.destination is None:
            print("")
            parser.print_help()
            print("")

        else:
            client(args.destination, args.config, path=args.path, payload=args.payload)

    except KeyboardInterrupt:
        print("")
        sys.exit(0)


if __name__ == "__main__":
    main()
