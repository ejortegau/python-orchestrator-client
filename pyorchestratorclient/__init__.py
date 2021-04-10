"""A simple client for `Orchestrator
<https://github.com/openark/orchestrator/>_` API."""
import logging
import os
import sys
from collections import defaultdict
from typing import Optional, Any

import requests


from pyorchestratorclient import endpoints


class OrchestratorBaseError(Exception):
    """Base exception for errors calling the Orchestrator API"""


class OrchestratorClientError(OrchestratorBaseError):
    """Exception for errors calling the Orchestrator API that are related to
    the client request"""


class OrchestratorServerError(OrchestratorBaseError):
    """Exception for errors calling the Orchestrator API that are related to
    the server"""


class OrchestratorRedirectionError(OrchestratorBaseError):
    """Exception for errors calling the Orchestrator API that are related to
    unexpected redirections being sent as response to the API request"""


class OrchestratorClient:
    """A Python client for Orchestrator API (
    https://github.com/openark/orchestrator)"""

    def __init__(
        self,
        url: Optional[str] = "",
        username: Optional[str] = "",
        password: Optional[str] = "",
    ) -> None:
        """
        Constructor for Orchestrator client. Requires the path to a text file
        specifying the supported Orchestrator endpoints and its corresponding
        parameters, as well as the base URL of orchestrator
        (Eg. https://orchestrator.example.com:3020).
        It can optionally take a username and password to perform HTTP basic
        authentication when issuing requests to Orchestrator.

        :param url: Base orchestrator URL. If not provided, it will default
        to https://orchestrator/
        :param username: Username to send as part of HTTP basic
        authentication. Can be left empty if your Orchestrator instance does not
        require authentication.
        :param password: Password to send as part of HTTP basic authentication.
        Can be left empty if your Orchestrator instance does not require
        authentication.
        """

        base_url = url or os.getenv("ORCHESTRATOR_URL", "https://orchestrator")
        self.base_url = f"{base_url}/api/"
        self.username = username or ""
        self.password = password or ""
        self.commands = defaultdict(list)

        for line in endpoints.SUPPORTED_ENDPOINTS.split("\n"):
            if not line:
                break
            url_tokens = line.strip().split("/")
            cmd = url_tokens[0]
            arguments = [a.strip(":") for a in url_tokens[1:]]
            logging.debug(
                "Registering command %s with arguments %s", cmd, arguments
            )
            self.commands[cmd].append(arguments)

    def run(self, cmd: str, *args: str) -> Any:
        """
        Send command cmd with arguments args to Orchestrator server. Returns
        a list or dictionary matching the JSON representation of the response
        body returned by the Orchestrator server.

        :param cmd: a valid orchestrator command.
        :param args: a list of arguments for the specified command.
        :return: a list or dictionary matching the decoded output of
        Orchestrator's response body.
        :raises OrchestratorClientError: if the command is invalid, or if
        Orchestrator's HTTP response status code >= 300 and < 500
        :raises OrchestratorServerError: if Orchestrator's response body cannot
        be JSON decoded, or if the response's HTTP status code >= 500
        :raises OrchestratorRedirectionError: if Orchestrator's response HTTP
        status code >= 300 and <= 400.
        """
        # Check whether the specified command exists
        if cmd not in self.commands.keys():
            raise OrchestratorBaseError("Orchestrator {cmd} is not valid")

        # Check whether the number of arguments received matches the number of
        # arguments expected by the command
        n_args = [len(a) for a in self.commands[cmd]]
        str_args = [str(a) for a in args]  # Stringify all the things
        if not len(str_args) in n_args:
            # Build text representation of list of arguments required by given
            # command
            usages = []
            for usage in self.commands[cmd]:
                usage = [f"'{a}'" for a in usage]
                sample = ", ".join(usage).strip().strip(",")
                usages.append(f"[{sample}]")
            raise OrchestratorClientError(
                f"Specified number of arguments for command {cmd} ({len(args)})"
                f" does not match expected number of arguments for it "
                f"({n_args}). Check that your call is correct."
            )
        # Insert the command as the first argument for building request path
        str_args.insert(0, cmd)

        path = "/".join(str_args)  # build request path

        url = f"{self.base_url}{path}"
        logging.debug("Calling endpoint %s", url)
        result = requests.get(url, auth=(self.username, self.password))

        if result.status_code < 300:
            try:
                return result.json()
            except ValueError as error:
                raise OrchestratorServerError(
                    f"Response cannot be JSON decoded. Response is"
                    f" {result.text}"
                ) from error
        elif result.status_code < 400:
            raise OrchestratorClientError(
                f"Command {cmd} resulted in redirect {[result.status_code]}"
                f" {result.text}, please verify that the base Orchestrator"
                f"URL {self.base_url} is correct"
            )
        elif result.status_code < 500:
            raise OrchestratorServerError(
                f"Command {cmd} resulted in client error "
                f"{[result.status_code]} {result.text}"
            )
        else:
            raise OrchestratorRedirectionError(
                f"Command {cmd} resulted in server error "
                f"{[result.status_code]} {result.text}"
            )

    def __getattr__(self, item):
        def _method_mapper(*args, **kwargs):
            return self.run(item.replace("_", "-"), *args, *kwargs)

        if item.replace("_", "-") in self.commands.keys():
            return _method_mapper
        raise AttributeError(f"No such attribute or method: {item}")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    try:
        o = OrchestratorClient("http://localhost:3010")
        logging.debug("Registered commands: %s", o.commands)
        logging.info(o.clusters("efsd"))
    except OrchestratorBaseError as err:
        logging.error("%s", err)
        sys.exit(1)
