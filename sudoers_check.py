#!/usr/bin/python
"""Given an unmodified sudoers (and a sha1 of system python), report on stuff to investigate."""


import hashlib
import platform

def main():
    """gimme some main"""
    clean_sudoers_one = 'bf682f2d93bbcb6465e302fc768646b02c304d40'
    clean_sudoers_two = 'da39a3ee5e6b4b0d3255bfef95601890afd80709'

    clean_python_one = 'ae79a52d9dc6ab37b8dcfc096faf9882ddd12e8e'
    # changed as of 10.10.5+python 2.7.10
    clean_python_two = '46480e019321f49050bbc3c5d087b28d878b6048'
    # if we have a bad sudoers, I want a diff against a 'clean' one
    clean_sudoers_string = """# sudoers file.
    #
    # This file MUST be edited with the 'visudo' command as root.
    # Failure to use 'visudo' may result in syntax or file permission errors
    # that prevent sudo from running.
    #
    # See the sudoers man page for the details on how to write a sudoers file.
    #

    # Host alias specification

    # User alias specification

    # Cmnd alias specification

    # Defaults specification
    Defaults	env_reset
    Defaults	env_keep += "BLOCKSIZE"
    Defaults	env_keep += "COLORFGBG COLORTERM"
    Defaults	env_keep += "__CF_USER_TEXT_ENCODING"
    Defaults	env_keep += "CHARSET LANG LANGUAGE LC_ALL LC_COLLATE LC_CTYPE"
    Defaults	env_keep += "LC_MESSAGES LC_MONETARY LC_NUMERIC LC_TIME"
    Defaults	env_keep += "LINES COLUMNS"
    Defaults	env_keep += "LSCOLORS"
    Defaults	env_keep += "SSH_AUTH_SOCK"
    Defaults	env_keep += "TZ"
    Defaults	env_keep += "DISPLAY XAUTHORIZATION XAUTHORITY"
    Defaults	env_keep += "EDITOR VISUAL"
    Defaults	env_keep += "HOME MAIL"

    # Runas alias specification

    # User privilege specification
    root	ALL=(ALL) ALL
    %admin	ALL=(ALL) ALL

    # Uncomment to allow people in group wheel to run all commands
    # %wheel	ALL=(ALL) ALL

    # Same thing without a password
    # %wheel	ALL=(ALL) NOPASSWD: ALL

    # Samples
    # %users  ALL=/sbin/mount /cdrom,/sbin/umount /cdrom
    # %users  localhost=/sbin/shutdown -h now"""
    clean_sudoers_lines = clean_sudoers_string.splitlines()
    # for returning where we had an issue
    baddy_list = []

    running_os_release = '.'.join(platform.mac_ver()[0].split('.')[0:2])
    if running_os_release == '10.10':
        with open('/usr/bin/python', 'rb') as checking_binary:
            actual_python = hashlib.sha1(checking_binary.read()).hexdigest()
        if actual_python != clean_python_one:
            if actual_python != clean_python_two:
                baddy_list.append('Actual python is %s' % actual_python)
    with open('/etc/sudoers', 'rb') as sudoers:
        actual_sudoers = [line.strip() for line in sudoers]
        actual_sudoers_sha = hashlib.sha1(sudoers.read()).hexdigest()

    if actual_sudoers_sha != clean_sudoers_one: 
        if actual_sudoers_sha != clean_sudoers_two:
            diff = []
            for phileline in actual_sudoers:
                if phileline:
                    if phileline[0] == '#':
                        pass
                    else:
                        subdline = ('	').join(phileline.split(4*' '))
                        if subdline not in clean_sudoers_lines:
                            diff.append('\t' + subdline)
            joint_list = '\n'.join(list(diff))
            baddy_list.append('Sudoers is modified, this version has:\n%s' % str(joint_list))

    if baddy_list:
        result = "Caught stuff, investigate: " + "\n".join(*[baddy_list])
    else:
        result = "Not (noticably) pwn3d yet."

    print "<result>%s</result>" % result

if __name__ == '__main__':
    main()
