#
# TODO: add gtk client package

Summary:	Nessus-core
Summary(pl):	Nessus-rdzeñ
Name:		nessus-core
Version:	2.0.0
Release:	1
License:	GPL
Group:		Networking
Source0:	ftp://ftp.nessus.org/pub/nessus/nessus-%{version}/src/%{name}-%{version}.tar.gz
Patch0:		%{name}-DESTDIR.patch
URL:		http://www.nessus.org/
BuildRequires:	autoconf
BuildRequires:	libtool
#BuildRequires:	gtk+-devel
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

%package -n nessus-devel
Summary:	-
Summary(pl):	-
Group:		Networking

%description -n nessus-devel

%description -n nessus-devel -l pl

%prep
%setup -q -n %{name}
#%patch0 -p1

%build
aclocal
%{__autoconf}
%configure \
	--disable-gtk \
	--without-x
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

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

%files -n nessus-client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%files -n nessus-devel
%defattr(644,root,root,755)
%{_includedir}/nessus/*
%exclude %{_includedir}/nessus/includes.h
