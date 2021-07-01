# Aurora+ Library

## Usage

AuroraPlus.py requires requests.py to run.

## Examples
```sh

AuroraPlus = api("username", "password", "timespan")

AuroraPlus = api("user.name@outlook.com", "password", "day")

if (not AuroraPlus.Error):
    print(AuroraPlus.AmountOwed)
else:
    print(AuroraPlus.Error)

```
Supported Timespans
```sh
day
week
month
quarter
year
```

## License

MIT