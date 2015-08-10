#!/usr/bin/python
# Culled from https://gist.github.com/arubdesu/05b4172890450fa2d9e6
"""Given a list of FW models and Thunderstrike patched FW versions,
report on whether a machine has been patched."""
#pylint: disable=invalid-name


import subprocess
import plistlib


FIRMWARE_DICT = {"MM51":"B12",
                 "MM61":"B08",
                 "MM71":"B03",
                 "MP61":"B15",
                 "MB81":"B06",
                 "IM121": "B21",
                 "IM131": "B08",
                 "IM141": "B11",
                 "IM142": "B11",
                 "IM143": "B11",
                 "IM144": "B10",
                 "IM151": "B03",
                 "MBP81": "B2A",
                 "MBP91": "B0B",
                 "MBA41": "B12",
                 "MBA51": "B03",
                 "MBA61": "B19",
                 "MBA71": "B06",
                 "MBP101": "B09",
                 "MBP102": "B08",
                 "MBP111": "B15",
                 "MBP112": "B15",
                 "MBP114": "B04",
                 "MBP121": "B07"}


CMD = ["/usr/sbin/system_profiler", "SPHardwareDataType", "-xml"]
HDWE_STDOUT = subprocess.check_output(CMD)

OUTPUT_PLIST = plistlib.readPlistFromString(HDWE_STDOUT)
FULL_ROM = OUTPUT_PLIST[0]["_items"][0]["boot_rom_version"]
(hdwe_code, _, current_fw_vers) = FULL_ROM.split(".")

PATCHED_VERS = FIRMWARE_DICT.get(hdwe_code)

if PATCHED_VERS:
    if current_fw_vers >= PATCHED_VERS:
        RESULT = "Patched"
    else:
        RESULT = ("Unpatched current version: %s required version: %s" %
                  (current_fw_vers, PATCHED_VERS))
else:
    RESULT = "NotPatchable"

print "<result>%s</result>" % RESULT
