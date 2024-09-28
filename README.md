# Garmin Connect Export

Retrieves rest heart rate and HRV data from Garmin Connect and writes it to a CSV file.

Example output file:
|date|rest heart rate|HRV|
|----|---------------|---|
|2022-11-16|46|30|
|2022-11-17|44|55|
|2022-11-18|48|46|
|2022-11-19|49|37|

## How to use?

### Get authentication keys
First get an authentication and cookie header by visiting https://connect.garmin.com/modern/home 
and copying the `Authorization` and `Cookie` request headers from a `userAuthorization` request in the browser developer console 'Network' tab.

### Run the script
See `garmin_export.py --help` for details.

Example:
```bash
python garmin_export.py --start-date 2022-11-16 --fileout=data.csv --auth-header="Bearer XXX" --cookie-header="GARMIN-SSO=1; GarminNoCache=true; XXXX"
```

## Alternatives

- [Garth](https://github.com/matin/garth)
