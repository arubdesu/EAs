#!/usr/bin/python
"""Given a whitelist of privHelpers from legit software, report on stuff to investigate."""
#pylint: disable=invalid-name


import os
import glob


ALLOWED = ["com.barebones.authd",
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


FOUND_PRIVS = glob.glob('/Library/PrivilegedHelperTools/*')

TO_INVESTIGATE = []

for priv in FOUND_PRIVS:
    if os.path.basename(priv) not in ALLOWED:
        TO_INVESTIGATE.append(priv)

if TO_INVESTIGATE:
    RESULT = "Not in whitelist, investigate: " + "\n".join(*[TO_INVESTIGATE])
else:
    RESULT = "Nothing to see here."

print "<result>%s</result>" % RESULT
