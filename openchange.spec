%define samba4_version 4.0.0-0.1.alpha10
%define talloc_version 1.2.0
%define nickname COCHRANE
%define libname %mklibname mapi 0
%define develname %mklibname -d mapi
%global build_server 1

Name: openchange
Version: 0.9
Release: %mkrel 2
Group: Networking/Mail
Summary: Provides access to Microsoft Exchange servers using native protocols
License: GPLv3+ and Public Domain
URL: http://www.openchange.org/
Source0: http://downloads.sourceforge.net/openchange/%{name}-%{version}-%{nickname}.tar.gz
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
BuildRequires: tevent-devel
BuildRequires: sqlite3-devel
BuildRequires: zlib-devel
BuildRequires: libical-devel
BuildRequires: boost-devel

%description
OpenChange provides libraries to access Microsoft Exchange servers
using native protocols.

#------------------------------------------------

%define mapi_major 0
%define libmapi %mklibname mapi %mapi_major

%package -n %libmapi
Summary: Openchange shared library supporting the MAPI protocol
Group: System/Libraries

%description -n %libmapi
Shared libraries from the Openchange project implementing the MAPI protocol

%files -n %libmapi
%defattr(-,root,root)
%{_libdir}/libmapi.so.%{mapi_major}*

#------------------------------------------------

%define mapiadmin_major 0
%define libmapiadmin %mklibname mapiadmin %mapiadmin_major

%package -n %libmapiadmin
Summary: Openchange shared library supporting the MAPI protocol
Group: System/Libraries
Conflicts:  %libname <= 0.8.2-1

%description -n %libmapiadmin
Shared libraries from the Openchange project implementing the MAPI protocol

%files -n %libmapiadmin
%defattr(-,root,root)
%{_libdir}/libmapiadmin.so.%{mapiadmin_major}*

#------------------------------------------------

%define ocpf_major 0
%define libocpf %mklibname ocpf %ocpf_major

%package -n %libocpf
Summary: Openchange shared library supporting the MAPI protocol
Group: System/Libraries
Conflicts:  %libname <= 0.8.2-1

%description -n %libocpf
Shared libraries from the Openchange project implementing the MAPI protocol

%files -n %libocpf
%defattr(-,root,root)
%{_libdir}/libocpf.so.%{ocpf_major}*

#--------------------------------------------------------------------

%package -n %develname
Summary: Developer tools for OpenChange libraries
Group: Development/C
Requires: %libmapi = %{version}-%{release}
Requires: %libmapiadmin = %{version}-%{release}
Requires: %libocpf = %{version}-%{release}
%if %build_server
Requires: %{name}-server = %{version}-%{release}
%endif
Provides: libmapi-devel = %{version}-%{release}

%description -n %develname
This package provides the development tools and headers for
OpenChange, providing libraries to access Microsoft Exchange servers
using native protocols.

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

#--------------------------------------------------------------------

%package client
Summary: User tools for OpenChange libraries
Group: Networking/Mail
Requires: %libmapi = %{version}-%{release}
Requires: %libmapiadmin = %{version}-%{release}
Requires: %libocpf = %{version}-%{release}

%description client
This package provides the user tools for OpenChange, providing access to
Microsoft Exchange servers using native protocols.

%files client
%defattr(-,root,root,-)
%doc ChangeLog COPYING IDL_LICENSE.txt VERSION
%{_bindir}/*
%{_mandir}/man1/*

#--------------------------------------------------------------------

%package -n python-openchange
Summary: Python bindings for OpenChange libraries
Group: Development/Python
Requires: openchange-client = %{version}-%{release}

%description -n python-openchange
This module contains a wrapper that allows the use of OpenChange via Python.

%files -n python-openchange
%defattr(0755,root,root,-)
%{python_sitearch}/openchange

#--------------------------------------------------------------------

%if %build_server
%package server
Summary: Server side modules for OpenChange
Group: System/Servers
Requires: samba4

%description server
This package provides the server elements for OpenChange.

%files server
%defattr(-,root,root,-)
%{_libdir}/mapistore_backends
%{_libdir}/libmapiserver.*
%{_libdir}/libmapistore.*
%endif

#--------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{version}-%{nickname}

%build
#./autogen.sh
%define _disable_ld_no_undefined 1
%configure2_5x

# Parallel builds prohibited by makefile
make
make doxygen

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

cp -r libmapi++ %{buildroot}%{_includedir}

rm -rf %{buildroot}%{_libdir}/nagios/check_exchange
rm -rf %{buildroot}%{_prefix}/modules
rm -rf %{buildroot}%{_datadir}/js
rm -rf %{buildroot}%{_datadir}/setup
rm -rf %{buildroot}%{_libdir}/libmapiproxy.so.*

# This makes the right links, as rpmlint requires that the
# ldconfig-created links be recorded in the RPM.
/sbin/ldconfig -N -n %{buildroot}/%{_libdir}

mkdir %{buildroot}%{_mandir}
cp -r doc/man/man1 %{buildroot}%{_mandir}
cp -r apidocs/man/man3 %{buildroot}%{_mandir}

%clean
rm -rf %{buildroot}
