#!/usr/bin/env python

from __future__ import division
import numpy as np
import datetime
import flightradar24


def log_to_csv(file_name, data_gen, print_every=1000):
    '''
    Log data from `data_gen` into CSV file `file_name`.
    Status will be printed after every `print_every` rows are written.
    '''
    import csv

    with open(file_name, "wb") as out_file:
        writer = csv.DictWriter(out_file, delimiter=',', fieldnames=flightradar24.FIELDS + flightradar24.FIELDS_EXTRA)
        writer.writeheader()

        print 'logging to file {}...'.format(file_name)

        i = -1
        for i, record in enumerate(data_gen):
            writer.writerow(record)

            if (i % print_every) == 0:
                print ' wrote {} records'.format(i + 1)

    print 'done with {} total records written'.format(i + 1)

def distance(origin, destination):
    '''
    Estimate distance (in meters) between two given lat/long coordinates.
    '''
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371e3 # radius of Earth in meters

    dlat = np.radians(lat2-lat1)
    dlon = np.radians(lon2-lon1)
    a = np.sin(dlat/2) * np.sin(dlat/2) + np.cos(np.radians(lat1)) \
        * np.cos(np.radians(lat2)) * np.sin(dlon/2) * np.sin(dlon/2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    d = radius * c

    return d

def recent_logger(file_name, time_dur, coord, radius):
    '''
    Log flights records going back `time_dur` (`timedelta` object) to `file_name`
    if flight is within `radius` meters of coordinate  `coord` (latitude, longitude).
    '''
    def is_within_radius(rec):
        coord_rec = rec['lat'], rec['long']
        dist = distance(coord_rec, coord)

        return dist <= radius

    data_gen = flightradar24.get_recent(time_dur)
    data_filtered = (rec for rec in data_gen if is_within_radius(rec))

    log_to_csv(file_name, data_filtered, print_every=10)

def date_logger(file_name, dates_durs, coord, radius):
    '''
    Log flights records starting at given dates and lasting given time durations.
    `date_durs` should be a list of tuples of the form (`datetime`, `timedelta`).
    '''
    import itertools

    def is_within_radius(rec):
        coord_rec = rec['lat'], rec['long']
        dist = distance(coord_rec, coord)

        return dist <= radius

    gens = []

    for start_date, dur in dates_durs:
        data_gen = flightradar24.get_historical(start_date, start_date + dur)
        data_filtered = (rec for rec in data_gen if is_within_radius(rec))
        gens.append(data_filtered)

    data_gen = itertools.chain(*gens)
    log_to_csv(file_name, data_gen, print_every=10)


def test_date_logger():
    dates_durs = [(datetime.datetime(year=2014, month=10, day=8, hour=8, minute=0), datetime.timedelta(minutes=15)), \
                  (datetime.datetime(2014, 10, 9, 13, 0), datetime.timedelta(minutes=15)), \
                  (datetime.datetime(2014, 10, 10, 9, 0), datetime.timedelta(minutes=15))]

    coord = (35, -39) # Atlantic ocean
    radius = 1000e3 # 1000 km
    file_name = 'flights.csv'

    date_logger(file_name, dates_durs, coord, radius)

def test_recent_logger():
    time_span = datetime.timedelta(minutes=5)
    coord = (35, -39) # Atlantic ocean
    radius = 1000e3 # 1000 km
    file_name = 'flights.csv'

    recent_logger(file_name, time_span, coord, radius)

if __name__ == '__main__':
    test_recent_logger()
