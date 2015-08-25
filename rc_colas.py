#!/usr/bin/python
"""Given sha1's of expected rc's, report on any altered or others w/ rc prefix."""


import glob
import hashlib


def main():
    """gimme some main"""
    expected_rc_colas = {"/etc/rc.common" : 'c2c9d79c11496a2bd59b9cec11bc5b6817098303',
                         "/etc/rc.common~previous" : 'c2c9d79c11496a2bd59b9cec11bc5b6817098303',
                         "/etc/rc.deferred_install" : '0c64ec4dfe03ccc8523a5872acf1bbcf48199f6a',
                         "/etc/rc.imaging" : '6d67f95a31b36116c5e4d1d09ff4cc03e046db60',
                         "/etc/rc.netboot" : '471e633b1f6bb3de9a48147ebfa5858f71ab0c32',
                         "/etc/rc.server" : '6dba02aa6e6f5eb9d9dc97bdd3dcef256a698163',}
    present_rcs = glob.glob('/etc/rc*')
    caught_rcs = []
    for cola in present_rcs:#expected_rc_colas.keys():
        with open(cola, 'rb') as sha_me:
            found_sha = hashlib.sha1(sha_me.read()).hexdigest()
        if expected_rc_colas.get(cola) == found_sha:
            pass
        else:
            caught_rcs.append(cola + ' sha: ' + found_sha[:7])

    if caught_rcs:
        result = "Caught 'off' rc, investigate: " + "\n".join(*[caught_rcs])
    else:
        result = "No unexpected or altered rc's present."

    print "<result>%s</result>" % result

if __name__ == '__main__':
    main()
