import pump_data
from operator import itemgetter

import datetime
import numpy as np
import arrow


class WaterPumpAnalyzer:
    def __init__(self):
        # Create your storage attributes here.
        self.storage_pump = []
        self.storage_rain_gauge = []
        self.locations_counter = 0
        self.location_dict = {}

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
        # Implement this in Scenario 1
        # print({"time": timestamp, "device": device, "location": location})

        time = arrow.get(timestamp)

        if device == "pump":
            for pump in self.storage_pump:
                if pump[0] == time and location == pump[1]:
                    return pump[2]
        else:
            for rain_gauge in self.storage_rain_gauge:
                if rain_gauge[0] == time and location == rain_gauge[1]:
                    return rain_gauge[2]

    def is_error_mode(self, start: datetime.date, end: datetime.date, location: str) -> bool:
        # Implement this in Scenario 2,3 and 4

        # print("location", location)
        # print("start", start)
        # print("end", end)

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

        # pump
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

        print(sum_pump_check, pump_records_check, sum_pump_now, pump_records_now)
        pump_mean_check = sum_pump_check / pump_records_check
        pump_mean_now = sum_pump_now / pump_records_now

        # print(pump_mean_check, pump_mean_now)

        # check rain_gauge
        if (pump_mean_now / pump_mean_check) >= 1.2:
            # print("Must check rain for error clarification")

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
            # print(rain_gauge_records_check, sum_rain_gauge_check, rain_gauge_records_now, sum_rain_gauge_now)

            rain_gauge_mean_check = sum_rain_gauge_check / rain_gauge_records_check
            rain_gauge_mean_now = sum_rain_gauge_now / rain_gauge_records_now

            # print(rain_gauge_mean_check, rain_gauge_mean_now)

            if (rain_gauge_mean_now / rain_gauge_mean_check) < 1.2:
                return True

        return False

    def sort_by_date(self):
        self.storage_pump.sort(key=itemgetter(0))
        self.storage_rain_gauge.sort(key=itemgetter(0))

##############
wpa = WaterPumpAnalyzer()

for x in pump_data.data_input:
    wpa.handle_message(x)

for x in pump_data.data_search:
    wpa.get_raw_data(x["time"], x["device"], x["location"])

wpa.sort_by_date()

for x in pump_data.data_is_error_mode:
    start = x["start"]
    end = x["end"]
    location = x["location"]
    wpa.is_error_mode(start, end, location)
