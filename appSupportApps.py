#!/usr/bin/python
"""Given a whitelist of legit helper apps, report on stuff to investigate."""
#pylint: disable=invalid-name


import fnmatch
import glob
import os


ALLOWED = ["asannotation2.app",
           "aswatcher.app",
           "atmsupload.app",
           "Box Edit.app",
           "Box Local Com Server.app",
           "Cisco WebEx Start.app",
           "CitrixOnlineLauncher.app",
           "CocoaDialog.app",
           "CommitWindow.app",
           "convertpdf.app",
           "Dropbox.app",
           "Event Center.app",
           "InstallBoxEdit.app",
           #"iSkysoft Helper Compact.app", same sketchy 'Wondershare' company as below
           "Meeting Center.app",
           "Network Recording Player.app",
           "org.eclipse.equinox.app",# smooth, IBM, bundling eclipse(!) w/ SPSS
           "SharedPackageExtensions.app",# something apple-related
           "TextExpander Helper.app",
           "TextExpander.app",
           "Training Center.app",# webex-related
           #"TunesGoWatch.app", sketchy senuti-like product
           #"Wondershare Helper Compact.app", see what I mean by sketchy?
           "XTrace.app",]

ALL_USERS_APP_SUPPORT = glob.glob('/Users/*/Library/Application Support')

FOUND_APPS = []
for userpath in ALL_USERS_APP_SUPPORT:
    for root, dirnames, filenames in os.walk(userpath):
        for dirname in fnmatch.filter(dirnames, '*.app'):
            FOUND_APPS.append(os.path.join(root, dirname))

TO_INVESTIGATE = []

for app in FOUND_APPS:
    if not "Google/Chrome/" in app:
        #pylint: disable=line-too-long
        if not app.endswith("TextExpander.app/Contents/Frameworks/Sparkle.framework/Versions/A/Resources/finish_installation.app"):
            if not app.endswith("Java/finish_installation.app"):
                if not os.path.basename(app).startswith("GoToMyPC Viewer"):
                    if os.path.basename(app) not in ALLOWED:
                        TO_INVESTIGATE.append(app)

if TO_INVESTIGATE:
    RESULT = "Not in whitelist, investigate:\n" + "\n".join(*[TO_INVESTIGATE])
else:
    RESULT = "No strange apps in ~/*/Lib/AppSupport."

print "<result>%s</result>" % RESULT
