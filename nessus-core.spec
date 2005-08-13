# TODO:
# - shared gdchart+gd
Summary:	Nessus core package
Summary(pl):	G³ówny pakiet Nessusa
Name:		nessus-core
Version:	2.2.5
Release:	1
License:	GPL
Group:		Networking
Source0:	ftp://ftp.nessus.org/pub/nessus/nessus-%{version}/src/%{name}-%{version}.tar.gz
# Source0-md5:	282de0aa80a5c85aeab12bf556933694
Source1:	nessusd.init
URL:		http://www.nessus.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gtk+2-devel >= 2.0.0
BuildRequires:	libnasl-devel >= %{version}
BuildRequires:	libtool
BuildRequires:	nessus-libs-devel >= %{version}
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# keep in sync with nessus-libs!
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
Requires:	libnasl >= %{version}
Requires:	nessus-libs >= %{version}

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
Summary:	Nessus client with GTK+ GUI
Summary(pl):	Klient Nessusa z graficznym interfejsem GTK+
Group:		Networking
Requires:	nessus-client = %{version}-%{release}

%description -n nessus-client-gtk
Nessus client with GTK+ GUI.

%description -n nessus-client-gtk -l pl
Klient Nessusa z graficznym interfejsem GTK+.

%package -n nessus-devel
Summary:	Header files for Nessus plugins development
Summary(pl):	Pliki nag³ówkowe do tworzenia wtyczek Nesussa
Group:		Networking
Requires:	nessus-libs-devel >= %{version}

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
install -d $RPM_BUILD_ROOT%{_localstatedir}/nessus/logs

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install nessus-gtk $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/nessusd

%clean
rm -rf $RPM_BUILD_ROOT

%post -n nessusd
echo "Run \"/sbin/chkconfig --add nessusd\" to activate nessus daemon."
echo "then run \"/etc/rc.d/init.d/nessusd start\" to start nessus daemon."
echo "don't forget about /etc/nessus/nessusd.conf file!"
echo "Note that if you don't have a nessusd.conf file, nessusd will create one for you!"

%preun -n nessusd
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/nessusd ]; then
		/etc/rc.d/init.d/nessusd stop >&2
	fi
	/sbin/chkconfig --del nessusd
fi

%files -n nessusd
%defattr(644,root,root,755)
%doc CHANGES README_SSL TODO doc/{*.txt,Top20*,WARNING.En,nsr.dtd,ntp}
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/nessusd
%{_mandir}/man8/*
%{_libdir}/nessus
%{_sysconfdir}/nessus
%dir %{_localstatedir}/nessus/logs

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
