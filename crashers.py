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

# how often you consider worth reporting, and how far back to include
FREQ = 5
DAYS_FROM = 30

DAS_CRASHERS = glob.glob('/Library/Logs/DiagnosticReports/*.crash')
DAS_CRASHERS += glob.glob('/Users/*/Library/Logs/DiagnosticReports/*.crash')
# build up interim list without more-than-month-old crashes, start by getting -30 date
FORMAT = "%Y-%M-%d-%H%M%S"
DELTA_OBJECT = datetime.timedelta(days=DAYS_FROM)
START_DATETIME = datetime.datetime.today() - DELTA_OBJECT
TIMESTAMP_AGO = START_DATETIME.strftime(FORMAT)

FREQ_LIST, PATH_LIST, OUR_PATHS_LIST = [], [], []

for crasher in DAS_CRASHERS:
    stripd_path = os.path.basename(crasher)
    dis_date = stripd_path.split('_')[1]
    if dis_date > TIMESTAMP_AGO:
        FREQ_LIST.append(stripd_path.split('_')[0])
        PATH_LIST.append(crasher)

CURRENTS_DICT = collections.Counter(FREQ_LIST)
# crazy list comprehension to make dict of app:frequency for processes that have crashed 5+ times
FREQS_DICT = dict((crashing_app, freq) for crashing_app, freq in CURRENTS_DICT.items() if freq >= FREQ)

RESULT_LIST = ["%s: %s" % (process, freq) for process, freq in FREQS_DICT.items()]
keylist = FREQS_DICT.keys()
for path in PATH_LIST:
    for key in keylist:
        if key in path:
            OUR_PATHS_LIST.append(path)
        
RESULT_LIST += OUR_PATHS_LIST

if RESULT_LIST:
    RESULT = "\n".join(*[RESULT_LIST])
else:
    RESULT = "No recent heavy crashers"

print "<result>%s</result>" % RESULT
