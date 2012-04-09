#!/usr/bin/env python2.7
# Waktu Solat Kuala Lumpur Checker
# Pihak pengguna bertanggungjawab sepenuhnya keatas penggunaan skrip ini
# 
# oleh Hakim' : 'akimrr {at} gmail {dor} com
# 
# Changelog
# + Isnin, 9 April 2012
#  - Prototaip dilancar
#  - Opsyen lokasi ditambah
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
import getopt
import string
import os.path

try:
    from BeautifulSoup import BeautifulSoup
except:
    print "Need BeautifulSoup 3"
    exit(1)

kod = {
    'JHR04' : 'Batu Pahat, Muar, Segamat, Gemas, JOHOR',
    'JHR03' : 'Kluang dan Pontian, JOHOR',
    'JHR02' : 'Kota Tinggi, Mersing, Johor Bahru, JOHOR',
    'JHR01' : 'Pulau Aur dan Pemanggil, JOHOR',
    'KDH01' : 'Kota Setar, Kubang Pasu, Pokok Sena, KEDAH',
    'KDH04' : 'Kulim, Bandar Baharu, KEDAH',
    'KDH05' : 'Langkawi, KEDAH',
    'KDH03' : 'Padang Terap, Sik, Baling, KEDAH',
    'KDH02' : 'Pendang, Kuala Muda, Yan, KEDAH',
    'KDH06' : 'Puncak Gunung Jerai, KEDAH',
    'KTN03' : 'Jeli, Gua Musang (Mukim Galas, Bertam), Kelantan',
    'KTN01' : 'K.Bharu,Bachok,Pasir Puteh,Tumpat,Pasir Mas,Tnh. Merah,Machang,Kuala Krai,Mukim Chiku, Kelantan',
    'MLK01' : 'Bandar Melaka, Alor Gajah, Jasin, Masjid Tanah, Merlimau, Nyalas, MELAKA',
    'NGS01' : 'Jempol, Tampin, NEGERI SEMBILAN',
    'NGS02' : 'Port Dickson, Seremban, Kuala Pilah, Jelebu, Rembau, NEGERI SEMBILAN',
    'PHG04' : 'Bentong, Raub, Kuala Lipis, PAHANG',
    'PHG06' : 'Bukit Fraser, Genting Higlands, Cameron Higlands, PAHANG',
    'PHG05' : 'Genting Sempah, Janda Baik, Bukit Tinggi, PAHANG',
    'PHG02' : 'Kuantan, Pekan, Rompin, Muadzam Shah, PAHANG',
    'PHG03' : 'Maran, Chenor, Temerloh, Bera, Jerantut, PAHANG',
    'PHG01' : 'Pulau Tioman, PAHANG',
    'PRK07' : 'Bukit Larut, PERAK',
    'PRK02' : 'Ipoh, Batu Gajah, Kampar, Sg. Siput dan Kuala Kangsar, PERAK',
    'PRK03' : 'Pengkalan Hulu, Grik dan Lenggong, PERAK',
    'PRK06' : 'Selama, Taiping, Bagan Serai dan Parit Buntar, PERAK',
    'PRK01' : 'Tapah,Slim River dan Tanjung Malim, PERAK',
    'PRK05' : 'Teluk Intan, Bagan Datoh, Kg.Gajah,Sri Iskandar, Beruas,Parit,Lumut,Setiawan dan Pulau Pangkor, PERAK',
    'PRK04' : 'Temengor dan Belum, PERAK',
    'PLS01' : 'Kangar, Padang Besar, Arau, PERLIS',
    'PNG01' : 'Seluruh Negeri Pulau Pinang, PULAU PINANG',
    'SBH01' : 'Zon 1 - Sandakan, Bdr. Bkt. Garam, Semawang, Temanggong, Tambisan, Sabah',
    'SBH02' : 'Zon 2 - Pinangah, Terusan, Beluran, Kuamut, Telupit, Sabah',
    'SBH03' : 'Zon 3 - Lahad Datu, Kunak, Silabukan, Tungku, Sahabat, Semporna, Sabah',
    'SBH04' : 'Zon 4 - Tawau, Balong, Merotai, Kalabakan, Sabah',
    'SBH05' : 'Zon 5 - Kudat, Kota Marudu, Pitas, Pulau Banggi, Sabah',
    'SBH06' : 'Zon 6 - Gunung Kinabalu, Sabah',
    'SBH07' : 'Zon 7 - Papar, Ranau, Kota Belud, Tuaran, Penampang, Kota Kinabalu, Sabah',
    'SBH08' : 'Zon 8 - Pensiangan, Keningau, Tambunan, Nabawan, Sabah',
    'SBH09' : 'Zon 9 - Sipitang, Membakut, Beaufort, Kuala Penyu, Weston, Tenom, Long Pa Sia, Sabah',
    'SWK01' : 'Zon 1 - Limbang, Sundar, Terusan, Lawas, Sarawak',
    'SWK02' : 'Zon 2 - Niah, Belaga, Sibuti, Miri, Bekenu, Marudi, Sarawak',
    'SWK03' : 'Zon 3 - Song, Belingan, Sebauh, Bintulu, Tatau, Kapit, Sarawak',
    'SWK04' : 'Zon 4 - Igan, Kanowit, Sibu, Dalat, Oya, Sarawak',
    'SWK05' : 'Zon 5 - Belawai, Matu, Daro, Sarikei, Julau, Bitangor, Rajang, Sarawak',
    'SWK06' : 'Zon 6 - Kabong, Lingga, Sri Aman, Engkelili, Betong, Spaoh, Pusa, Saratok, Roban, Debak, Sarawak',
    'SWK07' : 'Zon 7 - Samarahan, Simunjan, Serian, Sebuyau, Meludam, Sarawak',
    'SWK08' : 'Zon 8 - Kuching, Bau, Lundu,Sematan, Sarawak',
    'SGR01' : 'Gombak,H.Selangor,Rawang,H.Langat,Sepang,Petaling,S.Alam, SELANGOR DAN WILAYAH PERSEKUTUAN',
    'SGR03' : 'Kuala Lumpur, SELANGOR DAN WILAYAH PERSEKUTUAN',
    'SGR04' : 'Putrajaya, SELANGOR DAN WILAYAH PERSEKUTUAN',
    'SGR02' : 'Sabak Bernam, Kuala Selangor, Klang, Kuala Langat, SELANGOR DAN WILAYAH PERSEKUTUAN',
    'TRG02' : 'Besut, Setiu, Terengganu',
    'TRG03' : 'Hulu Terengganu, Terengganu',
    'TRG04' : 'Kemaman Dungun, Terengganu',
    'TRG01' : 'Kuala Terengganu, Marang, Terengganu',
    'WLY02' : 'Labuan, WILAYAH PERSEKUTUAN LABUAN'
}
    
class waktuSolat:
    def __init__(self, kawasan, solat, jam):
        self.kawasan = kawasan
        self.waktu = solat
        self.jam = jam
        
    def view(self):
        return '%s - %s' % (self.waktu, self.jam)

def process(location):
    
    url = 'http://www.e-solat.gov.my/bar_left.php?kod=' + location
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
        
        list.append(waktuSolat(location, solat, jam))
        j = j + 1
        
    return list

def usage():
    print "Usage: -c <code>"
    print "For location codes refer to README"
    print "If no option is used, location will automatically set to Kuala Lumpur"

def main():
    
    opts, args = getopt.getopt(sys.argv[1:], 'c:', ['code='])
    
    location = None
    
    for opt, arg in opts:
        if opt in ('-c', '--code'):
            if arg is None:
                location = 'SGR03'
            else:
                if (arg in kod) is False:
                    print "Error on your location code, please refer to README"
                    return 0
                else:
                    location = string.upper(arg)
                                
    if location is None:
        location = 'SGR03'
        
    item = process(location)
    
    if item:
        kawasan = kod[location]
        print 'Kawasan: ', kawasan
        for i in item:
            print i.view()
            
            
    else:
        print "Error!"
        return 1

if __name__ == '__main__':
    main()
