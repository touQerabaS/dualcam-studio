"""Run with the project virtual environment on Windows."""
import subprocess
import sys
import comtypes.client

comtypes.client.GetModule('PortableDeviceApi.dll')
comtypes.client.GetModule('PortableDeviceTypes.dll')
common = [sys.executable, '-m', 'PyInstaller', '--noconfirm', '--distpath', 'dist-preview', '--workpath', 'build-preview']
subprocess.run(common + ['--onedir', '--console', '--name', 'SonyUsbWorker',
    '--collect-submodules', 'comtypes.gen', '--collect-all', 'libusb_package',
    '--hidden-import', 'usb.backend.libusb1', 'worker_entry.py'], check=True)
subprocess.run(common + ['--onedir', '--console', '--name', 'PreviewDecoder',
    '--collect-all', 'av', 'preview_entry.py'], check=True)
subprocess.run(common + ['--onedir', '--windowed', '--name', 'DualCam Studio',
    '--add-data', 'dist-preview/SonyUsbWorker;sony-worker',
    '--add-data', 'dist-preview/PreviewDecoder;preview-worker',
    '--collect-data', 'open_gopro', '--collect-submodules', 'winrt',
    '--copy-metadata', 'open-gopro', 'app.py'], check=True)
