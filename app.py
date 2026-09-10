import asyncio
from datetime import datetime
import json
import io
import logging
from logging.handlers import RotatingFileHandler
import queue
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox

from dualcam.cameras import GoProCamera, SonyCamera, data_directory
from dualcam.core import Controller, DemoCamera
from dualcam.jobs import run_job
from dualcam.previews import Previews
from dualcam.neon import NeonCamera, normalize_address
from PIL import Image, ImageTk

BG, PANEL, TEXT, MUTED = '#101821', '#1b2733', '#f1f5f8', '#a9b8c7'
TEAL, RED, AMBER = '#62d5be', '#f16774', '#edc579'


class App:
    def __init__(self, root):
        self.root = root
        root.title('DualCam Studio')
        root.geometry('1080x800')
        root.minsize(960, 760)
        root.configure(bg=BG)
        self.events = queue.Queue()
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.loop.run_forever, daemon=True)
        self.thread.start()
        self.controller = None
        self.previews = None
        self.preview_active = {'GoPro': False, 'Sony': False, 'Neon': False}
        self.preview_seen = {}
        self.closed = False
        self.busy = False
        self.job_cancel = None
        self.job_cancellable = False
        self.job_error = None
        self.session = 0
        self.poll_future = None
        self.states = {}
        self.pending_stop = False
        self.countdown_id = None
        self.devices = []
        self.mode = tk.StringVar(value='Demo — simulated cameras')
        self.serial = tk.StringVar()
        self.wifi = tk.StringVar()
        self.sony = tk.StringVar(value='Automatically find ZV-1M2')
        self.neon_address = tk.StringVar(value='neon.local:8080')
        self.neon_enabled = tk.BooleanVar(value=False)
        self.delay = tk.StringVar(value='0')
        self.message = tk.StringVar(value='Try the demo, or choose Real cameras in Setup.')
        self.banner = tk.StringVar(value='DEMO MODE  •  No cameras will be controlled')
        self.settings_path = data_directory() / 'settings.json'
        try:
            settings = json.loads(self.settings_path.read_text())
            self.serial.set(settings.get('serial', ''))
            self.wifi.set(settings.get('wifi', ''))
            self.neon_address.set(settings.get('neon_address', 'neon.local:8080'))
            self.neon_enabled.set(bool(settings.get('neon_enabled', False)))
        except (OSError, ValueError):
            pass
        self.build()
        root.protocol('WM_DELETE_WINDOW', self.quit)
        root.after(75, self.drain)
        root.after(3000, self.poll)
        root.after(100, self.draw_previews)

    def emit(self, kind, value):
        self.events.put((kind, value))

    def label(self, parent, text='', size=11, color=TEXT, **kwargs):
        return tk.Label(parent, text=text, font=('Segoe UI', size), fg=color,
                        bg=parent.cget('bg'), **kwargs)

    def button(self, parent, text, command, bg=PANEL, fg=TEXT, **kwargs):
        return tk.Button(parent, text=text, command=command, bg=bg, fg=fg,
            activebackground=bg, activeforeground=fg, disabledforeground='#748492',
            relief='flat', bd=0, cursor='hand2', font=('Segoe UI', 12, 'bold'),
            padx=18, pady=12, **kwargs)

    def build(self):
        header = tk.Frame(self.root, bg=BG, padx=28, pady=20)
        header.pack(fill='x')
        self.label(header, 'DUALCAM / STUDIO', 23).pack(anchor='w')
        self.label(header, 'GoPro. Sony. Neon eye glasses. One recording control.', color=MUTED).pack(anchor='w', pady=(4, 0))
        self.label(header, size=10, color=AMBER, textvariable=self.banner).pack(anchor='w', pady=(16, 0))
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=BG, borderwidth=0)
        style.configure('TNotebook.Tab', background=PANEL, foreground=TEXT, padding=(18, 9), font=('Segoe UI', 10))
        style.map('TNotebook.Tab', background=[('selected', '#2b4051')])
        style.configure('TCombobox', padding=5)
        self.tabs = ttk.Notebook(self.root)
        footer = tk.Frame(self.root, bg=BG, padx=28, pady=8)
        footer.pack(side='bottom', fill='x')
        self.cancel_button = self.button(footer, 'Cancel', self.cancel_job, state='disabled')
        self.cancel_button.pack(side='right', padx=(12, 0))
        self.label(footer, textvariable=self.message, color=TEAL, wraplength=650,
                   justify='left', anchor='w').pack(side='left', fill='x', expand=True)
        self.tabs.pack(fill='both', expand=True, padx=28, pady=(0, 20))
        control, setup, logs = (tk.Frame(self.tabs, bg=BG) for _ in range(3))
        self.tabs.add(control, text='Recording')
        self.tabs.add(setup, text='Setup & help')
        self.tabs.add(logs, text='Session log')
        live = tk.Frame(self.tabs, bg=BG)
        self.tabs.add(live, text='Live preview')
        self.preview_widgets = {}
        self.label(live, 'Sony uses USB. Neon uses your local network. GoPro preview uses the camera’s Wi-Fi.',
                   10, MUTED, wraplength=800).pack(anchor='w', pady=(12, 2))
        self.label(live, 'For Neon + GoPro previews together, keep Neon reachable through Ethernet or a second Wi-Fi adapter.',
                   9, MUTED, wraplength=800).pack(anchor='w', pady=(0, 12))
        preview_bar = tk.Frame(live, bg=BG)
        preview_bar.pack(side='bottom', fill='x', pady=12)
        self.preview_start = self.button(preview_bar, '●   START ALL', self.start, bg=TEAL, fg=BG, state='disabled')
        self.preview_start.pack(side='left', fill='x', expand=True, padx=(0, 9))
        self.preview_stop = self.button(preview_bar, '■   STOP ALL', self.stop, bg='#54313b', state='disabled')
        self.preview_stop.pack(side='left', fill='x', expand=True, padx=(9, 0))
        previews = tk.Frame(live, bg=BG)
        previews.pack(fill='both', expand=True)
        previews.rowconfigure(0, weight=1)
        for index, key in enumerate(('GoPro', 'Sony', 'Neon')):
            panel = tk.Frame(previews, bg=PANEL, padx=10, pady=10)
            panel.grid(row=0, column=index, sticky='nsew', padx=(0, 8) if index == 0 else (8, 0))
            previews.columnconfigure(index, weight=1, uniform='preview')
            self.label(panel, key, 17).pack(anchor='w')
            state = self.label(panel, 'Disconnected', 11, MUTED)
            state.pack(anchor='w', pady=(4, 8))
            button = self.button(panel, 'Show preview', lambda k=key: self.toggle_preview(k), state='disabled')
            button.pack(side='bottom', fill='x', pady=(10, 0))
            status = self.label(panel, 'Preview off', 10, MUTED, height=4,
                                wraplength=270, justify='left', anchor='nw')
            status.pack(side='bottom', fill='x', pady=(8, 0))
            canvas = tk.Canvas(panel, bg='#080e14', highlightthickness=0, width=320, height=180)
            canvas.pack(fill='both', expand=True)
            self.preview_widgets[key] = (canvas, status, button, state)
        cards = tk.Frame(control, bg=BG)
        cards.pack(fill='x', pady=20)
        self.cards = {}
        for index, (key, model, route) in enumerate((('GoPro', 'HERO12 Black', 'WIRELESS / BLUETOOTH'),
                                                    ('Sony', 'ZV-1M2', 'USB / PC REMOTE'),
                                                    ('Neon', 'Eye glasses', 'LOCAL NETWORK'))):
            card = tk.Frame(cards, bg=PANEL, padx=16, pady=16)
            card.grid(row=0, column=index, sticky='nsew', padx=(0, 9) if index == 0 else (9, 0))
            cards.columnconfigure(index, weight=1, uniform='camera')
            self.label(card, route, 9, MUTED).pack(anchor='w')
            self.label(card, key + '  ' + model, 16).pack(anchor='w', pady=(8, 16))
            state = self.label(card, 'Disconnected', 14, MUTED, wraplength=250, height=2, anchor='w', justify='left')
            state.pack(anchor='w')
            battery = self.label(card, 'Battery  —', 11, MUTED)
            battery.pack(anchor='w', pady=(10, 12))
            detail = self.label(card, 'Connect to read camera status.', 10, MUTED,
                                justify='left', wraplength=245, height=4, anchor='nw')
            detail.pack(fill='x')
            self.cards[key] = state, battery, detail
        bar = tk.Frame(control, bg=BG)
        bar.pack(fill='x')
        self.connect_button = self.button(bar, 'Connect cameras', self.connect)
        self.connect_button.pack(side='left')
        self.disconnect_button = self.button(bar, 'Disconnect', self.disconnect, state='disabled')
        self.disconnect_button.pack(side='left', padx=10)
        self.label(bar, 'Countdown', color=MUTED).pack(side='left', padx=(18, 7))
        self.delay_box = ttk.Combobox(bar, textvariable=self.delay, values=('0', '3', '5', '10'), width=4, state='readonly')
        self.delay_box.pack(side='left')
        self.label(bar, 'seconds', color=MUTED).pack(side='left', padx=7)
        recordbar = tk.Frame(control, bg=BG)
        recordbar.pack(fill='x', pady=(20, 15))
        self.start_button = self.button(recordbar, '●   START ALL', self.start, bg=TEAL, fg=BG, height=2, state='disabled')
        self.start_button.pack(side='left', fill='x', expand=True, padx=(0, 9))
        self.stop_button = self.button(recordbar, '■   STOP ALL', self.stop, bg='#54313b', height=2, state='disabled')
        self.stop_button.pack(side='left', fill='x', expand=True, padx=(9, 0))
        self.label(control, 'GoPro / Sony save to their cards. Neon stops and saves on its companion phone. Starts are approximate.',
                   9, MUTED, wraplength=830, justify='left').pack(anchor='w')
        form = tk.Frame(setup, bg=BG, pady=16)
        form.pack(fill='x')
        fields = [('Connection mode', self.mode, ('Demo — simulated cameras', 'Real cameras')),
                  ('GoPro serial: last 4 digits', self.serial, None),
                  ('Sony USB device', self.sony, ('Automatically find ZV-1M2',)),
                  ('Neon address (current IP)', self.neon_address, None),
                  ('GoPro preview Wi-Fi adapter', self.wifi, None)]
        self.setup_widgets = []
        for row, (title, variable, options) in enumerate(fields):
            self.label(form, title, color=MUTED).grid(row=row, column=0, sticky='w', pady=6, padx=(0, 18))
            widget = ttk.Combobox(form, textvariable=variable, values=options, state='readonly') if options else ttk.Entry(form, textvariable=variable)
            widget.grid(row=row, column=1, sticky='ew', pady=6)
            self.setup_widgets.append(widget)
        form.columnconfigure(1, weight=1)
        self.setup_widgets[0].bind('<<ComboboxSelected>>', self.mode_changed)
        self.scan_button = self.button(form, 'Scan USB', self.scan)
        self.scan_button.grid(row=2, column=2, padx=(12, 0))
        self.setup_disconnect = self.button(form, 'Disconnect', self.disconnect, state='disabled')
        self.setup_disconnect.grid(row=0, column=2, padx=(12, 0))
        self.neon_check = tk.Checkbutton(form, text='Include Neon', variable=self.neon_enabled,
            command=self.neon_changed, bg=BG, fg=TEXT, selectcolor=PANEL, activebackground=BG,
            activeforeground=TEXT, font=('Segoe UI', 11))
        self.neon_check.grid(row=3, column=2, padx=(12, 0))
        self.label(form, 'Enter an IP or full URL; port 8080 is used if omitted. Disconnect before changing a connected address.',
                   9, MUTED).grid(row=5, column=0, columnspan=3, sticky='w', pady=(6, 0))
        help_text = (
            'GOPRO  •  Enable PC Bluetooth, close Quik, and pair HERO12. Enter its serial digits.\n'
            'Preview needs Wi-Fi; use 2.4 GHz on the camera. Adapter name is optional.\n\n'
            'SONY  •  Use Movie mode, a memory card and USB data cable; choose PC Remote.\n'
            'Close Sony Remote and disconnect Creators’ App before connecting here.\n\n'
            'NEON  •  Enable streaming in the companion app. Enter its current IP above and tick Include Neon.\n'
            'The PC must reach the phone on the same local network. Leave Neon unticked for two-camera use.\n\n'
            'Connect on Recording, then use Live preview. Start All requires every included device to be ready.\n'
            'If one device fails, another may keep recording. Stop All, or stop directly on each device.'
        )
        self.label(setup, help_text, 10, MUTED, justify='left', anchor='nw').pack(fill='both', expand=True, pady=10)
        self.log = tk.Text(logs, bg=PANEL, fg=MUTED, font=('Consolas', 10), relief='flat', wrap='word', state='disabled')
        self.log.pack(fill='both', expand=True, pady=16)

    def mode_changed(self, event=None):
        demo = self.mode.get().startswith('Demo')
        self.banner.set('DEMO MODE  •  No cameras will be controlled' if demo else 'REAL CAMERAS  •  GoPro Bluetooth + Sony USB' + (' + Neon local network' if self.neon_enabled.get() else ''))

    def neon_changed(self):
        self.mode_changed()
        self.render_states()

    def run(self, coroutine, complete=None, *, label='Camera operation', timeout=120,
            cancellable=False, on_error=None):
        self.busy = True
        self.job_cancel = asyncio.Event()
        self.job_cancellable = cancellable
        self.job_error = on_error
        self.buttons()
        future = asyncio.run_coroutine_threadsafe(
            run_job(coroutine, self.job_cancel, timeout, label), self.loop)
        def done(f):
            try:
                value = f.result()
                self.emit('job_done', (complete, value, None))
            except BaseException as exc:
                self.emit('job_done', (complete, None, str(exc) or 'Operation cancelled'))
        future.add_done_callback(done)

    def cancel_job(self):
        if self.busy and self.job_cancellable and self.job_cancel:
            self.message.set('Cancelling… releasing the camera connection.')
            self.job_cancellable = False
            self.buttons()
            self.loop.call_soon_threadsafe(self.job_cancel.set)

    def session_emit(self, session, kind, value):
        self.emit('session', (session, kind, value))

    def connection_failed(self):
        controller, self.controller = self.controller, None
        previews, self.previews = self.previews, None
        self.preview_active = dict.fromkeys(self.preview_active, False)
        self.session += 1
        self.states = {}
        self.render_states()
        if controller:
            # This session's late status messages must not affect a new attempt.
            async def release():
                if previews:
                    await previews.close()
                await run_job(controller.close(), asyncio.Event(), 12, 'Disconnect')
            future = asyncio.run_coroutine_threadsafe(release(), self.loop)
            future.add_done_callback(lambda f: f.exception())

    def connect(self):
        if self.busy or self.controller:
            return
        demo = self.mode.get().startswith('Demo')
        if not demo and (len(self.serial.get().strip()) < 4 or not self.serial.get().strip().isdigit()):
            self.message.set('Enter the GoPro serial digits in Setup first.')
            self.tabs.select(1)
            return
        chosen = next((d['id'] for d in self.devices if d['name'] == self.sony.get()), '')
        cameras = {'GoPro': DemoCamera(85), 'Sony': DemoCamera(72)} if demo else {
            'GoPro': GoProCamera(self.serial.get(), self.wifi.get()), 'Sony': SonyCamera(chosen)}
        if self.neon_enabled.get():
            try:
                address = normalize_address(self.neon_address.get())
            except ValueError as exc:
                self.message.set(str(exc))
                self.tabs.select(1)
                return
            cameras['Neon'] = DemoCamera(60) if demo else NeonCamera(address)
        self.session += 1
        session = self.session
        self.controller = Controller(cameras, lambda k, v: self.session_emit(session, k, v))
        self.previews = Previews(self.controller, lambda key, text, active:
            self.session_emit(session, 'preview', (key, text, active)))
        try:
            self.settings_path.write_text(json.dumps({'serial': self.serial.get(), 'wifi': self.wifi.get(),
                'neon_address': self.neon_address.get().strip(), 'neon_enabled': self.neon_enabled.get()}, indent=2))
        except OSError as exc:
            self.add_log(f'Could not save settings: {exc}')
        self.message.set('Connecting demo cameras…' if demo else 'Connecting… confirm pairing on GoPro if requested (up to 100 seconds).')
        self.run(self.controller.connect(), self.connected, label='Connection',
                 timeout=110, cancellable=True, on_error=self.connection_failed)

    def connected(self, _):
        if not any(s.get('connected') for s in self.states.values()):
            self.connection_failed()
            self.message.set('No devices connected. Check the details in Session log, then retry.')
        elif not all(s.get('connected') for s in self.states.values()):
            self.message.set('Some devices did not connect. Disconnect to edit setup and retry. Check Session log for details.')

    def start(self):
        if self.busy or not self.controller or self.countdown_id:
            return
        self.count_down(int(self.delay.get()))

    def count_down(self, remaining):
        self.countdown_id = None
        if remaining:
            self.message.set(f'Starting all in {remaining}…  Stop cancels the countdown.')
            self.countdown_id = self.root.after(1000, self.count_down, remaining-1)
            self.buttons()
        else:
            self.message.set('Sending start commands…')
            self.run(self.controller.record(True))

    def stop(self):
        if self.countdown_id:
            self.root.after_cancel(self.countdown_id)
            self.countdown_id = None
            self.message.set('Countdown cancelled')
            self.buttons()
            return
        if not self.controller:
            return
        if self.busy:
            self.pending_stop = True
            self.message.set('Stop queued • waiting for the current camera operation')
            return
        self.message.set('Sending stop to all included devices…')
        self.run(self.controller.record(False))

    def disconnect(self):
        if self.busy or not self.controller:
            return
        if any(s.get('recording') is True for s in self.states.values()):
            self.message.set('Stop all devices before disconnecting.')
            return
        if self.countdown_id:
            self.root.after_cancel(self.countdown_id)
            self.countdown_id = None
        self.run(self.close_session(), self.disconnected, label='Disconnect', timeout=70,
                 on_error=self.connection_failed)

    async def close_session(self):
        if self.previews:
            await self.previews.close()
        if self.controller:
            await self.controller.close()

    def disconnected(self, _):
        self.controller = None
        self.previews = None
        self.preview_active = dict.fromkeys(self.preview_active, False)
        self.session += 1
        self.states = {}
        self.render_states()
        self.message.set('Disconnected. Camera recording is not stopped by disconnecting.')

    def scan(self):
        if not self.busy and not self.controller:
            self.message.set('Scanning Sony USB… up to 15 seconds. You can cancel below.')
            self.run(SonyCamera.scan(), self.scanned, label='USB scan', timeout=15, cancellable=True)

    def scanned(self, devices):
        self.devices = devices
        self.setup_widgets[2]['values'] = ['Automatically find ZV-1M2'] + [d['name'] for d in devices]
        self.message.set(f'Found {len(devices)} USB portable device(s). Select the Sony in Setup.' if devices else 'No USB camera detected. Check the data cable and PC Remote mode.')
        if len(devices) == 1:
            self.sony.set(devices[0]['name'])

    def buttons(self):
        attached = self.controller is not None
        ready = attached and len(self.states) == len(self.controller.cameras) and all(s.get('connected') and s.get('recording') is False for s in self.states.values())
        self.connect_button['state'] = 'normal' if not attached and not self.busy else 'disabled'
        self.disconnect_button['state'] = 'normal' if attached and not self.busy else 'disabled'
        self.setup_disconnect['state'] = self.disconnect_button['state']
        self.cancel_button['state'] = 'normal' if self.busy and self.job_cancellable else 'disabled'
        self.scan_button['text'] = 'Scanning…' if self.busy and not attached else 'Scan USB'
        self.start_button['state'] = 'normal' if ready and not self.busy and not self.countdown_id else 'disabled'
        self.stop_button['state'] = 'normal' if attached else 'disabled'
        self.preview_start['state'] = self.start_button['state']
        self.preview_stop['state'] = self.stop_button['state']
        for key, widgets in self.preview_widgets.items():
            active = self.preview_active[key]
            widgets[2]['text'] = 'Hide preview' if active else 'Show preview'
            widgets[2]['state'] = 'normal' if active or (not self.busy and self.states.get(key, {}).get('connected')) else 'disabled'
        for widget in self.setup_widgets:
            widget['state'] = 'disabled' if attached or self.busy else ('readonly' if isinstance(widget, ttk.Combobox) else 'normal')
        self.scan_button['state'] = 'disabled' if attached or self.busy else 'normal'
        self.neon_check['state'] = 'disabled' if attached or self.busy else 'normal'
        self.delay_box['state'] = 'disabled' if self.busy or self.countdown_id else 'readonly'

    def render_states(self):
        for key, widgets in self.cards.items():
            state = self.states.get(key, {})
            recording = state.get('recording')
            if key == 'Neon' and not self.neon_enabled.get():
                label, color = 'Not included', MUTED
            elif not state.get('connected'):
                label, color = 'Disconnected / check camera', AMBER
            elif recording is True:
                label, color = '●  Recording', RED
            elif recording is False:
                label, color = 'Ready • stopped', TEAL
            else:
                label, color = 'Recording status unknown', AMBER
            if self.mode.get().startswith('Demo') and state.get('connected'):
                label += '  [DEMO]'
            widgets[0].configure(text=label, fg=color)
            self.preview_widgets[key][3].configure(text=label, fg=color)
            battery = state.get('battery')
            widgets[1].configure(text=f'Battery  {battery}%' if battery is not None else 'Battery  —')
            widgets[2].configure(text=state.get('detail', 'Connect to read camera status.'))
            if key == 'Neon' and not self.neon_enabled.get():
                widgets[2].configure(text='Enter its current IP in Setup and tick Include Neon when needed.')
        self.buttons()

    def toggle_preview(self, key):
        if not self.previews:
            return
        if self.preview_active[key]:
            self.preview_widgets[key][1].configure(text='Closing preview…')
            self.loop.call_soon_threadsafe(self.previews.stop, key)
        elif not self.busy and self.states.get(key, {}).get('connected'):
            self.preview_active[key] = True
            self.preview_seen.pop(key, None)
            self.loop.call_soon_threadsafe(self.previews.start, key)
        self.buttons()

    def draw_previews(self):
        frames = self.previews.snapshot() if self.previews else {}
        for key, (canvas, status, _, _) in self.preview_widgets.items():
            frame = frames.get(key)
            if frame and time.monotonic() - frame[0] <= 2:
                stamp, data = frame
                size = (max(1, canvas.winfo_width()), max(1, canvas.winfo_height()))
                if self.preview_seen.get(key) != (stamp, size):
                    try:
                        with Image.open(io.BytesIO(data)) as picture:
                            picture.thumbnail(size, Image.Resampling.BILINEAR)
                            photo = ImageTk.PhotoImage(picture)
                        canvas.delete('all')
                        canvas.create_image(size[0]//2, size[1]//2, image=photo)
                        canvas.photo = photo
                        self.preview_seen[key] = (stamp, size)
                        status.configure(text='Live • simulated demo' if self.mode.get().startswith('Demo') else 'Live • preview only; clips save on the camera', fg=TEAL)
                    except (OSError, ValueError):
                        status.configure(text='Could not display this preview frame', fg=AMBER)
            else:
                if self.preview_seen.pop(key, None):
                    canvas.delete('all')
                    canvas.photo = None
                    status.configure(text='Waiting for a fresh picture…' if self.preview_active[key] else 'Preview off', fg=MUTED)
                if not self.previews:
                    status.configure(text='Connect cameras on the Recording tab first.', fg=MUTED)
        if not self.closed:
            self.root.after(100, self.draw_previews)

    def drain(self):
        try:
            while True:
                kind, value = self.events.get_nowait()
                if kind == 'session':
                    session, kind, value = value
                    if session != self.session:
                        continue
                if kind == 'states':
                    self.states = value
                    self.render_states()
                elif kind == 'message':
                    self.message.set(value)
                    self.add_log(value)
                elif kind == 'log':
                    self.add_log(value)
                elif kind == 'preview':
                    key, text, active = value
                    self.preview_active[key] = active
                    self.preview_widgets[key][1].configure(text=text, fg=MUTED if active else AMBER)
                    if not active:
                        self.preview_seen.pop(key, None)
                        self.preview_widgets[key][0].delete('all')
                        self.add_log(f'{key}: {text}')
                    self.buttons()
                elif kind == 'job_done':
                    complete, result, error = value
                    self.busy = False
                    self.job_cancel = None
                    self.job_cancellable = False
                    error_handler, self.job_error = self.job_error, None
                    if error:
                        if error_handler:
                            error_handler()
                        self.message.set(error)
                        self.add_log(error)
                    elif complete:
                        complete(result)
                    if self.closed:
                        return
                    if self.pending_stop:
                        self.pending_stop = False
                        self.stop()
                    self.buttons()
        except queue.Empty:
            pass
        if self.root.winfo_exists():
            self.root.after(75, self.drain)

    def add_log(self, message):
        logging.getLogger('dualcam').info(message)
        self.log.configure(state='normal')
        self.log.insert('end', f'{datetime.now():%H:%M:%S}  {message}\n')
        if int(self.log.index('end-1c').split('.')[0]) > 600:
            self.log.delete('1.0', '101.0')
        self.log.see('end')
        self.log.configure(state='disabled')

    def poll(self):
        if self.controller and not self.busy and not self.countdown_id and (not self.poll_future or self.poll_future.done()):
            self.poll_future = asyncio.run_coroutine_threadsafe(self.controller.refresh(), self.loop)
        self.root.after(3000, self.poll)

    def quit(self):
        if self.busy:
            if self.job_cancellable:
                self.cancel_job()
            else:
                self.message.set('Finishing the camera operation. You can close when it finishes.')
            return
        if self.controller and any(s.get('recording') is not False for s in self.states.values()):
            if not messagebox.askyesno('Cameras may be recording',
                'Closing does not stop camera recordings. Close anyway?', default='no', parent=self.root):
                return
        if self.countdown_id:
            self.root.after_cancel(self.countdown_id)
            self.countdown_id = None
        if self.controller:
            self.run(self.close_session(), lambda _: self.finish_quit(), timeout=70)
        else:
            self.finish_quit()

    def finish_quit(self):
        self.closed = True
        for callback in self.root.tk.call('after', 'info'):
            self.root.after_cancel(callback)
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.root.destroy()


def main():
    handler = RotatingFileHandler(data_directory() / 'session.log', maxBytes=500000, backupCount=2, encoding='utf-8')
    logger = logging.getLogger('dualcam')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    # SDK debug logs can contain Wi-Fi credentials. Do not save them.
    logging.getLogger('open_gopro').addHandler(logging.NullHandler())
    logging.getLogger('open_gopro').propagate = False
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
