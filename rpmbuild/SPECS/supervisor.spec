%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
Summary:  A System for Allowing the Control of Process State on UNIX
Name: supervisor
Version: 3.1.1
Release: 0.1%{?prever:.%{prever}}%{?dist}
Vendor: Mozilla Release Engineering

License: ZPLv2.1 and BSD and MIT
Group: System Environment/Base
URL: http://supervisord.org/
Source0: http://pypi.python.org/packages/source/s/%{name}/%{name}-%{version}%{?prever}.tar.gz
Source1: supervisord.init
Source2: supervisord.conf
Source3: supervisor.logrotate
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
BuildRequires: python-devel
BuildRequires: python-setuptools

Requires: python-meld3 >= 0.6.5
Requires: python-setuptools
Requires(preun): /sbin/service, /sbin/chkconfig
Requires(postun): /sbin/service, /sbin/chkconfig


%description
The supervisor is a client/server system that allows its users to control a
number of processes on UNIX-like operating systems.

%prep
%setup -q -n %{name}-%{version}%{?prever}

%build
CFLAGS="%{optflags}" %{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}
mkdir -p %{buildroot}/%{_sysconfdir}
mkdir -p %{buildroot}/%{_sysconfdir}/supervisord.d
mkdir -p %{buildroot}/%{_sysconfdir}/logrotate.d/
mkdir -p %{buildroot}/etc/init.d
mkdir -p %{buildroot}/%{_localstatedir}/log/%{name}
chmod 770 %{buildroot}/%{_localstatedir}/log/%{name}
install -p -m 755 %{SOURCE1} %{buildroot}/etc/init.d/supervisord
install -p -m 644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/supervisord.conf
install -p -m 644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/logrotate.d/supervisor
sed -i s'/^#!.*//' $( find %{buildroot}/%{python_sitelib}/supervisor/ -type f)

rm -rf %{buildroot}/%{python_sitelib}/supervisor/meld3/
rm -f %{buildroot}%{_prefix}/doc/*.txt

%clean
rm -rf %{buildroot}

%post
/sbin/chkconfig --add %{name}d || :

%preun
if [ $1 = 0 ]; then
    /sbin/service supervisord stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}d || :
fi

%files
%defattr(-,root,root,-)
%dir %{_localstatedir}/log/%{name}
/etc/init.d/supervisord
%{python_sitelib}/*
%{_bindir}/supervisor*
%{_bindir}/echo_supervisord_conf
%{_bindir}/pidproxy

%config(noreplace) %{_sysconfdir}/supervisord.conf
%dir %{_sysconfdir}/supervisord.d
%config(noreplace) %{_sysconfdir}/logrotate.d/supervisor

%changelog

