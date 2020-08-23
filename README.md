# SiteParsers

**Requirements**

* python 3.6
* pandas 1.0.3
* selenium 3.141.0

**Usage**

iem_scraper.py - download weather data in METAR format from http://mesonet.agron.iastate.edu.  

Git clone, import class Loader to project and run function save_station(station)- where station must be specified in the ICAO format.

ParserWiki.py - opens Yandex search bar and inputs request about airport, find wiki site and gets a page with info about airport from wiki, finds and reads table with characteristics.


Git clone, import class ParserWiki to project and run function get_runways(airport) and then parse_html_table(table).


