#!/usr/bin/env python

from __future__ import division
import requests
import json
import datetime


__all__ = ['get_historical_data', 'get_last_data', 'get_current_data', \
           'TIME_RES_HISTORICAL', 'TIME_RES_CURRENT']

FIELDS = 'icao_addr', 'lat', 'long', 'track', 'alt', 'speed', 'squawk', 'radar', \
         'type', 'reg_num', 'time_epoch', 'src', 'dest', 'flight_num', 'unknown1', \
         'vert_speed', 'callsign', 'unknown2'
# unknown1 sometimes == '1', usually == '0'

URL_JSON_CURRENT = "http://db8.flightradar24.com/zones/{zone_name}.js"
URL_JSON_HISTORICAL = 'http://db.flightradar24.com/playback/%Y%m%d/%H%M00.js'

TIME_RES_HISTORICAL = datetime.timedelta(minutes=1)
TIME_RES_CURRENT = datetime.timedelta(seconds=12) # estimated

# multiplicative factors to convert to SI units
CONV_KT_TO_MPS = 0.514444444
CONV_FPM_TO_MPS = 5.08e-3
CONV_FT_TO_M = 0.3048


def iter_historical_data(date_start, date_stop, step=TIME_RES_HISTORICAL):
    if date_stop < date_start:
        raise Exception('stop date is before start date')

    date_cur = date_start

    while date_cur < date_stop:
        url = date_cur.strftime(URL_JSON_HISTORICAL)
        yield date_cur, load_data(url)

        date_cur += step

def iter_recent_data(time_span, step=TIME_RES_HISTORICAL):
    stop = datetime.datetime.now()
    start = stop - time_span

    return iter_historical_data(start, stop, step=step)

def get_current_data(zone_name='full', use_faa=True):
    if use_faa and not zone_name.endswith('_all'):
        zone_name += '_all'

    url = URL_JSON_CURRENT.format(zone_name=zone_name)

    return load_data(url)

def load_data(url, convert=True):
    content = requests.get(url).content

    # delete JS to make text valid JSON
    content = content.replace('pd_callback(', '')
    content = content.replace('fetch_playback_cb(', '')
    content = content.replace(');', '')

    # replace emply strings so Python gives us None's
    content = content.replace('""', 'null')

    json_data = json.loads(content)

    # delete unused fields
    version = json_data.pop('version')
    full_count = json_data.pop('full_count')

    data = []

    for identifier, fields in json_data.items():
        # convert unicode to strings to avoid issues later on
        fields = [f.encode('utf-8') if isinstance(f, unicode) else f for f in fields]

        f = dict(zip(FIELDS, fields))
        f['id'] = identifier.encode('utf-8')

        # convert units to SI
        if convert:
            f['time'] = datetime.datetime.fromtimestamp(f['time_epoch'])
            f['speed'] *= CONV_KT_TO_MPS
            f['alt'] *= CONV_FT_TO_M
            f['vert_speed'] *= CONV_FPM_TO_MPS

        data.append(f)

    return data


def main():
    zone = 'full'
    data = get_current_data(zone)

    print data[0]
    print len(data)

    span = datetime.timedelta(minutes=10)
    iter = iter_recent_data(span)

    for date, data in iter:
        print 'date:', date
        print 'num records:', len(data)

if __name__ == '__main__':
    main()
