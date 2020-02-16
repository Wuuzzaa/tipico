import pump_data
import sys

import datetime
import numpy as np
import arrow
from operator import itemgetter


class WaterPumpAnalyzer:
    def __init__(self):
        # Create your storage attributes here.
        self.storage_pump = []
        self.storage_rain_gauge = []
        self.location_dict = {}
        self.lists_sorted = False
        self.pump_days_dict = {}
        self.rain_gauge_days_dict = {}

    def handle_message(self, data: dict):
        # This method gets called with the raw data. Implement this in Scenario 1.
        time = arrow.get(data["time"])

        # use location dict here to store as number
        location = data["location"]

        if data["device"] == "pump":
            energy_consumption = data["energy_consumption"]
            array = np.array([time, location, energy_consumption])
            self.storage_pump.append(array)

        else:
            value = data["value"]
            array = np.array([time, location, value])
            self.storage_rain_gauge.append(array)

    def get_raw_data(self, timestamp: str, device: str, location: str) -> dict:
        time = arrow.get(timestamp)

        if device == "pump":
            for pump in self.storage_pump:
                if pump[0] == time and location == pump[1]:
                    return pump[2]
        else:
            for rain_gauge in self.storage_rain_gauge:
                if rain_gauge[0] == time and location == rain_gauge[1]:
                    return rain_gauge[2]

    def is_pump_above_average(self, time_check_start, time_check_end, location, time_start, time_end):
        """
        method to check if the pump energy consumption is 20% higher than normal
        """
        sum_pump_check = 0
        pump_records_check = 0

        sum_pump_now = 0
        pump_records_now = 0

        for pump in self.storage_pump:
            if pump[0] >= time_check_start and pump[0] <= time_check_end and location == pump[1]:
                pump_records_check += 1
                sum_pump_check += pump[2]
            elif pump[0] >= time_start and pump[0] <= time_end and location == pump[1]:
                pump_records_now += 1
                sum_pump_now += pump[2]
            elif pump[0] > time_end:
                break

        pump_mean_check = sum_pump_check / pump_records_check
        pump_mean_now = sum_pump_now / pump_records_now

        return (pump_mean_now / pump_mean_check) >= 1.2

    def is_rain_gauge_above_average(self, time_check_start, time_check_end, location, time_start, time_end):
        """
        method to check if the rain_gauge value is 20% higher than normal
        """
        rain_gauge_records_check = 0
        sum_rain_gauge_check = 0
        rain_gauge_records_now = 0
        sum_rain_gauge_now = 0

        for rain_gauge in self.storage_rain_gauge:
            if rain_gauge[0] >= time_check_start and rain_gauge[0] <= time_check_end and location == rain_gauge[1]:
                rain_gauge_records_check += 1
                sum_rain_gauge_check += rain_gauge[2]
            elif rain_gauge[0] >= time_start and rain_gauge[0] <= time_end and location == rain_gauge[1]:
                rain_gauge_records_now += 1
                sum_rain_gauge_now += rain_gauge[2]
            elif rain_gauge[0] > time_end:
                break

        rain_gauge_mean_check = sum_rain_gauge_check / rain_gauge_records_check
        rain_gauge_mean_now = sum_rain_gauge_now / rain_gauge_records_now

        return (rain_gauge_mean_now / rain_gauge_mean_check) >= 1.2

    def is_error_mode(self, start: datetime.date, end: datetime.date, location: str) -> bool:
        # Implement this in Scenario 2,3 and 4

        # print("location", location)
        # print("start", start)
        # print("end", end)

        # sort the data first and get the startindex for each day
        if not self.lists_sorted:
            self.sort_by_date()
            self.refresh_datestart_indices()

        # calculate the start and end days for the checkperiode and the periode to be checked against
        delta = (end - start).days + 1

        check_start = start - datetime.timedelta(days=delta)
        check_end = start - datetime.timedelta(days=1)

        # print("delta", delta)

        time_check_start = arrow.get(check_start)
        time_check_end = arrow.get(check_end)

        time_check_end = time_check_end.replace(hour=23, minute=59, second=59)

        time_start = arrow.get(start)
        time_end = arrow.get(end)

        time_end = time_end.replace(hour=23, minute=59, second=59)

        # print("time_check_start", time_check_start)
        # print("time_check_end", time_check_end)

        # print(pump_mean_check, pump_mean_now)

        if not self.is_rain_gauge_above_average(time_check_start, time_check_end, location, time_start, time_end):
            if self.is_pump_above_average(time_check_start, time_check_end, location, time_start, time_end):
                return True
        return False

    def sort_by_date(self):
        self.storage_pump.sort(key=itemgetter(0))
        self.storage_rain_gauge.sort(key=itemgetter(0))

        self.lists_sorted = True

    def refresh_datestart_indices(self):
        """
        Method to refresh the indicies for pump and rain gauge for the first day in the storage lists
        key = day, value = first index of this day in the store lists
        """
        # reset
        self.pump_days_dict = {}
        self.rain_gauge_days_dict = {}

        # pump
        for i in range(len(self.storage_pump)):
            day = self.storage_pump[i][0].date()
            if day not in self.pump_days_dict:
                self.pump_days_dict[day] = i

        # rain gauge
        for i in range(len(self.storage_rain_gauge)):
            day = self.storage_rain_gauge[i][0].date()
            if day not in self.rain_gauge_days_dict:
                self.rain_gauge_days_dict[day] = i


##############
wpa = WaterPumpAnalyzer()

for x in pump_data.data_input:
    wpa.handle_message(x)

for x in pump_data.data_search:
    wpa.get_raw_data(x["time"], x["device"], x["location"])

for x in pump_data.data_is_error_mode:
    start = x["start"]
    end = x["end"]
    location = x["location"]
    wpa.is_error_mode(start, end, location)
