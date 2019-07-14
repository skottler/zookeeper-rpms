# Overview

This repository contains everything needed to build RPM's for zookeeper-server.
The spec has been tested on EL7 with the EPEL repo enabled and Fedora 30.

## Prepare

Ensure packages are installed that provide tools to build the srpm and mock build the binary rpms.

- `sudo yum install -y rpm-build rpmdevtools mock`

## Building

1. `git clone https://github.com/skottler/zookeeper-rpms`
2. `cd zookeeper-rpms`
3. `rpmdev-setuptree`
4. `spectool -g zookeeper.spec`
5. `rpmbuild -bs --nodeps --define "_sourcedir $(pwd)" --define "_srcrpmdir $(pwd)" zookeeper.spec`
6. `sudo mock <the srpm from step 5>`

## Start/Stop Zookeeper service

```
# systemctl start zookeeper
# systemctl status zookeeper
● zookeeper.service - Apache Zookeeper server
   Loaded: loaded (/usr/lib/systemd/system/zookeeper.service; disabled; vendor preset: disabled)
   Active: active (running) since Mon 2019-05-27 13:04:43 UTC; 3min 16s ago
     Docs: http://zookeeper.apache.org
 Main PID: 16416 (java)
   CGroup: /system.slice/zookeeper.service
           └─16416 /usr/bin/java -Dzookeeper.log.dir=/var/log/zookeeper -Dlog4j.configuration=fi...
...
# systemctl stop zookeeper
```

### Accessing zookeeper log files

Zookeepers logs are available in systemd's `journal` facility with `zookeeper` identifier and can be accessed as:

```
$ journalctl -t zookeeper
```

### Troubleshooting systemd installation

Due to systemd/selinux [issue](https://bugzilla.redhat.com/show_bug.cgi?id=1224211) it may  be required to restart `systemd` daemon:

```
# systemctl status zookeeper
Failed to get properties: Access denied
# systemctl daemon-reexec
systemctl status zookeeper
● zookeeper.service - Apache Zookeeper server
   Loaded: loaded (/usr/lib/systemd/system/zookeeper.service; disabled; vendor preset: disabled)
   Active: inactive (dead)
     Docs: http://zookeeper.apache.org
```

## License

All files in this repository are licensed under the Apache 2 license. Any
redistribution of these files must include the original license as well as
attribution to this repository.
