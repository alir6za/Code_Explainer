#!/usr/bin/env python3
import subprocess
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from ui.code_explainer_window import CodeExplainerWindow

def main():
    try:
        selected_text = subprocess.check_output(
            "xclip -o -selection primary", shell=True
        ).decode("utf-8").strip()
    except subprocess.CalledProcessError:
        selected_text = ""
    if not selected_text:
        subprocess.run([
            "notify-send",
            "-u", "normal",
            "-t", "2000",
            "Code Explainer",
            "No code selected!"
        ])
        return
    if len(selected_text) > 5000:
        subprocess.run([
            "notify-send",
            "-u", "normal",
            "-t", "3000",
            "Code Explainer",
            "The selected code is too long!"
        ])
        return
    win = CodeExplainerWindow(selected_text)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()