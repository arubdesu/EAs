#!/usr/bin/python
"""Summarizes any crashes logged in the last 30 days, if it was more than 5 times.
Inspired by:
https://github.com/tulgeywood/JAMF/tree/master/Extension%20Attributes/Panic%20Watch
"""


import collections
import datetime
import glob
import os


EXCLUDED = ['blued',]
            # 'snmpInk',# print-related tomfoolery
            # 'QuickLookSatellite',# on my system that's TextMate messing up


FREQ = 5
DAYS_FROM = 30

SYS_CRASHERS = glob.glob('/Library/Logs/DiagnosticReports/*.crash')
USR_CRASHERS = glob.glob('/Users/*/Library/Logs/DiagnosticReports/*.crash')
# join into master list
DAS_CRASHERS = SYS_CRASHERS + USR_CRASHERS
# build up interim list without more-than-month-old crashes, start by getting -30 date
FORMAT = "%Y-%M-%d-%H%M%S"
DELTA_OBJECT = datetime.timedelta(days=DAYS_FROM)
START_DATETIME = datetime.datetime.today() - DELTA_OBJECT
MONTH_AGO = START_DATETIME.strftime(FORMAT)

CURRENTS = []
for crasher in DAS_CRASHERS:
    stripd_path = os.path.basename(crasher)
    dis_date = stripd_path.split('_')[1]
    if dis_date < MONTH_AGO:
        CURRENTS.append(stripd_path.split('_')[0])
CURRENT_DICT = collections.Counter(CURRENTS)
# crazy list comprehension to make new dict of apps that have crashed 5+ times
JUST_OFTENS = dict((crasher, freq) for crasher, freq in CURRENT_DICT.items() if freq >= FREQ)

if JUST_OFTENS:
    RESULT = JUST_OFTENS
else:
    RESULT = "No recent heavy crashers"

print "<result>%s</result>" % RESULT
