
Summary: EdgeTX Companion
Name: edgetx-companion

Version: 2.12.0
Release: 0.rc2.1%{?dist}
License: GPLv2
URL: https://edgetx.org/
Source0: https://github.com/EdgeTX/edgetx/archive/refs/tags/v%{version}-rc2.tar.gz#/edgetx-%{version}.tar.gz
Source12: https://github.com/nothings/stb/archive/5c205738c191bcb0abc65c4febfa9bd25ff35234.tar.gz#/stb-5c205738.tar.gz
Source14: https://github.com/EdgeTX/lvgl/archive/5f129c540ec43a4e5aebff9f77b3688b57a78063.tar.gz#/lvgl-5f129c54.tar.gz
Source15: https://github.com/google/googletest/archive/refs/tags/v1.14.0.tar.gz#/googletest-1.14.0.tar.gz
Source16: https://github.com/edgetx/maxLibQt/archive/7e433da60d3f2e975d46afc91804a88029cd1b78.tar.gz#/maxLibQt-7e433da6.tar.gz
Source17: https://github.com/microsoft/uf2/archive/d03b585ed780ed51bb0d1e6e8cf233aacb408305.tar.gz#/uf2-d03b585e.tar.gz
Source18: https://github.com/ocornut/imgui/archive/refs/tags/v1.91.8.tar.gz#/imgui-1.91.8.tar.gz

Patch1: edgetx-cmake.patch
Patch2: edgetx-desktop.patch
Patch4: edgetx-disable-appimage.patch
Patch6: build-simulator.sh.patch
Patch7: edgetx-miniz.patch
Patch8: edgetx-rs_dfu.patch

BuildRequires: cmake
BuildRequires: make
BuildRequires: gcc-c++
BuildRequires: clang-devel
BuildRequires: qt6-qttools-devel, qt6-qtsvg-devel, qt6-qtmultimedia-devel, qt6-qtserialport-devel
BuildRequires: fox-devel
BuildRequires: SDL2-devel
BuildRequires: openssl-devel
BuildRequires: python3-pillow python3-lz4 python3-clang
BuildRequires: yaml-cpp-devel
BuildRequires: miniz-devel
BuildRequires: python3-jinja2
BuildRequires: rs_dfu-devel

%description
OpenTX Companion transmitter support software is used for many different
tasks like loading OpenTX firmware to the radio, backing up model
settings, editing settings and running radio simulators.

%global debug_package %{nil}
%prep
%autosetup -n edgetx-%{version}-rc2 -p1
mkdir deps
( cd radio/src/thirdparty && tar xvzf %SOURCE12 && rmdir stb && ln -sv stb-* stb )
( cd radio/src/thirdparty && tar xvzf %SOURCE14 && rmdir lvgl && ln -sv lvgl-* lvgl )
( cd radio/src/thirdparty && tar xvzf %SOURCE17 && rmdir uf2 && ln -sv uf2-* uf2 )
( cd deps && tar xvzf %SOURCE15 && ln -sv googletest-* googletest )
( cd deps && tar xvzf %SOURCE16 && ln -sv maxLibQt-* maxLibQt )
( cd radio/src/targets/simu && rm -rf imgui && tar xvzf %SOURCE18 && ln -sv imgui-* imgui )

%build
CMAKE_OPTS=$( eval echo $( cat <<'EOS' | sed -e '1,\#%{__cmake}#d' -e '/ -S /d' -e '/ -B /d' -e 's/\\$//'
%cmake
EOS
))
export COMMON_OPTIONS="${CMAKE_OPTS} -DCMAKE_NO_SYSTEM_FROM_IMPORTED=ON -DDEBUG=YES -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS:BOOL=OFF -DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=ON -DINSTALL_GTEST=OFF -DFETCHCONTENT_SOURCE_DIR_GOOGLETEST=$(pwd)/deps/googletest -DFETCHCONTENT_SOURCE_DIR_MAXLIBQT=$(pwd)/deps/maxLibQt -DFETCHCONTENT_SOURCE_DIR_IMGUI=$(pwd)/radio/src/thirdparty"
export EDGETX_VERSION_SUFFIX=%{release}
export CMAKE_BUILD_PARALLEL_LEVEL=${RPM_BUILD_NCPUS}
tools/build-companion.sh "$(pwd)" "$(pwd)/%{_vpath_builddir}"

%install
%{cmake_install}/native

%files
%defattr(-,root,root,-)
%{_bindir}/edgetx-companion
%{_bindir}/edgetx-simulator
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libedgetx-boxer-simulator.so
%{_libdir}/%{name}/libedgetx-bumblebee-simulator.so
%{_libdir}/%{name}/libedgetx-commando8-simulator.so
%{_libdir}/%{name}/libedgetx-el18-simulator.so
%{_libdir}/%{name}/libedgetx-gx12-simulator.so
%{_libdir}/%{name}/libedgetx-f16-simulator.so
%{_libdir}/%{name}/libedgetx-lr3pro-simulator.so
%{_libdir}/%{name}/libedgetx-mt12-simulator.so
%{_libdir}/%{name}/libedgetx-nv14-simulator.so
%{_libdir}/%{name}/libedgetx-pa01-simulator.so
%{_libdir}/%{name}/libedgetx-pl18-simulator.so
%{_libdir}/%{name}/libedgetx-pl18ev-simulator.so
%{_libdir}/%{name}/libedgetx-pl18u-simulator.so
%{_libdir}/%{name}/libedgetx-pocket-simulator.so
%{_libdir}/%{name}/libedgetx-st16-simulator.so
%{_libdir}/%{name}/libedgetx-t8-simulator.so
%{_libdir}/%{name}/libedgetx-t12-simulator.so
%{_libdir}/%{name}/libedgetx-t12max-simulator.so
%{_libdir}/%{name}/libedgetx-t14-simulator.so
%{_libdir}/%{name}/libedgetx-t15-simulator.so
%{_libdir}/%{name}/libedgetx-t15pro-simulator.so
%{_libdir}/%{name}/libedgetx-t16-simulator.so
%{_libdir}/%{name}/libedgetx-t18-simulator.so
%{_libdir}/%{name}/libedgetx-t20-simulator.so
%{_libdir}/%{name}/libedgetx-t20v2-simulator.so
%{_libdir}/%{name}/libedgetx-tlite-simulator.so
%{_libdir}/%{name}/libedgetx-tpro-simulator.so
%{_libdir}/%{name}/libedgetx-tpros-simulator.so
%{_libdir}/%{name}/libedgetx-tprov2-simulator.so
%{_libdir}/%{name}/libedgetx-tx12-simulator.so
%{_libdir}/%{name}/libedgetx-tx12mk2-simulator.so
%{_libdir}/%{name}/libedgetx-tx15-simulator.so
%{_libdir}/%{name}/libedgetx-tx16s-simulator.so
%{_libdir}/%{name}/libedgetx-v14-simulator.so
%{_libdir}/%{name}/libedgetx-v16-simulator.so
%{_libdir}/%{name}/libedgetx-x7-simulator.so
%{_libdir}/%{name}/libedgetx-x7access-simulator.so
%{_libdir}/%{name}/libedgetx-x9d-simulator.so
%{_libdir}/%{name}/libedgetx-x9d+-simulator.so
%{_libdir}/%{name}/libedgetx-x9d+2019-simulator.so
%{_libdir}/%{name}/libedgetx-x9e-simulator.so
%{_libdir}/%{name}/libedgetx-x9lite-simulator.so
%{_libdir}/%{name}/libedgetx-x9lites-simulator.so
%{_libdir}/%{name}/libedgetx-x10-simulator.so
%{_libdir}/%{name}/libedgetx-x10express-simulator.so
%{_libdir}/%{name}/libedgetx-x12s-simulator.so
%{_libdir}/%{name}/libedgetx-xlite-simulator.so
%{_libdir}/%{name}/libedgetx-xlites-simulator.so
%{_libdir}/%{name}/libedgetx-zorro-simulator.so
%{_datadir}/applications/edgetx-companion.desktop
%{_datadir}/applications/edgetx-simulator.desktop
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/22x22/apps/%{name}.png
%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
%{_datadir}/icons/hicolor/512x512/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%changelog
%autochangelog
