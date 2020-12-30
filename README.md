# Scrape Reserve America

Scrape Reserve America for your favorite campsite.  Scraper crawls over a config file with campsites, and preferred sites identified (if desired).

Modified from:  [streeter/reserve-america-scraper](https://github.com/streeter/reserve-america-scraper).

## Setup

Set up config.py.  Enter date, length of stay and RV length, and campground urls, in this format: [https://floridastateparks.reserveamerica.com/camping/manatee-springs-sp/r/campgroundDetails.do?contractCode=FL&parkId=28105](https://floridastateparks.reserveamerica.com/camping/manatee-springs-sp/r/campgroundDetails.do?contractCode=FL&parkId=281053).

If you want to use email notification via gmail, create a `secrets.py` file like:
```
email=phil@aol.com
password=abc123
```

For new york, an additional script `getWaterSites.py` scrapes campadk.com to find a list of waterfront campsites

## Usage

Run the script like so:

```sh
./scraper.py
```

Or put in a cron:

```sh
*/10 * * * * /usr/bin/python3 /home/pi/reserve-america-scraper/scraper.py
```
