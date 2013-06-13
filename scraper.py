""" Dainik Bhaskar Scraper.

Currently fetches pages only for Bhopal City edition.
Automatically figures out the url as well as number of pages.
Usage:
To fetch all pages of between June 01 to June 10, 2013.
python scraper.py --startdate=01062013 --enddate=10062013

"""

import sys
import os
import urllib2
from datetime import date
from datetime import datetime
from datetime import timedelta
from optparse import OptionParser

def GetCityTag(city_name):
  raise NotImplementedError

def GetUrl(date, city_tag, page_number):
  assert type(date) == datetime, 'type(date) is %s' %str(type(date))
  assert ' ' not in city_tag
  page_number = '%d' % page_number
  # Date in DDMMYYYY format.
  date_str = date.strftime('%d%m%Y')
  # For some reason previous day (eg. 31 in case of 01 is used as a part of url).
  previous_day = (date + timedelta(days=-1)).strftime('%d')
  if previous_day[0] == '0':
    previous_day = previous_day[1:]
  url = 'http://digitalimages.bhaskar.com/mpcg/epaperpdf/%s/%s%s-PG%s-0.PDF' %(
      date_str, previous_day, city_tag, page_number)
  return url

def FetchUrl(url, filename):
  try:
    result = urllib2.urlopen(url)
    # Deal with crappy redirection.
    if result.getcode() == 200 and result.geturl().upper() == url.upper():
#import pdb; pdb.set_trace()
      data = result.read()
      open(filename, 'w').write(data)
      print 'Wrote page %s to file %s' %(url, filename)
#import pdb; pdb.set_trace()
      return True
    else:
      print 'resultcode for url %s is %d' %(url, result.getcode()) 
      print 'url: %s,\ngeturl:%s' %(url, result.geturl())
      print 'may be we past the last page?'
      return False
  except urllib2.URLError, e:
    print 'Fetch failed: ',
    print str(e),
    print 'may be we past the last page?'
    return False

def GetFilename(city_tag, iteratedate, page_number):
  if page_number < 10:
    page_number = '0%d' % page_number
  else:
    page_number = '%d' % page_number
  return './data/' + city_tag.replace('%20', '_') + '_' + iteratedate.strftime('%d%m%Y') + '_' + page_number + '.pdf'

def FetchPages(startdate_str, enddate_str):
  """As of now, fetches pages only for the "BHOPAL CITY". """
  city_tag = 'BHOPAL%20CITY'
  startdate = datetime.strptime(startdate_str, '%d%m%Y')
  enddate = datetime.strptime(enddate_str, '%d%m%Y')
  if not os.path.exists('./data'):
    os.mkdir('./data')  # location to write pages to.
  print 'Fetchign pages between date %s and %s' %(startdate_str, enddate_str)
  iteratedate = startdate
  while iteratedate <= enddate:
    print 'Fetching pages for date %s' % iteratedate.strftime('%d%m%Y')
    page_number = 1
    while True:
      url = GetUrl(iteratedate, city_tag, page_number)
      filename = GetFilename(city_tag, iteratedate, page_number)
#      print 'Fetching %s' % url
      if not FetchUrl(url, filename):
        # Fetch till we get an error then we are on last page.
        break
#      print 'Done fetching %s' % url
      page_number += 1
    iteratedate = iteratedate + timedelta(days=1)


def main(argv=sys.argv):
  parser = OptionParser()
  parser.add_option('-s', '--startdate', dest='startdate', help='Start date to fetch from (DDMMYYYY format)')
  parser.add_option('-e', '--enddate', dest='enddate', help='End date to fetch from (default:start date)')
  (options, args) = parser.parse_args()
#import pdb; pdb.set_trace()
  assert options.startdate, 'Please pass --startdate.'
  if options.enddate is None:
    options.enddate = options.startdate
  assert len(options.startdate) == 8, '--startdate should be in DDMMYYYY format.'
  assert len(options.enddate) == 8, '--enddate should be in DDMMYYYY format.'
  FetchPages(options.startdate, options.enddate)

if __name__ == '__main__':
  main()
