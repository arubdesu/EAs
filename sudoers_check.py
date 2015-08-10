#!/usr/bin/python
"""Given an unmodified sudoers (and a sha1 of system python), report on stuff to investigate."""


import hashlib
import platform


CLEAN_SUDOERSv1 = 'bf682f2d93bbcb6465e302fc768646b02c304d40'
CLEAN_SUDOERSv2 = 'da39a3ee5e6b4b0d3255bfef95601890afd80709'
# this will change as of 10.10.5+python 2.7.10, 46480e019321f49050bbc3c5d087b28d878b6048
CLEAN_PYTHON = 'ae79a52d9dc6ab37b8dcfc096faf9882ddd12e8e'
# if we have a bad sudoers, I want a diff against a 'clean' 10.10.4 one
CLEAN_SUDOERS_STRING = """# sudoers file.
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
CLEAN_SUDOERS_LINES = CLEAN_SUDOERS_STRING.splitlines()
# for returning where we had an issue
BADDY_LIST = []

RUNNING_OS_RELEASE = '.'.join(platform.mac_ver()[0].split('.')[0:2])
if RUNNING_OS_RELEASE == '10.10':
    with open('/usr/bin/python', 'rb') as checking_binary:
        ACTUAL_PYTHON = hashlib.sha1(checking_binary.read()).hexdigest()
    if ACTUAL_PYTHON != CLEAN_PYTHON:
        BADDY_LIST.append('Actual python is %s' % ACTUAL_PYTHON)
with open('/etc/sudoers', 'rb') as sudoers:
    ACTUAL_SUDOERS = [line.strip() for line in sudoers]
    ACTUAL_SUDOERS_SHA1 = hashlib.sha1(sudoers.read()).hexdigest()

if ACTUAL_SUDOERS_SHA1 != CLEAN_SUDOERSv1: 
    if ACTUAL_SUDOERS_SHA1 != CLEAN_SUDOERSv2:
        DIFF = []
        for phileline in ACTUAL_SUDOERS:
            if phileline:
                if phileline[0] == '#':
                    pass
                else:
                    subdline = ('	').join(phileline.split(4*' '))
                    if subdline not in CLEAN_SUDOERS_LINES:
                        DIFF.append('\t' + subdline)
        JOINT_LIST = '\n'.join(list(DIFF))
        BADDY_LIST.append('Sudoers is modified, this version has:\n%s' % str(JOINT_LIST))

if BADDY_LIST:
    RESULT = "Caught stuff, investigate: " + "\n".join(*[BADDY_LIST])
else:
    RESULT = "Not (noticably) pwn3d yet."

print "<result>%s</result>" % RESULT
