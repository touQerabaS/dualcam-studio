# DualCam Studio

**One Windows application to start and stop recording on a GoPro HERO12 Black, Sony ZV-1M2, and optional Neon eye glasses.**

The application uses Bluetooth for GoPro recording control, a USB data cable for Sony, and the Neon companion phone's local network API. **Start All** operates every included device. **Stop All** stops the included devices and uses **stop and save** for Neon.

Despite the original DualCam name, this version supports three devices. Neon is optional, so the original two-camera setup still works. Live previews are optional and are not needed for recording.

This repository contains source code and installation instructions. Each user downloads the external software and Python packages on their own computer. No virtual environment, installed libraries, Sony installer, camera recordings, or prebuilt executable is included.

## Contents

- [Supported setup and current limitations](#supported-setup-and-current-limitations)
- [What to download and where it goes](#what-to-download-and-where-it-goes)
- [Install from GitHub](#install-from-github)
- [Set up the three devices](#set-up-the-three-devices)
- [Use the application](#use-the-application)
- [Optional live previews and networking](#optional-live-previews-and-networking)
- [Folder structure](#folder-structure)
- [Build a Windows executable](#build-a-windows-executable)
- [Offline installation](#offline-installation)
- [Tests and validation](#tests-and-validation)
- [Troubleshooting](#troubleshooting)
- [Settings, logs, and saved recordings](#settings-logs-and-saved-recordings)
- [Included fixes and dependency sources](#included-fixes-and-dependency-sources)
- [Publishing this folder on GitHub](#publishing-this-folder-on-github)
- [License and acknowledgments](#license-and-acknowledgments)

## Supported setup and current limitations

| Device | Recording connection | Save location | Preview status |
| --- | --- | --- | --- |
| GoPro HERO12 Black | PC Bluetooth | GoPro memory card | Optional Wi-Fi preview implementation; complete live display remains unresolved |
| Sony ZV-1M2 / ZV-1 II | USB data cable, PC Remote mode | Sony memory card | USB scene preview tested |
| Pupil Labs Neon eye glasses | Local network to the Neon companion phone | Neon companion phone | Scene-camera preview tested |

Development and hardware checks used **64-bit Windows and Python 3.13.9**. Use the Windows 64-bit Python 3.13 series for the closest match. Other Python versions, operating systems, camera models, firmware versions and driver combinations have not all been validated. This application uses Windows-specific USB, Bluetooth and Wi-Fi components; it is not a tested macOS/Linux application.

The implementation was tested starting all three attached devices, waiting five seconds and stopping all three. Sony and Neon previews remained live during that test. The test checked device-reported recording state, including Neon's stop-and-save confirmation. It did not download or play back the saved clips, certify long recording sessions, or measure frame-level synchronization.

Starts are approximate. Sending commands together does **not** make the cameras frame synchronized. When one device fails, another may keep recording. Inspect each device's REC indicator and use Stop All or the physical device controls as appropriate.

There is no automatic clip download, merging, gaze overlay, eye-camera preview, cloud upload feature, or automatic camera firmware update in this application. Settings on the Neon companion phone itself may independently control its own cloud behavior.

## What to download and where it goes

### External applications and drivers

| Item | Download / official documentation | Required for | Where to install |
| --- | --- | --- | --- |
| Python 3.13, Windows 64-bit | [Python Windows releases](https://www.python.org/downloads/windows/) | Running from source or building an executable | Use the Python installer; create the project `.venv` afterward |
| Tcl/Tk and Tkinter support | [Python Tkinter documentation](https://docs.python.org/3/library/tkinter.html) | Desktop interface | Include with the Python installation; no separate pip download |
| Sony Imaging Edge Desktop and Remote | [Sony installation/download page](https://support.d-imaging.sony.co.jp/app/imagingedge/en/) | The tested Sony USB driver setup and an independent connection check | Install through Sony's installer, outside this repository |
| Neon Companion | [Pupil Labs Neon documentation](https://docs.pupil-labs.com/neon/) | Neon recording and streaming | On the Neon companion phone |
| Bluetooth / Wi-Fi drivers | Your PC or USB adapter manufacturer's support page | Wireless connections | Install for your own Windows hardware |
| Git, optional | [Git for Windows](https://git-scm.com/download/win) | Cloning and publishing | Standard Windows installation; GitHub Download ZIP also works |

The development PC already had Sony's driver installed. Its exact original installer version was not recorded. Obtain the installer from Sony and verify your camera in Remote; do not look for the author's personal installed driver folder on GitHub.

### Python packages

The following versions are declared in `requirements.txt`. Install them with one pip command, shown below. You do not need to download or unpack each package manually.

| Package | Version | Purpose | Official package/download page |
| --- | --- | --- | --- |
| open-gopro | 0.22.0 | GoPro SDK and Bluetooth commands | [PyPI](https://pypi.org/project/open-gopro/0.22.0/) |
| comtypes | 1.4.16 | Windows COM / portable-device USB support | [PyPI](https://pypi.org/project/comtypes/1.4.16/) |
| pyusb | 1.3.1 | Sony bulk USB communication | [PyPI](https://pypi.org/project/pyusb/1.3.1/) |
| libusb-package | 1.0.30.0 | Native libusb runtime used by PyUSB | [PyPI](https://pypi.org/project/libusb-package/1.0.30.0/) |
| pillow | 12.3.0 | JPEG handling and displaying preview pictures | [PyPI](https://pypi.org/project/pillow/12.3.0/) |
| av | 18.1.0 | Video decoding for network previews | [PyPI](https://pypi.org/project/av/18.1.0/) |
| aiohttp | 3.14.3 | Neon HTTP recording/status requests | [PyPI](https://pypi.org/project/aiohttp/3.14.3/) |
| requests | 2.34.2 | GoPro preview HTTP requests | [PyPI](https://pypi.org/project/requests/2.34.2/) |
| pyinstaller, optional | 6.22.2 | Build the Windows executable and helper programs | [PyPI](https://pypi.org/project/pyinstaller/6.22.2/) |

Supporting packages such as Bleak, Windows Runtime bindings, protobuf and HTTP libraries are installed automatically by pip. Their observed versions and upstream links are listed in [DEPENDENCIES.md](DEPENDENCIES.md). Preview packages are still imported by this version of the application, so install the complete runtime requirements even when you plan to leave previews off.

Pip places libraries under `.venv/Lib/site-packages/` and Python launchers under `.venv/Scripts/`. This keeps downloaded dependencies inside a local environment in your project folder, while `.gitignore` keeps that environment out of GitHub.

Compatible PyAV binary wheels include the native video libraries they need. A separate `ffmpeg.exe`, VLC, OpenCV, PyQt, `sony-camera-api` or `pupil-labs-realtime-api` installation is not required by this code. See [PyAV installation documentation](https://pyav.org/docs/stable/overview/installation.html) if pip cannot obtain a compatible wheel.

## Install from GitHub

### 1. Download the source

On the repository's GitHub page, select **Code → Download ZIP**, then extract it. Alternatively, clone it with Git.

Open PowerShell in the extracted folder containing `app.py`, `requirements.txt` and this README. All commands below run from that folder. The folder may be named `Github`, or GitHub may extract it as `repository-name-main`; the name does not matter.

### 2. Install and check Python

Install 64-bit Python 3.13 with pip and Tcl/Tk support. Open a new PowerShell window after installation.

```powershell
py -3.13 --version
```

If your installation uses `python` rather than the `py` launcher, check `python --version` and use `python` instead of `py -3.13` for the next command. A pre-existing Miniconda installation can work, but Conda is not a project requirement.

### 3. Create the local environment

```powershell
py -3.13 -m venv .venv
```

This creates `.venv` inside the project. Do not copy another person's `.venv`; it contains paths and binaries specific to their Python installation.

### 4. Download and install runtime dependencies

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install --index-url https://pypi.org/simple -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
```

The final command checks installed dependency compatibility. An internet connection is needed for these downloads. Environment activation is optional because these commands explicitly use the project Python executable; there is no need to change PowerShell's execution policy to activate the environment.

### 5. Start the application

```powershell
.\.venv\Scripts\python.exe app.py
```

Start in **Demo — simulated cameras** to inspect the controls without operating hardware. To include a simulated third device, tick **Include Neon** in Setup. Demo pictures and status are explicitly labeled simulated.

After source installation, double-clicking `Start DualCam.cmd` also works. The launcher prefers a locally built executable if one exists, and otherwise uses `.venv/Scripts/pythonw.exe`. If a source edit seems to have no effect, run the explicit `python.exe app.py` command above: you may otherwise be launching an older local executable.

Normal use does not require running the entire application as administrator. Driver installation and explicit firewall configuration are separate Windows administration tasks.

## Set up the three devices

### GoPro HERO12 Black

1. Insert a usable memory card, charge the camera, and power it on.
2. Enable Bluetooth on the PC.
3. Open the camera's wireless pairing screen for **Pair Device / GoPro Quik App** and complete any requested pairing confirmation.
4. Close GoPro Quik on your phone while testing this controller.
5. In Setup, enter the last four digits of the GoPro serial number.

Recording control uses Bluetooth. The PC can remain on the local network used by Neon. The **GoPro preview Wi-Fi adapter** field is unrelated to Bluetooth recording and can be left blank if previews are not used. See [Open GoPro](https://gopro.github.io/OpenGoPro/) for the upstream SDK and protocols.

### Sony ZV-1M2 / ZV-1 II

1. Install Sony Imaging Edge Desktop and its Remote application from Sony's official source.
2. Power on the camera, insert a memory card and choose Movie mode.
3. Connect it to the PC with a **USB data cable**. A charging-only cable cannot provide remote control.
4. Select **Remote Shoot / PC Remote** on the camera's USB connection screen.
5. Test the connection in Sony Remote if needed. Then fully close Remote before opening a DualCam USB session.
6. Disconnect any competing Creators' App connection.
7. In DualCam Setup, use automatic Sony selection, or click **Scan USB** and select the listed Sony device.

The tested installation used Sony's libusbK driver. The application also contains a Windows Portable Devices fallback, but that fallback has not been validated across all Windows driver configurations.

The bulk USB backend looks for Sony's installed library at:

```text
%ProgramFiles%\Sony\Imaging Edge\Driver\amd64\libusbK.dll
```

`libusb-package` supplies a USB runtime in `.venv`; it does not install Sony's camera driver. The two components have different jobs. Do not copy Sony DLLs into the source tree or replace camera drivers simply to follow this README. If a Sony installer places its driver elsewhere, check the path in `dualcam/usb_bulk.py` against that installation.

### Neon eye glasses

1. Connect the glasses to their Neon companion phone and open the companion app.
2. Complete the companion app's required setup, including wearer/workspace/template choices where applicable.
3. Enable streaming in the companion app.
4. Connect the PC to a network from which the companion phone is reachable.
5. Read the phone's current local IP/port and enter it in **Neon address (current IP)**.
6. Tick **Include Neon**.

Accepted examples:

```text
192.168.1.50
192.168.1.50:8080
http://192.168.1.50:8080/
neon.local:8080
```

The example IP is a placeholder, not a fixed address for your glasses. Port `8080` is used when omitted. `neon.local` works only where local hostname discovery is available. A numeric current IP is often easier when the network blocks discovery.

**The IP can change.** Disconnect the application's device session, replace the address in Setup, then reconnect. The application remembers the last address used when connecting. A changed text field does not silently redirect an existing recording session to another device.

If Neon is not available, untick Include Neon before connecting. Start All requires every included device to be connected and stopped; it does not silently omit a failed Neon connection. The supported local API and its recording prerequisites are documented by [Pupil Labs](https://pupil-labs.github.io/pl-realtime-api/dev/guides/under-the-hood/).

## Use the application

1. Open **Setup & help** and choose **Real cameras**.
2. Enter the GoPro serial digits and select the Sony USB device if necessary.
3. For three-device recording, enter Neon's current address and tick Include Neon.
4. Open **Recording** and select **Connect cameras**.
5. Wait for each included device to report **Ready • stopped**.
6. Optionally choose a countdown, then select **Start All**.
7. Check the REC indicator on each physical camera and the Neon companion phone.
8. Select **Stop All** and wait for stopped status from every included device.
9. Check a short saved clip on each device before relying on a longer session.

Stop All cancels a pending countdown. If another camera operation is running, Stop is queued for that operation to finish. Disconnecting or closing the application is not a substitute for stopping recordings.

Setup controls are locked while a device session is attached. Use Disconnect after stopping before editing connection information. Cancellation is available for scanning and connection jobs; it is not a promise to undo a recording command that already reached a camera.

## Optional live previews and networking

You can leave every preview off and still use all recording controls. Open **Live preview** and choose **Show preview** under a device only when wanted. Start All / Stop All are also available on that tab.

- Sony preview uses the existing USB cable.
- Neon preview uses the companion phone's advertised scene-camera stream. The app displays the scene picture without gaze or eye-camera overlays.
- GoPro preview requires Wi-Fi to the GoPro access point. Its complete live display has not been verified successfully in this release. Do not make a working preview a prerequisite for using recording controls.

With **one Wi-Fi adapter**, keep the PC connected to Neon's network and control GoPro over Bluetooth. To use GoPro Wi-Fi preview and Neon at the same time, provide another network path, such as Ethernet to Neon's network or a second Wi-Fi adapter for GoPro.

The **GoPro preview Wi-Fi adapter** field accepts the adapter's Windows name, for example `Wi-Fi 2`. It is not a camera IP, Wi-Fi password, or network SSID. Blank means automatic selection. The application checks the current Neon route before switching Wi-Fi and refuses to take over the adapter carrying that connection when it can identify it.

GoPro's 2.4 GHz setting was needed for discovery in the tested environment. On the camera, look under **Preferences → Connections → Wi-Fi Band**. Showing GoPro preview can temporarily disconnect that adapter from its normal internet network. Hiding preview attempts to restore the previous Wi-Fi profile if the user has not selected a different network in the meantime.

The included `Allow GoPro Preview.ps1` is an **optional administrative helper for the built GoPro preview receiver**, not an installation prerequisite or a guaranteed preview fix. It creates an inbound allow rule for the exact packaged receiver, GoPro address `10.5.5.9`, and UDP port `8554`; it can disable a conflicting UDP block for that same executable. Review it before running from an administrator PowerShell window. It does not configure Neon stream ports. Normal recording control does not use this inbound preview port.

## Folder structure

```text
repository/
├── README.md                     Installation and user guide
├── LICENSE                       MIT license for this project
├── DEPENDENCIES.md                Download sources and full package inventory
├── PATCHES.md                     Included fixes and implementation notes
├── requirements.txt              Direct runtime dependencies
├── requirements-dev.txt          Runtime dependencies plus executable builder
├── requirements-environment.txt  Optional full development version snapshot
├── .gitignore                    Excludes installed/generated/private files
├── app.py                        Desktop interface
├── Start DualCam.cmd              Windows launcher
├── build_windows.py               Builds the app and both helper programs
├── worker_entry.py                Sony USB helper entry point
├── preview_entry.py               Video decoder helper entry point
├── Allow GoPro Preview.ps1        Optional scoped firewall helper
├── dualcam/                       Camera, network, protocol and preview source
└── tests/                         Automated tests using simulated/mocked devices
```

Created locally after installation or building, and excluded from GitHub:

```text
.venv/                            Downloaded Python packages and interpreter links
build-preview/                    PyInstaller work files
dist-preview/DualCam Studio/       Locally built executable plus required helpers
downloads/ or wheelhouse/          Optional offline dependency downloads
```

Sony's installer goes into Windows' application/driver locations, not one of these project folders. Windows system DLLs stay in Windows. Device recordings stay on the cameras or Neon companion phone.

## Build a Windows executable

Building is optional. Running `app.py` from the environment is sufficient.

Install the packaging tools:

```powershell
.\.venv\Scripts\python.exe -m pip install --index-url https://pypi.org/simple -r requirements-dev.txt
```

Close any copy of the built app and its helpers before rebuilding. A running executable can prevent Windows from replacing its files.

```powershell
.\.venv\Scripts\python.exe build_windows.py
```

The build script generates Windows COM wrappers and packages the Sony USB helper, preview decoder and desktop app. The main result is:

```text
dist-preview\DualCam Studio\DualCam Studio.exe
```

Its `_internal` folder includes `sony-worker/SonyUsbWorker.exe`, `preview-worker/PreviewDecoder.exe` and their runtime files. Keep the **entire `DualCam Studio` folder** together; copying only the main EXE will break helper loading. A packaged app normally does not need a separate Python installation on the destination PC, but Sony's device driver and working device/network setup are still needed.

This source repository intentionally excludes build output. If distributing binaries later, keep their dependency license notices with them and review the licenses of native libraries carried in the bundle.

## Offline installation

Prepare wheels on an internet-connected **Windows 64-bit computer using the same Python version** as the destination:

```powershell
.\.venv\Scripts\python.exe -m pip download --index-url https://pypi.org/simple --only-binary=:all: --dest downloads -r requirements.txt
```

Transfer the source folder and the downloaded wheel folder to the offline computer. Install Python first, create its own `.venv`, then run:

```powershell
.\.venv\Scripts\python.exe -m pip install --no-index --find-links downloads -r requirements.txt
```

Download Sony's installer separately from Sony if needed. If pip reports that a matching wheel is unavailable, use a compatible Python/platform combination; do not substitute arbitrary DLL downloads. Building packages from source may require additional compiler/native-library tooling that is outside this installation route.

## Tests and validation

After installing runtime dependencies:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The automated suite covers recording coordination, partial failures, duplicate-start prevention, protocol parsing, scan timeout/cancellation, GUI recovery, manual Neon address handling and parts of preview handling. These tests do not intentionally start physical camera recordings. Some create hidden Tk windows, so run them on a Windows desktop with Tk available.

Hardware checks during development confirmed recording start/stop on all three devices and Sony/Neon previews during a short recording. Private diagnostic logs, status dumps, screenshots and camera frame captures are deliberately absent from this repository. Repeat a short real recording and verify saved clips on your own devices after installation.

## Troubleshooting

| Problem | Check / action |
| --- | --- |
| `py` or Python is not found | Install Python, open a new terminal, or use the full path to your installed Python. Confirm the version before creating `.venv`. |
| `No module named ...` | Install `requirements.txt` using `.venv/Scripts/python.exe`; make sure the application uses that same interpreter. |
| Tkinter fails to import | Repair Python with Tcl/Tk support enabled. Tkinter is not installed through pip. |
| Pip cannot find the pinned wheel | Check Python version, 64-bit architecture, network access and the linked PyPI release page. Do not silently upgrade all dependencies and assume hardware compatibility. |
| Sony is absent from Scan USB | Use a data cable, Movie mode and PC Remote. Check that Sony Remote can connect, then fully close Remote. |
| Sony Remote works but DualCam does not | Remote may still hold the USB connection. Close it, disconnect/reconnect the camera cable and retry. Check the Session log. |
| Sony USB library cannot load | Confirm the complete environment or built app folder is present, `libusb-package` is installed, and Sony's installed driver/library is available. |
| Scan seems stuck | Wait for its bounded timeout or use Cancel. Read the displayed error before reconnecting. |
| GoPro connects but Start is disabled | Every included device must report connected and stopped. An unknown state or an unavailable Neon device blocks Start All. |
| GoPro does not connect over Bluetooth | Power on the camera, enable PC Bluetooth, open pairing, check serial digits, close Quik and retry. |
| Neon no longer connects | Its IP may have changed. Stop/disconnect, enter the current address, confirm local-network reachability and reconnect. |
| `neon.local` fails | Enter the companion phone's numeric IP. Some networks do not support local hostname discovery or isolate wireless clients. |
| Neon rejects Start or Stop/Save | Check the companion phone for required template fields, wearer/workspace setup, battery or storage conditions. |
| Neon disappears when GoPro preview connects | They need separate network paths. Leave GoPro preview off with one adapter. |
| No GoPro live picture | This preview remains unresolved. Recording over Bluetooth can still work; use physical camera framing or leave preview off. |
| Controls remain locked after a partial connection | Stop recording, then Disconnect before editing Setup. Read the original device error in Session log. |
| A device continues recording after an error | Stop All and check every physical device. A failed response may leave recording status uncertain. |
| Source changes are not visible | The launcher may be using a built EXE. Run `.venv/Scripts/python.exe app.py`, or rebuild the executable. |
| Build reports a file in use | Close the app and its helper processes, then rebuild. Do not rebuild over a running packaged app. |

## Settings, logs, and saved recordings

The normal per-user application data location is:

```text
%LOCALAPPDATA%\DualCamStudio\
```

This includes saved connection settings and the rotating `session.log`. The GoPro SDK also uses a connection-data path there. Treat these files as machine-specific; do not upload them with the source. SDK debug logs are suppressed by the app because they can contain connection details.

For development, `DUALCAM_DATA_DIR` can select an alternative data directory. The app creates that directory when needed. This environment variable is optional and is not a requirement for ordinary use.

GoPro and Sony recordings are saved on their own memory cards. Neon recordings are saved by its companion phone. The application does not collect those clips into the repository folder.

## Included fixes and dependency sources

[PATCHES.md](PATCHES.md) explains the changes already implemented in this source, including the USB helper, recording confirmations, Bluetooth heartbeat and manual Neon IP support. There is no separate patch archive for a new user to download or apply.

[DEPENDENCIES.md](DEPENDENCIES.md) lists the external package versions, official distribution links, upstream project links, native components and protocol references. It distinguishes installed dependencies from research/reference projects that are not needed at runtime.

`requirements.txt` is the normal installation manifest. `requirements-dev.txt` adds the builder. `requirements-environment.txt` records all observed development-environment versions, including indirect/development packages; it is optional and is not a hash-locked guarantee of identical builds on every machine.

## Publishing this folder on GitHub

Upload the **contents of this source folder**, so README.md and app.py appear at the repository root. Use the included MIT LICENSE and keep `.gitignore`.

The source folder excludes downloaded dependencies and development data. After installing or building locally, those files will exist again on your PC, but `.gitignore` excludes them from ordinary Git adds. In particular, do not upload `.venv`, `build*`, `dist*`, installers, camera media, diagnostic captures, saved connection settings or backup ZIP files. GitHub's browser upload does not apply `.gitignore` automatically; choose source files deliberately if using browser upload.

For Git users, create an empty GitHub repository and run the following from this folder. Replace the placeholder URL with your real repository URL before the remote/push commands:

```powershell
git init
git add .
git status
git commit -m "Initial DualCam Studio source release"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

Check `git status` before committing to confirm only intended source/documentation files are staged. If Git asks for an author name and email, configure the identity you want attached to your public commits. GitHub sign-in is handled by your Git installation; no GitHub access token belongs in this project's source.

## License and acknowledgments

The application source in this repository is released under the [MIT License](LICENSE). Third-party packages, native libraries and manufacturer applications retain their own licenses; this project's MIT license does not relicense them.

Development uses GoPro's open SDK, Pupil Labs' documented local API, Python libraries listed in DEPENDENCIES.md, and Sony protocol research references. Sony's USB implementation here is experimental and is not an official Sony SDK integration. This is an independent project and does not claim endorsement by GoPro, Sony or Pupil Labs.
