# TODO:
# - shared gdchart+gd
# - 17 3 * * * /usr/local/sbin/nessus-update-plugins in cron (register)
# - register banner
Summary:	Nessus core package
Summary(pl.UTF-8):	Główny pakiet Nessusa
Name:		nessus-core
Version:	2.2.11
Release:	2
License:	GPL
Group:		Networking
# Source0:	ftp://ftp.nessus.org/pub/nessus/nessus-%{version}/src/%{name}-%{version}.tar.gz
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	b778c4c8e0eee912c7d62b80de920ef4
Source1:	nessusd.init
Patch0:		build.patch
URL:		http://www.nessus.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gtk+2-devel >= 2.0.0
BuildRequires:	libnasl-devel >= %{version}
BuildRequires:	libtool
BuildRequires:	nessus-libs-devel >= %{version}
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# keep in sync with nessus-libs!
%define		_localstatedir		/var/lib

%description
The "Nessus" Project aims to provide to the Internet community a free,
powerful, up-to-date and easy to use remote security scanner (i.e. a
software which will audit remotely a given network and determine
whether bad guys may break into it, or misuse it in some way).

This package contains core part of Nessus.

%description -l pl.UTF-8
Celem projektu "Nessus" jest dostarczenie społeczności internetowej
wolnodostępnego, potężnego, aktualnego i łatwego w użyciu zdalnego
skanera bezpieczeństwa (tzn. oprogramowania, które zdalnie
przeprowadza audyt podanej sieci i sprawdza, czy źli ludzie mogą się
do niej włamać lub jej nadużyć w jakiś sposób).

Ten pakiet zawiera podstawową część Nessusa.

%package -n nessusd
Summary:	Nessus daemon
Summary(pl.UTF-8):	Demon Nessusa
Group:		Networking
Requires(post,preun):	/sbin/chkconfig
Requires:	libnasl >= %{version}
Requires:	nessus-libs >= %{version}
Requires:	rc-scripts

%description -n nessusd
The "Nessus" Project aims to provide to the Internet community a free,
powerful, up-to-date and easy to use remote security scanner (i.e. a
software which will audit remotely a given network and determine
whether bad guys may break into it, or misuse it in some way).

This package contains the Nessus daemon.

%description -n nessusd -l pl.UTF-8
Celem projektu "Nessus" jest dostarczenie społeczności internetowej
wolnodostępnego, potężnego, aktualnego i łatwego w użyciu zdalnego
skanera bezpieczeństwa (tzn. oprogramowania, które zdalnie
przeprowadza audyt podanej sieci i sprawdza, czy źli ludzie mogą się
do niej włamać lub jej nadużyć w jakiś sposób).

Ten pakiet zawiera demona Nessusa.

%package -n nessus-client
Summary:	Nessus client
Summary(pl.UTF-8):	Klient nessusa
Group:		Networking

%description -n nessus-client
The "Nessus" Project aims to provide to the Internet community a free,
powerful, up-to-date and easy to use remote security scanner (i.e. a
software which will audit remotely a given network and determine
whether bad guys may break into it, or misuse it in some way).

This package contains the Nessus client.

%description -n nessus-client -l pl.UTF-8
Celem projektu "Nessus" jest dostarczenie społeczności internetowej
wolnodostępnego, potężnego, aktualnego i łatwego w użyciu zdalnego
skanera bezpieczeństwa (tzn. oprogramowania, które zdalnie
przeprowadza audyt podanej sieci i sprawdza, czy źli ludzie mogą się
do niej włamać lub jej nadużyć w jakiś sposób).

Ten pakiet zawiera klienta Nessusa.

%package -n nessus-client-gtk
Summary:	Nessus client with GTK+ GUI
Summary(pl.UTF-8):	Klient Nessusa z graficznym interfejsem GTK+
Group:		Networking
Requires:	nessus-client = %{version}-%{release}

%description -n nessus-client-gtk
Nessus client with GTK+ GUI.

%description -n nessus-client-gtk -l pl.UTF-8
Klient Nessusa z graficznym interfejsem GTK+.

%package -n nessus-devel
Summary:	Header files for Nessus plugins development
Summary(pl.UTF-8):	Pliki nagłówkowe do tworzenia wtyczek Nesussa
Group:		Networking
Requires:	nessus-libs-devel >= %{version}

%description -n nessus-devel
Header files for Nessus plugins development.

%description -n nessus-devel -l pl.UTF-8
Pliki nagłówkowe do tworzenia wtyczek Nesussa.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%configure \
	--enable-gtk
#--enable-syslog		 log messages via syslog()
#--enable-tcpwrappers	use the libwrap.a library
#--enable-unix-socket=/path	use a unix socket for client server communication
#--enable-release		set the compiler flags to -O
#--with-x				use the X Window System

%{__make} -j1

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
install nessus-services $RPM_BUILD_ROOT%{_localstatedir}/nessus/

%clean
rm -rf $RPM_BUILD_ROOT

%post -n nessusd
/sbin/chkconfig --add nessusd
%service nessusd restart "nessus daemon"
if [ "$1" = 1 ]; then
	echo "Don't forget about %{_sysconfdir}/nessus/nessusd.conf file!"
	echo "Note that if you don't have a nessusd.conf file, nessusd will create one for you!"
fi

%preun -n nessusd
if [ "$1" = "0" ]; then
	%service nessusd stop
	/sbin/chkconfig --del nessusd
fi

%files -n nessusd
%defattr(644,root,root,755)
%doc CHANGES README_SSL TODO doc/{*.txt,Top20*,WARNING.En,nsr.dtd,ntp}
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/nessusd
%{_mandir}/man8/*
%{_libdir}/nessus
%{_localstatedir}/nessus/nessus-services
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
%dir %{_includedir}/nessus
%{_includedir}/nessus/*
%exclude %{_includedir}/nessus/includes.h
