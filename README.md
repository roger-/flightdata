A Python library to download data from [flightradar24.com](http://www.flightradar24.com/).

Supports downloading both archived ("playback") as well as "real-time" data, and will convert
all units to SI.

# Note

This uses an unofficial API that can (and has) change at any moment, so try not to abuse it.
Also there are two unknown fields (`unknown1` and `unknown2`) which don't seem important, but
are still returned.

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

All units are converted to SI (m and m/s) and a list of zones can be found [here](http://www.flightradar24.com/js/zones.js.php).

The `get_historical_data()` method can get data beginning from a certain data (going back a few weeks) and also supports a callback function which will be passed the above dictionary for every record.
