
Summary: OpenTX Companion
Name: opentx-companion
Version: 2.1.9
Release: 2%{?dist}
License: GPLv2
URL: http://www.open-tx.org
Source0: https://github.com/opentx/opentx/archive/%{version}.tar.gz#/opentx-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: git svn qt qt-devel cmake patch xsd gcc-c++ SDL-devel phonon phonon-devel
BuildRequires: xerces-c-devel PyQt4 python2 avr-gcc
Requires: dfu-util

%description
OpenTX Companion transmitter support software is used for many different
tasks like loading OpenTX firmware to the radio, backing up model
settings, editing settings and running radio simulators. 

%prep
%setup -q -n opentx-%{version}

%build
rm -rf companion/lbuild
mkdir companion/lbuild
cd companion/lbuild
cmake ../src
make clean
make

sed 's/companion21/opentx-companion/' companion.desktop > opentx-companion.desktop

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
install -m 755 companion/lbuild/companion21 $RPM_BUILD_ROOT/usr/bin/opentx-companion
mkdir -p $RPM_BUILD_ROOT/etc/udev/rules.d
install -m 644 companion/targets/linux/* $RPM_BUILD_ROOT/etc/udev/rules.d
mkdir -p $RPM_BUILD_ROOT/usr/share/applications
install -m 644 companion/lbuild/opentx-companion.desktop $RPM_BUILD_ROOT/usr/share/applications
mkdir -p $RPM_BUILD_ROOT/usr/share/icons/hicolor/16x16/apps
install -m 644 companion/src/images/linuxicons/16x16/companion.png $RPM_BUILD_ROOT/usr/share/icons/hicolor/16x16/apps/opentx-companion.png
mkdir -p $RPM_BUILD_ROOT/usr/share/icons/hicolor/32x32/apps
install -m 644 companion/src/images/linuxicons/32x32/companion.png $RPM_BUILD_ROOT/usr/share/icons/hicolor/32x32/apps/opentx-companion.png
mkdir -p $RPM_BUILD_ROOT/usr/share/icons/hicolor/128x128/apps
install -m 644 companion/src/images/linuxicons/128x128/companion.png $RPM_BUILD_ROOT/usr/share/icons/hicolor/128x128/apps/opentx-companion.png
mkdir -p $RPM_BUILD_ROOT/usr/share/icons/hicolor/512x512/apps
install -m 644 companion/src/images/linuxicons/512x512/companion.png $RPM_BUILD_ROOT/usr/share/icons/hicolor/512x512/apps/opentx-companion.png
mkdir -p $RPM_BUILD_ROOT/usr/share/icons/hicolor/scalable/apps
install -m 644 companion/src/images/linuxicons/scalable/companion.svg $RPM_BUILD_ROOT/usr/share/icons/hicolor/scalable/apps/opentx-companion.svg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/usr/bin/opentx-companion
/etc/udev/rules.d/*
/usr/share/applications
/usr/share/icons/hicolor/*

%changelog
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

