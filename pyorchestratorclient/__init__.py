import logging
import requests

from collections import defaultdict


class OrchestratorClientException(BaseException):
    def __init__(self, code: str, message: str):
        """
        Orchestrator client exception constructor. Requires a computer-friendly code and a human friendly message.
        :param str code: an error code for the exception
        :param str message: a description of the exception
        """
        super(OrchestratorClientException, self).__init__()
        self.code = code
        self.message = message

    def __str__(self) -> str:
        """
        Returns a textual representation of the exception
        :return: a human-readable string representation of the exception
        :rtype str
        """
        return f"[{self.code}] {self.message}"


class OrchestratorClient:
    """A Python client for Orchestrator API (https://github.com/github/orchestrator)"""

    def __init__(self, endpoints_file: str, url: str, username: str = None, password: str = None):
        """
        Constructor for Orchestrator client. Requires the path to a text file specifying the supported Orchestrator
        endpoints and its corresponding parameters, as well as the base URL of orchestrator (Eg. http://localhost:3000).
        It can optionally take a username and password to perform HTTP basic authentication when issuing requests to
        Orchestrator.
        :param str endpoints_file: path to a file with configuration for all supported Orchestrator endpoints
        :param str url: Base orchestrator URL
        :param str username: Username to send as part of HTTP basic authentication (Optional)
        :param str password: Password to send as part of HTTP basic authentication (Optional)
        """
        self.base_url = f"{url}/api/"
        self.username = username
        self.password = password
        self.commands = defaultdict(list)
        try:
            with open(endpoints_file, "r") as f:
                while(True):
                    line=f.readline()
                    if not line:
                        break
                    url_tokens = line.strip().split('/')
                    cmd = url_tokens[0]
                    arguments = [a.strip(':') for a in url_tokens[1:] ]
                    logging.debug("Registering command %s with arguments %s", cmd, arguments)
                    self.commands[cmd].append(arguments)
        except Exception as e:
            raise OrchestratorClientException('ERR_NO_CFG', f"Endpoints definition file {endpoints_file} not found, "
                                                            f"cannot instantiate an orchestrator client")

    def run(self, cmd: str, *args: str) -> iter:
        """
        Send command cmd with arguments args to Orchestrator server. Returns a list or dictionary matching the JSON
        representation of the response body returned by the Orchestrator server.

        :param str cmd: a valid orchestrator command.
        :param list args: a list of arguments for the specified command.
        :return: a list or dictionary matching the decoded output of Orchestrator's response body
        :rtype: list or dict
        :raises OrchestratorClientException: if the command is invalid, or if Orchestrator HTTP status code >= 300
        """
        # Check whether the specified command exists
        if cmd not in self.commands.keys():
            raise OrchestratorClientException('ERR_NO_SUCH_CMD', f"Command {cmd} is not valid")

        # Check whether the number of arguments received matches the number of arguments expected by the command
        n_args = [len(a) for a in self.commands[cmd]]
        args = list(args)
        args = [str(a) for a in args]  # Stringify all the things
        if not len(args) in n_args:
            # Build text representation of list of arguments required by given command
            usages = []
            for usage in self.commands[cmd]:
                usage = [ f"'{a}'" for a in usage]
                sample = ", ".join(usage).strip().strip(",")
                usages.append(f"[{sample}l]")
            usages = " or ".join(usages).strip(" or ")
            logging.error("Command '%s' needs the following arguments: %s", cmd, usages)
            raise OrchestratorClientException('ERR_BAD_CMD_ARGS', f"Specified number of arguments for "
                                                                  f"command {cmd} ({len(args)}) does not match expected"
                                                                  f" number of arguments for it ({n_args})")
        args.insert(0, cmd)  # Insert the command as the first argument for building request path

        path = '/'.join(args)  # build request path

        url = f"{self.base_url}{path}"
        logging.info("Calling endpoint %s", url)
        if self.username is not None or self.password is not None:
            result = requests.get(url, auth=(self.username, self.password))
        else:
            result = requests.get(url)

        if result.status_code < 300:
            return result.json()
        elif result.status_code < 400:
            raise OrchestratorClientException('ERR_REDIRCT', f"Command {cmd} resulted in redirect"
                                                             f" {[result.status_code]} {result.text}, please verify "
                                                             f"base Orchestrator URL {self.base_url} is correct")
        elif result.status_code < 500:
            raise OrchestratorClientException('ERR_CLIENT', f"Command {cmd} resulted in client error "
                                                            f"{[result.status_code]} {result.text}")
        else:
            raise OrchestratorClientException('ERR_SERVER', f"Command {cmd} resulted in server error "
                                                            f"{[result.status_code]} {result.text}")


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    try:
        o = OrchestratorClient('../conf/orchestrator_endpoints.txt', 'http://localhost:3000')
        logging.debug("Registered commands: %s", o.commands)
        logging.info(o.run('relocate', 'deceive', '20518', 'deceive', '20517'))
    except OrchestratorClientException as e:
        logging.error("%s", e)
        exit(1)

