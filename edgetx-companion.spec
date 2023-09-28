
Summary: EdgeTX Companion
Name: edgetx-companion

Version: 2.9.1
Release: 1%{?dist}
License: GPLv2
URL: https://edgetx.org/
Source0: https://github.com/EdgeTX/edgetx/archive/refs/tags/v%{version}.tar.gz#/edgetx-%{version}.tar.gz
Source12: https://github.com/nothings/stb/archive/7cce4c3ad9a147c67258c5966f676d8436140939.tar.gz#/stb-7cce4c3a.tar.gz
Source13: https://github.com/jbeder/yaml-cpp/archive/1b50109f7bea60bd382d8ea7befce3d2bd67da5f.tar.gz#/yaml-cpp-1b50109f.tar.gz
Source14: https://github.com/EdgeTX/lvgl/archive/9a414b1d48d2893133b6038ec80d59fb157aade4.tar.gz#/lvgl-9a414b1d.tar.gz
Patch1: edgetx-cmake.patch
Patch2: edgetx-desktop.patch
Patch4: edgetx-disable-appimage.patch
Patch5: build-simulator.sh.patch

BuildRequires: cmake
BuildRequires: make
BuildRequires: gcc-c++
BuildRequires: clang-devel
BuildRequires: qt5-qttools-devel, qt5-qtsvg-devel, qt5-qtmultimedia-devel
BuildRequires: fox-devel
BuildRequires: SDL2-devel
BuildRequires: python3-pillow python3-lz4 python3-clang
Requires: dfu-util

%description
OpenTX Companion transmitter support software is used for many different
tasks like loading OpenTX firmware to the radio, backing up model
settings, editing settings and running radio simulators. 

%prep
%autosetup -n edgetx-%{version} -p1
( cd radio/src/thirdparty/libopenui/thirdparty && tar xvzf %SOURCE12 && rmdir stb && ln -s stb-* stb )
( cd radio/src/thirdparty/libopenui/thirdparty && tar xvzf %SOURCE14 && rmdir lvgl && ln -s lvgl-* lvgl )
( cd companion/src/thirdparty && tar xvzf %SOURCE13 && rmdir yaml-cpp && ln -s yaml-cpp-* yaml-cpp )

%set_build_flags
mkdir bin
cat > bin/cmake <<'EOS'
#!/bin/bash
set -x
%cmake "$@"
EOS
chmod a+x bin/cmake

%build
CMAKE_OPTS="-DGVARS=YES -DLUA=YES -DHELI=YES -DMULTIMODULE=YES -DPPM_LIMITS_SYMETRICAL=YES -DAUTOSWITCH=YES -DAUTOSOURCE=YES -DPPM_CENTER_ADJUSTABLE=YES -DFLIGHT_MODES=YES -DOVERRIDE_CHANNEL_FUNCTION=YES -DFRSKY_STICKS=YES -DDEBUG=YES -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS:BOOL=OFF -DGTEST_ROOT=$(pwd)/companion/src/thirdparty/yaml-cpp/test/gtest-1.11.0/googletest"
%cmake $CMAKE_OPTS -DPCB=X9D
make -C %{_vpath_builddir} native-configure
make -C %{_vpath_builddir} companion
make -C %{_vpath_builddir} simulator
tools/build-companion.sh "$(pwd)" "$(pwd)/%{_vpath_builddir}" "$CMAKE_OPTS" release

%install
%{cmake_install}/native

%files
%defattr(-,root,root,-)
%{_bindir}/edgetx-companion
%{_bindir}/edgetx-simulator
%dir %{_libdir}/edgetx-companion-29
%{_libdir}/edgetx-companion-29/libedgetx-boxer-simulator.so
%{_libdir}/edgetx-companion-29/libedgetx-commando8-simulator.so
%{_libdir}/edgetx-companion-29/libedgetx-lr3pro-simulator.so
%{_libdir}/edgetx-companion-29/libedgetx-nv14-simulator.so
%{_libdir}/edgetx-companion-29/libedgetx-t8-simulator.so
%{_libdir}/edgetx-companion-29/libedgetx-t16-simulator.so
%{_libdir}/edgetx-companion-29/libedgetx-t12-simulator.so
%{_libdir}/edgetx-companion-29/libedgetx-t18-simulator.so
%{_libdir}/edgetx-companion-29/libedgetx-tlite-simulator.so
%{_libdir}/edgetx-companion-29/libedgetx-tpro-simulator.so
%{_libdir}/edgetx-companion-29/libedgetx-tx12-simulator.so
%{_libdir}/edgetx-companion-29/libedgetx-tx12mk2-simulator.so
%{_libdir}/edgetx-companion-29/libedgetx-tx16s-simulator.so
%{_libdir}/edgetx-companion-29/libedgetx-x7-simulator.so
%{_libdir}/edgetx-companion-29/libedgetx-x7access-simulator.so
%{_libdir}/edgetx-companion-29/libedgetx-x9d-simulator.so
%{_libdir}/edgetx-companion-29/libedgetx-x9d+-simulator.so
%{_libdir}/edgetx-companion-29/libedgetx-x9d+2019-simulator.so
%{_libdir}/edgetx-companion-29/libedgetx-x9e-simulator.so
%{_libdir}/edgetx-companion-29/libedgetx-x9lite-simulator.so
%{_libdir}/edgetx-companion-29/libedgetx-x9lites-simulator.so
%{_libdir}/edgetx-companion-29/libedgetx-x10-simulator.so
%{_libdir}/edgetx-companion-29/libedgetx-x10express-simulator.so
%{_libdir}/edgetx-companion-29/libedgetx-x12s-simulator.so
%{_libdir}/edgetx-companion-29/libedgetx-xlite-simulator.so
%{_libdir}/edgetx-companion-29/libedgetx-xlites-simulator.so
%{_libdir}/edgetx-companion-29/libedgetx-zorro-simulator.so
%{_prefix}/lib/udev/rules.d/45-edgetx-companion-taranis.rules
%{_prefix}/lib/udev/rules.d/45-edgetx-companion-usbasp.rules
%{_datadir}/applications/edgetx-companion29.desktop
%{_datadir}/applications/edgetx-simulator29.desktop
%{_datadir}/icons/hicolor/16x16/apps/edgetx-companion.png
%{_datadir}/icons/hicolor/22x22/apps/edgetx-companion.png
%{_datadir}/icons/hicolor/24x24/apps/edgetx-companion.png
%{_datadir}/icons/hicolor/32x32/apps/edgetx-companion.png
%{_datadir}/icons/hicolor/48x48/apps/edgetx-companion.png
%{_datadir}/icons/hicolor/128x128/apps/edgetx-companion.png
%{_datadir}/icons/hicolor/256x256/apps/edgetx-companion.png
%{_datadir}/icons/hicolor/512x512/apps/edgetx-companion.png
%{_datadir}/icons/hicolor/scalable/apps/edgetx-companion.svg

%changelog
* Thu Sep 28 2023 Jan Pazdziora <jpx-edgetx@adelton.com> - 2.9.1-1
- Update to EdgeTX 2.9.1.

* Sat Sep 02 2023 Jan Pazdziora <jpx-edgetx@adelton.com> - 2.9.0-1
- Update to EdgeTX 2.9.0.

* Sat Aug 05 2023 Jan Pazdziora <jpx-edgetx@adelton.com> - 2.9.0-0.rc2.1
- Update to EdgeTX 2.9.0-rc2.

* Sat Aug 05 2023 Jan Pazdziora <jpx-edgetx@adelton.com> - 2.8.5-1
- Update to EdgeTX 2.8.5.

* Mon May 15 2023 Jan Pazdziora <jpx-edgetx@adelton.com> - 2.8.4-1
- Update to EdgeTX 2.8.4.

* Sun Apr 23 2023 Jan Pazdziora <jpx-edgetx@adelton.com> - 2.8.3-4
- Use Google Test from yaml-cpp.

* Wed Apr 19 2023 Jan Pazdziora <jpx-edgetx@adelton.com> - 2.8.3-1
- Update to EdgeTX 2.8.3.

* Mon Apr 03 2023 Jan Pazdziora <jpx-edgetx@adelton.com> - 2.8.2-1
- Update to EdgeTX 2.8.2.

* Tue Feb 21 2023 Jan Pazdziora <jpx-edgetx@adelton.com> - 2.8.1-2
- Update to EdgeTX 2.8.1.
- Fixes https://github.com/EdgeTX/edgetx/issues/3222 on Fedora 38+.

* Sun Jan 01 2023 Jan Pazdziora <jpx-edgetx@adelton.com> - 2.8.0-1
- Rebase to EdgeTX 2.8.0.

* Sun Jan 01 2023 Jan Pazdziora <jpx-edgetx@adelton.com> - 2.7.2-2
- Update to EdgeTX 2.7.2.

* Mon May 09 2022 Jan Pazdziora <jpx-edgetx@adelton.com> - 2.7.1-1
- Rebase to EdgeTX 2.7.1.

* Sat Apr 16 2022 Jan Pazdziora <jpx-edgetx@adelton.com> - 2.7.0-1
- Rebase to EdgeTX 2.7.0.

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

