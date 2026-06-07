from collections.abc import Callable

import RNS


class Route:
    url: str
    callback: Callable

    def __init__(self, url: str, callback: Callable) -> None:
        self.url = url
        self.callback = callback


class Router:
    
    def __init__(self, prefix: str | None = None):
        self.prefix = prefix
        self.ROUTES_REGISTRY: list[Route] = []

    def route_decorator(self, path):
        """Route decorator to add paths to the router."""
        def decorator(func):
            def wrapped(path, data, request_id, link_id, remote_identity, requested_at):
                RNS.log(f"Route '{path}' triggered. Calling function '{func.__name__}'")
                RNS.log(f"Arguments passed: {path=}, {data=}")

                try:
                    # Run the callback function and return the result
                    result = func(
                        path, 
                        data, 
                        request_id, 
                        link_id, 
                        remote_identity, 
                        requested_at
                    )
                    return result
                except Exception as e:
                    RNS.log(f"Error executing route '{path}': {str(e)}")
                    raise e
        
            # Attach the wrapped function to the router callback for the server
            router_instance = Route(
                url=path,
                callback=wrapped
            )
            
            # Register it to your collection at startup
            self.ROUTES_REGISTRY.append(router_instance)

            # TOOD (GONZA): I don't think i need to return the function here?, check!
            # return wrapped

        return decorator
    