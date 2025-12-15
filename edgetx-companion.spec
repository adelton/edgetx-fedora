
Summary: EdgeTX Companion
Name: edgetx-companion

Version: 2.11.4
Release: %autorelease
License: GPLv2
URL: https://edgetx.org/
Source0: https://github.com/EdgeTX/edgetx/archive/refs/tags/v%{version}.tar.gz#/edgetx-%{version}.tar.gz
Source12: https://github.com/nothings/stb/archive/5c205738c191bcb0abc65c4febfa9bd25ff35234.tar.gz#/stb-5c205738.tar.gz
Source14: https://github.com/EdgeTX/lvgl/archive/19d397271e195320c32fd73eb132642aa4acf3ce.tar.gz#/lvgl-19d39727.tar.gz
Source15: https://github.com/google/googletest/archive/refs/tags/v1.14.0.tar.gz#/googletest-1.14.0.tar.gz
Source16: https://github.com/edgetx/maxLibQt/archive/ac1988ffd005cd15a8449b92150ce6c08574a4f1.tar.gz#/maxLibQt-ac1988ff.tar.gz
Source17: https://github.com/microsoft/uf2/archive/d03b585ed780ed51bb0d1e6e8cf233aacb408305.tar.gz#/uf2-d03b585e.tar.gz

Patch1: edgetx-cmake.patch
Patch2: edgetx-desktop.patch
Patch4: edgetx-disable-appimage.patch
Patch5: edgetx-simulator-name.patch
Patch6: build-simulator.sh.patch
Patch7: edgetx-miniz.patch

BuildRequires: cmake
BuildRequires: make
BuildRequires: gcc-c++
BuildRequires: clang-devel
BuildRequires: qt5-qttools-devel, qt5-qtsvg-devel, qt5-qtmultimedia-devel, qt5-qtserialport-devel
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

%global debug_package %{nil}
%prep
%autosetup -n edgetx-%{version} -p1
( cd radio/src/thirdparty && tar xvzf %SOURCE12 && rmdir stb && ln -sv stb-* stb )
( cd radio/src/thirdparty && tar xvzf %SOURCE14 && rmdir lvgl && ln -sv lvgl-* lvgl )
( cd radio/src/thirdparty && tar xvzf %SOURCE17 && rmdir uf2 && ln -sv uf2-* uf2 )
tar xvzf %SOURCE15 && ln -sv googletest-* googletest
( cd companion/src && tar xvzf %SOURCE16 && ln -sv maxLibQt-* maxLibQt )

%set_build_flags
mkdir bin
cat > bin/cmake <<'EOS'
#!/bin/bash
set -x
%cmake "$@"
EOS
chmod a+x bin/cmake

sed -i 's/include(FetchGtest)/add_subdirectory(googletest)/' cmake/NativeTargets.cmake
sed -i 's/include(FetchMiniz)/find_package(miniz REQUIRED CONFIG)/' companion/src/CMakeLists.txt
sed -i '/include(FetchYamlCpp)/d' companion/src/CMakeLists.txt
sed -i 's/include(FetchMaxLibQt)/add_subdirectory(maxLibQt)/' companion/src/CMakeLists.txt

%build
CMAKE_OPTS="-DCMAKE_NO_SYSTEM_FROM_IMPORTED=ON -DGVARS=YES -DLUA=YES -DHELI=YES -DMULTIMODULE=YES -DPPM_LIMITS_SYMETRICAL=YES -DAUTOSWITCH=YES -DAUTOSOURCE=YES -DPPM_CENTER_ADJUSTABLE=YES -DFLIGHT_MODES=YES -DOVERRIDE_CHANNEL_FUNCTION=YES -DFRSKY_STICKS=YES -DDEBUG=YES -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS:BOOL=OFF -Dgoogletest_SOURCE_DIR=$(pwd)/googletest -Dmaxlibqt_SOURCE_DIR=$(pwd)/maxLibQt -DINSTALL_GTEST=OFF -DINSTALL_GMOCK=OFF"
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
%dir %{_libdir}/edgetx-companion-211
%{_libdir}/edgetx-companion-211/libedgetx-boxer-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-bumblebee-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-commando8-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-el18-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-gx12-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-f16-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-lr3pro-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-mt12-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-nv14-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-pa01-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-pl18-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-pl18ev-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-pl18u-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-pocket-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-st16-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-t8-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-t12-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-t12max-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-t14-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-t15-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-t16-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-t18-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-t20-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-t20v2-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-tlite-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-tpro-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-tpros-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-tprov2-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-tx12-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-tx12mk2-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-tx16s-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-v14-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-v16-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-x7-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-x7access-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-x9d-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-x9d+-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-x9d+2019-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-x9e-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-x9lite-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-x9lites-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-x10-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-x10express-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-x12s-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-xlite-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-xlites-simulator.so
%{_libdir}/edgetx-companion-211/libedgetx-zorro-simulator.so
%{_prefix}/lib/udev/rules.d/45-edgetx-companion-taranis.rules
%{_prefix}/lib/udev/rules.d/45-edgetx-companion-usbasp.rules
%{_datadir}/applications/edgetx-companion211.desktop
%{_datadir}/applications/edgetx-simulator211.desktop
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
