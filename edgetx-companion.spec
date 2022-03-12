
Summary: EdgeTX Companion
Name: edgetx-companion

Version: 2.6.0
Release: 1%{?dist}
License: GPLv2
URL: https://edgetx.org/
Source0: https://github.com/EdgeTX/edgetx/archive/refs/tags/v%{version}.tar.gz#/edgetx-%{version}.tar.gz
Source1: https://github.com/MikeBland/OpenRcBootloader/releases/download/V1.9/bootflash4.lbm
Source2: https://github.com/MikeBland/OpenRcBootloader/releases/download/V1.9/bootflash8.lbm
Source11: https://github.com/EdgeTX/libopenui/archive/f193395874ef6d371ce4fca9c3c222db88d60816.tar.gz#/libopenui-f1933958.tar.gz
Source12: https://github.com/nothings/stb/archive/7cce4c3ad9a147c67258c5966f676d8436140939.tar.gz#/stb-7cce4c3a.tar.gz
Source13: https://github.com/jbeder/yaml-cpp/archive/bce601f2bf25b6579eb94d6d3402d645aae3c375.tar.gz#/yaml-cpp-bce601f2.tar.gz
Patch1: edgetx-cmake.patch
Patch2: edgetx-desktop.patch
Patch3: edgetx-OpenRcBootloader-local.patch
Patch4: edgetx-disable-appimage.patch

BuildRequires: cmake
BuildRequires: make
BuildRequires: gcc-c++
BuildRequires: qt5-qttools-devel, qt5-qtsvg-devel, qt5-qtmultimedia-devel
BuildRequires: fox-devel
BuildRequires: SDL-devel
BuildRequires: arm-none-eabi-gcc-cs-c++
BuildRequires: arm-none-eabi-newlib
BuildRequires: python3-pillow
BuildRequires: llvm-googletest
Requires: dfu-util

%description
OpenTX Companion transmitter support software is used for many different
tasks like loading OpenTX firmware to the radio, backing up model
settings, editing settings and running radio simulators. 

%prep
%setup -n edgetx-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
( cd radio/src/thirdparty && tar xvzf %SOURCE11 && rmdir libopenui && ln -s libopenui-* libopenui )
( cd radio/src/thirdparty/libopenui/src/thirdparty && tar xvzf %SOURCE12 && rmdir stb && ln -s stb-* stb )
( cd companion/src/thirdparty && tar xvzf %SOURCE13 && rmdir yaml-cpp && ln -s yaml-cpp-* yaml-cpp )
mkdir -p %{_vpath_builddir}/radio/src
cp %SOURCE1 %SOURCE2 %{_vpath_builddir}/radio/src/

%set_build_flags
mkdir bin
cat > bin/cmake <<'EOS'
#!/bin/bash
set -x
%cmake "$@"
EOS
cat > bin/cmake_build <<'EOS'
#!/bin/bash
set -x
%cmake_build "$@"
EOS
sed '1,/^cd build/d;/^make.*package/,$d;s%^cmake%bin/&%;s#^make .* libsimulator#bin/cmake_build --target libsimulator#;s#CMakeCache.txt#%{_vpath_builddir}/&#;' tools/build-companion-release.sh > bin/build-companion-release.sh
chmod a+x bin/*

%build
CMAKE_OPTS="-DGVARS=YES -DLUA=YES -DHELI=YES -DMULTIMODULE=YES -DPPM_LIMITS_SYMETRICAL=YES -DAUTOSWITCH=YES -DAUTOSOURCE=YES -DPPM_CENTER_ADJUSTABLE=YES -DFLIGHT_MODES=YES -DOVERRIDE_CHANNEL_FUNCTION=YES -DFRSKY_STICKS=YES -DDEBUG=YES -DCMAKE_BUILD_TYPE=Debug -DBUILD_SHARED_LIBS:BOOL=OFF -DGTEST_ROOT=%{_datarootdir}/llvm/src/utils/unittest/googletest"
%cmake $CMAKE_OPTS
%cmake_build --target edgetx-companion
%cmake_build --target edgetx-simulator
COMMON_OPTIONS="$CMAKE_OPTS" bin/build-companion-release.sh

%install
%cmake_install

%files
%defattr(-,root,root,-)
%{_bindir}/edgetx-companion
%{_bindir}/edgetx-simulator
%dir %{_libdir}/edgetx-companion-26
%{_libdir}/edgetx-companion-26/libedgetx-t8-simulator.so
%{_libdir}/edgetx-companion-26/libedgetx-t16-simulator.so
%{_libdir}/edgetx-companion-26/libedgetx-t12-simulator.so
%{_libdir}/edgetx-companion-26/libedgetx-t18-simulator.so
%{_libdir}/edgetx-companion-26/libedgetx-tlite-simulator.so
%{_libdir}/edgetx-companion-26/libedgetx-tx12-simulator.so
%{_libdir}/edgetx-companion-26/libedgetx-tx16s-simulator.so
%{_libdir}/edgetx-companion-26/libedgetx-x7-simulator.so
%{_libdir}/edgetx-companion-26/libedgetx-x7access-simulator.so
%{_libdir}/edgetx-companion-26/libedgetx-x9d-simulator.so
%{_libdir}/edgetx-companion-26/libedgetx-x9d+-simulator.so
%{_libdir}/edgetx-companion-26/libedgetx-x9d+2019-simulator.so
%{_libdir}/edgetx-companion-26/libedgetx-x9e-simulator.so
%{_libdir}/edgetx-companion-26/libedgetx-x9lite-simulator.so
%{_libdir}/edgetx-companion-26/libedgetx-x9lites-simulator.so
%{_libdir}/edgetx-companion-26/libedgetx-x10-simulator.so
%{_libdir}/edgetx-companion-26/libedgetx-x10express-simulator.so
%{_libdir}/edgetx-companion-26/libedgetx-x12s-simulator.so
%{_libdir}/edgetx-companion-26/libedgetx-xlite-simulator.so
%{_libdir}/edgetx-companion-26/libedgetx-xlites-simulator.so
%{_prefix}/lib/udev/rules.d/45-edgetx-companion-taranis.rules
%{_prefix}/lib/udev/rules.d/45-edgetx-companion-usbasp.rules
%{_datadir}/applications/edgetx-companion26.desktop
%{_datadir}/applications/edgetx-simulator26.desktop
%{_datadir}/icons/hicolor/16x16/apps/edgetx-companion.png
%{_datadir}/icons/hicolor/22x22/apps/edgetx-companion.png
%{_datadir}/icons/hicolor/24x24/apps/edgetx-companion.png
%{_datadir}/icons/hicolor/32x32/apps/edgetx-companion.png
%{_datadir}/icons/hicolor/48x48/apps/edgetx-companion.png
%{_datadir}/icons/hicolor/128x128/apps/edgetx-companion.png
%{_datadir}/icons/hicolor/256x256/apps/edgetx-companion.png
%{_datadir}/icons/hicolor/512x512/apps/edgetx-companion.png
%{_datadir}/icons/hicolor/scalable/apps/edgetx-companion.png

%changelog
* Mon Mar 21 2022 Jan Pazdziora <jpx-edgetx@adelton.com> - 2.6.0-1
- Rebase to EdgeTX 2.6.0.

* Sun Mar 20 2022 Jan Pazdziora <jpx-edgetx@adelton.com> - 2.5.0-1
- Rebase to EdgeTX 2.5.0.

* Sun Mar 20 2022 Jan Pazdziora <jpx-opentx@adelton.com> - 2.3.14-3
- Switch to building using upstream's tools/build-companion-release.sh.

* Fri Mar 11 2022 Jan Pazdziora <jpx-opentx@adelton.com> - 2.3.14-2
- Include missing update of the revision to 2.3.14.

* Sat Jul 24 2021 Jan Pazdziora <jpx-opentx@adelton.com> - 2.3.14-1
- Rebase to 2.3.14.

* Thu Jun 24 2021 Jan Pazdziora <jpx-opentx@adelton.com> - 2.3.13-1
- Rebase to 2.3.13.

* Tue Jun 15 2021 Jan Pazdziora <jpx-opentx@adelton.com> - 2.3.12-1
- Rebase to 2.3.12.

* Sat Jan 09 2021 Jan Pazdziora <jpx-opentx@adelton.com> - 2.3.11-1
- Rebase to 2.3.11.

* Fri Oct 16 2020 Jan Pazdziora <jpx-opentx@adelton.com> - 2.3.10-1
- Rebase to 2.3.10.

* Mon Jun 15 2020 Jan Pazdziora <jpx-opentx@adelton.com> - 2.3.9-1
- Rebase to 2.3.9.

* Sat Jun 13 2020 Jan Pazdziora <jpx-opentx@adelton.com> - 2.3.8-1
- Rebase to 2.3.8.

* Sat Apr 18 2020 Jan Pazdziora <jpx-opentx@adelton.com> - 2.3.7-3
- Enable building simulator of Jumper T16.

* Sun Mar 29 2020 Jan Pazdziora <jpx-opentx@adelton.com> - 2.3.7-1
- Rebase to 2.3.7.

* Sun Jan 19 2020 Jan Pazdziora <jpx-opentx@adelton.com> - 2.3.5-1
- Rebase to 2.3.5.

* Fri Dec 27 2019 Jan Pazdziora <jpx-opentx@adelton.com> - 2.3.4-1
- Rebase to 2.3.4.

* Sat Dec 21 2019 Jan Pazdziora <jpx-opentx@adelton.com> - 2.3.3-1
- Rebase to 2.3.3.

* Sat Nov 16 2019 Jan Pazdziora <jpx-opentx@adelton.com> - 2.3.2-2
- Rebase to 2.3.2.

* Sat Oct 05 2019 Jan Pazdziora <jpx-opentx@adelton.com> - 2.3.1-1
- Rebase to 2.3.1.

* Sat Sep 28 2019 Jan Pazdziora <jpx-opentx@adelton.com> - 2.3.0-1
- Rebase to 2.3.0 GA.

* Sun Sep 15 2019 Jan Pazdziora <jpx-opentx@adelton.com> - 2.3.0-RC3.1
- Test build of 2.3.0-RC3.

* Fri Jul 12 2019 Jan Pazdziora <jpx-opentx@adelton.com> - 2.2.4-1
- Rebase to 2.2.4 release.

* Fri Jul 12 2019 Jan Pazdziora <jpx-opentx@adelton.com> - 2.2.3-1
- Address compile errors on Fedora 30+.
- Rebase to 2.2.3 release.

* Sun Sep 30 2018 Jan Pazdziora <jpx-opentx@adelton.com> - 2.2.2-1
- Rebase to 2.2.2 release.

* Sun Sep 30 2018 Jan Pazdziora <jpx-opentx@adelton.com> - 2.2.1-1
- Rebase to 2.2.1 release.

* Sun Aug 20 2017 Jan Pazdziora <jpx-opentx@adelton.com> - 2.2.1-*
- Rebase to 2.2 master.

* Sat Aug 19 2017 Jan Pazdziora <jpx-opentx@adelton.com> - 2.2.0-1
- Rebase to 2.2.0.

* Sat Jul 15 2017 Jan Pazdziora <jpx-opentx@adelton.com> - 2.1.9-4
- Drive the build and installation by cmake and macros more.

* Fri Jul 14 2017 Jan Pazdziora <jpx-opentx@adelton.com> - 2.1.9-2
- Rebase to 2.1.9.

* Fri Jun 27 2014 Jan Pazdziora <jpx-opentx@adelton.com> - 2.0.5-1
- Use 2.0.5.

* Fri Jun 13 2014 Jan Pazdziora <jpx-opentx@adelton.com> - 2.0.2-0.1
- Use 2.0.2.

* Fri Jun 06 2014 Jan Pazdziora <jpx-opentx@adelton.com> - 2.0.1-0.1
- Use 2.0.1.

* Sun Jun 01 2014 Jan Pazdziora <jpx-opentx@adelton.com> - 1.99.7-0.1
- Initial attempt to build on Fedora 20.

