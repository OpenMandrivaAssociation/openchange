%define samba4_version 4.0.0-0.1.alpha18
%define talloc_version 1.2.0
%define nickname VULCAN
%define libname %mklibname mapi 1
%define devname %mklibname -d mapi

Summary:	Library for communicating with M$ Exchange and Outlook
Name:		openchange
Version:	2.3
Release:	1
Group:		Networking/Mail
License:	GPLv3+ and Public Domain
URL:		https://www.openchange.org/
Source0:	https://github.com/openchange/openchange/archive/openchange-%{version}-%{nickname}.tar.gz
Patch0:		openchange-2.2-linkage.patch
# 10-19 "borrowed" from Arch Linux AUR
Patch10:	nanomsg-0.9.patch
Patch11:	openchange-issue-249.patch
Patch12:	openchange-provision-type-error.patch
Patch13:	yyunput_flex2.6.patch
Patch14:	remove-private-headers.patch
#Patch15:	openchange-add_SizedXid-1.patch
Patch20:	openchange-2.3-samba-4.5.patch

BuildRequires:	bison
BuildRequires:	doxygen
BuildRequires:	flex
BuildRequires:	magic-devel
BuildRequires:	talloc-devel >= %{talloc_version}
BuildRequires:	tdb-devel
BuildRequires:	ldb-devel
BuildRequires:	popt-devel
BuildRequires:	samba-devel >= %{samba4_version}
BuildRequires:	samba-pidl >= %{samba4_version}
BuildRequires:	tevent-devel
BuildRequires:	sqlite3-devel
BuildRequires:	zlib-devel
BuildRequires:	libical-devel
BuildRequires:	boost-devel
BuildRequires:	flex-devel
BuildRequires:	pkgconfig(samba-hostconfig)
BuildRequires:	pkgconfig(samba-credentials)
BuildRequires:	pkgconfig(dcerpc)
BuildRequires:	pkgconfig(samdb)
#BuildRequires:	qt4-devel
BuildRequires:	mariadb-common
BuildRequires:	pkgconfig(mariadb)
BuildRequires:	python2-devel

%description
OpenChange is a portable Open Source implementation of Microsoft
Exchange server and Exchange protocols. It provides a complete
solution to interoperate with Microsoft Outlook clients or
Microsoft Exchange servers.

OpenChange client-side library is used in existing messaging
clients and is the solution in new projects to communicate natively
with Microsoft Exchange and Exchange-compatible servers. OpenChange
server is a transparent Microsoft Exchange server replacement using
native Exchange protocols and does not require any plugin installation
in Outlook.

#------------------------------------------------
%package -n nagios-%{name}
Summary:	NAGIOS module for checking %{name} integrity
Group:		System/Libraries

%description -n nagios-%{name}
NAGIOS module for checking %{name} integrity

%files -n nagios-%{name}
%{_libdir}/nagios/check_exchange

#------------------------------------------------

%define mapi_major 0
%define libmapi %mklibname mapi %mapi_major

%package -n %libmapi
Summary:	Openchange shared library supporting the MAPI protocol
Group:		System/Libraries

%description -n %libmapi
Shared libraries from the Openchange project implementing
the MAPI protocol

%files -n %libmapi
%{_libdir}/libmapi.so.%{mapi_major}*
%{_libdir}/libmapi.so.%{version}
%{_libdir}/libmapipp.so.%{mapi_major}*
%{_libdir}/libmapipp.so.%{version}
#------------------------------------------------

%define mapiadmin_major 0
%define libmapiadmin %mklibname mapiadmin %mapiadmin_major

%package -n %libmapiadmin
Summary:	Openchange shared library supporting the MAPI protocol
Group:		System/Libraries
Conflicts:	%{libname} <= 0.8.2-1

%description -n %libmapiadmin
Shared libraries from the Openchange project implementing
the MAPI protocol

%files -n %libmapiadmin
%{_libdir}/libmapiadmin.so.%{mapiadmin_major}*
%{_libdir}/libmapiadmin.so.%{version}

#------------------------------------------------

%define mapiproxy_major 0
%define libmapiproxy %mklibname mapiproxy %mapiproxy_major

%package -n %libmapiproxy
Summary:	Openchange shared library supporting the MAPI Proxy protocol
Group:		System/Libraries

%description -n %libmapiproxy
Shared libraries from the Openchange project implementing
the MAPI Proxy protocol

%files -n %libmapiproxy
%{_libdir}/libmapiproxy.so.%{mapiproxy_major}*
%{_libdir}/libmapiproxy.so.%{version}


#------------------------------------------------

%define mapiserver_major 0
%define libmapiserver %mklibname mapiserver %mapiserver_major

%package -n %libmapiserver
Summary:	Openchange shared library supporting the MAPI Server protocol
Group:		System/Libraries

%description -n %libmapiserver
Shared libraries from the Openchange project implementing
the MAPI Server protocol

%files -n %libmapiserver
%{_libdir}/libmapiserver.so.%{mapiserver_major}*
%{_libdir}/libmapiserver.so.%{version}

#------------------------------------------------

%define mapistore_major 0
%define libmapistore %mklibname mapistore %mapistore_major

%package -n %libmapistore
Summary:	Openchange shared library supporting the MAPI Store protocol
Group:		System/Libraries

%description -n %libmapistore
Shared libraries from the Openchange project implementing
the MAPI Store protocol

%files -n %libmapistore
%{_libdir}/libmapistore.so.%{mapistore_major}*
%{_libdir}/libmapistore.so.%{version}

#------------------------------------------------

%define ocpf_major 0
%define libocpf %mklibname ocpf %ocpf_major

%package -n %libocpf
Summary:	Openchange shared library supporting the MAPI protocol
Group:		System/Libraries
Conflicts:	%{libname} <= 0.8.2-1

%description -n %libocpf
Shared libraries from the Openchange project implementing
the MAPI protocol

%files -n %libocpf
%{_libdir}/libocpf.so.%{ocpf_major}*
%{_libdir}/libocpf.so.%{version}

#--------------------------------------------------------------------

%package -n %{devname}
Summary:	Developer tools for OpenChange libraries
Group:		Development/C
Requires:	%libmapi = %{EVRD}
Requires:	%libmapiadmin = %{EVRD}
Requires:	%libocpf = %{EVRD}
Requires:	%libmapiserver = %{EVRD}
Requires:	%libmapistore = %{EVRD}
Provides:	libmapi-devel = %{EVRD}
%define __noautoreq 'devel.*libndr-samba'

%description -n %{devname}
This package provides the development tools and headers for
OpenChange, providing libraries to access Microsoft Exchange servers
using native protocols.

%files -n %{devname}
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
Summary:	User tools for OpenChange libraries
Group:		Networking/Mail
Requires:	%libmapi = %{version}-%{release}
Requires:	%libmapiadmin = %{version}-%{release}
Requires:	%libocpf = %{version}-%{release}

%description client
This package provides the user tools for OpenChange, providing access to
Microsoft Exchange servers using native protocols.

%files client
%doc COPYING IDL_LICENSE.txt VERSION
%{_bindir}/*
%{_mandir}/man1/*

#--------------------------------------------------------------------

%package -n python2-openchange
Summary:	Python 2.x bindings for OpenChange libraries
Group:		Development/Python
Requires:	openchange-client = %{version}-%{release}

%description -n python2-openchange
This module contains a wrapper that allows the use of OpenChange via Python.

%files -n python2-openchange
%{python2_sitearch}/openchange

#--------------------------------------------------------------------

%package server
Summary:	Server side modules for OpenChange
Group:		System/Servers
Requires:	samba-server >= 4.0
Requires:	%libmapiserver = %{EVRD}
Requires:	%libmapistore = %{EVRD}

%description server
This package provides the server elements for OpenChange.

%files server
%{_libdir}/openchange/modules
%{_sbindir}/openchange_newuser
%{_sbindir}/openchange_group
%{_sbindir}/openchange_migrate
%{_sbindir}/openchange_neworganization
%{_sbindir}/openchange_provision
%{_libdir}/samba/dcerpc_server/dcesrv_mapiproxy.so
%{_libdir}/samba/dcerpc_server/dcesrv_asyncemsmdb.so
%{_datadir}/samba/setup/AD
%{_datadir}/samba/setup/mapistore
%{_datadir}/samba/setup/openchangedb
%{_datadir}/samba/setup/profiles
%{_datadir}/mapitest

#--------------------------------------------------------------------

%prep
%setup -qn %{name}-%{name}-%{version}-%{nickname}
%autopatch -p1
# Configure @LIBDIR@ bits introduced by patch 1
sed -i -e 's,@LIBDIR@,%{_libdir},g' Makefile
# Share the setup dir with samba
sed -i -e 's,$(datadir)/setup,$(datadir)/samba/setup,g' Makefile config.mk.in
[ -e configure ] || ./autogen.sh

%build
#./autogen.sh
%define _disable_ld_no_undefined 1
find . -name "*.py" |xargs sed -i -e 's,#!/usr/bin/python,#!/usr/bin/python2,'
export PYTHON=%{_bindir}/python2
export PYTHON_CONFIG=%{_bindir}/python2-config
%configure \
	--with-modulesdir=%{_libdir}/openchange/modules \
	--enable-pyopenchange \
	--enable-openchange-qt4


# Parallel builds prohibited by makefile
%make
make doxygen

%install
%makeinstall_std samba_setupdir=%{_datadir}/samba/setup

#cp -r libmapi++ %{buildroot}%{_includedir}

# This makes the right links, as rpmlint requires that the
# ldconfig-created links be recorded in the RPM.
/sbin/ldconfig -N -n %{buildroot}/%{_libdir}

mkdir %{buildroot}%{_mandir}
cp -r doc/man/man1 %{buildroot}%{_mandir}
cp -r apidocs/man/man3 %{buildroot}%{_mandir}
