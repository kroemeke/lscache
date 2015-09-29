#!/usr/bin/python
# GPL 2.0
from optparse import OptionParser
import struct
import datetime
import time
import platform
import os
import fnmatch
import re


architecture = platform.architecture()[0]

class disk_cache_header:
  def __init__(self,filename):
    self.filename = filename
    self.file = open(self.filename,'rb')
    self.data = self.file.read()
    version = struct.unpack('i',self.data[0:4])[0]
    if version == 6 or version == 4:
      if architecture == '32bit':
        self.parsed = struct.unpack('iiiiQQQQ',self.data[0:48])
        self.offset = 48
      elif architecture == '64bit':
        self.parsed = struct.unpack('iiQQQQQQ',self.data[0:56])
        self.offset = 56
      else:
        raise SystemExit
    else:
      raise ValueError
  def format(self):
    return self.parsed[0]
  def status(self):
    return self.parsed[1]
  def name_len(self):
    return self.parsed[2]
  def entity_version(self):
    return self.parsed[3]
  def date_epoch(self):
    return self.parsed[4]
  def date(self):
    self.date = datetime.datetime.fromtimestamp(self.parsed[4]/1000000L)
    return self.date
  def expire_epoch(self):
    return self.parsed[5]
  def expire(self):
    self.expire = datetime.datetime.fromtimestamp(self.parsed[5]/1000000L)
    return self.expire
  def request_time_epoch(self):
    return self.parsed[6]
  def request_time(self):
    self.request_time = datetime.datetime.fromtimestamp(self.parsed[6]/1000000L)
    return self.request_time
  def response_time_epoch(self):
    return self.parsed[7]
  def response_time(self):
    self.response_time = datetime.datetime.fromtimestamp(self.parsed[7]/1000000L)
    return self.response_time
  def url(self):
    if self.parsed[0] == 6:
      self.url = struct.unpack(str(self.parsed[2])+'s',self.data[self.offset+64:self.offset+64+self.parsed[2]])
    else:
      self.url = struct.unpack(str(self.parsed[2])+'s',self.data[self.offset:self.offset+self.parsed[2]])
    return self.url[0]
  def all(self):
    if self.parsed[0] == 6:
      self.file.seek(self.offset + self.parsed[2] + 64)
    else:
      self.file.seek(self.offset + self.parsed[2])
    return self.file.read() 


def find_and_list_headers(show_url,show_path,show_status,show_date,show_expire,show_request,show_response,url_search_pattern,show_verbose,header_search_pattern,cachedir,skipexpired):
  counter = 0
  skipped = 0
  if url_search_pattern:
    try:
      pattern = re.compile(url_search_pattern)
    except:
      print "[!] Your regex-fu needs some polishing..."
      raise SystemExit
  if header_search_pattern:
    try:
      hpattern = re.compile(header_search_pattern)
    except:
      print "[!] Your regex-fu needs some polishing..."
      raise SystemExit 
  for path, dirs, files in os.walk(cachedir):
    for filename in fnmatch.filter(files,'*.header'):
      try:
        header = disk_cache_header(os.path.join(path, filename))
      except ValueError:
        continue
      extracted_url = header.url()
      if skipexpired:
        if time.time() > header.expire_epoch()/1000000L:
          skipped += 1 
          continue
        else:
          pass
      if url_search_pattern:
        result = re.search(pattern,extracted_url)
        if result:
          pass
        else:
           skipped += 1
           continue
      if header_search_pattern:
        hresult = re.search(hpattern,header.all())
        if hresult:
          pass
        else:
          skipped += 1
          continue
      if show_url:
        print "[i] %s " % extracted_url,
      if show_status:
        print "%d   " % header.status(),
      if show_path:
        print "%s   " % os.path.join(path, filename),
      if show_date:
        print "%s   " % header.date(),
      if show_expire:
        print "%s   " % header.expire(),
      if show_request:
        print "%s   " % header.request_time(),
      if show_response:
        print "%s   " % header.response_time(),
      if show_verbose:
        print "\n-------------------------\n%s " % header.all(),
      counter += 1
      print 
  print "[?] Found %d headers, %d skipped." % (counter,skipped)



# This is to extract _EVERYTHING_ from a header.
def read_whole_header_and_data(filename):
  try:
    header = disk_cache_header(filename)
    print "[i] File: %s\n[i] URL: %s\n[i] Header version: %d\n[i] HTTP status: %d\n[i] Request date: %s\n[i] Cache expire: %s\n[i] Request time: %s\n[i] Response time: %s\n[i] Header content: \n--- cut ---\n%s\n--- cut ---\n\n" % (filename,header.url(),header.format(),header.status(),header.date(),header.expire(),header.request_time(),header.response_time(),header.all())
    raise SystemExit
  except ValueError:
    print "Unsupported header format."
    raise SystemExit



def main():
  usage = "usage: %prog [options] arg\n\n\tIF YOU HAVE HUGE CACHE - BE CAREFUL (load++)\n"
  parser = OptionParser(usage,version="%prog 0.2")
  parser.add_option("-o","--showpath",dest="showpath",action="store_true",help="show path to each header file",default=False)
  parser.add_option("-s","--status",dest="status",action="store_true",help="display HTTP status code",default=False)
  parser.add_option("-d","--date",dest="date",action="store_true",help="display cache file date",default=False)
  parser.add_option("-l","--skipexpired",dest="skipexpired",action="store_true",help="skip expired headers",default=False)
  parser.add_option("-v","--verbose",dest="verbose",action="store_true",help="display whole request including headers",default=False)
  parser.add_option("-e","--expire",dest="expire",action="store_true",help="display cache file expire date",default=False)
  parser.add_option("-r","--request",dest="request",action="store_true",help="display request time",default=False)
  parser.add_option("-p","--response",dest="response",action="store_true",help="display response time",default=False)
  parser.add_option("-u","--showurl",dest="showurl",action="store_false",help="DON'T display url",default=True)
  parser.add_option("-F","--file",dest="filename",help="read all data from header file")
  parser.add_option("-S","--search",dest="search",help="search inside the header (unlike -P which searches in url)")
  parser.add_option("-P","--pattern",dest="pattern",help="show only headers where url matches this pattern")
  parser.add_option("-C","--cachedir",dest="cachedir",help="specify a non-default cache directory",default='/var/cache/apache2/mod_disk_cache')
  (options,args) = parser.parse_args()
 
  if options.filename:
    read_whole_header_and_data(options.filename) 
  if options.pattern:
    print "[?] searching for %s in url" % options.pattern
  if options.search:
    print "[?] searching for %s in header" % options.search
  find_and_list_headers(options.showurl,options.showpath,options.status,options.date,options.expire,options.request,options.response,options.pattern,options.verbose,options.search,options.cachedir,options.skipexpired)

if __name__ == "__main__":
  main()
