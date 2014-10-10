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
    if flight is within `radius` meters of coordinate  `coord` (latitude, longitude).
    '''
    def is_within_radius(rec):
        coord_rec = rec['lat'], rec['long']
        dist = distance(coord_rec, coord)

        return dist <= radius

    data_gen = flightradar24.get_recent(time_span)
    data_filtered = (rec for rec in data_gen if is_within_radius(rec))

    flightradar24.log_to_csv(file_name, data_filtered, print_every=10)


if __name__ == '__main__':
    time_span = datetime.timedelta(minutes=5)
    coord = (35, -39) # Atlantic ocean
    radius = 1000e3 # 1000 km
    file_name = 'flights.csv'

    logger(file_name, time_span, coord, radius)
