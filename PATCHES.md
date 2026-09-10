# Included fixes and implementation notes

These are application changes already present in the repository. A new user installs the dependencies and runs the code; there are no separate downloaded patch files to apply, and no need to edit an installed SDK's source.

## Recording coordination

**Files:** `dualcam/core.py`, `dualcam/cameras.py`, `dualcam/neon.py`.

- Each included device must respond and report stopped before a new shared start.
- Preparation runs before the concurrent start commands. A failed preflight prevents the shared start.
- Start/stop results are checked against device-reported state; a command acknowledgment alone is insufficient.
- Unknown or transitional recording state is not displayed as stopped.
- Duplicate starts are rejected; a timed-out recording command is not silently resent.
- Stop is sent to all included devices even when another device fails. There is no automatic rollback that silently stops a successfully recording peer.
- The controller accepts the optional third Neon device; recording buttons and messages operate on the included device set.

## GoPro Bluetooth recording fix

**Files:** `dualcam/cameras.py`, `dualcam/gopro_support.py`.

- Recording control uses Bluetooth and does not require taking over the PC's Wi-Fi.
- SDK automatic state maintenance is disabled for this integration; bounded direct reads replace notification waits that previously stalled recording operations.
- Video preset selection is skipped when the camera is already in video mode.
- A serialized heartbeat maintains the connection.
- Heartbeat shutdown waits for in-flight Bluetooth work before closing the SDK connection, reducing Windows callback/cancellation errors.
- `UnusedWifi` prevents the SDK from unnecessarily discovering a Wi-Fi adapter for a Bluetooth-only recording session.

Upstream dependency: [Open GoPro 0.22.0](https://pypi.org/project/open-gopro/0.22.0/). The installed upstream package is not patched by this repository.

## Sony driver compatibility and USB transport

**Files:** `dualcam/usb_bulk.py`, `dualcam/wpd_worker.py`, `dualcam/sony_protocol.py`, `dualcam/cameras.py`.

- Windows portable-device enumeration did not expose the tested Sony libusbK device. A bulk USB path was added alongside the portable-device fallback.
- The bulk backend loads the existing Sony-installed libusbK library and the libusb runtime supplied by `libusb-package`.
- The connected camera model is checked and Sony's remote-control handshake is performed.
- USB packet framing handles fragmented/coalesced input, validates lengths and transaction identifiers, and bounds response sizes.
- Sony property parsing handles the observed property formats and reads the movie status used for recording confirmation.
- Writes exposed by this transport are restricted to movie start and stop. Preview object reads are restricted to the designated live-view object.
- The code does not install/replace USB drivers or expose card-format/media-delete operations.

Protocol research included [libgphoto2's Sony/PTP code](https://github.com/gphoto/libgphoto2/blob/master/camlibs/ptp2/library.c) and [pysonycam](https://github.com/olkham/pysonycam). These are references, not packages a user must copy into this project. Sony's own driver comes from Sony's installer and is not included here.

## Scan, cancellation and interface recovery

**Files:** `dualcam/jobs.py`, `dualcam/cameras.py`, `app.py`, `build_windows.py`.

- USB operations run in a helper process so an unresponsive driver cannot indefinitely lock the Tk interface.
- The helper is packaged as an onedir process rather than the earlier one-file arrangement that could leave inherited output pipes open.
- USB requests and high-level scan/connection jobs have timeouts and bounded cleanup paths.
- Scan and connection jobs expose Cancel; completion, failure and cancellation restore appropriate controls.
- Session identifiers keep late events from an old connection from relocking a new session.
- Subsequent failed status polling preserves the original connection error for diagnosis.
- A request lock keeps Sony preview reads and recording commands from interleaving on the JSON/USB conversation.

## Neon manual address and recording support

**Files:** `dualcam/neon.py`, `app.py`.

- The user enters a current IPv4 address, host:port, local hostname or HTTP root URL in Setup.
- Port 8080 is the default. Credentials, unsupported schemes, invalid ports and non-root page paths are rejected.
- The last address used for connection and Include Neon setting are saved locally.
- The public source uses `neon.local:8080` as a generic default, rather than the development phone's changing IP.
- Include Neon is optional. When included, it participates in the same start/stop preflight as the other devices.
- Local HTTP responses are bounded and validated. Redirects are not followed.
- Stop uses `/api/recording:stop_and_save`; no cancel/discard endpoint is exposed.
- The scene preview URL uses the user-entered host, avoiding a stale host advertised in stream metadata.

Reference: [Pupil Labs' local API](https://pupil-labs.github.io/pl-realtime-api/dev/guides/under-the-hood/). The code calls this API directly; the separate Pupil Labs Python client is not required.

## Optional previews

**Files:** `dualcam/previews.py`, `dualcam/preview_decoder.py`, `dualcam/preview_wifi.py`, `preview_entry.py`, `app.py`.

- Sony live-view JPEG data is read over the existing USB session. The JPEG offset in its header is used when valid.
- Neon scene video uses its supported UDP RTSP transport; the companion tested here did not accept the attempted TCP transport.
- The decoder runs in a separate process, so shutting down a stalled network decoder does not send a camera shutter command.
- Only the newest picture per device is retained. Pictures older than two seconds are cleared instead of being presented as live.
- Preview start/stop never sends recording commands. The GoPro SDK's high-level preview wrapper was avoided because that wrapper also sends a shutter-stop command.
- GoPro preview uses direct stream HTTP requests, a temporary Wi-Fi profile and conditional restoration of the previous network.
- Before switching Wi-Fi, the app checks whether that adapter carries Neon's connection and refuses a switch that would remove that route.
- Invalid startup video packets are skipped in the decoder, but a full GoPro live preview remained unresolved, including stream-discovery behavior. This is not a claim that GoPro preview has been completely fixed.

Sony and Neon previews were verified during recording on the development setup. Previews remain optional; three-device recording was tested independently of a working GoPro preview.

## Source-release preparation

- Third-party package files, compiled executables, development environments, logs, camera frames, saved settings and backups were excluded from the GitHub folder.
- Runtime requirements explicitly include `requests`, which the preview module imports; it was previously also supplied indirectly by the GoPro SDK.
- A separate build manifest pins PyInstaller. A separate full environment manifest records indirect/development versions for reference.
- Installation/download links and where files belong are documented in README.md and DEPENDENCIES.md.
- This repository carries an MIT license for its application source. Dependency licenses remain separate.
