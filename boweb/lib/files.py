# -*- coding: utf8 -*-
# -*- coding: utf8 -*-

'''

@author Andreas Würl

'''

import os, subprocess
import glob
import datetime

import blitzortung.builder as builder

class Raw(object):

    def __init__(self, rawPath):
        raw_file_names = glob.glob(os.path.join(rawPath, '*.bor'))

        raw_file_names.sort()

        self.raw_files = {}

        for raw_file_name in raw_file_names:
            try:
                date = datetime.datetime.strptime(raw_file_name[-12:-4], '%Y%m%d').date()
            except ValueError:
                continue
            if not self.raw_files.has_key(date):
                self.raw_files[date] = raw_file_name
            else:
                raise Exception("ERROR: double date! " + raw_file_name + " vs. " + self.raw_files[date])

    def get(self, date):
        if date in self.raw_files:
            return self.raw_files[date]
        else:
            raise Exception("no file for date " + date.strftime('%Y-%m-%d'))

    def get_dates(self):
        dates = self.raw_files.keys()
        dates.sort()
        return dates


class Data(object):

    def __init__(self, raw_file_path, time):
        self.raw_file_path = raw_file_path
        self.time = time
        self.error = False

    def get(self, long_format=False):
        start = self.time.get_start_time()
        start_time = start.strftime("%H%M")
        start_date = start.strftime("%Y%m%d")

        end = self.time.get_end_minute()
        end_time = end.strftime("%H%M")

        self.error = False

        raw_file = self.raw_file_path.get(start.date())

        if long_format:
            return self.get_output(raw_file, start_time, end_time, True)
        else:
            return self.get_data(raw_file, start_time, end_time)

    def get_output(self, raw_file, starttime, endtime, long_format=False):
        cmd = ['bo-data','-i', raw_file, '-s', starttime, '-e', endtime]
        if long_format:
            cmd.append('--long-data')
        dataPipe = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        (output, _) = dataPipe.communicate()

        return output.splitlines()

    def get_data(self, raw_file, starttime, endtime):
        rawEvents = []

        for line in self.get_output(raw_file, starttime, endtime):
            raw_event_builder = builder.RawEvent()
            raw_event_builder.from_string(line)
            rawEvents.append(raw_event_builder.build())

        return rawEvents

    def list(self):
        for event in self.get():
            print event

    def list_long(self):
        for line in self.get(True):
            print line

class StatisticsData(Data):

    def get_data(self, raw_file, starttime, endtime):
        args = ['bo-data','-i', raw_file, '-s', starttime, '-e', endtime, '--mode', 'statistics']
        dataPipe = subprocess.Popen(args, stdout=subprocess.PIPE)
        (output, _) = dataPipe.communicate()

        results = output.strip().split(" ")

        self.count = int(results[0])
        self.mean = float(results[1])
        self.variance = float(results[2])

    def getCount(self):
        if not self.error:
            return self.count
        return 0

    def getMean(self):
        if not self.error:
            return self.mean
        return float('nan')

    def getVariance(self):
        if not self.error:
            return self.variance
        return float('nan')

class HistogramData(Data):

    def get_data(self, raw_file, starttime, endtime):
        dataPipe = subprocess.Popen(['bo-data','-i', raw_file, '-s', starttime, '-e', endtime, '--mode', 'histogram'], stdout=subprocess.PIPE)
        (output, _) = dataPipe.communicate()

        return output.splitlines()
