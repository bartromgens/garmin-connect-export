# Garmin Connect Export

Retrieves rest heart rate and HRV data from Garmin Connect and writes it to a CSV file.

## How to use?

### Get authentication keys
First get an authentication and cookie header by visiting https://connect.garmin.com/modern/home 
and copying the `Authorization` and `Cookie` request headers from a request in the browser developer console 'network' tab.

### Run the script
See `get_stats.py --help` for details.

Example:
```bash
python get_stats.py --start-date 2022-11-16 --fileout=data.csv --auth-header="Bearer XXX" --cookie-header="GARMIN-SSO=1; GarminNoCache=true; XXXX"
```
