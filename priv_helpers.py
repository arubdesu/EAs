#!/usr/bin/python
"""Given a whitelist of privHelpers from legit software, report on stuff to investigate."""


import os
import glob


def main():
    """gimme some main"""
    allowed = ["com.barebones.authd",
               "com.bombich.ccc",
               "com.bombich.ccchelper",
               "com.box.sync.bootstrapper",
               "com.box.sync.iconhelper",
               "com.github.GitHub.GHInstallCLI",# old?
               "com.logmein.join.me.update-helper",
               "com.macromates.auth_server",# old?
               "com.microsoft.office.licensing.helper",
               "com.microsoft.office.licensingV2.helper",
               "com.oracle.java.JavaUpdateHelper",
               "com.tunnelbear.mac.tbeard",
               "com.teamviewer.Helper",
               "fr.whitebox.packages",
               "Google Drive Icon Helper"]# srsly, Google?


    found_privs = glob.glob('/Library/PrivilegedHelperTools/*')

    to_investigate = []

    for priv in found_privs:
        if os.path.basename(priv) not in allowed:
            to_investigate.append(priv)

    if to_investigate:
        result = "Not in whitelist, investigate: \n" + "\n".join(*[to_investigate])
    else:
        result = "Nothing to see here."

    print "<result>%s</result>" % result

if __name__ == '__main__':
    main()
