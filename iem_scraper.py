#!/usr/bin/env python
# coding: utf-8

# In[42]:


from __future__ import print_function
import json
import time
import datetime
import argparse


# In[43]:


import pandas as pd
import numpy as np


# In[44]:


try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

# Number of attempts to download data
#MAX_ATTEMPTS = 6
# HTTPS here can be problematic for installs that don't have Lets Encrypt CA
#SERVICE = "http://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?"


# In[61]:


class Loader:
    def __init__(self, MAX_ATTEMPTS, SERVICE):
        self.max_attemps = MAX_ATTEMPTS
        self.service = SERVICE
    
    def get_date(self, start = [2012, 1, 1], end = [2020, 2, 20]):
        self.startts = datetime.datetime(start[0], start[1], start[2])
        self.endts = datetime.datetime(end[0], end[1], end[2])
        
        self.serv = self.service + "data=all&tz=Etc/UTC&format=comma&latlon=yes&"

        self.serv += self.startts.strftime("year1=%Y&month1=%m&day1=%d&")
        self.serv += self.endts.strftime("year2=%Y&month2=%m&day2=%d&")
    
    def download_data(self, uri):
        """Fetch the data from the IEM
        The IEM download service has some protections in place to keep the number
        of inbound requests in check.  This function implements an exponential
        backoff to keep individual downloads from erroring.
        Args:
          uri (string): URL to fetch
        Returns:
          string data
        """
        attempt = 0
        while attempt < self.max_attemps:
            try:
                data = urlopen(uri, timeout=300).read().decode("utf-8")
                if data is not None and not data.startswith("ERROR"):
                    return data
            except Exception as exp:
                print("download_data(%s) failed with %s" % (uri, exp))
                time.sleep(5)
            attempt += 1

        print("Exhausted attempts to download, returning empty data")
        return ""
    
    
    def save_station(self, station):
        uri = "%s&station=%s" % (self.serv, station)
        self.data = self.download_data(uri)
        outfn = "%s_%s_%s.txt" % (
            station,
            self.startts.strftime("%Y%m%d%H%M"),
            self.endts.strftime("%Y%m%d%H%M"),
        )
        print("Open file:")
        out = open(outfn, "w")
        out.write(self.data)
        out.close()
    def get_excel(self, name):
        pass
        
        
    
        

