A Python library to download data from [flightradar24.com](http://www.flightradar24.com/).

Supports downloading both archived ("playback") as well as "real-time" data, and will convert
all units to SI.

# Note

This uses an unofficial and completely unsupported API that can (and has) change at any moment, so try not to abuse it.
Also there are two unknown fields (`unknown1` and `unknown2`) which don't seem important (they're usually zero), but
are still returned.

# Requirements

* Python 2.7 (3.x may also work)
* [requests](http://docs.python-requests.org/en/latest/)

# Usage

Sample usage:

```python
from flightradar import get_current_data

zone = 'full' # downloads current data for every tracked flight in the world!
data = get_current_data(zone) 

print data[0] # ranges in the thousands (e.g. 7,000+) so just print the first flight
```

gives:

```python
{'src': 'HGH', 'squawk': '1306', 'track': 253, 'type': 'A333', 'icao_addr': '78012D', 'reg_num': 'B-HLJ', 'long': 115.46, 'unknown2': 0, 'dest': 'HKG', 'radar': 'T-VHHH21', 'unknown1': 0, 'callsign': 'HDA623', 'time': datetime.datetime(2014, 6, 15, 20, 35, 23), 'flight_num': 'KA623', 'lat': 22.62, 'alt': 8092.4400000000005, 'time_epoch': 1402882523, 'speed': 240.759999792, 'id': '395791a', 'vert_speed': -12.354560000000001}
```

All units are converted to SI (m and m/s) and time stamps are made available as Python `datetime` objects. A list of supported zones can be found [here](http://www.flightradar24.com/js/zones.js.php).

The `get_historical_data()` function can get data from a given time span (going back a few weeks). It supports a callback function which will be passed the above dictionary for every record and can also be used to filter each record by return `True`/`False` if it should be retained.

`get_last_data()` is a helper function that accepts a Python `timedelta` object specifying the time span of data to retrieve, beginning from the current date and time.


# Credit

This is based on some code by @palli found [here](https://github.com/palli/monitor-iceland/blob/master/scripts/dataminers/flightradar24.com.py).
