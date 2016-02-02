#!/usr/bin/python
"""Given a list of sparkle-updated apps using http, with other helpful info."""


import json
from operator import itemgetter
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

def main():
    """gimme some main"""
    osquery_check()
    #pylint: disable=line-too-long
    all_app_sufeeds_etc_dicts = run_osquery("""select feeds.*, p2.value as sparkle_version from (select a.name as app_name, a.path as app_path, a.bundle_identifier as bundle_id, p.value as feed_url from (select name, path, bundle_identifier from apps) a, preferences p where p.path = a.path || '/Contents/Info.plist' and p.key = 'SUFeedURL' and feed_url like 'http://%') feeds left outer join preferences p2 on p2.path = app_path || '/Contents/Frameworks/Sparkle.framework/Resources/Info.plist' where (p2.key = 'CFBundleShortVersionString' OR coalesce(p2.key, '') = '');""")
    baddys = []
    length_list = sorted(all_app_sufeeds_etc_dicts, key=itemgetter('app_path'))
    for jisho in length_list:
        result_string = ''.join([jisho['app_name'], ' - Sparkle Version: ',
                        jisho.get('sparkle_version', 'Not found'),' - ',
                        jisho['feed_url'], '\n\t', jisho['app_path']])
        baddys.append(result_string)
    if baddys:
        result = "\n".join(*[baddys])
    else:
        result = "No sparkle apps"

    print "<result>%s</result>" % result

if __name__ == '__main__':
    main()
