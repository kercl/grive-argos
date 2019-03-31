import os
import sys
import json

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

class GriveArgosConfig:
  def read(self):
    with open(f"{SCRIPT_PATH}/config.json") as f:
      return json.load(f)

  def __getitem__(self, key):
    with open(f"{SCRIPT_PATH}/config.json") as f:
      c = json.load(f)
    
    return c[key]
  
  def __setitem__(self, key, data):
    with open(f"{SCRIPT_PATH}/config.json") as f:
      c = json.load(f)
    
    c[key] = data
    
    with open(f"{SCRIPT_PATH}/config.json", "w") as f:
      json.dump(c, f)
  
  @property
  def ui(self):
    return f"{SCRIPT_PATH}/ui.glade"
  
  def script(self, name):
    return f"python3 {SCRIPT_PATH}/../grive-argos.py {name}"

