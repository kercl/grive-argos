#!/usr/bin/env python3

import sys
import os
import time

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import grive_argos.config

class GnomeShellMenu:
  def __init__(self):
    self._menu = [
      ("Synchronize folder", "view-refresh-symbolic",     "synchronize", "true"),
      (None,                 None,                        None,          None),
      ("Push changes",       "network-transmit-symbolic", "push",        "true"),
      ("Pull changes",       "network-receive-symbolic",  "pull",        "true"),
      (None,                 None,                        None,          None),
      ("Settings",           "system-run-symbolic",       "settings",    "false")
    ]
    
    self._main_icon = "fa_google_logo-symbolic"
    self.build_menu()
  
  def build_menu(self):
    cfg = grive_argos.config.GriveArgosConfig()
    
    print(f"| iconName={self._main_icon}\n---")
    
    for title,icon,callback,show_term in self._menu:
      if title is None:
        print("---")
        continue
      
      callback = cfg.script(callback)
      print(f"{title} | iconName={icon} terminal={show_term} bash='{callback}; exit'")

class SettingsDialog:
  def __init__(self):
    cfg = grive_argos.config.GriveArgosConfig()
    
    builder = Gtk.Builder()
    builder.add_from_file(cfg.ui)
    
    builder.connect_signals(self)

    cfg = grive_argos.config.GriveArgosConfig().read()
    builder.get_object("grive_folder_chooser").set_filename(cfg["google-drive-folder"])
    builder.get_object("dry_run_switch").set_state(cfg["dry-run"])
    

    window = builder.get_object("settings")
    window.show_all()
    Gtk.main()
  
  def folder_set(self, widget):
    cfg = grive_argos.config.GriveArgosConfig()
    cfg["google-drive-folder"] = widget.get_filename()
  
  def mode_change(self, widget, state):
    cfg = grive_argos.config.GriveArgosConfig()
    if state:
      cfg["dry-run"] = True
    else:
      cfg["dry-run"] = False
  
  def on_destroy(self, *args):
    Gtk.main_quit()

class GriveCallback:
  def __init__(self, name):
    self.call(name)
  
  def call(self, name):
    getattr(self, name)()
  
  def grive_and_notify(self, params):
    cfg = grive_argos.config.GriveArgosConfig().read()
    folder = cfg["google-drive-folder"]
    
    retcode = os.system(f"cd '{folder}' && grive -P {params}")
    
    notify_success = "Synchronizing with Google Drive finished successfully"
    notify_failure = f"Synchronization failed: error code {retcode}"
    notify_icon = "google"
    
    if retcode:
      os.system(f"notify-send -i {notify_icon} '{notify_failure}'")
      input("Press Enter to continue...")
    else:
      os.system(f"notify-send -i {notify_icon} '{notify_success}'")
      if cfg["dry-run"]:
        input("Press Enter to continue...")
      else:
        time.sleep(3)
  
  @property
  def configured_params(self):
    cfg = grive_argos.config.GriveArgosConfig().read()
    
    if cfg["dry-run"]:
      return "--dry-run"
    else:
      return ""
  
  def synchronize(self):
    self.grive_and_notify(self.configured_params)
  
  def pull(self):
    self.grive_and_notify(self.configured_params + " -f")
  
  def push(self):
    self.grive_and_notify(self.configured_params + " -u")
  
  def settings(self):
    SettingsDialog()
    
  
def main(argv):
  if len(argv) == 1:
    GnomeShellMenu()
  else:
    GriveCallback(argv[1])

if __name__ == "__main__":
    main(sys.argv)
