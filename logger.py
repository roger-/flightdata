#!/usr/bin/env python

from __future__ import division
import numpy as np
import datetime
import flightradar24


def distance(origin, destination):
    '''
    Estimate distance (in meters) between two given lat/long coordinates.
    '''
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371e3 # m

    dlat = np.radians(lat2-lat1)
    dlon = np.radians(lon2-lon1)
    a = np.sin(dlat/2) * np.sin(dlat/2) + np.cos(np.radians(lat1)) \
        * np.cos(np.radians(lat2)) * np.sin(dlon/2) * np.sin(dlon/2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    d = radius * c

    return d

def logger(file_name, time_span, coord, radius):
    '''
    Log flights records going back `time_span` (`timedelta` object) to `file_name`
    if flight is within `radius` meters of coordate  `coord` (latitude, longitude).
    '''
    data_gen = flightradar24.get_recent(time_span)

    def filter_distance(gen):
        for rec in gen:
            coord_rec = rec['lat'], rec['long']
            dist = distance(coord_rec, coord)

            if dist <= radius:
                yield rec

    flightradar24.log_to_csv(file_name, filter_distance(data_gen), print_every=10)


if __name__ == '__main__':
    time_span = datetime.timedelta(minutes=60)
    coord = (35, -39) # Atlantic ocean
    radius = 10e3 # 10 km
    file_name = 'flightss.csv'

    logger(file_name, time_span, coord, radius)
