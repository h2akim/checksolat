#!/usr/bin/env python2.7
# Waktu Solat Kuala Lumpur Checker
# Pihak pengguna bertanggungjawab sepenuhnya keatas penggunaan skrip ini
# 
# oleh Hakim - akimrr {at} gmail {dor} com
# 
# Changelog
# + Isnin, 9 April 2012
#   - Prototaip dilancar
#
# ------------------------------------------------------------------------
#
#  This program is free software. It comes without any warranty, to
#  the extent permitted by applicable law. You can redistribute it
#  and/or modify it under the terms of the Do What The Fuck You Want
#  To Public License, Version 2, as published by Sam Hocevar. See
#  http://sam.zoy.org/wtfpl/COPYING for more details.
#
# ------------------------------------------------------------------------

import re
import urllib2
import sys
import string
import os.path

try:
    from BeautifulSoup import BeautifulSoup
except:
    print "Need BeautifulSoup 3"
    exit(1)

def main():
    url = 'http://www.e-solat.gov.my/bar_left.php'
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'
        }
  
    request = urllib2.Request(url, None, headers)
  
    list = []
    
    document = urllib2.urlopen(request)
  
    soup = BeautifulSoup(document)
  	
    waktu = ['Imsak', 'Subuh', 'Syuruk', 'Zohor', 'Asar', 'Maghrib', 'Isyak']
  	
    solatWaktu = soup.findAll('font', size="2", face="Tahoma", color="#000000")
  	
    j = 0;
    for i in solatWaktu:
        solat = waktu[j]
        jam = i.renderContents()
        print solat, "-", jam
        j = j + 1

if __name__ == '__main__':
    main()
