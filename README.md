# python-orchestrator-client

A simple Python Orchestrator (https://github.com/github/orchestrator) client.

It ensures that the commands to be sent to Orchestrator API are valid, and that the number of arguments matches what the
API expects. This is achieved via the definition of all endpoints and their arguments. The configuration is under
`pyorchestratorclient/endpoints.py` and has been generated from Orchestrator's
[source code](https://github.com/github/orchestrator/blob/master/go/http/api.go) using 
`scripts/orchestrator_api_conf.sh`. You can generate your own to ensure its contents match what your Orchestrator
version supports, if required. 

## Usage:

```python
In [1]: from pyorchestratorclient import OrchestratorClient

In [2]: o = OrchestratorClient('http://localhost:3000')  # Orchestrator URL

In [3]: o.clusters()
Out[3]: ['deceive:20516']

In [4]: o.relocate('deceive', '20518', 'deceive', '20516')  # Call with methods
Out[4]: 
{'Code': 'OK',
 'Details': {'AllowTLS': False,
  'AncestryUUID': '00020516-1111-1111-1111-111111111111,00020518-3333-3333-3333-333333333333',
  'BinlogRowImage': 'FULL',
  'Binlog_format': 'ROW',
  'ClusterName': 'deceive:20516',
  ...
  'Version': '8.0.15',
  'VersionComment': 'MySQL Community Server - GPL'},
 'Message': 'Instance deceive:20518 relocated below deceive:20516'}

In [5]: o.check_global_recoveries()  # Notice that dashes in HTTP API are translated to underscores for the python client
Out[5]: {'Code': 'OK', 'Details': 'enabled', 'Message': 'Global recoveries enabled'}

In [6]: o.clusters("ssfd")  # Validation of expected number of arguments                                                                                                                                                                   
---------------------------------------------------------------------------
OrchestratorClientError                   Traceback (most recent call last)
<ipython-input-7-0494111cc886> in <module>
----> 1 o.clusters("ssfd")

~/git/python-orchestrator-client/pyorchestratorclient/__init__.py in _method_mapper(*args, **kwargs)
    151     def __getattr__(self, item):
    152         def _method_mapper(*args, **kwargs):
--> 153             return self.run(item.replace("_", "-"), *args, *kwargs)
    154 
    155         if item.replace("_", "-") in self.commands.keys():

~/git/python-orchestrator-client/pyorchestratorclient/__init__.py in run(self, cmd, *args)
    110                 sample = ", ".join(usage).strip().strip(",")
    111                 usages.append(f"[{sample}]")
--> 112             raise OrchestratorClientError(
    113                 f"Specified number of arguments for command {cmd} ({len(args)})"
    114                 f" does not match expected number of arguments for it "

OrchestratorClientError: Specified number of arguments for command clusters (1) does not match expected number of arguments for it ([0]). Check that your call is correct.

In [7]: o.something()  # Validation of supported methods                                                                                                                                                                    
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-10-3a11b5057530> in <module>
----> 1 o.something()

~/git/python-orchestrator-client/pyorchestratorclient/__init__.py in __getattr__(self, item)
    155         if item.replace("_", "-") in self.commands.keys():
    156             return _method_mapper
--> 157         raise AttributeError(f"No such attribute or method: {item}")
    158 
    159 

AttributeError: No such attribute or method: something

In [11]: 

```
