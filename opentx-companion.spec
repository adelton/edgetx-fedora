
Summary: OpenTX Companion
Name: opentx-companion

%global branch0 2.1
%global commit0 45dc76bf4be111a01d680eefe30be213daba95ce
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Version: 2.1.10
Release: git_%{shortcommit0}.4%{?dist}
License: GPLv2
URL: http://www.open-tx.org
Source0: https://github.com/opentx/opentx/archive/%{commit0}.tar.gz#/opentx-%{shortcommit0}.tar.gz
Patch1: opentx-cmake.patch
Patch2: opentx-desktop.patch
Patch3: opentx-springSF.patch
BuildRequires: git svn qt qt-devel cmake patch xsd gcc-c++ SDL-devel phonon phonon-devel
BuildRequires: xerces-c-devel PyQt4 python2 avr-gcc
Requires: dfu-util

%description
OpenTX Companion transmitter support software is used for many different
tasks like loading OpenTX firmware to the radio, backing up model
settings, editing settings and running radio simulators. 

%prep
%setup -n opentx-%{commit0}
%patch1
%patch2
%patch3 -p1

%build
rm -rf companion/lbuild
mkdir companion/lbuild
cd companion/lbuild
%cmake -DBUILD_SHARED_LIBS:BOOL=OFF ../src
make %{?_smp_mflags}

%install
make -C companion/lbuild install DESTDIR=%{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/opentx-companion
%{_bindir}/opentx-simulator
%{_libdir}/opentx-companion-21/
%{_prefix}/lib/udev/rules.d/*
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*

%changelog
* Sat Jul 15 2017 Jan Pazdziora <jpx-opentx@adelton.com> - 2.1.10-*
- WIP.

* Sat Jul 15 2017 Jan Pazdziora <jpx-opentx@adelton.com> - 2.1.9-4
- Drive the build and installation by cmake and macros more.

* Fri Jul 14 2017 Jan Pazdziora <jpx-opentx@adelton.com> - 2.1.9-2
- Rebase to 2.1.9.

* Fri Jun 27 2014 Jan Pazdziora <jpx-opentx@adelton.com> - 2.0.5-1
- Use 2.0.2.

* Fri Jun 13 2014 Jan Pazdziora <jpx-opentx@adelton.com> - 2.0.2-0.1
- Use 2.0.2.

* Fri Jun 06 2014 Jan Pazdziora <jpx-opentx@adelton.com> - 2.0.1-0.1
- Use 2.0.1.

* Sun Jun 01 2014 Jan Pazdziora <jpx-opentx@adelton.com> - 1.99.7-0.1
- Initial attempt to build on Fedora 20.

