%define _noarch_libdir /usr/lib
%define rel_ver 3.4.11

Summary: High-performance coordination service for distributed applications.
Name: zookeeper
Version: %{rel_ver}
Release: 1
License: Apache License v2.0
Group: Applications/Databases
URL: http://hadoop.apache.org/zookeeper/
Source0: http://mirror.cogentco.com/pub/apache/zookeeper/zookeeper-%{rel_ver}/zookeeper-%{rel_ver}.tar.gz
Source1: zookeeper.init
Source2: zookeeper.logrotate
Source3: zoo.cfg
Source4: log4j.properties
Source5: java.env
BuildRoot: %{_tmppath}/%{name}-%{rel_ver}-%{release}-root
BuildRequires: python-devel,gcc,make,libtool,autoconf,cppunit-devel
Requires: logrotate, java, nc
Requires(post): chkconfig initscripts
Requires(pre): chkconfig initscripts
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
%setup -q -n zookeeper-%{rel_ver}

%build
pushd src/c
rm -rf aclocal.m4 autom4te.cache/ config.guess config.status config.log \
    config.sub configure depcomp install-sh ltmain.sh libtool \
    Makefile Makefile.in missing stamp-h1 compile
autoheader
libtoolize --force
aclocal
automake -a
autoconf
autoreconf
%configure
%{__make} %{?_smp_mflags}
popd

%install
rm -rf %{buildroot}
install -p -d %{buildroot}%{_zookeeper_noarch_libdir}
cp -a bin lib %{buildroot}%{_zookeeper_noarch_libdir}

mkdir -p %{buildroot}%{_sysconfdir}/zookeeper
install -p -D -m 644 zookeeper-%{rel_ver}.jar %{buildroot}%{_zookeeper_noarch_libdir}/zookeeper-%{rel_ver}.jar
install -p -D -m 755 %{S:1} %{buildroot}%{_initrddir}/zookeeper
install -p -D -m 644 %{S:2} %{buildroot}%{_sysconfdir}/logrotate.d/zookeeper
install -p -D -m 644 %{S:3} %{buildroot}%{_sysconfdir}/zookeeper/zoo.cfg
install -p -D -m 644 %{S:4} %{buildroot}%{_sysconfdir}/zookeeper/log4j.properties
install -p -D -m 644 %{S:5} %{buildroot}%{_sysconfdir}/zookeeper/java.env
install -p -D -m 644 conf/configuration.xsl %{buildroot}%{_sysconfdir}/zookeeper/configuration.xsl
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_localstatedir}/log/zookeeper
install -d %{buildroot}%{_localstatedir}/lib/zookeeper
install -d %{buildroot}%{_localstatedir}/lib/zookeeper/data
install -p -d -D -m 0755 %{buildroot}%{_datadir}/zookeeper

%{makeinstall} -C src/c

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE.txt NOTICE.txt README.md
%doc docs recipes
%dir %attr(0750, zookeeper, zookeeper) %{_localstatedir}/lib/zookeeper
%dir %attr(0750, zookeeper, zookeeper) %{_localstatedir}/lib/zookeeper/data
%dir %attr(0750, zookeeper, zookeeper) %{_localstatedir}/log/zookeeper
%{_zookeeper_noarch_libdir}
%{_initrddir}/zookeeper
%config(noreplace) %{_sysconfdir}/logrotate.d/zookeeper
%config(noreplace) %{_sysconfdir}/zookeeper
%{_bindir}/cli_mt
%{_bindir}/cli_st
%{_bindir}/load_gen

# ------------------------------ libzookeeper ------------------------------

%package -n libzookeeper
Summary: C client interface to zookeeper server
Group: Development/Libraries
BuildRequires: gcc

%description -n libzookeeper
The client supports two types of APIs -- synchronous and asynchronous.

Asynchronous API provides non-blocking operations with completion callbacks and
relies on the application to implement event multiplexing on its behalf.

On the other hand, Synchronous API provides a blocking flavor of
zookeeper operations and runs its own event loop in a separate thread.

Sync and Async APIs can be mixed and matched within the same application.

%files -n libzookeeper
%defattr(-, root, root, -)
%doc src/c/README src/c/LICENSE
%{_libdir}/libzookeeper_mt.so.*
%{_libdir}/libzookeeper_st.so.*

# ------------------------------ libzookeeper-devel ------------------------------

%package -n libzookeeper-devel
Summary: Headers and static libraries for libzookeeper
Group: Development/Libraries
Requires: gcc

%description -n libzookeeper-devel
This package contains the libraries and header files needed for
developing with libzookeeper.

%files -n libzookeeper-devel
%defattr(-, root, root, -)
%{_includedir}
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so

%pre
getent group zookeeper >/dev/null || groupadd -r zookeeper
getent passwd zookeeper >/dev/null || useradd -r -g zookeeper -d / -s /sbin/nologin zookeeper
exit 0

%post
/sbin/chkconfig --add zookeeper

%preun
if [ $1 = 0 ] ; then
    /sbin/service zookeeper stop >/dev/null 2>&1
    /sbin/chkconfig --del zookeeper
fi

%postun
if [ "$1" -ge "1" ] ; then
    /sbin/service zookeeper condrestart >/dev/null 2>&1 || :
fi

%changelog
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
