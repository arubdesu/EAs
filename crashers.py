#!/usr/bin/python
"""Summarizes any crashes logged in the last 30 days, if it was more than 5 times.
Inspired by:
https://github.com/tulgeywood/JAMF/tree/master/Extension%20Attributes/Panic%20Watch
"""


import collections
import datetime
import glob
import os


def main():
    """gimme some main"""
    excluded = ['blued']
                # 'Tweetbot,]
                # 'snmpInk',# print-related tomfoolery
                # 'QuickLookSatellite',# on my system that's TextMate messing up

    # how often you consider worth reporting, and how far back to include
    das_freq = 5
    days_from = 30

    das_crashers = glob.glob('/Library/Logs/DiagnosticReports/*.crash')
    das_crashers += glob.glob('/Users/*/Library/Logs/DiagnosticReports/*.crash')
    # build up interim list without more-than-month-old crashes, start by getting -30 date
    das_format = "%Y-%M-%d-%H%M%S"
    delta_object = datetime.timedelta(days=days_from)
    start_datetime = datetime.datetime.today() - delta_object
    timestamp_ago = start_datetime.strftime(das_format)

    freq_list, path_list, our_paths_list = [], [], []

    for crasher in das_crashers:
        stripd_path = os.path.basename(crasher)
        dis_date = stripd_path.split('_')[1]
        if dis_date < timestamp_ago:
            freq_list.append(stripd_path.split('_')[0])
            path_list.append(crasher)

    currents_dict = collections.Counter(freq_list)
    #pylint: disable=line-too-long
    # crazy list comprehension to make dict of app:frequency for processes that have crashed 5+ times
    freqs_dict = dict((crashing_app, freq) for crashing_app, freq in currents_dict.items() if freq >= das_freq)
    filtered = {}
    for tup in freqs_dict.items():
        if tup[0] in excluded:
            continue
        else:
            filtered[tup[0]] = tup[1]
    result_list = ["%s: %s" % (process, freq) for process, freq in filtered.items()]
    keylist = filtered.keys()
    for path in path_list:
        for key in keylist:
            if key in path:
                our_paths_list.append(path)

    result_list += our_paths_list

    if result_list:
        result = "\n".join(*[result_list])
    else:
        result = "No recent heavy crashers"

    print "<result>%s</result>" % result

if __name__ == '__main__':
    main()
