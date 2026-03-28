
# EdgeTX Companion Fedora rpms

This repository contains [.spec file](edgetx-companion.spec) and patches
to build [EdgeTX Companion](https://edgetx.org/) from
https://github.com/EdgeTX/edgetx sources.

To help with controlled upgrades between versions, separate branches
contain content for individual minor versions of EdgeTX, and resulting
yum/dnf repositories are also separate.

## EdgeTX Companion 2.12

Built from [branch edgetx-2.12](https://github.com/adelton/edgetx-fedora/tree/edgetx-2.12),
rpms for contemporary Fedora versions are at
https://copr.fedorainfracloud.org/coprs/adelton/edgetx-companion-2.12/

Compatibility warning: any of the following radios
(STM32F2, per hackmd.io/@edgetx/B12oQyQKye) are no longer supported
with EdgeTX 2.12, use previous version (2.11, see below):

* BetaFPV: LR3Pro
* FrSky: X7, X9D (the original Taranis), X9D+, X9Lite, X9Lite S, XLite, XLite S
* Jumper: T12, TPro, TLite
* RadioMaster: T8, TX12

[![Copr build status](https://copr.fedorainfracloud.org/coprs/adelton/edgetx-companion-2.12/package/edgetx-companion/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/adelton/edgetx-companion-2.12/package/edgetx-companion/)

## Older versions

Built from [branch edgetx-2.11](https://github.com/adelton/edgetx-fedora/tree/edgetx-2.11),
rpms of older versions of EdgeTX are also available, at
https://copr.fedorainfracloud.org/coprs/adelton/edgetx-companion-2.11/

If you are looking for an ancient version, for example to migrate from OpenTX,
[OpenTX Companion 2.3](https://github.com/adelton/edgetx-fedora/tree/opentx-2.3)
rpm is available at https://copr.fedorainfracloud.org/coprs/adelton/opentx-companion-2.3/.

