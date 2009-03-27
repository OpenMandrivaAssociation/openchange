%define samba4_version 4.0.0-0.1.alpha7
%define talloc_version 1.2.0
%define nickname ROMULUS
%define libname %mklibname mapi 0
%define develname %mklibname -d mapi
%global build_server 0

Name: openchange
Version: 0.8.2
Release: %mkrel 1
Group: Networking/Mail
Summary: Provides access to Microsoft Exchange servers using native protocols
License: GPLv3+ and Public Domain
URL: http://www.openchange.org/
Source0: http://downloads.sourceforge.net/openchange/libmapi-%{version}-%{nickname}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: bison
BuildRequires: doxygen
BuildRequires: file-devel
BuildRequires: flex
BuildRequires: talloc-devel >= %{talloc_version}
BuildRequires: tdb-devel
BuildRequires: ldb-devel
BuildRequires: pkgconfig
BuildRequires: popt-devel
BuildRequires: python-devel
BuildRequires: samba4-devel >= %{samba4_version}
BuildRequires: samba-hostconfig-devel
BuildRequires: dcerpc-devel
BuildRequires: samba4-pidl >= %{samba4_version}
BuildRequires: sqlite3-devel
BuildRequires: zlib-devel

%description
OpenChange provides libraries to access Microsoft Exchange servers
using native protocols.

%package -n %libname
Summary: Openchange shared library supporting the MAPI protocol
Group: System/Libraries

%description -n %libname
Shared libraries from the Openchange project implementing the MAPI protocol

%package -n %develname
Summary: Developer tools for OpenChange libraries
Group: Development/C
Requires: %libname >= %version
Provides: libmapi-devel = %{version}-%{release}

%description -n %develname
This package provides the development tools and headers for
OpenChange, providing libraries to access Microsoft Exchange servers
using native protocols.

%package client
Summary: User tools for OpenChange libraries
Group: Networking/Mail
Requires: openchange = %{version}-%{release}

%description client
This package provides the user tools for OpenChange, providing access to
Microsoft Exchange servers using native protocols.

%package -n python-openchange
Summary: Python bindings for OpenChange libraries
Group: Development/Python
Requires: openchange = %{version}-%{release}

%description -n python-openchange
This module contains a wrapper that allows the use of OpenChange via Python.

# %package server
# Summary Server side modules for OpenChange
# Group: Applications/System
# Requires: samba4

# %description server
# This package provides the server elements for OpenChange.

%prep
%setup -q -n libmapi-%{version}-%{nickname}

%build
%configure

# Parallel builds prohibited by makefile
make
make doxygen

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

cp -r libmapi++ $RPM_BUILD_ROOT%{_includedir}

rm -rf $RPM_BUILD_ROOT%{_libdir}/nagios/check_exchange
rm -rf $RPM_BUILD_ROOT%{_prefix}/modules
rm -rf $RPM_BUILD_ROOT%{_datadir}/js
rm -rf $RPM_BUILD_ROOT%{_datadir}/setup
rm -rf $RPM_BUILD_ROOT%{_libdir}/libmapiproxy.so.*

# This makes the right links, as rpmlint requires that the
# ldconfig-created links be recorded in the RPM.
/sbin/ldconfig -N -n $RPM_BUILD_ROOT/%{_libdir}

mkdir $RPM_BUILD_ROOT%{_mandir}
cp -r doc/man/man1 $RPM_BUILD_ROOT%{_mandir}
cp -r apidocs/man/man3 $RPM_BUILD_ROOT%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %libname -p /sbin/ldconfig

%postun -n %libname -p /sbin/ldconfig

%files -n %libname
%defattr(-,root,root,-)
%doc ChangeLog COPYING IDL_LICENSE.txt VERSION
%{_libdir}/libmapi.so.*
%{_libdir}/libmapiadmin.so.*
%{_libdir}/libocpf.so.*

%files -n %develname
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_libdir}/pkgconfig
%{_includedir}/*
%doc apidocs/html/libmapi
%doc apidocs/html/libocpf
%doc apidocs/html/overview
%doc apidocs/html/index.html
%{_mandir}/man3/*

%files client
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*

%files -n python-openchange
%defattr(0755,root,root,-)
%{python_sitearch}/openchange

%if %build_server
# %files server
# %defattr(-,root,root,-)
# %{_libdir}/libmapiproxy.so
# %{_libdir}/dcesrv_mapiproxy.so
# %{_libdir}/dcesrv_exchange.so
# %doc doc/howto.txt
# %doc apidocs/html/mapiproxy
%else
%exclude %{_libdir}/libmapiserver.*
%exclude %{_libdir}/libmapistore.*
%exclude %{_libdir}/mapistore_backends
%endif
