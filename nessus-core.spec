# TODO: shared gdchart+gd
Summary:	Nessus core package
Summary(pl):	G³ówny pakiet Nessusa
Name:		nessus-core
Version:	2.0.6a
Release:	0.1
License:	GPL
Group:		Networking
Source0:	ftp://ftp.nessus.org/pub/nessus/nessus-%{version}/src/%{name}-%{version}.tar.gz
#Source0-md5:	2dd997d65d1785526fe9d87393ce0417
URL:		http://www.nessus.org/
BuildRequires:	autoconf
BuildRequires:	gtk+-devel
BuildRequires:	libnasl-devel >= 2.0.1
BuildRequires:	libtool
BuildRequires:	nessus-libs-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_localstatedir		/var/lib

%description
The "Nessus" Project aims to provide to the Internet community a free,
powerful, up-to-date and easy to use remote security scanner (i.e. a
software which will audit remotely a given network and determine
whether bad guys may break into it, or misuse it in some way).

This package contains core part of Nessus.

%description -l pl
Celem projektu "Nessus" jest dostarczenie spo³eczno¶ci internetowej
wolnodostêpnego, potê¿nego, aktualnego i ³atwego w u¿yciu zdalnego
skanera bezpieczeñstwa (tzn. oprogramowania, które zdalnie
przeprowadza audyt podanej sieci i sprawdza, czy ¼li ludzie mog± siê
do niej w³amaæ lub jej nadu¿yæ w jaki¶ sposób).

Ten pakiet zawiera podstawow± czê¶æ Nessusa.

%package -n nessusd
Summary:	Nessus daemon
Summary(pl):	Demon Nessusa
Group:		Networking

%description -n nessusd
The "Nessus" Project aims to provide to the Internet community a free,
powerful, up-to-date and easy to use remote security scanner (i.e. a
software which will audit remotely a given network and determine
whether bad guys may break into it, or misuse it in some way).

This package contains the Nessus daemon.

%description -n nessusd -l pl
Celem projektu "Nessus" jest dostarczenie spo³eczno¶ci internetowej
wolnodostêpnego, potê¿nego, aktualnego i ³atwego w u¿yciu zdalnego
skanera bezpieczeñstwa (tzn. oprogramowania, które zdalnie
przeprowadza audyt podanej sieci i sprawdza, czy ¼li ludzie mog± siê
do niej w³amaæ lub jej nadu¿yæ w jaki¶ sposób).

Ten pakiet zawiera demona Nessusa.

%package -n nessus-client
Summary:	Nessus client
Summary(pl):	Klient nessusa
Group:		Networking

%description -n nessus-client
The "Nessus" Project aims to provide to the Internet community a free,
powerful, up-to-date and easy to use remote security scanner (i.e. a
software which will audit remotely a given network and determine
whether bad guys may break into it, or misuse it in some way).

This package contains the Nessus client.

%description -n nessus-client -l pl
Celem projektu "Nessus" jest dostarczenie spo³eczno¶ci internetowej
wolnodostêpnego, potê¿nego, aktualnego i ³atwego w u¿yciu zdalnego
skanera bezpieczeñstwa (tzn. oprogramowania, które zdalnie
przeprowadza audyt podanej sieci i sprawdza, czy ¼li ludzie mog± siê
do niej w³amaæ lub jej nadu¿yæ w jaki¶ sposób).

Ten pakiet zawiera klienta Nessusa.

%package -n nessus-client-gtk
Summary:	Nessus client with GTK GUI
Summary(pl):	Klient Nessusa z graficznym interfejsem GTK
Group:		Networking
Requires:	nessus-client = %{version}

%description -n nessus-client-gtk
Nessus client with GTK GUI.

%description -n nessus-client-gtk -l pl
Klient Nessusa z graficznym interfejsem GTK.

%package -n nessus-devel
Summary:	Header files for Nessus plugins development
Summary(pl):	Pliki nag³ówkowe do tworzenia wtyczek Nesussa
Group:		Networking
Requires:	nessus-libs-devel

%description -n nessus-devel
Header files for Nessus plugins development.

%description -n nessus-devel -l pl
Pliki nag³ówkowe do tworzenia wtyczek Nesussa.

%prep
%setup -q -n %{name}

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%configure \
	--enable-gtk

%{__make}

mv -f nessus/nessus nessus-gtk

%{__make} -C nessus clean
sed -e 's@^#define USE_GTK 1@/* #undef USE_GTK */@' include/config.h > config.tmp
mv -f config.tmp include/config.h
%{__make} -C nessus \
	GTKLIBS= \
	GTKCONFIG_CFLAGS= \
	GLIBCONFIG_CFLAGS= \
	X_LIBS= \
	USE_GTK=

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install nessus-gtk $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files -n nessusd
%defattr(644,root,root,755)
%doc CHANGES README_SSL TODO doc/{*.txt,Top20*,WARNING.En,nsr.dtd,unbsp.c,ntp}
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*
%{_libdir}/nessus
%{_sysconfdir}/nessus
%{_localstatedir}/nessus

%files -n nessus-client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%exclude %{_bindir}/nessus-gtk
%{_mandir}/man1/*

%files -n nessus-client-gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/nessus-gtk

%files -n nessus-devel
%defattr(644,root,root,755)
%{_includedir}/nessus/*
%exclude %{_includedir}/nessus/includes.h
