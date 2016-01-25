#!/usr/bin/python
# Culled from https://gist.github.com/arubdesu/05b4172890450fa2d9e6
"""Given a list of FW models and Thunderstrike patched FW versions,
report on whether a machine has been patched."""
#pylint: disable=invalid-name


import subprocess
import plistlib


FIRMWARE_DICT = {"IM111": "B04",
                 "IM112": "B03",
                 "IM121": "B23",
                 "IM131": "B09",
                 "IM141": "B12",
                 "IM142": "B12",
                 "IM143": "B12",
                 "IM144": "B12",
                 "IM151": "B05",
                 "IM161": "B02",
                 "IM171": "B05",
                 "MB81": "B10",
                 "MBA41": "B14",
                 "MBA51": "B04",
                 "MBA61": "B21",
                 "MBA71": "B09",
                 "MBP101": "B0A",
                 "MBP102": "B0A",
                 "MBP111": "B16",
                 "MBP112": "B16",
                 "MBP114": "B07",
                 "MBP121": "B15",
                 "MBP61": "B11",
                 "MBP81": "B2C",
                 "MBP91": "B0C",
                 "MM51": "B14",
                 "MM61": "B0A",
                 "MM71": "B06",
                 "MP61": "B16"}


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
