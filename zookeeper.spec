%define _noarch_libdir /usr/lib
%define rel_ver 3.5.5

Summary: High-performance coordination service for distributed applications.
Name: zookeeper
Version: %{rel_ver}
Release: 2%{?dist}
License: Apache License v2.0
Group: Applications/Databases
URL: https://www.apache.org/dist/zookeeper/
BuildArch: noarch
Source0: https://www.apache.org/dist/zookeeper/zookeeper-%{rel_ver}/apache-zookeeper-%{rel_ver}.tar.gz
Source1: zookeeper.service
Source2: zoo.cfg
Source3: log4j.properties
Source4: zookeeper.sysconfig
BuildRoot: %{_tmppath}/%{name}-%{rel_ver}-%{release}-root
BuildRequires: python-devel,gcc,make,libtool,autoconf,cppunit-devel,maven,hostname,systemd
Requires: java,nc,systemd
AutoReqProv: no

%description
ZooKeeper is a distributed, open-source coordination service for distributed
applications. It exposes a simple set of primitives that distributed
applications can build upon to implement higher level services for
synchronization, configuration maintenance, and groups and naming. It is
designed to be easy to program to, and uses a data model styled after the
familiar directory tree structure of file systems. It runs in Java and has
bindings for both Java and C.

Coordination services are notoriously hard to get right. They are especially
prone to errors such as race conditions and deadlock. The motivation behind
ZooKeeper is to relieve distributed applications the responsibility of
implementing coordination services from scratch.

%define _zookeeper_noarch_libdir %{_noarch_libdir}/zookeeper
%define _maindir %{buildroot}%{_zookeeper_noarch_libdir}

%prep
%setup -q -n apache-zookeeper-%{rel_ver}

%build
mvn -DskipTests package

%install
rm -rf %{buildroot}
install -p -d %{buildroot}%{_zookeeper_noarch_libdir}
cp -a bin %{buildroot}%{_zookeeper_noarch_libdir}

mkdir -p %{buildroot}%{_sysconfdir}/zookeeper
cp -a zookeeper-server/target/lib %{buildroot}%{_zookeeper_noarch_libdir}
install -p -D -m 644 zookeeper-server/target/zookeeper-%{rel_ver}.jar %{buildroot}%{_zookeeper_noarch_libdir}/lib/zookeeper-%{rel_ver}.jar
install -p -D -m 644 %{S:1} %{buildroot}%{_unitdir}/%{name}.service
install -p -D -m 644 %{S:2} %{buildroot}%{_sysconfdir}/zookeeper/zoo.cfg
install -p -D -m 644 %{S:3} %{buildroot}%{_sysconfdir}/zookeeper/log4j.properties
install -p -D -m 644 %{S:4} %{buildroot}%{_sysconfdir}/sysconfig/zookeeper
install -p -D -m 644 conf/configuration.xsl %{buildroot}%{_sysconfdir}/zookeeper/configuration.xsl
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_localstatedir}/log/zookeeper
install -d %{buildroot}%{_localstatedir}/lib/zookeeper
install -d %{buildroot}%{_localstatedir}/lib/zookeeper/data
install -p -d -D -m 0755 %{buildroot}%{_datadir}/zookeeper

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE.txt NOTICE.txt README.md
%doc zookeeper-docs zookeeper-recipes
%dir %attr(0750, zookeeper, zookeeper) %{_localstatedir}/lib/zookeeper
%dir %attr(0750, zookeeper, zookeeper) %{_localstatedir}/lib/zookeeper/data
%dir %attr(0750, zookeeper, zookeeper) %{_localstatedir}/log/zookeeper
%{_zookeeper_noarch_libdir}
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/zookeeper
%config(noreplace) %{_sysconfdir}/sysconfig/zookeeper

%pre
getent group zookeeper >/dev/null || groupadd -r zookeeper
getent passwd zookeeper >/dev/null || useradd -r -g zookeeper -d / -s /sbin/nologin zookeeper
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%changelog
* Thu Jul 11 2019 Anton Samets <sharewax@gmail.com>
- add needed Requeries for correct rpm building and fix URL and Source paths
* Fri Jul 5 2019 Sam Kottler <skottler@github.com>
- Remove systemd-rpm-macros from BuildRequires
* Tue Jun 25 2019 Tigran Mkrtchyan <tigran.mkrtchyan@desy.de>
- remove obsolete files
* Tue Jun 25 2019 Tigran Mkrtchyan <tigran.mkrtchyan@desy.de> - 3.5.5-1
- migrate to zookeeper 3.5.5
* Mon May 27 2019 Tigran Mkrtchyan <tigran.mkrtchyan@desy.de> - 3.4.14-2
- Migrate to systemd
* Thu May 02 2019 Tigran Mkrtchyan <tigran.mkrtchyan@desy.de> - 3.4.14-1
- Bump version to 3.4.14
* Mon Apr 17 2017 itxx00 <itxx00@gmail.com> - 3.4.10-1
- Bump version to 3.4.10
* Mon Mar 13 2017 itxx00 <itxx00@gmail.com> - 3.4.9-1
- Bump version to 3.4.9
* Thu Jul 7 2016 Jeremy Christian <jchristi@redhat.com> - 3.4.8-1
- Bump version to 3.4.8
* Mon Dec 8 2014 David Xie <david.scriptfan@gmail.com> - 3.4.6-1
- Bump version to 3.4.6
* Thu May 30 2013 Sam Kottler <shk@linux.com> - 3.4.5-1
- Updated to 3.4.5
* Tue Oct 2 2012 Sam Kottler <sam@kottlerdevelopment.com> - 3.3.2-1
- Initialize package creation
