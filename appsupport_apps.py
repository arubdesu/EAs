#!/usr/bin/python
"""Given a whitelist of legit helper apps, report on stuff to investigate."""


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

def run_osquery(sql):
    """take sql command you'd like json output for from osquery"""
    cmd = ['/usr/local/bin/osqueryi', '--json', sql]
    jsony_out = subprocess.check_output(cmd)
    try:
        jsony_dictlist = json.loads(jsony_out)
    except ValueError:
        sys.exit(1)
    return jsony_dictlist

def check_app(app):
    """rather than doing 'starts/endswith' tomfoolery, check in function"""
    crappy_paths = ["CitrixOnline/",
                    "Web Applications",
                    "GoToMyPC Viewer",
                    "Java/",
                    "TextExpander",]
    for path in crappy_paths:
        if path in app:
            return
    return app

def main():
    """gimme some main"""
    osquery_check()
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

    #pylint: disable=line-too-long
    all_users_app_support_dicts = run_osquery("select path from apps where path like '/Users/%/%Library/Application Support%'")
    just_paths, to_investigate = [], []
    for path_dict in all_users_app_support_dicts:
        if os.path.basename(path_dict['path']) not in allowed:
            just_paths.append(path_dict['path'])
    for path in just_paths:
        got_caught = check_app(path)
        if got_caught:
            to_investigate.append(got_caught)
    if to_investigate:
        result = "Not in whitelist, investigate:\n" + "\n".join(*[to_investigate])
    else:
        result = "No strange apps in ~/*/Lib/AppSupport."

    print "<result>%s</result>" % result

if __name__ == '__main__':
    main()
