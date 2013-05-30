# Overview
This repository contains everything needed to build RPM's for zookeeper, including libzookeeper and the devel packages. Different pieces are taken from places around the internet; the init script is quite close to Cassandra's. Individual packages will be built for zookeeper, libzookeeper, and zookeeper-devel.

The spec has been tested only on EL6 with the EPEL repo enabled, but should also work on recent Fedoras, too.

# Building
1. `git clone https://github.com/skottler/zookeeper-rpms`
2. `cd zookeeper-rpms`
3. `rpmdev-setuptree`
4. `spectool -g zookeeper.spec`
5. `rpmbuild -bs --nodeps --define "_sourcedir ." --define "_srcrpmdir ." zookeeper.spec` 
6. `sudo mock <the srpm from step 5>`
