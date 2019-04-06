# python-orchestrator-client

A simple Python Orchestrator (https://github.com/github/orchestrator) client.

It ensures that the commands to be send to Orchestrator API are valid, and that the number of arguments matches what the
API expects. This is achieved via dynamic configuration from a text file with the definition of all endpoints and their 
arguments. The sample file included under `conf/orchestrator_endpoints.txt` has been generated from Orchestrator's 
source code (src/github.com/github/orchestrator/go/http/api.go) using `scripts/orchestrator_api_conf.sh`. You can 
generate your own to ensure its contents match what your Orchestrator version supports. 

## Usage:

```python
In [1]: from pyorchestratorclient import OrchestratorClient

In [2]: o = OrchestratorClient('/path/to/orchestrator/endpoints.txt', 'http://localhost:3000')

In [3]: o.clusters()  # Directly call a method known to the Orchestrator HTTP API
Out[3]: ['deceive:20516']

In [4]: o.run("clusters")  # Or call it by specifying its name to the run() method
Out[4]: ['deceive:20516']

In [5]: o.relocate('deceive', '20518', 'deceive', '20516')  # Direct call using method arguments 
Out[5]: 
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

In [6]: o.run('relocate', 'deceive', '20518', 'deceive', '20516')  # Indirect call via method name and arguments
Out[6]: 
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

In [7]: 
```
