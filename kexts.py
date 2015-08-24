#!/usr/bin/python
"""Check osquery output against whitelisted kexts."""


import json
import os
import subprocess
import sys


def osquery_check():
    """bail early if osquery not installed"""
    if not os.path.exists('/usr/local/bin/osqueryi'):
        result = 'wha? no osquery? bro, do you even lift?'
        print "<result>%s</result>" % result
        sys.exit(0)

def main():
    """gimme some main"""
    osquery_check()

    allowed = ["/Library/Application Support/VirtualBox/VBoxDrv.kext",
               "/Library/Application Support/VirtualBox/VBoxNetAdp.kext",
               "/Library/Application Support/VirtualBox/VBoxNetFlt.kext",
               "/Library/Application Support/VirtualBox/VBoxUSB.kext",
               "/System/Library/Extensions/dne.kext",
               "/System/Library/Extensions/dniregistry.kext",
               "/System/Library/Extensions/net6im.kext",]

    cmd = ['/usr/local/bin/osqueryi', '--json', 'select name, path from kernel_extensions']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    out = proc.communicate()[0]
    try:
        jsony_dictlist = json.loads(out)
    except ValueError:
        print ValueError
    just_non_apples = []
    for each in jsony_dictlist:
        if each['name'].startswith("com.apple"):
            pass
        else:
            just_non_apples.append(each['path'])

    to_investigate = []

    for kext in just_non_apples:
        if kext not in allowed:
            if repr(kext) != "u''":
                to_investigate.append(kext)

    if to_investigate:
        result = "Kext not in whitelist, investigate:\n" + "\n".join(*[to_investigate])
    else:
        result = "No non-standard kexts installed."

    print "<result>%s</result>" % result

if __name__ == '__main__':
    main()
