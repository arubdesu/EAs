#!/usr/bin/python
"""Checks what xprotect is blocking against installed java/flash"""


import os
import CoreFoundation


VERSIONKEY = 'CFBundleVersion'

FLASHINFOPATH = "/Library/Internet Plug-Ins/Flash Player.plugin/Contents/Info.plist"
FLASHINXPROTECT = "com.macromedia.Flash Player.plugin"

JAVAINFOPATH = "/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Info.plist"
JAVAINXPROTECT = "com.oracle.java.JavaAppletPlugin"
#pylint: disable=line-too-long
XPROTECTPATH = '/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/XProtect.meta.plist'
XPROTECTMINVERSIONKEY = 'MinimumPlugInBundleVersion'
# yes, this isn't strictly a pref value, it's just less code to do it this way
BLACKLISTSTANZA = CoreFoundation.CFPreferencesCopyAppValue("PlugInBlacklist", XPROTECTPATH)

MINFLASH = BLACKLISTSTANZA['10'][FLASHINXPROTECT][XPROTECTMINVERSIONKEY]
MINJAVA = BLACKLISTSTANZA['10'][JAVAINXPROTECT][XPROTECTMINVERSIONKEY]
# since we're only checking two values I'm not even making a list, just building up a string
XPROTECTCAUGHT = ''

if os.path.exists(FLASHINFOPATH):
    FLASHVERSION = CoreFoundation.CFPreferencesCopyAppValue(VERSIONKEY, FLASHINFOPATH)
    if FLASHVERSION < MINFLASH:
        XPROTECTCAUGHT += 'installed flash version %s less than xprotects minimum %s' % (FLASHVERSION, MINFLASH)

if os.path.exists(JAVAINFOPATH):
    JAVAVERSION = CoreFoundation.CFPreferencesCopyAppValue(VERSIONKEY, JAVAINFOPATH)
    if JAVAVERSION < MINJAVA:
        if not XPROTECTCAUGHT == '':
            XPROTECTCAUGHT += '\ninstalled java version %s less than xprotects minimum %s' % (JAVAVERSION, MINJAVA)
        else:
            XPROTECTCAUGHT += 'installed java version %s less than xprotects minimum %s' % (JAVAVERSION, MINJAVA)

if not XPROTECTCAUGHT:
    RESULT = "Patched"
else:
    RESULT = XPROTECTCAUGHT

print "<result>%s</result>" % RESULT

