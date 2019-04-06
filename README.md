# python-orchestrator-client

A simple Python Orchestrator (https://github.com/github/orchestrator) client.

It ensures that the commands to be send to Orchestrator API are valid, and that the number of arguments matches what the
API expects. This is achieved via dynamic configuration from a text file with the definition of all endpoints and their 
arguments. The sample file included under `conf/orchestrator_endpoints.txt` has been generated from Orchestrator's 
source code (https://github.com/github/orchestrator/blob/master/go/http/api.go) using `scripts/orchestrator_api_conf.sh`. You can 
generate your own to ensure its contents match what your Orchestrator version supports. 

## Usage:

```python
In [1]: from pyorchestratorclient import OrchestratorClient

In [2]: o = OrchestratorClient('conf/orchestrator_endpoints.txt', 'http://localhost:3000')  # Adjust config  path and Orchestrator URL

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

In [6]: 

```
