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

In [2]: o = OrchestratorClient('conf/orchestrator_endpoints.txt', 'http://localhost:3000')  # Adjust for your path and Orchestrator instance

In [3]: o.run('clusters')
Out[3]: ['deceive:20516']

In [4]: o.run('relocate', 'deceive', '20518', 'deceive', '20516')
Out[4]: 
{'Code': 'OK',
 'Details': {'AllowTLS': False,
  'AncestryUUID': '00020516-1111-1111-1111-111111111111,00020518-3333-3333-3333-333333333333',
  'BinlogRowImage': 'FULL',
  'Binlog_format': 'ROW',
  'ClusterName': 'deceive:20516',
  'CountMySQLSnapshots': 0,
  'DataCenter': '',
  'DowntimeEndTimestamp': '',
  'DowntimeOwner': '',
  'DowntimeReason': '',
  'ElapsedDowntime': 0,
  'ExecBinlogCoordinates': {'LogFile': 'mysql-bin.000001',
   'LogPos': 12861694,
   'Type': 0},
  'ExecutedGtidSet': '',
  'FlavorName': '',
  'GTIDMode': 'OFF',
  'GtidErrant': '',
  'GtidPurged': '',
  'HasReplicationCredentials': True,
  'HasReplicationFilters': False,
  'InstanceAlias': '',
  'IsCandidate': False,
  'IsCoMaster': False,
  'IsDetached': False,
  'IsDetachedMaster': False,
  'IsDowntimed': False,
  'IsLastCheckValid': True,
  'IsRecentlyChecked': True,
  'IsUpToDate': True,
  'Key': {'Hostname': 'deceive', 'Port': 20518},
  'LastDiscoveryLatency': 3906357,
  'LastIOError': '',
  'LastSQLError': '',
  'LastSeenTimestamp': '',
  'LogBinEnabled': True,
  'LogSlaveUpdatesEnabled': True,
  'MasterKey': {'Hostname': 'deceive', 'Port': 20516},
  'MasterUUID': '00020516-1111-1111-1111-111111111111',
  'PhysicalEnvironment': '',
  'Problems': [],
  'PromotionRule': 'neutral',
  'ReadBinlogCoordinates': {'LogFile': 'mysql-bin.000001',
   'LogPos': 12861694,
   'Type': 0},
  'ReadOnly': False,
  'RelaylogCoordinates': {'LogFile': 'mysql-relay.000001',
   'LogPos': 4,
   'Type': 1},
  'ReplicationCredentialsAvailable': False,
  'ReplicationDepth': 1,
  'ReplicationIOThreadState': 1,
  'ReplicationSQLThreadState': 1,
  'SQLDelay': 0,
  'SecondsBehindMaster': {'Int64': 0, 'Valid': True},
  'SecondsSinceLastSeen': {'Int64': 0, 'Valid': False},
  'SelfBinlogCoordinates': {'LogFile': 'mysql-bin.000001',
   'LogPos': 12616180,
   'Type': 0},
  'SemiSyncEnforced': False,
  'SemiSyncMasterEnabled': False,
  'SemiSyncReplicaEnabled': False,
  'ServerID': 300,
  'ServerUUID': '00020518-3333-3333-3333-333333333333',
  'SlaveHosts': [],
  'SlaveLagSeconds': {'Int64': 0, 'Valid': True},
  'Slave_IO_Running': True,
  'Slave_SQL_Running': True,
  'SuggestedClusterAlias': 'deceive',
  'SupportsOracleGTID': False,
  'UnresolvedHostname': '',
  'Uptime': 8008,
  'UsingMariaDBGTID': False,
  'UsingOracleGTID': False,
  'UsingPseudoGTID': False,
  'Version': '8.0.15',
  'VersionComment': 'MySQL Community Server - GPL'},
 'Message': 'Instance deceive:20518 relocated below deceive:20516'}
```
