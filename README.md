A Python library to download data from [flightradar24.com](http://www.flightradar24.com/).

Supports downloading both archived ("playback") as well as "real-time" data, and can convert
all units to SI.

# Note

This uses an unofficial and completely unsupported API that can (and has in the past) change at any moment, so try not to abuse it.
Also there are two unknown fields (`unknown1` and `unknown2`) which don't seem important (they're usually zero), but
are still returned.

# Requirements

* Python 2.7 (3.x may also work)
* [requests](http://docs.python-requests.org/en/latest/)

# Usage

Sample usage:

```python
import flightradar

zone = 'full' # gets current data for every tracked flight in the world!
data = flightradar.get_current(zone)

print data.next() # ranges in the thousands (e.g. 7,000+) so just print the first flight
```

gives:

```python
{'src': 'HGH', 'squawk': '1306', 'track': 253, 'type': 'A333', 'icao_addr': '78012D', 'reg_num': 'B-HLJ', 'long': 115.46, 'unknown2': 0, 'dest': 'HKG', 'radar': 'T-VHHH21', 'unknown1': 0, 'callsign': 'HDA623', 'time': datetime.datetime(2014, 6, 15, 20, 35, 23), 'flight_num': 'KA623', 'lat': 22.62, 'alt': 8092.4400000000005, 'time_epoch': 1402882523, 'speed': 240.759999792, 'id': '395791a', 'vert_speed': -12.354560000000001}
```

All units are (optionally) converted to SI (m and m/s) and time stamps are made available as Python `datetime` objects.

## API

* `get_historical()` will get data from a given time span (going back a few weeks) and return an iterator yielding dictionaries as above.

* `get_recent()` is a helper that does the same for a given time span, beginning from the current date and time.

* `get_current()` returns all the current data for a given zone. A list of supported zones can be found [here](http://www.flightradar24.com/js/zones.js.php).

Also see logger.py for some CSV logging functionality.

# Credit

This is based on some code by @palli found [here](https://github.com/palli/monitor-iceland/blob/master/scripts/dataminers/flightradar24.com.py).
