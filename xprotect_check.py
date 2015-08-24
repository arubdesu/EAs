#!/usr/bin/python
"""Checks what xprotect is blocking against installed java/flash"""


import os
import CoreFoundation


def main():
    """gimme some main"""
    versionkey = 'CFBundleVersion'

    flashinfopath = "/Library/Internet Plug-Ins/Flash Player.plugin/Contents/Info.plist"
    flashinxprotect = "com.macromedia.Flash Player.plugin"

    javainfopath = "/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Info.plist"
    javainxprotect = "com.oracle.java.JavaAppletPlugin"
    #pylint: disable=line-too-long
    xprotectpath = '/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/XProtect.meta.plist'
    xprotectminversionkey = 'MinimumPlugInBundleVersion'
    # yes, this isn't strictly a pref value, it's just less code to do it this way
    blackliststanza = CoreFoundation.CFPreferencesCopyAppValue("PlugInBlacklist", xprotectpath)

    minflash = blackliststanza['10'][flashinxprotect][xprotectminversionkey]
    minjava = blackliststanza['10'][javainxprotect][xprotectminversionkey]
    # since we're only checking two values I'm not even making a list, just building up a string
    xprotectcaught = ''

    if os.path.exists(flashinfopath):
        flashversion = CoreFoundation.CFPreferencesCopyAppValue(versionkey, flashinfopath)
        if flashversion < minflash:
            xprotectcaught += 'installed flash version %s less than xprotects minimum %s' % (flashversion, minflash)

    if os.path.exists(javainfopath):
        javaversion = CoreFoundation.CFPreferencesCopyAppValue(versionkey, javainfopath)
        if javaversion < minjava:
            if not xprotectcaught == '':
                xprotectcaught += '\ninstalled java version %s less than xprotects minimum %s' % (javaversion, minjava)
            else:
                xprotectcaught += 'installed java version %s less than xprotects minimum %s' % (javaversion, minjava)

    if not xprotectcaught:
        result = "Patched"
    else:
        result = xprotectcaught

    print "<result>%s</result>" % result

if __name__ == '__main__':
    main()
