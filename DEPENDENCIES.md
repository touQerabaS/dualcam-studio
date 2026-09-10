# Download sources and dependency inventory

This repository contains application source, dependency manifests and documentation. It does not contain installed third-party packages, installers, DLLs, wheels or development environments.

The table below records the 64 distributions observed in the Windows / Python 3.13.9 development environment on 2026-09-10. This is an environment inventory, not a claim that every package is directly imported by DualCam. Runtime dependencies, their supporting dependencies, packaging tools and development tools are included. The project/version links are official distribution pages; historic pip cache URLs and the exact Sony installer build were not recorded.

For a normal installation, use `requirements.txt`. For executable packaging, use `requirements-dev.txt`. Pip resolves the supporting packages automatically. `requirements-environment.txt` is an optional full version snapshot of the development environment, not a portable cross-platform or hash-verified lockfile.

## Python packages

All packages below are downloaded from [PyPI](https://pypi.org/); distribution files are normally served by `files.pythonhosted.org`. Use the **Download files** section of a linked version page to obtain a wheel manually. Prefer the pip commands in [README.md](README.md), which select compatible wheels and install them into `.venv/Lib/site-packages/`.

| Package | Observed version | Distribution/download page | Upstream source or project | License metadata |
| --- | --- | --- | --- | --- |
| aiohappyeyeballs | 2.7.1 | [PyPI 2.7.1](https://pypi.org/project/aiohappyeyeballs/2.7.1/) | [Upstream](https://github.com/aio-libs/aiohappyeyeballs) | PSF-2.0 |
| aiohttp | 3.14.3 | [PyPI 3.14.3](https://pypi.org/project/aiohttp/3.14.3/) | [Upstream](https://codecov.io/github/aio-libs/aiohttp) | Apache-2.0 AND MIT |
| aiosignal | 1.4.0 | [PyPI 1.4.0](https://pypi.org/project/aiosignal/1.4.0/) | [Upstream](https://codecov.io/github/aio-libs/aiosignal) | Apache 2.0 |
| altgraph | 0.17.5 | [PyPI 0.17.5](https://pypi.org/project/altgraph/0.17.5/) | [Upstream](https://github.com/ronaldoussoren/altgraph) | MIT |
| annotated-types | 0.8.0 | [PyPI 0.8.0](https://pypi.org/project/annotated-types/0.8.0/) | [Upstream](https://github.com/annotated-types/annotated-types) | MIT |
| ast_serialize | 0.11.0 | [PyPI 0.11.0](https://pypi.org/project/ast-serialize/0.11.0/) | [Upstream](https://github.com/mypyc/ast_serialize) | MIT |
| asyncstdlib | 3.14.0 | [PyPI 3.14.0](https://pypi.org/project/asyncstdlib/3.14.0/) | [Upstream](https://github.com/maxfischer2781/asyncstdlib) | See upstream license |
| attrs | 26.1.0 | [PyPI 26.1.0](https://pypi.org/project/attrs/26.1.0/) | [Upstream](https://www.attrs.org/) | MIT |
| av | 18.1.0 | [PyPI 18.1.0](https://pypi.org/project/av/18.1.0/) | [Upstream](https://github.com/PyAV-Org/PyAV) | BSD-3-Clause |
| bleak | 0.22.3 | [PyPI 0.22.3](https://pypi.org/project/bleak/0.22.3/) | [Upstream](https://github.com/hbldh/bleak/blob/develop/CHANGELOG.rst) | MIT |
| certifi | 2026.7.22 | [PyPI 2026.7.22](https://pypi.org/project/certifi/2026.7.22/) | [Upstream](https://github.com/certifi/python-certifi) | MPL-2.0 |
| charset-normalizer | 3.5.1 | [PyPI 3.5.1](https://pypi.org/project/charset-normalizer/3.5.1/) | [Upstream](https://github.com/jawah/charset_normalizer) | MIT |
| comtypes | 1.4.16 | [PyPI 1.4.16](https://pypi.org/project/comtypes/1.4.16/) | [Upstream](https://github.com/enthought/comtypes) | MIT |
| construct | 2.10.70 | [PyPI 2.10.70](https://pypi.org/project/construct/2.10.70/) | [Upstream](https://github.com/construct/construct) | MIT |
| frozenlist | 1.8.0 | [PyPI 1.8.0](https://pypi.org/project/frozenlist/1.8.0/) | [Upstream](https://github.com/aio-libs/.github/blob/master/CODE_OF_CONDUCT.md) | Apache-2.0 |
| idna | 3.19 | [PyPI 3.19](https://pypi.org/project/idna/3.19/) | [Upstream](https://github.com/kjd/idna) | BSD-3-Clause |
| ifaddr | 0.2.0 | [PyPI 0.2.0](https://pypi.org/project/ifaddr/0.2.0/) | [Upstream](https://github.com/pydron/ifaddr) | MIT |
| importlib_resources | 7.1.0 | [PyPI 7.1.0](https://pypi.org/project/importlib-resources/7.1.0/) | [Upstream](https://github.com/python/importlib_resources) | Apache-2.0 |
| librt | 0.15.0 | [PyPI 0.15.0](https://pypi.org/project/librt/0.15.0/) | [Upstream](https://github.com/mypyc/librt) | MIT |
| libusb-package | 1.0.30.0 | [PyPI 1.0.30.0](https://pypi.org/project/libusb-package/1.0.30.0/) | [Upstream](https://github.com/pyocd/libusb-package/issues) | Apache 2.0 |
| markdown-it-py | 4.2.0 | [PyPI 4.2.0](https://pypi.org/project/markdown-it-py/4.2.0/) | [Upstream](https://github.com/executablebooks/markdown-it-py) | See upstream license |
| mdurl | 0.1.2 | [PyPI 0.1.2](https://pypi.org/project/mdurl/0.1.2/) | [Upstream](https://github.com/executablebooks/mdurl) | See upstream license |
| multidict | 6.8.0 | [PyPI 6.8.0](https://pypi.org/project/multidict/6.8.0/) | [Upstream](https://github.com/aio-libs/.github/blob/master/CODE_OF_CONDUCT.md) | Apache License 2.0 |
| mypy | 2.3.1 | [PyPI 2.3.1](https://pypi.org/project/mypy/2.3.1/) | [Upstream](https://github.com/python/mypy) | MIT |
| mypy_extensions | 1.1.0 | [PyPI 1.1.0](https://pypi.org/project/mypy-extensions/1.1.0/) | [Upstream](https://github.com/python/mypy_extensions) | MIT |
| open_gopro | 0.22.0 | [PyPI 0.22.0](https://pypi.org/project/open-gopro/0.22.0/) | [Upstream](https://github.com/gopro/OpenGoPro/tree/main/demos/python/sdk_wireless_camera_control) | MIT |
| packaging | 25.0 | [PyPI 25.0](https://pypi.org/project/packaging/25.0/) | [Upstream](https://github.com/pypa/packaging) | See upstream license |
| pathspec | 1.1.1 | [PyPI 1.1.1](https://pypi.org/project/pathspec/1.1.1/) | [Upstream](https://github.com/cpburnz/python-pathspec) | See upstream license |
| pefile | 2024.8.26 | [PyPI 2024.8.26](https://pypi.org/project/pefile/2024.8.26/) | [Upstream](https://github.com/erocarrera/pefile) | MIT |
| pexpect | 4.9.0 | [PyPI 4.9.0](https://pypi.org/project/pexpect/4.9.0/) | [Upstream](https://github.com/pexpect/pexpect) | ISC license |
| pillow | 12.3.0 | [PyPI 12.3.0](https://pypi.org/project/pillow/12.3.0/) | [Upstream](https://github.com/python-pillow/Pillow) | MIT-CMU |
| pip | 25.2 | [PyPI 25.2](https://pypi.org/project/pip/25.2/) | [Upstream](https://github.com/pypa/pip) | MIT |
| propcache | 0.5.2 | [PyPI 0.5.2](https://pypi.org/project/propcache/0.5.2/) | [Upstream](https://github.com/aio-libs/.github/blob/master/CODE_OF_CONDUCT.md) | Apache-2.0 |
| protobuf | 6.33.6 | [PyPI 6.33.6](https://pypi.org/project/protobuf/6.33.6/) | [Upstream](https://developers.google.com/protocol-buffers/) | 3-Clause BSD License |
| ptyprocess | 0.7.0 | [PyPI 0.7.0](https://pypi.org/project/ptyprocess/0.7.0/) | [Upstream](https://github.com/pexpect/ptyprocess) | UNKNOWN |
| pydantic | 2.13.5 | [PyPI 2.13.5](https://pypi.org/project/pydantic/2.13.5/) | [Upstream](https://github.com/pydantic/pydantic) | MIT |
| pydantic_core | 2.46.5 | [PyPI 2.46.5](https://pypi.org/project/pydantic-core/2.46.5/) | [Upstream](https://github.com/pydantic/pydantic/tree/main/pydantic-core) | MIT |
| Pygments | 2.21.0 | [PyPI 2.21.0](https://pypi.org/project/Pygments/2.21.0/) | [Upstream](https://github.com/pygments/pygments) | BSD-2-Clause |
| pyinstaller | 6.22.2 | [PyPI 6.22.2](https://pypi.org/project/pyinstaller/6.22.2/) | [Upstream](https://github.com/pyinstaller/pyinstaller) | See upstream license files (metadata includes full license text) |
| pyinstaller-hooks-contrib | 2026.7 | [PyPI 2026.7](https://pypi.org/project/pyinstaller-hooks-contrib/2026.7/) | [Upstream](https://github.com/pyinstaller/pyinstaller-hooks-contrib) | See upstream license |
| pytz | 2026.3.post1 | [PyPI 2026.3.post1](https://pypi.org/project/pytz/2026.3.post1/) | [Upstream](https://github.com/stub42/pytz.git) | MIT |
| pyusb | 1.3.1 | [PyPI 1.3.1](https://pypi.org/project/pyusb/1.3.1/) | [Upstream](https://github.com/pyusb/pyusb) | See upstream license |
| pywin32-ctypes | 0.2.3 | [PyPI 0.2.3](https://pypi.org/project/pywin32-ctypes/0.2.3/) | [Upstream](https://github.com/enthought/pywin32-ctypes) | BSD-3-Clause |
| requests | 2.34.2 | [PyPI 2.34.2](https://pypi.org/project/requests/2.34.2/) | [Upstream](https://github.com/psf/requests) | Apache-2.0 |
| returns | 0.29.0 | [PyPI 0.29.0](https://pypi.org/project/returns/0.29.0/) | [Upstream](https://github.com/dry-python/returns) | BSD-3-Clause |
| rich | 14.3.4 | [PyPI 14.3.4](https://pypi.org/project/rich/14.3.4/) | [Upstream](https://github.com/Textualize/rich) | MIT |
| setuptools | 84.0.0 | [PyPI 84.0.0](https://pypi.org/project/setuptools/84.0.0/) | [Upstream](https://github.com/pypa/setuptools) | MIT |
| tinydb | 4.9.0 | [PyPI 4.9.0](https://pypi.org/project/tinydb/4.9.0/) | [Upstream](https://github.com/msiemens/tinydb) | MIT |
| typing_extensions | 4.16.0 | [PyPI 4.16.0](https://pypi.org/project/typing-extensions/4.16.0/) | [Upstream](https://github.com/python/typing_extensions) | PSF-2.0 |
| typing-inspection | 0.4.4 | [PyPI 0.4.4](https://pypi.org/project/typing-inspection/0.4.4/) | [Upstream](https://github.com/pydantic/typing-inspection) | MIT |
| tzdata | 2026.3 | [PyPI 2026.3](https://pypi.org/project/tzdata/2026.3/) | [Upstream](https://github.com/python/tzdata) | Apache-2.0 |
| tzlocal | 5.4.4 | [PyPI 5.4.4](https://pypi.org/project/tzlocal/5.4.4/) | [Upstream](https://github.com/regebro/tzlocal) | MIT |
| urllib3 | 2.7.0 | [PyPI 2.7.0](https://pypi.org/project/urllib3/2.7.0/) | [Upstream](https://github.com/urllib3/urllib3) | MIT |
| winrt-runtime | 2.3.0 | [PyPI 2.3.0](https://pypi.org/project/winrt-runtime/2.3.0/) | [Upstream](https://github.com/pywinrt/pywinrt) | MIT |
| winrt-Windows.Devices.Bluetooth | 2.3.0 | [PyPI 2.3.0](https://pypi.org/project/winrt-Windows.Devices.Bluetooth/2.3.0/) | [Upstream](https://github.com/pywinrt/pywinrt) | MIT |
| winrt-Windows.Devices.Bluetooth.Advertisement | 2.3.0 | [PyPI 2.3.0](https://pypi.org/project/winrt-Windows.Devices.Bluetooth.Advertisement/2.3.0/) | [Upstream](https://github.com/pywinrt/pywinrt) | MIT |
| winrt-Windows.Devices.Bluetooth.GenericAttributeProfile | 2.3.0 | [PyPI 2.3.0](https://pypi.org/project/winrt-Windows.Devices.Bluetooth.GenericAttributeProfile/2.3.0/) | [Upstream](https://github.com/pywinrt/pywinrt) | MIT |
| winrt-Windows.Devices.Enumeration | 2.3.0 | [PyPI 2.3.0](https://pypi.org/project/winrt-Windows.Devices.Enumeration/2.3.0/) | [Upstream](https://github.com/pywinrt/pywinrt) | MIT |
| winrt-Windows.Foundation | 2.3.0 | [PyPI 2.3.0](https://pypi.org/project/winrt-Windows.Foundation/2.3.0/) | [Upstream](https://github.com/pywinrt/pywinrt) | MIT |
| winrt-Windows.Foundation.Collections | 2.3.0 | [PyPI 2.3.0](https://pypi.org/project/winrt-Windows.Foundation.Collections/2.3.0/) | [Upstream](https://github.com/pywinrt/pywinrt) | MIT |
| winrt-Windows.Storage.Streams | 2.3.0 | [PyPI 2.3.0](https://pypi.org/project/winrt-Windows.Storage.Streams/2.3.0/) | [Upstream](https://github.com/pywinrt/pywinrt) | MIT |
| wrapt | 1.17.3 | [PyPI 1.17.3](https://pypi.org/project/wrapt/1.17.3/) | [Upstream](https://github.com/GrahamDumpleton/wrapt/issues/) | BSD |
| yarl | 1.24.5 | [PyPI 1.24.5](https://pypi.org/project/yarl/1.24.5/) | [Upstream](https://github.com/aio-libs/.github/blob/master/CODE_OF_CONDUCT.md) | Apache-2.0 |
| zeroconf | 0.151.3 | [PyPI 0.151.3](https://pypi.org/project/zeroconf/0.151.3/) | [Upstream](https://github.com/python-zeroconf/python-zeroconf) | LGPL-2.1-or-later |

License entries reproduce package metadata for identification. Native libraries bundled in wheels can carry additional licenses; check each distribution's included notices when redistributing binaries. The MIT license for this repository does not replace third-party licenses.

## Software and native components outside pip

| Component | Official source | Installation location / purpose |
| --- | --- | --- |
| Python for Windows, 64-bit | [Python Windows releases](https://www.python.org/downloads/windows/) | Install using Python's installer; then create `.venv` inside the repository. The development machine used Python 3.13.9 from an existing Miniconda installation. Miniconda is not required. |
| Tkinter and Tcl/Tk | [Python Tkinter documentation](https://docs.python.org/3/library/tkinter.html) | Include Tcl/Tk support when installing Python. Tkinter is not a separate pip requirement. |
| Sony Imaging Edge Desktop / Remote | [Sony download and installation](https://support.d-imaging.sony.co.jp/app/imagingedge/en/) | Install with Sony's Windows installer, outside the repository. The tested PC already had Sony's USB driver. |
| Sony-installed libusbK DLL | Same Sony installer; [libusbK upstream](https://sourceforge.net/projects/libusbk/) for project information | The code looks under `%ProgramFiles%/Sony/Imaging Edge/Driver/amd64/libusbK.dll`. Do not copy this installed DLL into the GitHub repository. The precise Sony installer version used originally is not recorded. |
| Windows Portable Devices / COM | [Microsoft WPD documentation](https://learn.microsoft.com/en-us/windows/win32/wpd_sdk/windows-portable-devices) | Windows component. `comtypes` generates wrappers from `PortableDeviceApi.dll` and `PortableDeviceTypes.dll`; do not download these system DLLs from unofficial sites. |
| libusb native runtime | [libusb-package distribution](https://pypi.org/project/libusb-package/1.0.30.0/), [libusb upstream](https://libusb.info/) | Supplied by the libusb-package wheel inside the virtual environment. Separate from Sony's installed device driver. |
| FFmpeg libraries used by PyAV | [PyAV installation](https://pyav.org/docs/stable/overview/installation.html), [FFmpeg](https://ffmpeg.org/) | Compatible PyAV binary wheels carry their native libraries. This app does not launch a standalone ffmpeg.exe or require VLC. Source-building PyAV is a separate advanced installation route. |
| Neon Companion | [Pupil Labs Neon documentation](https://docs.pupil-labs.com/neon/) | Runs on the Neon companion phone. Enable local streaming; nothing from the phone is copied into this repository. |
| Bluetooth / Wi-Fi adapter drivers | The PC or adapter manufacturer's support site | Install for the user's own hardware. No particular adapter driver is bundled or supplied by this repository. |
| Git, optional | [Git for Windows](https://git-scm.com/download/win) | Optional for cloning and publishing; GitHub Download ZIP also works. |

## Protocol references used during development

- [Open GoPro source and SDK](https://github.com/gopro/OpenGoPro): installed SDK and official protocol documentation.
- [Open GoPro FAQ and preview limitations](https://gopro.github.io/OpenGoPro/docs/faq/): reference for preview networking.
- [libgphoto2 Sony/PTP implementation](https://github.com/gphoto/libgphoto2/blob/master/camlibs/ptp2/library.c): Sony protocol research/reference. libgphoto2 is not an installed runtime dependency or a bundled source tree here. Its source has its own upstream license.
- [pysonycam source](https://github.com/olkham/pysonycam): additional Sony protocol research/reference. The `pysonycam` package is not required or bundled.
- [Pupil Labs Neon network API specification](https://github.com/pupil-labs/realtime-network-api): reference for local status, recording and scene streams.
- [Pupil Labs Python real-time API implementation](https://github.com/pupil-labs/pl-realtime-api): reference for status fields and scene stream addressing. The `pupil-labs-realtime-api` package is not a dependency of this implementation.

Protocol reference links are not a request to download and paste those projects into this repository. The application implementations and local fixes are already in `dualcam/`; see [PATCHES.md](PATCHES.md).

