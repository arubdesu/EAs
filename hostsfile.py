#!/usr/bin/python
"""Check osquery output against whitelisted hostfile entries."""


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

def main():
    """gimme some main"""
    osquery_check()

    expected = [{u'hostnames': u'localhost', u'address': u'127.0.0.1'},
                {u'hostnames': u'broadcasthost', u'address': u'255.255.255.255'},
                {u'hostnames': u'localhost', u'address': u'::1'},]

    jsony_dictlist = run_osquery('select * from etc_hosts')
    to_investigate = []

    for host_dict in jsony_dictlist:
        if host_dict not in expected:
            dict_string = ''
            for key, value in host_dict.items():
                dict_string += str(key + ':' + value + ' ')
            to_investigate.append(dict_string)

    if to_investigate:
        result = "Unexpected hostsfile entry found, investigate:\n" + "\n".join(*[to_investigate])
    else:
        result = "No non-standard hosts."

    print "<result>%s</result>" % result

if __name__ == '__main__':
    main()
