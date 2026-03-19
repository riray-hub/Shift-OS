#!/usr/bin/env python3
import gi
import os
import sys
import subprocess
import platform
import random
import shutil
import threading
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GdkPixbuf, Gdk, GLib

FLAG_FILE = os.path.expanduser("~/.config/shift-welcome-done")
CHECKLIST_FILE = os.path.expanduser("~/.config/shift-welcome-checklist")
if os.path.exists(FLAG_FILE):
    sys.exit(0)

TIPS = [
    ("Super", "Open the Activities overview — search apps, files, and more."),
    ("Super + A", "Open the full Applications grid."),
    ("Ctrl + Alt + T", "Open a Terminal window instantly."),
    ("Super + Left/Right", "Snap a window to the left or right half of your screen."),
    ("Alt + F4", "Close the current window."),
    ("Super + L", "Lock the screen immediately."),
    ("Alt + Tab", "Switch between open application windows."),
    ("Ctrl + Shift + Alt + R", "Start/stop a screen recording (built-in GNOME)."),
    ("sudo apt update && sudo apt upgrade -y", "Keep your system fully up to date."),
    ("flatpak update", "Update all Flatpak apps in one command."),
    ("sudo apt autoremove", "Clean up unused packages and free disk space."),
    ("htop", "A beautiful interactive process viewer — better than top."),
    ("history | grep <keyword>", "Search your terminal command history fast."),
    ("Ctrl + R (terminal)", "Reverse-search your command history interactively."),
    ("Super + V", "Open the notification / calendar panel."),
]

# ==========================================
# CSS UNTUK MODE TERANG (LIGHT)
# ==========================================
CSS_LIGHT = b"""
window, viewport { background-color: #ffffff; color: #1a1a2e; }
label { color: #1a1a2e; }
label.dim-label { color: #555577; }
button { background: #f0f4ff; color: #1a1a2e; border: 1px solid #d0d8ee; border-radius: 6px; }
button:hover { background: #e0e8ff; border-color: #03a1fe; color: #03a1fe; }
button.flat, button.flat:hover { background: transparent; border: none; color: #555577; }
button.flat:hover { color: #03a1fe; }
button.suggested-action { background: #03a1fe; color: #ffffff; border: none; }
button.suggested-action:hover { background: #0288d1; color: #ffffff; }
.stats-bar { background-color: #f5f8ff; border-radius: 10px; border: 1px solid #dde3f0; }
.tip-box { background-color: #f0f7ff; border-radius: 8px; border-left: 4px solid #03a1fe; }
.tip-key, .shortcut-key { background-color: #e8eeff; border: 1px solid #c0d0f0; border-radius: 5px; color: #1a1a2e; font-family: monospace; font-weight: bold; padding: 3px 10px; }
.badge-installed { background: #e8f5e9; border: 1px solid #a5d6a7; border-radius: 12px; color: #2e7d32; padding: 2px 10px; font-size: small; }
.badge-not-installed { background: #fff3e0; border: 1px solid #ffcc80; border-radius: 12px; color: #e65100; padding: 2px 10px; font-size: small; }

/* FIX: Nama elemen GTK yang benar untuk list/tabel */
list { background-color: #ffffff; color: #1a1a2e; }
row { background-color: #ffffff; color: #1a1a2e; border-bottom: 1px solid #eef0f8; }
row:hover { background-color: #f5f8ff; }

notebook, notebook stack { background-color: #ffffff; color: #1a1a2e; }
notebook header { background-color: #f5f8ff; border-bottom: 1px solid #dde3f0; }
notebook tab { color: #555577; padding: 6px 14px; background-color: transparent; }
notebook tab:checked { color: #03a1fe; border-bottom: 2px solid #03a1fe; }
scrolledwindow { background-color: transparent; }
separator { background-color: #e8ecf5; min-height: 1px; }
checkbutton label { color: #444466; }
progressbar trough { background: #e0e8ff; border-radius: 4px; min-height: 8px; }
progressbar progress { background: #03a1fe; border-radius: 4px; }
textview, textview text { background-color: #f8f9ff; color: #1a1a2e; font-family: monospace; }
"""

# ==========================================
# CSS UNTUK MODE GELAP (DARK)
# ==========================================
CSS_DARK = b"""
window, viewport { background-color: #1a1b26; color: #c0caf5; }
label { color: #c0caf5; }
label.dim-label { color: #7aa2f7; }
button { background: #24283b; color: #c0caf5; border: 1px solid #414868; border-radius: 6px; }
button:hover { background: #2f334d; border-color: #03a1fe; color: #03a1fe; }
button.flat, button.flat:hover { background: transparent; border: none; color: #7aa2f7; }
button.flat:hover { color: #03a1fe; }
button.suggested-action { background: #03a1fe; color: #ffffff; border: none; }
button.suggested-action:hover { background: #0288d1; color: #ffffff; }
.stats-bar { background-color: #24283b; border-radius: 10px; border: 1px solid #414868; }
.tip-box { background-color: #1f2335; border-radius: 8px; border-left: 4px solid #03a1fe; }
.tip-key, .shortcut-key { background-color: #292e42; border: 1px solid #414868; border-radius: 5px; color: #c0caf5; font-family: monospace; font-weight: bold; padding: 3px 10px; }
.badge-installed { background: #1e3a29; border: 1px solid #27a159; border-radius: 12px; color: #73daca; padding: 2px 10px; font-size: small; }
.badge-not-installed { background: #4a2727; border: 1px solid #f7768e; border-radius: 12px; color: #ff9e64; padding: 2px 10px; font-size: small; }

/* FIX: Nama elemen GTK yang benar untuk list/tabel */
list { background-color: #1a1b26; color: #c0caf5; }
row { background-color: #1a1b26; color: #c0caf5; border-bottom: 1px solid #24283b; }
row:hover { background-color: #24283b; }

notebook, notebook stack { background-color: #1a1b26; color: #c0caf5; }
notebook header { background-color: #24283b; border-bottom: 1px solid #414868; }
notebook tab { color: #565f89; padding: 6px 14px; background-color: transparent; }
notebook tab:checked { color: #03a1fe; border-bottom: 2px solid #03a1fe; }
scrolledwindow { background-color: transparent; }
separator { background-color: #414868; min-height: 1px; }
checkbutton label { color: #9aa5ce; }
progressbar trough { background: #24283b; border-radius: 4px; min-height: 8px; }
progressbar progress { background: #03a1fe; border-radius: 4px; }
textview, textview text { background-color: #1f2335; color: #c0caf5; font-family: monospace; }
"""

def get_system_info():
    info = {}
    try:
        import re
        with open("/proc/cpuinfo") as f:
            for line in f:
                if line.startswith("model name"):
                    info["cpu"] = re.sub(r'\s+', ' ', line.split(":")[1].strip())
                    break
    except:
        info["cpu"] = platform.processor() or "Unknown"
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemTotal"):
                    info["ram"] = f"{int(line.split()[1]) // 1024 // 1024} GB"
                    break
    except:
        info["ram"] = "Unknown"
    try:
        r = subprocess.run(["lspci"], capture_output=True, text=True, timeout=3)
        for line in r.stdout.splitlines():
            if "VGA" in line or "3D" in line or "Display" in line:
                info["gpu"] = line.split(":")[-1].strip()[:60]
                break
        else:
            info["gpu"] = "Unknown"
    except:
        info["gpu"] = "Unknown"
    try:
        r = subprocess.run(["df", "-h", "/"], capture_output=True, text=True, timeout=3)
        parts = r.stdout.strip().splitlines()[1].split()
        info["disk_total"] = parts[1]
        info["disk_used"] = parts[2]
        info["disk_free"] = parts[3]
    except:
        info["disk_total"] = info["disk_used"] = info["disk_free"] = "?"
    info["kernel"] = platform.release()
    info["arch"] = platform.machine()
    try:
        info["hostname"] = subprocess.run(["hostname"], capture_output=True, text=True, timeout=2).stdout.strip()
    except:
        info["hostname"] = "shift-os"
    return info

def is_installed(cmd):
    return shutil.which(cmd) is not None

def load_checklist():
    done = set()
    if os.path.exists(CHECKLIST_FILE):
        with open(CHECKLIST_FILE) as f:
            for line in f:
                done.add(line.strip())
    return done

def save_checklist(done):
    os.makedirs(os.path.dirname(CHECKLIST_FILE), exist_ok=True)
    with open(CHECKLIST_FILE, "w") as f:
        for item in done:
            f.write(item + "\n")


class ShiftWelcome(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Welcome to Shift OS")
        self.set_default_size(920, 700)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(0)
        
        # Setup CSS Provider
        self.css_provider = Gtk.CssProvider()
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), self.css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
            
        # Bind ke mode GNOME (Light/Dark)
        self.settings = Gio.Settings.new("org.gnome.desktop.interface")
        self.settings.connect("changed::color-scheme", self.on_theme_changed)
        self.apply_theme()

        self.checklist_done = load_checklist()
        self.step_checks = {}
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(300)
        self.add(self.stack)
        
        self.stack.add_named(self.build_home_page(), "home")
        self.stack.add_named(self.build_intro_page(), "intro")
        self.stack.add_named(self.build_features_page(), "features")
        self.stack.add_named(self.build_start_page(), "start")
        self.stack.add_named(self.build_recs_page(), "recs")
        self.stack.add_named(self.build_about_page(), "about")
        self.stack.add_named(self.build_shortcuts_page(), "shortcuts")
        self.stack.add_named(self.build_privacy_page(), "privacy")
        self.stack.add_named(self.build_appearance_page(), "appearance")
        self.stack.add_named(self.build_devsetup_page(), "devsetup")

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

    def wrap_page(self, content_widget):
        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        header.set_border_width(6)
        btn_back = Gtk.Button()
        btn_back.set_relief(Gtk.ReliefStyle.NONE)
        btn_back.get_style_context().add_class("flat")
        bb = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        bb.pack_start(Gtk.Image.new_from_icon_name("go-previous", Gtk.IconSize.BUTTON), False, False, 0)
        bb.pack_start(Gtk.Label(label="Back"), False, False, 0)
        btn_back.add(bb)
        btn_back.connect("clicked", lambda w: self.stack.set_visible_child_name("home"))
        header.pack_start(btn_back, False, False, 0)
        outer.pack_start(header, False, False, 0)
        outer.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 0)
        outer.pack_start(content_widget, True, True, 0)
        return outer

    def icon(self, name, size=Gtk.IconSize.LARGE_TOOLBAR):
        return Gtk.Image.new_from_icon_name(name, size)

    def section_label(self, text):
        lbl = Gtk.Label()
        lbl.set_markup(f"<span font_desc='10' weight='bold' color='#03a1fe'>{text.upper()}</span>")
        lbl.set_halign(Gtk.Align.START)
        lbl.set_margin_top(10)
        lbl.set_margin_bottom(4)
        return lbl

    # ==========================================
    # HOME
    # ==========================================
    def build_home_page(self):
        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=11)
        vbox.set_border_width(24)
        vbox.set_valign(Gtk.Align.CENTER)

        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("/usr/share/pixmaps/shift-logo.png", 88, 88, True)
            img = Gtk.Image.new_from_pixbuf(pixbuf)
        except:
            img = self.icon("start-here", Gtk.IconSize.DIALOG)
        img.set_halign(Gtk.Align.CENTER)
        vbox.pack_start(img, False, False, 0)

        t = Gtk.Label()
        t.set_markup("<span font_desc='23' weight='bold'>Welcome to Shift OS</span>")
        t.set_halign(Gtk.Align.CENTER)
        vbox.pack_start(t, False, False, 0)

        s = Gtk.Label()
        s.set_markup("<span color='#666688'>Harmonia v26.03.1 \u2014 Elegance Meets Pure Performance</span>")
        s.set_halign(Gtk.Align.CENTER)
        vbox.pack_start(s, False, False, 0)

        # System Health
        health_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        health_box.set_halign(Gtk.Align.CENTER)
        health_box.get_style_context().add_class("stats-bar")
        health_box.set_border_width(10)
        for icon_name, label, status, ok in self._get_health():
            item = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
            item.set_border_width(3)
            item.pack_start(self.icon(icon_name, Gtk.IconSize.SMALL_TOOLBAR), False, False, 0)
            kl = Gtk.Label()
            kl.set_markup(f"<span font_desc='9' weight='bold'>{label}: </span>")
            item.pack_start(kl, False, False, 0)
            vl = Gtk.Label()
            color = '#2e7d32' if ok else '#e65100'
            vl.set_markup(f"<span font_desc='9' color='{color}'>{status}</span>")
            item.pack_start(vl, False, False, 0)
            health_box.pack_start(item, False, False, 0)
            sep = Gtk.Label()
            sep.set_markup("<span color='#c0c8e0'>  |  </span>")
            health_box.pack_start(sep, False, False, 0)
        vbox.pack_start(health_box, False, False, 0)

        # Quick Stats
        stats_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        stats_box.set_halign(Gtk.Align.CENTER)
        stats_box.get_style_context().add_class("stats-bar")
        stats_box.set_border_width(7)
        for val, desc in [("~700 MB","Idle RAM"),("·",""),("~4.2 GB","ISO"),("·",""),
                          ("~10 min","Install"),("·",""),("GNOME 46","Desktop"),("·",""),("Wayland","Display")]:
            if val == "·":
                l = Gtk.Label(); l.set_markup("<span color='#c0c8e0' font_desc='14'> · </span>")
                stats_box.pack_start(l, False, False, 0)
            else:
                item = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
                item.set_border_width(5)
                lv = Gtk.Label(); lv.set_markup(f"<span font_desc='11' weight='bold' color='#03a1fe'>{val}</span>")
                ld = Gtk.Label(); ld.set_markup(f"<span font_desc='8' color='#888899'>{desc}</span>")
                item.pack_start(lv, False, False, 0); item.pack_start(ld, False, False, 0)
                stats_box.pack_start(item, False, False, 0)
        vbox.pack_start(stats_box, False, False, 0)

        vbox.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 1)

        # Nav Grid
        grid = Gtk.Grid()
        grid.set_column_spacing(9); grid.set_row_spacing(9); grid.set_halign(Gtk.Align.CENTER)
        nav = [
            ("dialog-information",       "Introduction",       "intro",      0, 0),
            ("starred",                  "Features",           "features",   1, 0),
            ("system-run",               "Getting Started",    "start",      2, 0),
            ("system-software-install",  "Install Software",   "sw",         0, 1),
            ("preferences-system",       "Driver Manager",     "driver",     1, 1),
            ("emblem-favorite",          "Recommendations",    "recs",       2, 1),
            ("computer",                 "About This System",  "about",      0, 2),
            ("input-keyboard",           "Keyboard Shortcuts", "shortcuts",  1, 2),
            ("security-high",            "Privacy & Security", "privacy",    2, 2),
            ("preferences-desktop",      "Theme & Appearance", "appearance", 0, 3),
            ("applications-development", "Developer Setup",    "devsetup",   1, 3),
        ]
        for icon_name, label, page, col, row in nav:
            btn = Gtk.Button(); btn.set_size_request(196, 52)
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=7); box.set_halign(Gtk.Align.CENTER)
            box.pack_start(self.icon(icon_name, Gtk.IconSize.BUTTON), False, False, 0)
            box.pack_start(Gtk.Label(label=label), False, False, 0)
            btn.add(box)
            if page == "sw": btn.connect("clicked", lambda w: subprocess.Popen(["gnome-software"]))
            elif page == "driver": btn.connect("clicked", lambda w: subprocess.Popen(["/usr/bin/shift-driver-manager"]))
            else: btn.connect("clicked", lambda w, p=page: self.stack.set_visible_child_name(p))
            grid.attach(btn, col, row, 1, 1)
        vbox.pack_start(grid, False, False, 2)

        # Tip of the Day
        tip_key, tip_text = random.choice(TIPS)
        tip_outer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        tip_outer.set_border_width(10); tip_outer.get_style_context().add_class("tip-box")
        tip_outer.set_halign(Gtk.Align.CENTER); tip_outer.set_size_request(660, -1)
        tip_outer.pack_start(self.icon("dialog-information", Gtk.IconSize.BUTTON), False, False, 0)
        tv = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        tit = Gtk.Label(); tit.set_markup("<span weight='bold' color='#03a1fe' font_desc='8'>TIP OF THE DAY</span>")
        tit.set_halign(Gtk.Align.START); tv.pack_start(tit, False, False, 0)
        tc = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        kl = Gtk.Label(label=tip_key); kl.get_style_context().add_class("tip-key")
        tc.pack_start(kl, False, False, 0)
        dl = Gtk.Label(label=tip_text); dl.set_halign(Gtk.Align.START); tc.pack_start(dl, True, True, 0)
        tv.pack_start(tc, False, False, 0); tip_outer.pack_start(tv, True, True, 0)
        vbox.pack_start(tip_outer, False, False, 0)

        outer.pack_start(vbox, True, True, 0)
        outer.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 0)

        bottom = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        bottom.set_border_width(12)
        chk = Gtk.CheckButton(label="Don\u2019t show this again on next login")
        chk.set_valign(Gtk.Align.CENTER); chk.connect("toggled", self.on_check_toggled)
        bottom.pack_start(chk, False, False, 0)
        soc = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        for lbl, ic, url in [("GitHub","github-alt","https://github.com/riray-hub"),
                              ("Website","applications-internet","https://shift-os.netlify.app"),
                              ("Email","mail-send","mailto:kharisdestian862@gmail.com"),
                              ("Telegram","user-available","https://t.me/shiftos"),
                              ("Discord","system-users","https://discord.gg/shiftos")]:
            b = Gtk.Button(); b.set_relief(Gtk.ReliefStyle.NONE); b.get_style_context().add_class("flat")
            b.set_tooltip_text(lbl)
            bb = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
            bb.pack_start(Gtk.Image.new_from_icon_name(ic, Gtk.IconSize.BUTTON), False, False, 0)
            ll = Gtk.Label(label=lbl); ll.get_style_context().add_class("dim-label"); bb.pack_start(ll, False, False, 0)
            b.add(bb); b.connect("clicked", lambda w, u=url: subprocess.Popen(["xdg-open", u]))
            soc.pack_start(b, False, False, 0)
        bottom.pack_end(soc, False, False, 0)
        outer.pack_end(bottom, False, False, 0)
        return outer

    def _get_health(self):
        items = []
        try:
            r = subprocess.run(["apt-get", "-s", "upgrade"], capture_output=True, text=True, timeout=4)
            n = sum(1 for l in r.stdout.splitlines() if l.startswith("Inst "))
            items.append(("software-update-available", "Updates", "Up to date \u2713" if n==0 else f"{n} pending \u26a0", n==0))
        except:
            items.append(("software-update-available", "Updates", "Unknown", False))
        try:
            r = subprocess.run(["ufw", "status"], capture_output=True, text=True, timeout=3)
            ok = "active" in r.stdout.lower()
            items.append(("security-high", "Firewall", "Active \u2713" if ok else "Inactive \u26a0", ok))
        except:
            items.append(("security-high", "Firewall", "Not found", False))
        try:
            subprocess.run(["ping", "-c1", "-W1", "8.8.8.8"], capture_output=True, timeout=3, check=True)
            items.append(("network-transmit-receive", "Network", "Online \u2713", True))
        except:
            items.append(("network-offline", "Network", "Offline", False))
        return items

    # ==========================================
    # INTRODUCTION
    # ==========================================
    def build_intro_page(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        vbox.set_border_width(40)
        t = Gtk.Label(); t.set_markup("<span font_desc='22' weight='bold'>Why Shift OS Exists</span>")
        t.set_halign(Gtk.Align.CENTER); vbox.pack_start(t, False, False, 0)
        tq = Gtk.Label(); tq.set_markup("<span style='italic' color='#777799'>\u201cAn OS that gets out of your way and lets you create.\u201d</span>")
        tq.set_halign(Gtk.Align.CENTER); vbox.pack_start(tq, False, False, 0)
        story = ("Shift OS was born from a simple frustration: most Linux distros either ship "
            "bloated with software you never asked for, or strip things down so much they\u2019re "
            "unusable out of the box.\n\nShift OS Harmonia hits the sweet spot. It\u2019s based on Ubuntu 24.04 LTS, runs a "
            "pure unmodified GNOME 46, uses Wayland by default, and includes only what a "
            "developer or creator actually needs \u2014 nothing more, nothing less.")
        lbl = Gtk.Label(label=story); lbl.set_line_wrap(True); lbl.set_max_width_chars(75)
        lbl.set_justify(Gtk.Justification.FILL); lbl.set_halign(Gtk.Align.CENTER)
        vbox.pack_start(lbl, False, False, 5)
        vbox.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 5)
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=30); hbox.set_halign(Gtk.Align.CENTER)
        vbox.pack_start(hbox, True, False, 10)
        for icon_name, p_title, p_desc in [
            ("system-lock-screen","Privacy First","Zero telemetry. Zero ads.\nYour machine, your data."),
            ("security-high","Rock-Solid Base","Ubuntu 24.04 LTS means 5 years\nof security updates & stability."),
            ("preferences-desktop-wallpaper","Designed to Inspire","Pure GNOME 46 \u2014 beautiful,\nconsistent, distraction-free."),
        ]:
            pv = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
            pv.set_valign(Gtk.Align.START); pv.set_size_request(180, -1)
            ic = self.icon(icon_name, Gtk.IconSize.DIALOG); ic.set_halign(Gtk.Align.CENTER)
            pv.pack_start(ic, False, False, 0)
            lt = Gtk.Label(); lt.set_markup(f"<b>{p_title}</b>"); lt.set_halign(Gtk.Align.CENTER)
            pv.pack_start(lt, False, False, 0)
            ld = Gtk.Label(label=p_desc); ld.set_justify(Gtk.Justification.CENTER); ld.set_halign(Gtk.Align.CENTER)
            pv.pack_start(ld, False, False, 0); hbox.pack_start(pv, True, False, 10)
        footer = Gtk.Label(); footer.set_markup("<span size='small' color='#aaaacc'>Shift OS Harmonia v26.03.1 \u00b7 Built by Kharis Destian Maulana (riray-hub)</span>")
        footer.set_halign(Gtk.Align.CENTER); vbox.pack_end(footer, False, False, 0)
        return self.wrap_page(vbox)

    # ==========================================
    # FEATURES
    # ==========================================
    def build_features_page(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12); vbox.set_border_width(30)
        t = Gtk.Label(); t.set_markup("<span font_desc='22' weight='bold'>What Makes Shift OS Different</span>")
        t.set_halign(Gtk.Align.CENTER); vbox.pack_start(t, False, False, 5)
        s = Gtk.Label(); s.set_markup("<span color='#666688'>Every decision was intentional. Here\u2019s what you get.</span>")
        s.set_halign(Gtk.Align.CENTER); vbox.pack_start(s, False, False, 5)
        features = [
            ("system-run","Blazing Fast Boot","Idles at ~700MB RAM. Boots in seconds. Optimized systemd services mean no hidden background processes eating your resources."),
            ("preferences-desktop","Pure GNOME 46","Unmodified, stock GNOME 46. No custom forks, no ugly patches \u2014 just the desktop as the GNOME team intended it."),
            ("video-display","Wayland Native","Runs Wayland by default for tear-free rendering, better HiDPI support, and improved security isolation. X11 fallback is always available."),
            ("system-software-install","Ubuntu Package Base","Full access to the entire Ubuntu/Debian package ecosystem. Millions of packages available via APT, plus Flatpak support out of the box."),
            ("security-high","Secure by Design","Ships with Linux Kernel 6.8, the latest Ubuntu security patches, and no unnecessary network services running by default."),
            ("applications-development","Creator-Ready","Godot, VS Code, Docker, Git, Python3 are pre-installed or one command away. Your workflow starts the moment you log in."),
        ]
        scrolled = Gtk.ScrolledWindow(); scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        lb = Gtk.ListBox(); lb.set_selection_mode(Gtk.SelectionMode.NONE)
        for icon_name, f_title, f_desc in features:
            row = Gtk.ListBoxRow()
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15); hbox.set_border_width(12)
            row.add(hbox)
            ic = self.icon(icon_name, Gtk.IconSize.LARGE_TOOLBAR); ic.set_valign(Gtk.Align.START); ic.set_margin_top(4)
            hbox.pack_start(ic, False, False, 0)
            vb = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3); hbox.pack_start(vb, True, True, 0)
            lt = Gtk.Label(); lt.set_markup(f"<b>{f_title}</b>"); lt.set_halign(Gtk.Align.START)
            vb.pack_start(lt, False, False, 0)
            ld = Gtk.Label(label=f_desc); ld.set_line_wrap(True); ld.set_max_width_chars(70)
            ld.set_halign(Gtk.Align.START); ld.set_xalign(0); vb.pack_start(ld, False, False, 0)
            lb.add(row)
        scrolled.add(lb); vbox.pack_start(scrolled, True, True, 5)
        return self.wrap_page(vbox)

    # ==========================================
    # GETTING STARTED
    # ==========================================
    def build_start_page(self):
        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0); outer.set_border_width(28)
        t = Gtk.Label(); t.set_markup("<span font_desc='22' weight='bold'>First Steps on Shift OS</span>")
        t.set_halign(Gtk.Align.CENTER); outer.pack_start(t, False, False, 5)
        s = Gtk.Label(); s.set_markup("<span color='#666688'>Check off each step as you complete it. Progress is saved.</span>")
        s.set_halign(Gtk.Align.CENTER); outer.pack_start(s, False, False, 5)
        self.start_progress = Gtk.ProgressBar(); self.start_progress.set_show_text(True)
        self.start_progress.set_margin_bottom(6); outer.pack_start(self.start_progress, False, False, 0)
        steps = [
            ("software-update-urgent","1. Update System","Get the latest security patches and package updates.","update-manager",None),
            ("preferences-system","2. Check Drivers","Install the best GPU and hardware drivers for your machine.","shift-driver-manager",None),
            ("gnome-control-center","3. System Settings","Configure display, network, users, accessibility, and more.","gnome-control-center",None),
            ("system-software-install","4. Install Software","Browse and install apps from the Shift App Center.","gnome-software",None),
            ("applications-engineering","5. GNOME Extensions","Browse, install, and manage GNOME Shell extensions locally.","extension-manager",None),
            ("document-save","6. Set up Timeshift","Create system snapshots so you can restore if something breaks.","timeshift-launcher",None),
            ("security-high","7. Enable Firewall","Enable UFW for basic network protection.","ufw",None),
        ]
        lb = Gtk.ListBox(); lb.set_selection_mode(Gtk.SelectionMode.NONE)
        for icon_name, s_title, s_desc, cmd, arg in steps:
            row = Gtk.ListBoxRow()
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12); hbox.set_border_width(10)
            row.add(hbox)
            check = Gtk.CheckButton(); check.set_valign(Gtk.Align.CENTER)
            if s_title in self.checklist_done: check.set_active(True)
            check.connect("toggled", self.on_step_toggled, s_title)
            self.step_checks[s_title] = check; hbox.pack_start(check, False, False, 0)
            ic = self.icon(icon_name, Gtk.IconSize.LARGE_TOOLBAR); ic.set_valign(Gtk.Align.CENTER)
            hbox.pack_start(ic, False, False, 0)
            vb = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2); hbox.pack_start(vb, True, True, 0)
            lt = Gtk.Label(); lt.set_markup(f"<b>{s_title}</b>"); lt.set_halign(Gtk.Align.START)
            vb.pack_start(lt, False, False, 0)
            ld = Gtk.Label(label=s_desc); ld.set_halign(Gtk.Align.START); ld.set_xalign(0)
            vb.pack_start(ld, False, False, 0)
            btn = Gtk.Button()
            ob = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
            ob.pack_start(Gtk.Label(label="Open"), False, False, 0)
            ob.pack_start(self.icon("go-next", Gtk.IconSize.BUTTON), False, False, 0)
            btn.add(ob); btn.set_valign(Gtk.Align.CENTER)
            if cmd == "ufw":
                btn.connect("clicked", lambda w: subprocess.Popen(["bash", "-c", "pkexec ufw enable && zenity --info --text='Firewall enabled!'"]))
            elif arg:
                btn.connect("clicked", lambda w, c=cmd, a=arg: subprocess.Popen([c, a]))
            else:
                btn.connect("clicked", lambda w, c=cmd: subprocess.Popen([c]))
            hbox.pack_end(btn, False, False, 0)
            lb.add(row)
        scrolled = Gtk.ScrolledWindow(); scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.add(lb); outer.pack_start(scrolled, True, True, 0)
        btn_reset = Gtk.Button(label="Reset Progress"); btn_reset.set_halign(Gtk.Align.END); btn_reset.set_margin_top(6)
        btn_reset.connect("clicked", self.on_reset_checklist); outer.pack_start(btn_reset, False, False, 0)
        self.update_progress_bar()
        return self.wrap_page(outer)

    def on_step_toggled(self, button, step_title):
        if button.get_active(): self.checklist_done.add(step_title)
        else: self.checklist_done.discard(step_title)
        save_checklist(self.checklist_done); self.update_progress_bar()

    def on_reset_checklist(self, button):
        self.checklist_done.clear(); save_checklist(self.checklist_done)
        for c in self.step_checks.values(): c.set_active(False)
        self.update_progress_bar()

    def update_progress_bar(self):
        total = len(self.step_checks)
        done = sum(1 for c in self.step_checks.values() if c.get_active())
        self.start_progress.set_fraction(done / total if total else 0)
        self.start_progress.set_text(f"{done} of {total} steps completed")

    # ==========================================
    # RECOMMENDATIONS
    # ==========================================
    def build_recs_page(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12); vbox.set_border_width(30)
        t = Gtk.Label(); t.set_markup("<span font_desc='22' weight='bold'>Power User Arsenal</span>")
        t.set_halign(Gtk.Align.CENTER); vbox.pack_start(t, False, False, 5)
        s = Gtk.Label(); s.set_markup("<span color='#666688'>Hand-picked apps. Click <b>Find</b> to search in Software Center.</span>")
        s.set_halign(Gtk.Align.CENTER); vbox.pack_start(s, False, False, 5)
        cats = {
            "Dev Tools": [
                ("applications-development","Docker","docker","Containerization for modern dev workflows."),
                ("applications-internet","Postman","postman","The industry standard for API testing."),
                ("applications-development","DBeaver","dbeaver","Universal database manager — SQL, NoSQL, everything."),
                ("applications-development","Android Studio","android-studio","Official IDE for Android development."),
                ("applications-development","IntelliJ IDEA","idea","Powerful IDE for Java, Kotlin, and more."),
            ],
            "Design & Media": [
                ("applications-graphics","Figma","figma-linux","UI/UX design and prototyping in the browser."),
                ("applications-graphics","GIMP","gimp","Full-featured image editor — free Photoshop alternative."),
                ("applications-graphics","Inkscape","inkscape","Professional vector graphics editor."),
                ("applications-multimedia","Kdenlive","kdenlive","Powerful open-source video editor."),
                ("applications-multimedia","OBS Studio","obs","Screen recording and live streaming."),
            ],
            "Games": [
                ("applications-games","Steam","steam","The world's largest PC gaming platform with Proton."),
                ("applications-games","Lutris","lutris","Open gaming platform — run Windows games on Linux."),
                ("applications-games","Heroic Games","heroic","Open-source Epic & GOG launcher."),
                ("applications-games","ProtonUp-Qt","protonup-qt","Manage Proton-GE and Wine versions."),
                ("applications-games","Bottles","bottles","Run Windows software in isolated environments."),
            ],
            "Productivity": [
                ("applications-office","LibreOffice","libreoffice","Full office suite — Writer, Calc, Impress."),
                ("applications-office","Obsidian","obsidian","Markdown-based knowledge base and note-taking."),
                ("applications-internet","Notion","notion","All-in-one workspace for notes, docs, and projects."),
                ("applications-internet","Thunderbird","thunderbird","Powerful email and calendar client by Mozilla."),
                ("applications-office","Drawio","drawio","Diagram and flowchart editor — great for planning."),
            ],
            "Communication": [
                ("applications-internet","Discord","discord","Chat, voice, and screen share with your team."),
                ("applications-internet","Slack","slack","Team messaging and collaboration platform."),
                ("applications-internet","Zoom","zoom","Video meetings and webinars."),
            ],
            "Security": [
                ("network-wired","Wireshark","wireshark","Network protocol analyzer for security experts."),
                ("dialog-password","Bitwarden","bitwarden","Open-source password manager."),
            ],
        }
        nb = Gtk.Notebook(); nb.set_tab_pos(Gtk.PositionType.TOP); vbox.pack_start(nb, True, True, 5)
        for cat_label, apps in cats.items():
            scrolled = Gtk.ScrolledWindow(); scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
            lb = Gtk.ListBox(); lb.set_selection_mode(Gtk.SelectionMode.NONE)
            for icon_name, name, cmd, dsc in apps:
                row = Gtk.ListBoxRow()
                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12); hbox.set_border_width(10)
                row.add(hbox)
                ic = self.icon(icon_name, Gtk.IconSize.LARGE_TOOLBAR); ic.set_valign(Gtk.Align.CENTER)
                hbox.pack_start(ic, False, False, 0)
                vb = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3); hbox.pack_start(vb, True, True, 0)
                ln = Gtk.Label(); ln.set_markup(f"<b>{name}</b>"); ln.set_halign(Gtk.Align.START)
                vb.pack_start(ln, False, False, 0)
                ld = Gtk.Label(label=dsc); ld.set_halign(Gtk.Align.START); ld.set_xalign(0)
                vb.pack_start(ld, False, False, 0)
                installed = is_installed(cmd)
                badge = Gtk.Label(label="\u2713 Installed" if installed else "Not Installed")
                badge.get_style_context().add_class("badge-installed" if installed else "badge-not-installed")
                badge.set_valign(Gtk.Align.CENTER); hbox.pack_start(badge, False, False, 0)
                btn_f = Gtk.Button(label="Find"); btn_f.set_valign(Gtk.Align.CENTER)
                btn_f.connect("clicked", lambda w, n=name: subprocess.Popen(["gnome-software", "--search", n]))
                hbox.pack_end(btn_f, False, False, 0); lb.add(row)
            scrolled.add(lb); nb.append_page(scrolled, Gtk.Label(label=cat_label))
        return self.wrap_page(vbox)

    # ==========================================
    # ABOUT THIS SYSTEM
    # ==========================================
    def build_about_page(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14); vbox.set_border_width(34)
        t = Gtk.Label(); t.set_markup("<span font_desc='22' weight='bold'>About This System</span>")
        t.set_halign(Gtk.Align.CENTER); vbox.pack_start(t, False, False, 0)
        s = Gtk.Label(); s.set_markup("<span color='#666688'>Hardware and system information detected on this machine.</span>")
        s.set_halign(Gtk.Align.CENTER); vbox.pack_start(s, False, False, 0)
        info = get_system_info()
        rows = [
            ("computer","OS","Shift OS Harmonia v26.03.1"),
            ("applications-system","Kernel",info.get("kernel","?")),
            ("cpu","Architecture",info.get("arch","?")),
            ("processor","CPU",info.get("cpu","?")),
            ("memory","RAM",info.get("ram","?")),
            ("video-display","GPU",info.get("gpu","?")),
            ("drive-harddisk","Disk Total",info.get("disk_total","?")),
            ("drive-harddisk","Disk Free",info.get("disk_free","?")),
            ("network-server","Hostname",info.get("hostname","?")),
            ("preferences-desktop","Desktop","GNOME 46 (Wayland)"),
        ]
        specs = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        specs.set_halign(Gtk.Align.CENTER); specs.set_size_request(660, -1)
        for icon_name, key, val in rows:
            rb = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=14); rb.set_border_width(9)
            ic = self.icon(icon_name, Gtk.IconSize.BUTTON); ic.set_valign(Gtk.Align.CENTER)
            rb.pack_start(ic, False, False, 0)
            kl = Gtk.Label(); kl.set_markup(f"<span color='#888899' font_desc='9' weight='bold'>{key.upper()}</span>")
            kl.set_size_request(110, -1); kl.set_halign(Gtk.Align.START); rb.pack_start(kl, False, False, 0)
            vl = Gtk.Label(label=val); vl.set_halign(Gtk.Align.START); vl.set_xalign(0); vl.set_ellipsize(3)
            rb.pack_start(vl, True, True, 0)
            specs.pack_start(rb, False, False, 0)
            specs.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 0)
        scrolled = Gtk.ScrolledWindow(); scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.add(specs); vbox.pack_start(scrolled, True, True, 0)
        btn_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12); btn_row.set_halign(Gtk.Align.CENTER)
        btn_copy = Gtk.Button(label="Copy System Info")
        btn_copy.connect("clicked", lambda w: Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD).set_text(
            "\n".join([f"{k}: {v}" for _, k, v in rows]), -1))
        btn_row.pack_start(btn_copy, False, False, 0)
        self.bench_btn = Gtk.Button(label="\u25b6 Run CPU Benchmark")
        self.bench_btn.get_style_context().add_class("suggested-action")
        self.bench_btn.connect("clicked", self.run_benchmark); btn_row.pack_start(self.bench_btn, False, False, 0)
        self.bench_result = Gtk.Label(label=""); self.bench_result.set_halign(Gtk.Align.CENTER)
        btn_row.pack_start(self.bench_result, False, False, 0)
        vbox.pack_start(btn_row, False, False, 0)
        return self.wrap_page(vbox)

    def run_benchmark(self, button):
        self.bench_btn.set_sensitive(False)
        self.bench_result.set_markup("<span color='#888899'>Running benchmark\u2026</span>")
        def do_bench():
            import time, math
            try:
                t0 = time.time()
                x = 0.0
                for i in range(1, 3_000_001): x += math.sqrt(i)
                elapsed = time.time() - t0
                score = int(3_000_000 / elapsed)
                GLib.idle_add(self._bench_done, f"Score: {score:,} ops/sec  ({elapsed:.2f}s)")
            except Exception as e:
                GLib.idle_add(self._bench_done, f"Error: {e}")
        threading.Thread(target=do_bench, daemon=True).start()

    def _bench_done(self, result):
        self.bench_result.set_markup(f"<b><span color='#03a1fe'>{result}</span></b>")
        self.bench_btn.set_sensitive(True)

    # ==========================================
    # KEYBOARD SHORTCUTS
    # ==========================================
    def build_shortcuts_page(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12); vbox.set_border_width(30)
        t = Gtk.Label(); t.set_markup("<span font_desc='22' weight='bold'>Keyboard Shortcuts</span>")
        t.set_halign(Gtk.Align.CENTER); vbox.pack_start(t, False, False, 5)
        search_entry = Gtk.SearchEntry(); search_entry.set_placeholder_text("Search shortcuts\u2026")
        search_entry.set_size_request(380, -1); search_entry.set_halign(Gtk.Align.CENTER)
        vbox.pack_start(search_entry, False, False, 0)
        self._shortcut_rows = []
        all_shortcuts = {
            "Navigation": [
                ("Super","Open Activities overview"),("Super + A","Open Applications grid"),
                ("Super + Tab","Switch workspaces"),("Super + D","Show desktop"),
                ("Super + Left/Right","Snap window to half screen"),("Super + Up","Maximize window"),
                ("Super + Down","Restore window"),("Super + H","Hide / minimize window"),
            ],
            "System": [
                ("Super + L","Lock screen"),("Alt + F4","Close current window"),
                ("Ctrl + Alt + T","Open Terminal"),("Super + V","Open notification panel"),
                ("Ctrl + Shift + Alt + R","Start/stop screen recording"),
                ("Print Screen","Take a screenshot"),("Alt + Print Screen","Screenshot of active window"),
            ],
            "Text & Editing": [
                ("Ctrl + C","Copy"),("Ctrl + V","Paste"),("Ctrl + X","Cut"),
                ("Ctrl + Z","Undo"),("Ctrl + Shift + Z","Redo"),
                ("Ctrl + A","Select all"),("Ctrl + F","Find"),("Ctrl + S","Save"),
            ],
            "Terminal": [
                ("Ctrl + C","Interrupt running command"),("Ctrl + Z","Suspend process"),
                ("Ctrl + D","Close terminal / logout"),("Ctrl + L","Clear screen"),
                ("Ctrl + R","Search command history"),("Tab","Autocomplete"),
                ("Up / Down","Navigate history"),("Ctrl + Shift + C/V","Copy / Paste in terminal"),
            ],
        }
        nb = Gtk.Notebook(); nb.set_tab_pos(Gtk.PositionType.TOP)
        for cat_label, shortcuts in all_shortcuts.items():
            scrolled = Gtk.ScrolledWindow(); scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
            lb = Gtk.ListBox(); lb.set_selection_mode(Gtk.SelectionMode.NONE)
            for keys, desc in shortcuts:
                row = Gtk.ListBoxRow()
                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16); hbox.set_border_width(10)
                row.add(hbox)
                kl = Gtk.Label(label=keys); kl.get_style_context().add_class("shortcut-key")
                kl.set_size_request(200, -1); kl.set_halign(Gtk.Align.START); hbox.pack_start(kl, False, False, 0)
                dl = Gtk.Label(label=desc); dl.set_halign(Gtk.Align.START); dl.set_xalign(0)
                hbox.pack_start(dl, True, True, 0)
                lb.add(row); self._shortcut_rows.append((row, keys.lower(), desc.lower()))
            scrolled.add(lb); nb.append_page(scrolled, Gtk.Label(label=cat_label))
        def on_search(entry):
            q = entry.get_text().lower().strip()
            for row, keys, desc in self._shortcut_rows:
                if not q or q in keys or q in desc: row.show()
                else: row.hide()
        search_entry.connect("search-changed", on_search)
        vbox.pack_start(nb, True, True, 5)
        return self.wrap_page(vbox)

    # ==========================================
    # PRIVACY & SECURITY
    # ==========================================
    def build_privacy_page(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14); vbox.set_border_width(34)
        t = Gtk.Label(); t.set_markup("<span font_desc='22' weight='bold'>Privacy & Security</span>")
        t.set_halign(Gtk.Align.CENTER); vbox.pack_start(t, False, False, 0)
        s = Gtk.Label(); s.set_markup("<span color='#666688'>Quick shortcuts and tips to keep your system safe.</span>")
        s.set_halign(Gtk.Align.CENTER); vbox.pack_start(s, False, False, 5)
        scrolled = Gtk.ScrolledWindow(); scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        inner = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8); inner.set_border_width(4)
        privacy_items = [
            ("security-high","Firewall (UFW)","Block unauthorized network access.","ufw",None),
            ("preferences-system","GNOME Privacy Settings","Manage location, microphone, camera access.","gnome-control-center","privacy"),
            ("system-lock-screen","Screen Lock Settings","Configure auto-lock timeout.","gnome-control-center","lock"),
            ("password-storage","GNOME Keyring","Manage stored passwords and secrets.","seahorse",None),
            ("system-search","Disk Usage Analyzer","Visualize disk usage and find large files.","baobab",None),
        ]
        for icon_name, label, desc, cmd, arg in privacy_items:
            rb = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=14); rb.set_border_width(12)
            rb.get_style_context().add_class("stats-bar")
            ic = self.icon(icon_name, Gtk.IconSize.LARGE_TOOLBAR); ic.set_valign(Gtk.Align.CENTER)
            rb.pack_start(ic, False, False, 0)
            vb = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2); rb.pack_start(vb, True, True, 0)
            lt = Gtk.Label(); lt.set_markup(f"<b>{label}</b>"); lt.set_halign(Gtk.Align.START)
            vb.pack_start(lt, False, False, 0)
            ld = Gtk.Label(label=desc); ld.set_halign(Gtk.Align.START); ld.set_xalign(0); vb.pack_start(ld, False, False, 0)
            btn = Gtk.Button(label="Open" if cmd != "ufw" else "Enable Firewall")
            btn.set_valign(Gtk.Align.CENTER)
            if cmd == "ufw":
                btn.connect("clicked", lambda w: subprocess.Popen(["bash", "-c", "pkexec ufw enable && zenity --info --text='Firewall enabled!'"]))
            elif arg:
                btn.connect("clicked", lambda w, c=cmd, a=arg: subprocess.Popen([c, a]))
            else:
                btn.connect("clicked", lambda w, c=cmd: subprocess.Popen([c]))
            rb.pack_end(btn, False, False, 0); inner.pack_start(rb, False, False, 0)
        inner.pack_start(self.section_label("Security Tips"), False, False, 0)
        for tip in [
            "Use strong, unique passwords — Bitwarden is free and open-source.",
            "Enable full-disk encryption (LUKS) during installation for maximum privacy.",
            "Regularly run: sudo apt update && sudo apt upgrade -y",
            "Only install software from trusted sources (apt, Flatpak, official .deb).",
            "Review GNOME Privacy Settings to control app permissions.",
        ]:
            tb = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8); tb.set_border_width(3)
            tb.pack_start(Gtk.Label(label="\u2022"), False, False, 0)
            tl = Gtk.Label(label=tip); tl.set_halign(Gtk.Align.START); tl.set_xalign(0)
            tl.set_line_wrap(True); tl.set_max_width_chars(70); tb.pack_start(tl, True, True, 0)
            inner.pack_start(tb, False, False, 0)
        scrolled.add(inner); vbox.pack_start(scrolled, True, True, 0)
        return self.wrap_page(vbox)

    # ==========================================
    # THEME & APPEARANCE
    # ==========================================
    def build_appearance_page(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14); vbox.set_border_width(34)
        t = Gtk.Label(); t.set_markup("<span font_desc='22' weight='bold'>Theme & Appearance</span>")
        t.set_halign(Gtk.Align.CENTER); vbox.pack_start(t, False, False, 0)
        s = Gtk.Label(); s.set_markup("<span color='#666688'>Customize how Shift OS looks and feels.</span>")
        s.set_halign(Gtk.Align.CENTER); vbox.pack_start(s, False, False, 5)
        scrolled = Gtk.ScrolledWindow(); scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        inner = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10); inner.set_border_width(4)
        for icon_name, label, desc, cmd, arg in [
            ("preferences-desktop-wallpaper","Wallpaper","Change your desktop background.","gnome-control-center","background"),
            ("preferences-desktop-theme","Color Scheme","Switch between Light, Dark, or Auto modes.","gnome-control-center","color"),
            ("preferences-desktop-font","Fonts","Set system fonts, size, and hinting.","gnome-tweaks",None),
            ("preferences-desktop","GNOME Tweaks","Advanced tweaks: icons, window buttons, animations.","gnome-tweaks",None),
            ("applications-graphics","GNOME Extensions","Install and manage Shell extensions.","xdg-open","https://extensions.gnome.org"),
            ("video-display","Display Settings","Resolution, refresh rate, night light, HiDPI.","gnome-control-center","display"),
            ("input-mouse","Mouse & Touchpad","Speed, natural scroll, gestures.","gnome-control-center","mouse"),
        ]:
            rb = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=14); rb.set_border_width(12)
            rb.get_style_context().add_class("stats-bar")
            ic = self.icon(icon_name, Gtk.IconSize.LARGE_TOOLBAR); ic.set_valign(Gtk.Align.CENTER)
            rb.pack_start(ic, False, False, 0)
            vb = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2); rb.pack_start(vb, True, True, 0)
            lt = Gtk.Label(); lt.set_markup(f"<b>{label}</b>"); lt.set_halign(Gtk.Align.START)
            vb.pack_start(lt, False, False, 0)
            ld = Gtk.Label(label=desc); ld.set_halign(Gtk.Align.START); ld.set_xalign(0); vb.pack_start(ld, False, False, 0)
            btn = Gtk.Button(label="Open"); btn.set_valign(Gtk.Align.CENTER)
            if arg and arg.startswith("http"): btn.connect("clicked", lambda w, c=cmd, a=arg: subprocess.Popen([c, a]))
            elif arg: btn.connect("clicked", lambda w, c=cmd, a=arg: subprocess.Popen([c, a]))
            else: btn.connect("clicked", lambda w, c=cmd: subprocess.Popen([c]))
            rb.pack_end(btn, False, False, 0); inner.pack_start(rb, False, False, 0)
        inner.pack_start(self.section_label("Recommended GNOME Extensions"), False, False, 0)
        for ext_name, ext_desc in [
            ("Dash to Dock","A dock for quick app launching, like macOS or Windows taskbar."),
            ("Blur My Shell","Beautiful blur effect on the shell top bar and overview."),
            ("GSConnect","Connect your Android phone — share files, notifications, clipboard."),
            ("Clipboard Indicator","Keep a clipboard history — never lose copied text again."),
            ("TopHat","Live CPU, RAM, and network usage in the top bar."),
        ]:
            eb = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10); eb.set_border_width(5)
            nl = Gtk.Label(); nl.set_markup(f"<b>{ext_name}</b>"); nl.set_size_request(160, -1); nl.set_halign(Gtk.Align.START)
            eb.pack_start(nl, False, False, 0)
            dl = Gtk.Label(label=ext_desc); dl.set_halign(Gtk.Align.START); dl.set_xalign(0)
            dl.set_line_wrap(True); eb.pack_start(dl, True, True, 0)
            inner.pack_start(eb, False, False, 0)
        scrolled.add(inner); vbox.pack_start(scrolled, True, True, 0)
        return self.wrap_page(vbox)

    # ==========================================
    # DEVELOPER SETUP WIZARD
    # ==========================================
    def build_devsetup_page(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12); vbox.set_border_width(34)
        t = Gtk.Label(); t.set_markup("<span font_desc='22' weight='bold'>Developer Setup Wizard</span>")
        t.set_halign(Gtk.Align.CENTER); vbox.pack_start(t, False, False, 0)
        s = Gtk.Label(); s.set_markup("<span color='#666688'>Select your tech stack. We\u2019ll generate the install script.</span>")
        s.set_halign(Gtk.Align.CENTER); vbox.pack_start(s, False, False, 5)
        stacks = {
            "Languages": [
                ("Python 3 + pip","python3 python3-pip python3-venv"),
                ("Node.js + npm","nodejs npm"),("Go","golang"),
                ("Rust","rustup"),("Java (JDK 17)","openjdk-17-jdk"),
                ("PHP","php php-cli"),("Ruby","ruby ruby-dev"),
            ],
            "Tools & Runtimes": [
                ("Git","git"),("Docker","docker.io docker-compose"),
                ("VS Code","code"),("Vim / Neovim","neovim"),
                ("Make / CMake","make cmake"),("curl + wget","curl wget"),("zsh","zsh"),
            ],
            "Databases": [
                ("PostgreSQL","postgresql postgresql-client"),("MySQL","mysql-server"),
                ("SQLite 3","sqlite3"),("Redis","redis-server"),("MongoDB","mongodb"),
            ],
        }
        self.dev_checks = {}
        nb = Gtk.Notebook(); nb.set_tab_pos(Gtk.PositionType.LEFT)
        for cat, items in stacks.items():
            inner = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2); inner.set_border_width(12)
            for label, pkgs in items:
                cb = Gtk.CheckButton(label=label)
                installed = any(is_installed(p.split()[0]) for p in pkgs.split())
                if installed: cb.set_label(f"{label}  \u2713"); cb.set_active(True); cb.set_sensitive(False)
                cb.connect("toggled", lambda w: self.generate_dev_script(None))
                self.dev_checks[label] = (cb, pkgs); inner.pack_start(cb, False, False, 0)
            sc = Gtk.ScrolledWindow(); sc.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
            sc.add(inner); nb.append_page(sc, Gtk.Label(label=cat))
        vbox.pack_start(nb, True, True, 0)
        self.dev_script_buf = Gtk.TextBuffer()
        tv = Gtk.TextView(buffer=self.dev_script_buf); tv.set_editable(False); tv.set_monospace(True)
        tv.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        dsc = Gtk.ScrolledWindow(); dsc.set_size_request(-1, 90)
        dsc.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        dsc.add(tv); vbox.pack_start(dsc, False, False, 0)
        btn_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10); btn_row.set_halign(Gtk.Align.CENTER)
        bg = Gtk.Button(label="Generate Script"); bg.get_style_context().add_class("suggested-action")
        bg.connect("clicked", self.generate_dev_script); btn_row.pack_start(bg, False, False, 0)
        bc = Gtk.Button(label="Copy Script")
        bc.connect("clicked", lambda w: Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD).set_text(
            self.dev_script_buf.get_text(self.dev_script_buf.get_start_iter(),
            self.dev_script_buf.get_end_iter(), True), -1))
        btn_row.pack_start(bc, False, False, 0)
        br = Gtk.Button(label="Run in Terminal"); br.connect("clicked", self.run_dev_script)
        btn_row.pack_start(br, False, False, 0)
        vbox.pack_start(btn_row, False, False, 0)
        self.generate_dev_script(None)
        return self.wrap_page(vbox)

    def generate_dev_script(self, button):
        selected = [pkgs for label, (cb, pkgs) in self.dev_checks.items() if cb.get_active() and cb.get_sensitive()]
        if selected:
            script = "#!/bin/bash\n# Shift OS Developer Setup Script\n\nsudo apt update\n"
            script += "sudo apt install -y " + " ".join(selected) + "\n"
            if any("zsh" in p for p in selected):
                script += '\n# Install oh-my-zsh\nsh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"\n'
            if any("rustup" in p for p in selected):
                script += "\n# Install Rust via rustup\ncurl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh\n"
            script += "\necho 'Done! Restart your terminal.'\n"
        else:
            script = "# Select packages from the tabs above, then click Generate."
        self.dev_script_buf.set_text(script)

    def run_dev_script(self, button):
        script = self.dev_script_buf.get_text(self.dev_script_buf.get_start_iter(),
            self.dev_script_buf.get_end_iter(), True)
        if script.startswith("#!"):
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as f:
                f.write(script); tmp = f.name
            os.chmod(tmp, 0o755)
            try: subprocess.Popen(["gnome-terminal", "--", "bash", tmp])
            except: subprocess.Popen(["bash", tmp])

    def on_check_toggled(self, button):
        if button.get_active():
            os.makedirs(os.path.dirname(FLAG_FILE), exist_ok=True)
            open(FLAG_FILE, 'a').close()
        else:
            if os.path.exists(FLAG_FILE): os.remove(FLAG_FILE)


win = ShiftWelcome()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
