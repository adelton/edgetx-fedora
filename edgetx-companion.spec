
Summary: EdgeTX Companion
Name: edgetx-companion

Version: 2.10.7
Release: %autorelease
License: GPLv2
URL: https://edgetx.org/
Source0: https://github.com/EdgeTX/edgetx/archive/refs/tags/v%{version}.tar.gz#/edgetx-%{version}.tar.gz
Source12: https://github.com/nothings/stb/archive/7cce4c3ad9a147c67258c5966f676d8436140939.tar.gz#/stb-7cce4c3a.tar.gz
Source14: https://github.com/EdgeTX/lvgl/archive/9a414b1d48d2893133b6038ec80d59fb157aade4.tar.gz#/lvgl-9a414b1d.tar.gz
Source15: https://github.com/google/googletest/archive/refs/tags/v1.14.0.tar.gz#/googletest-1.14.0.tar.gz
Source16: https://github.com/edgetx/maxLibQt/archive/b5418f76cc4891e09f4e21276175d39dbb130f66.tar.gz#/maxLibQt-b5418f76.tar.gz

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
BuildRequires: libusb1-devel
BuildRequires: yaml-cpp-devel
BuildRequires: miniz-devel
BuildRequires: python3-jinja2
Requires: dfu-util

%description
OpenTX Companion transmitter support software is used for many different
tasks like loading OpenTX firmware to the radio, backing up model
settings, editing settings and running radio simulators.

%prep
%autosetup -n edgetx-%{version} -p1
( cd radio/src/thirdparty/libopenui/thirdparty && tar xvzf %SOURCE12 && rmdir stb && ln -s stb-* stb )
( cd radio/src/thirdparty/libopenui/thirdparty && tar xvzf %SOURCE14 && rmdir lvgl && ln -s lvgl-* lvgl )
tar xvzf %SOURCE15 && ln -s googletest-* googletest
( cd companion/src && tar xvzf %SOURCE16 && ln -s maxLibQt-* maxLibQt )

%set_build_flags
mkdir bin
cat > bin/cmake <<'EOS'
#!/bin/bash
set -x
%cmake "$@"
EOS
chmod a+x bin/cmake

sed -i 's/include(FetchGtest)/add_subdirectory(googletest)/' cmake/NativeTargets.cmake
sed -i '/include(FetchMiniz)/d' companion/src/CMakeLists.txt
sed -i '/include(FetchYamlCpp)/d' companion/src/CMakeLists.txt
sed -i 's/include(FetchMaxLibQt)/add_subdirectory(maxLibQt)/' companion/src/CMakeLists.txt

%build
CMAKE_OPTS="-DGVARS=YES -DLUA=YES -DHELI=YES -DMULTIMODULE=YES -DPPM_LIMITS_SYMETRICAL=YES -DAUTOSWITCH=YES -DAUTOSOURCE=YES -DPPM_CENTER_ADJUSTABLE=YES -DFLIGHT_MODES=YES -DOVERRIDE_CHANNEL_FUNCTION=YES -DFRSKY_STICKS=YES -DDEBUG=YES -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS:BOOL=OFF -Dgoogletest_SOURCE_DIR=$(pwd)/googletest -Dmaxlibqt_SOURCE_DIR=$(pwd)/maxLibQt -DINSTALL_GTEST=OFF -DINSTALL_GMOCK=OFF"
# Build shared libraries for simulator
MAKEFLAGS="-O -j${RPM_BUILD_NCPUS}" tools/build-companion.sh "$(pwd)" "$(pwd)/%{_vpath_builddir}" "$CMAKE_OPTS" release
# Clean slate? There is probaly nothing wrong reusing the configuration
# left over from previous step, but be safe
rm -f "$(pwd)/%{_vpath_builddir}/CMakeCache.txt" "$(pwd)/%{_vpath_builddir}/native/CMakeCache.txt"
%cmake $CMAKE_OPTS -DPCB=X9D
%make_build -C %{_vpath_builddir} native-configure
%make_build -C %{_vpath_builddir} companion
%make_build -C %{_vpath_builddir} simulator

%install
%{cmake_install}/native

%files
%defattr(-,root,root,-)
%{_bindir}/edgetx-companion
%{_bindir}/edgetx-simulator
%dir %{_libdir}/edgetx-companion-210
%{_libdir}/edgetx-companion-210/libedgetx-boxer-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-bumblebee-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-commando8-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-el18-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-f16-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-lr3pro-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-nv14-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-pl18-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-pl18ev-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-pocket-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-t8-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-t12-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-t12max-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-t14-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-t15-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-t16-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-t18-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-t20-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-t20v2-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-tlite-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-tpro-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-tpros-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-tprov2-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-tx12-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-tx12mk2-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-tx16s-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-x7-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-x7access-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-x9d-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-x9d+-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-x9d+2019-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-x9e-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-x9lite-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-x9lites-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-x10-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-x10express-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-x12s-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-xlite-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-xlites-simulator.so
%{_libdir}/edgetx-companion-210/libedgetx-zorro-simulator.so
%{_prefix}/lib/udev/rules.d/45-edgetx-companion-taranis.rules
%{_prefix}/lib/udev/rules.d/45-edgetx-companion-usbasp.rules
%{_datadir}/applications/edgetx-companion210.desktop
%{_datadir}/applications/edgetx-simulator210.desktop
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
%autochangelog
