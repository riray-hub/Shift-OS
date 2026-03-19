#!/usr/bin/env python3
import gi
import os
import sys
import subprocess
import threading
import time

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk, Gio

# ==========================================
# CSS UNTUK MODE TERANG (LIGHT)
# ==========================================
CSS_LIGHT = b"""
window, viewport { background-color: #ffffff; color: #1a1a2e; }
.title { font-size: 22px; font-weight: bold; color: #1a1a2e; }
.subtitle { color: #666688; font-size: 14px; }
.success-box { margin-top: 20px; margin-bottom: 20px; }
.success-text { color: #2e7d32; font-weight: bold; font-size: 16px; }
.hw-list-title { font-weight: bold; font-size: 14px; color: #1a1a2e; margin-top: 10px; }
.kernel-text { font-size: 12px; color: #8888aa; margin-top: 8px; font-weight: bold; }
.hw-item { background: #f8f9fa; border: 1px solid #e0e0e0; border-radius: 6px; padding: 12px; margin-bottom: 6px; }
.danger-text { color: #e65100; font-weight: bold; font-size: 16px; }
button { background: #f0f4ff; color: #1a1a2e; border: 1px solid #d0d8ee; border-radius: 6px; padding: 8px 16px; }
button:hover { background: #e0e8ff; border-color: #03a1fe; color: #03a1fe; }
button.suggested-action { background: #03a1fe; color: #ffffff; border: none; font-weight: bold; }
button.suggested-action:hover { background: #0288d1; color: #ffffff; }
button.close-action { background: #e2e8f0; color: #475569; border: none; font-weight: bold; }
button.close-action:hover { background: #cbd5e1; color: #1e293b; }
textview, textview text { background-color: #f8f9ff; color: #1a1a2e; font-family: monospace; }
"""

# ==========================================
# CSS UNTUK MODE GELAP (DARK)
# ==========================================
CSS_DARK = b"""
window, viewport { background-color: #1a1b26; color: #c0caf5; }
.title { font-size: 22px; font-weight: bold; color: #c0caf5; }
.subtitle { color: #7aa2f7; font-size: 14px; }
.success-box { margin-top: 20px; margin-bottom: 20px; }
.success-text { color: #73daca; font-weight: bold; font-size: 16px; }
.hw-list-title { font-weight: bold; font-size: 14px; color: #c0caf5; margin-top: 10px; }
.kernel-text { font-size: 12px; color: #565f89; margin-top: 8px; font-weight: bold; }
.hw-item { background: #24283b; border: 1px solid #414868; border-radius: 6px; padding: 12px; margin-bottom: 6px; }
.danger-text { color: #ff9e64; font-weight: bold; font-size: 16px; }
button { background: #24283b; color: #c0caf5; border: 1px solid #414868; border-radius: 6px; padding: 8px 16px; }
button:hover { background: #2f334d; border-color: #03a1fe; color: #03a1fe; }
button.suggested-action { background: #03a1fe; color: #ffffff; border: none; font-weight: bold; }
button.suggested-action:hover { background: #0288d1; color: #ffffff; }
button.close-action { background: #292e42; color: #9aa5ce; border: none; font-weight: bold; }
button.close-action:hover { background: #414868; color: #c0caf5; }
textview, textview text { background-color: #1f2335; color: #c0caf5; font-family: monospace; }
"""

class ShiftDriverManager(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Shift OS Driver Manager")
        self.set_default_size(650, 550)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        self.css_provider = Gtk.CssProvider()
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), self.css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.settings = Gio.Settings.new("org.gnome.desktop.interface")
        self.settings.connect("changed::color-scheme", self.on_theme_changed)
        self.apply_theme()

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.add(self.stack)
        self.needs_install = False

        # --- PAGE 1: LOADING ---
        self.loading_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.loading_box.set_valign(Gtk.Align.CENTER)
        self.spinner = Gtk.Spinner()
        self.spinner.set_size_request(64, 64)
        self.loading_box.pack_start(self.spinner, False, False, 0)
        
        self.loading_label = Gtk.Label(label="Analyzing Hardware & Drivers...")
        self.loading_label.get_style_context().add_class("title")
        self.loading_label.set_justify(Gtk.Justification.CENTER)
        self.loading_box.pack_start(self.loading_label, False, False, 0)
        self.stack.add_named(self.loading_box, "loading")

        # --- PAGE 2: OFFLINE (Desain Baru) ---
        self.offline_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.offline_box.set_valign(Gtk.Align.CENTER)
        self.offline_box.set_halign(Gtk.Align.CENTER)
        
        img_off = Gtk.Image.new_from_icon_name("network-offline-symbolic", Gtk.IconSize.DIALOG)
        img_off.set_pixel_size(96)
        self.offline_box.pack_start(img_off, False, False, 10)
        
        lbl_off_title = Gtk.Label(label="You're Offline")
        lbl_off_title.get_style_context().add_class("title")
        self.offline_box.pack_start(lbl_off_title, False, False, 0)
        
        lbl_off_desc = Gtk.Label(label="Shift OS needs an internet connection to fetch\nthe latest driver catalog for your hardware.")
        lbl_off_desc.set_justify(Gtk.Justification.CENTER)
        lbl_off_desc.get_style_context().add_class("subtitle")
        self.offline_box.pack_start(lbl_off_desc, False, False, 0)
        
        btn_retry = Gtk.Button(label="Try Again")
        btn_retry.get_style_context().add_class("suggested-action")
        btn_retry.set_size_request(200, 45)
        btn_retry.connect("clicked", self.start_check)
        self.offline_box.pack_start(btn_retry, False, False, 10)
        
        self.stack.add_named(self.offline_box, "offline")

        # --- PAGE 3: RESULT ---
        self.result_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.result_box.set_border_width(20)
        
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        title = Gtk.Label(label="System Hardware & Drivers")
        title.get_style_context().add_class("title")
        header_box.pack_start(title, False, False, 0)
        
        kernel_info = f"Kernel: {os.uname().release}"
        kernel_label = Gtk.Label(label=kernel_info)
        kernel_label.get_style_context().add_class("kernel-text")
        header_box.pack_end(kernel_label, False, False, 0)
        
        self.result_box.pack_start(header_box, False, False, 0)
        self.result_box.pack_start(Gtk.Separator(), False, False, 5)

        self.status_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.result_box.pack_start(self.status_container, False, False, 0)
        
        self.hw_label = Gtk.Label(label="Hardware Detected on your Device:")
        self.hw_label.get_style_context().add_class("hw-list-title")
        self.hw_label.set_halign(Gtk.Align.START)
        self.result_box.pack_start(self.hw_label, False, False, 5)

        self.driver_list_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.add(self.driver_list_container)
        self.result_box.pack_start(scrolled, True, True, 0)
        
        self.btn_action = Gtk.Button(label="Check Drivers")
        self.btn_action.connect("clicked", self.on_action_clicked)
        self.result_box.pack_end(self.btn_action, False, False, 0)

        self.stack.add_named(self.result_box, "result")
        self.start_check(None)

    def on_theme_changed(self, settings, key):
        self.apply_theme()

    def apply_theme(self):
        scheme = self.settings.get_string("color-scheme")
        if scheme == 'prefer-dark':
            self.css_provider.load_from_data(CSS_DARK)
            Gtk.Settings.get_default().set_property("gtk-application-prefer-dark-theme", True)
        else:
            self.css_provider.load_from_data(CSS_LIGHT)
            Gtk.Settings.get_default().set_property("gtk-application-prefer-dark-theme", False)

    def start_check(self, widget):
        self.loading_label.set_text("Analyzing Hardware & Drivers...")
        self.stack.set_visible_child_name("loading")
        self.spinner.start()
        threading.Thread(target=self.check_system_background, daemon=True).start()

    def check_system_background(self):
        time.sleep(1.5)
        try:
            subprocess.run(["ping", "-c", "1", "-W", "2", "8.8.8.8"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            is_online = True
        except:
            is_online = False

        if not is_online:
            GLib.idle_add(lambda: self.stack.set_visible_child_name("offline"))
            return

        try:
            drv_res = subprocess.run(["ubuntu-drivers", "devices"], capture_output=True, text=True)
            drv_out = drv_res.stdout
        except: drv_out = ""

        try:
            hw_res = subprocess.run(["lspci", "-mm"], capture_output=True, text=True)
            hw_list = hw_res.stdout.splitlines()
        except: hw_list = []

        GLib.idle_add(self.show_results, drv_out, hw_list)

    def show_results(self, drv_out, hw_list):
        self.spinner.stop()
        for child in self.status_container.get_children(): self.status_container.remove(child)
        for child in self.driver_list_container.get_children(): self.driver_list_container.remove(child)

        if not drv_out.strip():
            self.needs_install = False
            self.btn_action.set_label("Close Manager")
            self.btn_action.get_style_context().remove_class("suggested-action")
            self.btn_action.get_style_context().add_class("close-action")
            
            success_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            success_box.get_style_context().add_class("success-box")
            success_box.pack_start(Gtk.Image.new_from_icon_name("emblem-ok-symbolic", Gtk.IconSize.LARGE_TOOLBAR), False, False, 0)
            msg = Gtk.Label(label="Your system is fully optimized.\nAll drivers are up to date.")
            msg.get_style_context().add_class("success-text")
            success_box.pack_start(msg, False, False, 0)
            self.status_container.pack_start(success_box, False, False, 0)
        else:
            self.needs_install = True
            self.btn_action.set_label("Auto-Install Drivers")
            self.btn_action.get_style_context().remove_class("close-action")
            self.btn_action.get_style_context().add_class("suggested-action")
            
            warn_label = Gtk.Label(label="New proprietary drivers are available for your hardware!")
            warn_label.get_style_context().add_class("danger-text")
            self.status_container.pack_start(warn_label, False, False, 0)
            
            drv_box = Gtk.Label(label=drv_out)
            drv_box.get_style_context().add_class("hw-item")
            self.driver_list_container.pack_start(drv_box, False, False, 5)

        for hw in hw_list:
            parts = hw.split('"')
            if len(parts) >= 6:
                hw_type = parts[1]
                hw_vendor = parts[3]
                hw_device = parts[5]
                clean_hw = f"<b>{hw_vendor} {hw_device}</b>\n<span size='small' color='#666688'><i>{hw_type}</i></span>"
                
                item_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
                item_box.get_style_context().add_class("hw-item")
                
                hw_lower = hw_type.lower()
                icon_name = "emblem-system-symbolic"
                if "vga" in hw_lower or "3d" in hw_lower: icon_name = "video-display"
                elif "audio" in hw_lower: icon_name = "audio-card"
                elif "network" in hw_lower or "ethernet" in hw_lower or "wireless" in hw_lower: icon_name = "network-transmit-receive"
                elif "usb" in hw_lower: icon_name = "drive-removable-media"
                elif "sata" in hw_lower or "storage" in hw_lower or "memory" in hw_lower: icon_name = "drive-harddisk"
                
                img = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.DND)
                item_box.pack_start(img, False, False, 0)
                
                lbl = Gtk.Label()
                lbl.set_markup(clean_hw)
                lbl.set_halign(Gtk.Align.START)
                item_box.pack_start(lbl, False, False, 0)
                
                self.driver_list_container.pack_start(item_box, False, False, 0)

        self.result_box.show_all()
        self.stack.set_visible_child_name("result")

    def on_action_clicked(self, widget):
        if self.needs_install:
            self.loading_label.set_text("Downloading & Installing Drivers...\n\nPlease enter your password if prompted.\nThis may take a few minutes depending on your internet connection.")
            self.stack.set_visible_child_name("loading")
            self.spinner.start()
            
            threading.Thread(target=self.run_install_background, daemon=True).start()
        else:
            self.destroy()

    def run_install_background(self):
        try:
            # Pkexec dipanggil KHUSUS pas tombol install ditekan aja
            result = subprocess.run(["pkexec", "ubuntu-drivers", "autoinstall"], capture_output=True, text=True)
            success = (result.returncode == 0)
        except Exception:
            success = False

        GLib.idle_add(self.on_install_finished, success)

    def on_install_finished(self, success):
        self.stack.set_visible_child_name("result")
        if success:
            self.needs_install = False
            self.btn_action.set_label("Installation Complete! Click to Close.")
            self.btn_action.get_style_context().remove_class("suggested-action")
            self.btn_action.get_style_context().add_class("close-action")
            
            for child in self.status_container.get_children(): self.status_container.remove(child)
            success_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            success_box.get_style_context().add_class("success-box")
            success_box.pack_start(Gtk.Image.new_from_icon_name("emblem-ok-symbolic", Gtk.IconSize.LARGE_TOOLBAR), False, False, 0)
            msg = Gtk.Label(label="Successfully installed! Please restart your computer to apply changes.")
            msg.get_style_context().add_class("success-text")
            success_box.pack_start(msg, False, False, 0)
            self.status_container.pack_start(success_box, False, False, 0)
            self.status_container.show_all()
        else:
            self.btn_action.set_label("Install Failed / Canceled. Try Again")

win = ShiftDriverManager()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
