#!/usr/bin/python
"""Given a whitelist of legit helper apps, report on stuff to investigate."""


import fnmatch
import glob
import os


def main():
    """gimme some main"""
    allowed = ["Android File Transfer Agent.app",
               "asannotation2.app",
               "aswatcher.app",
               "atmsupload.app",
               "Box Edit.app",
               "Box Local Com Server.app",
               "Cisco WebEx Start.app",
               "CitrixOnlineLauncher.app",
               "CocoaDialog.app",
               "CommitWindow.app",
               "convertpdf.app",
               "crash_report_sender.app",
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

    crappy_paths = ["CitrixOnline/",
                    "Web Applications",
                    "GoToMyPC Viewer",
                    "Java/",
                    "TextExpander",]

    all_users_app_support = glob.glob('/Users/*/Library/Application Support')

    found_apps = []
    for userpath in all_users_app_support:
        for root, dirnames, _ in os.walk(userpath):
            for dirname in fnmatch.filter(dirnames, '*.app'):
                found_apps.append(os.path.join(root, dirname))

    to_investigate = []

    def check_apps(app):
        """rather than doing 'starts/endswith' tomfoolery, check in function"""
        for path in crappy_paths:
            if path in app:
                return to_investigate
        if os.path.basename(app) not in allowed:
            to_investigate.append(app)
        return to_investigate

    for app in found_apps:
        check_apps(app)

    if to_investigate:
        result = "Not in whitelist, investigate:\n" + "\n".join(*[to_investigate])
    else:
        result = "No strange apps in ~/*/Lib/AppSupport."

    print "<result>%s</result>" % result

if __name__ == '__main__':
    main()
