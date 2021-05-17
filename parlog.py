#!/usr/local/bin/python3.7
import re
from os import environ
from json import load
from urllib.request import urlopen

environ['LANG']   = 'en_US.utf8'
environ['LC_ALL'] = 'en_US.utf8'

# file name to parse out IPs
Infile = "/var/log/filter.log"

##############################################
def ipInfo(addr='', count=0):
    if addr == '':
        return 
    else:
        url = 'https://ipinfo.io/' + addr + '/json'
    try:
        res = urlopen(url)
    except:
        print ('%4d: %-18s   Unable to obtain info (likely due to monthly limit).' % (count, addr))
        return;
    #response from url(if res==None then check connection)
    data = load(res)
    s = '%4d: %-18s'  % (count, data['ip'])
    if 'city' in data:
        s += '%-25s'  % (data['city'])
    else:
        s+= '%-25s'  % (' ')
    if 'region' in data:
        s += '%-25s' %  (data['region'])
    else:
        s += '%-25s' % (' ')
    if 'country' in data:
        s +=  '%-6s' % (data['country'])
    else:
        s +=  '%-6s' % (' ')
    if 'org' in data:
        s += data['org']
    print (s)

##############################################
# opening and reading the file
with open(Infile) as fh:
   fstring = fh.readlines()
# decalring the regex pattern for IP addresses
pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
# initializing the list object
lst = []
s   = ''
# extracting the IP addresses
for line in fstring:
    m  = pattern.search(line)
    if m is not None:
        s = m.group(1)
        lst.append (s)
cdict = {i:lst.count(i) for i in lst}
for key in cdict:
    ipInfo (key, cdict[key])    # get ip information (IP, count of IP if file).

