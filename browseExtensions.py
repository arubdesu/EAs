#!/usr/bin/python
"""Naively checks browser extensions against self-maintained whitelist"""
#pylint: disable=invalid-name


import os
import glob
import json
import sys
sys.path.append("/usr/local/munki/munkilib")
import FoundationPlist


CAUGHT_EXTENSION_LIST = []

SAFARI_WHITELIST = ['1Password-2.safariextz',
                    '1Password.safariextz',
                    'AdBlock.safariextz',
                    'AdBlock-2.safariextz',
                    'BugMeNot.safariextz',
                    'Clip to DEVONthink.safariextz',
                    'Clip to DEVONthink-2.safariextz',
                    'Evernote Web Clipper-2.safariextz',
                    'Evernote Web Clipper.safariextz',
                    'Ghostery.safariextz',
                    'Ghostery-2.safariextz',
                    'Instapaper-2.safariextz',
                    'KasperskyURLAdvisor.safariextz',
                    'KasperskyVirtualKeyboard.safariextz',
                    'Open in Chrome.safariextz',
                    'Stylish.safariextz',
                    'Stylish-2.safariextz',
                    'TabLinks.safariextz',]

ALL_USER_SAFARIEXT_PLISTS = glob.glob('/Users/*/Library/Safari/Extensions/Extensions.plist')
for plist in ALL_USER_SAFARIEXT_PLISTS:
    list_of_dicts = FoundationPlist.readPlist(plist)
    for ext_info_dict in list_of_dicts['Installed Extensions']:
        if ext_info_dict['Archive File Name'] not in SAFARI_WHITELIST:
            caught_tuple = (ext_info_dict.get('Archive File Name'),
                            ext_info_dict.get('Bundle Identifier'),
                            ext_info_dict.get('Developer Identifier'))
            CAUGHT_EXTENSION_LIST.append("\n" + str(caught_tuple))
if CAUGHT_EXTENSION_LIST:
    CAUGHT_EXTENSION_LIST.insert(0, "\t\nCaught Safari's: ")

FIREFOX_WHITELIST = ['onepassword4@agilebits.com.xpi',
                     '{d10d0bf8-f5b5-c8b4-a8b2-2b9879e08c5d}.xpi',
                     'Clip-to-DEVONthink@devon-technologies.com.xpi',
                     'firefox-hotfix@mozilla.org.xpi',
                     'jid1-YcMV6ngYmQRA2w@jetpack']#unofficial pinterest...

#pylint: disable=line-too-long
FIREFOX_FOUND_EXTZ = glob.glob('/Users/*/Library/Application Support/Firefox/Profiles/*.default/extensions/*.xpi')
FFOX_JSONS = glob.glob('/Users/*/Library/Application Support/Firefox/Profiles/*.default/extensions.json')
SUSPECTS = []
for extz in FIREFOX_FOUND_EXTZ:
    if not os.path.basename(extz) in FIREFOX_WHITELIST:
        SUSPECTS.append(os.path.splitext(os.path.basename(extz))[0])
if SUSPECTS:
    CAUGHT_EXTENSION_LIST.append("\t\nCaught Firefoxens: ")
    for MANI in FFOX_JSONS:
        try:
            with open(MANI, 'r') as phile:
                manifest = json.loads(phile.read())
                FFOX_STRING = ''
                for ext_dict in manifest['addons']:
                    dict_type = ext_dict.get('type')
                    if dict_type == 'extension':
                        dict_id = ext_dict.get('id')
                        if dict_id in SUSPECTS:
                            CAUGHT_EXTENSION_LIST.append("\n" + dict_id + "\t" + str(ext_dict.get('defaultLocale')))
        #pylint: disable=invalid-name,broad-except
        except Exception, e:
            print e

CHROME_WHITELIST = ["Temp",
                    "aomjjhallfgjeglblehebfpbcfeobpgk",# 1Password
                    "lbfehkoinhhcknnbdgnnmjhiladcgbol",# Evernote 'Web'
                    "pioclpoplcdbaefihamjohnefbikjilc",# Evernote Web Clipper
                    "cfhdojbkjhnklbpkdaibdccddilifddb",# AdBlockPlus
                    "gighmmpiobklfepjocnamgkkbiglidom",#adblockRegular...
                    "iooicodkiihhpojmmeghjclgihfjdjhj",# Clearly
                    "jlhmfgmfgeifomenelglieieghnjghma",# WebEx,
                    "bfogiafebfohielmmehodmfbbebbbpei",# Keeper password mgr
                    "gcgikpombjkodabhbdalkcdhmllafipp",# GoToMeetingProSomethingOrOther
                    "lneaknkopdijkpnocmklfnjbeapigfbh",# Google Maps
                    "mgndgikekgjfcpckkfioiadnlibdjbkf",# "Chrome",
                    "dliochdbjfkdbacpmhlcpmleaejidimm",# chromecast beta
                    "noondiphcddnnabmjcihcjfbhfklnnep",# Google phishing/password checker
                    "lccekmodgklaepjeofjdjpbminllajkg",# Chrome Hotword for 'Ok, Google'
                    "nmmhkkegccagdldgiimedpiccmgmieda",# "Google Wallet",
                    "ahfgeienlihckogmohjhadlkjgocpleb",# "Google Store",
                    "aapocclcgogkmnckokdopfmhonfmgoek",# "Google Slides"
                    "boadgeojelhgndaghljhdicfkmllpafd",# "Google Cast"
                    "felcaaldnbdncclmgdcncolpebgiejap",# "Google Sheets"
                    "gfdkimpbcpahaombhbimeihdjnejgicl",# "Chrome FeedBack",
                    "pjkljhegncpnkpknbcohdijeoejaedia",# "Gmail",
                    "nkeimhogjdpnpccoofpliimaahmaaome",# "Google Hangouts",
                    "nckgahadagoaajjgafhacjanaoiihapd",# "
                    "coobgpohoikkiipiblmjeljniedjpjpf",# "Google Search",
                    "neajdppkdcdipfabeoofebfddakdcjhd",# "Google Network Speech",
                    "kmendfapggjehodndflmmgagdbamhnfd",# "Chrome Crypto Token Extension",
                    "apdfllckaahabafndbhieahigkjlhalf",# "Google Drive",
                    "lmjegmlicamnimmfhcmpkclmigmmcbeh",# Google Drive file open in native apps
                    "dnhpdliibojhegemfjheidglijccjfmc",# "Google Hotword Helper",
                    "bepbmhgboaologfdajaanbcjmnhjmhfn",# "Google Voice Search Hotword",
                    "blpcfgokakmgnkcojhhkbfbldkacnbeo",# "Google YouTube",
                    "aohghmighlieiainnegkcijnfilokake",# "Google Docs",
                    "eemcgdkfndhakfknompkggombfjjjeno",# "Chrome Bookmark Manager",
                    "gmlllbghnfkpflemihljekbapjopfjik",# ditto
                    "mfehgcgbbipciphmccgaenjidiccnmng",# "Chrome Cloud Print",
                    "ennkphjdgehloodpbhlhldgbnhmacadg",# "Chrome Settings",
                    "pafkbggdmjlpgkdkcbjmhmfcdpncadgh",# "Google Now",
                    "kcnhkahnjcbndmmehfkdnkjomaanaooo",# GoogleVoice
                    "gpdjojdkbbmdfjfahjcgigfpmkopogic",# Pinterest...
                    "pkehgijcmpdhfbdbbnkijodmdjhbjlgp",# EFF's Privacy Badger
                    "mfffpogegjflfpflabcdkioaeobkgjik",# "GAIA Component Extension"
                    #"gkojfkhlekighikafcpjkiklfbnlmeio", unless you like customers using free VPN services like 'hola internet'
                    "aknpkdffaafgjchaibgeefbgmgeghloj",# misc junk, not reported diseased yet
                    "ejjicmeblgpmajnghnpcppodonldlgfn",
                    "knipolnnllmklapflnccelgolnpehhpl",
                    "mcemheplgccbimaplmppfdofjghnpmmn",
                    "aciahcmjmecflokailenpkdchphgkefd",
                    "bfjgbcjfpbbfepcccpaffkjofcmglifg",
                    "bhmicilclplefnflapjmnngmkkkkpfad",
                    "hnkkehjnlfplmdnallbjjdnokolhblgb",
                    "mcbkbpnkkkipelfledbfocopglifcfmi",
                    "ajpgkpeckebdhofmmjfgcjjiiejpodla",
                    "aofbadhekfmdddiihifojhjjpkaoojkn",
                    "dhaphijmoldalicdpbnpgjeeheglbppo",
                    "elicpjhcidhpjomhibiffojpinpmmpil",
                    "hdgenjhkjihnmigcommchefpajjhdmba",
                    "idknbmbdnapjicclomlijcgfpikmndhd",
                    "ifhgjbjejfocglfphkdecifccicemfll",
                    "ghbmnnjooekpmoecnnnilnnbdlolhkhi"]

CHROME_FOUND_EXTZ = glob.glob(
    '/Users/*/Library/Application Support/Google/Chrome/Default/Extensions/*')
TEMP_CHROMER = []
for extz in CHROME_FOUND_EXTZ:
    if not os.path.basename(extz) in CHROME_WHITELIST:
        TO_GLOBD = extz + "/*/manifest.json"
        MANI_PATH = glob.glob(TO_GLOBD)
        try:
            with open((MANI_PATH[0]), 'r') as phile:
                manifest = json.loads(phile.read())
                DESCRIPT_STRING = ''
                if 'name' in manifest:
                    DESCRIPT_STRING += (manifest['name'] + " ")
                if 'description' in manifest:
                    DESCRIPT_STRING += (manifest['description'] + " ")
                chrome_tuple = (extz, DESCRIPT_STRING)
        #pylint: disable=invalid-name,broad-except
        except Exception, e:
            print e
        TEMP_CHROMER.append("\n" + str(chrome_tuple))
if TEMP_CHROMER:
    CAUGHT_EXTENSION_LIST.append("\t\nCaught Chromens: ")
    CAUGHT_EXTENSION_LIST += TEMP_CHROMER

if CAUGHT_EXTENSION_LIST:
    RESULT = "Not in whitelist, investigate: " + "".join(*[CAUGHT_EXTENSION_LIST])
else:
    RESULT = 'Passed'
print "<result>%s</result>" % RESULT
