Summary:	Nessus-core
Summary(pl):	Nessus-rdzeñ
Name:		nessus-core
Version:	1.2.5
Release:	1
License:	GPL
Group:		Networking
Source0:	ftp://ftp.nessus.org/pub/nessus/nessus-%{version}/src/%{name}-%{version}.tar.gz
Patch0:		%{name}-DESTDIR.patch
URL:		http://www.nessus.org/
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRequires:	gtk+-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_localstatedir		/var/lib

%description

%package -n nessusd
Summary:	-
Summary(pl):	-
Group:		Networking

%description -n nessusd

%description -n nessusd -l pl

%package -n nessus-client
Summary:	-
Summary(pl):	-
Group:		Networking

%description -n nessus-client

%description -n nessus-client -l pl

%prep
%setup -q -n %{name}
%patch0 -p1

%build
aclocal
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_includedir}/nessus/includes.h

%clean
rm -rf $RPM_BUILD_ROOT

%files -n nessusd
%defattr(644,root,root,755)
%doc doc/*.txt
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*
%{_libdir}/nessus
%{_sysconfdir}/nessus
%{_localstatedir}/nessus
%{_includedir}/nessus/*

%files -n nessus-client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*
