# lscache
Apache mod_cache file inspection tool

Example session may look like this :

dft:~# lscache --help
Usage: lscache [options] arg

        IF YOU HAVE HUGE CACHE - BE CAREFUL (load++)


Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -o, --showpath        show path to each header file
  -s, --status          display HTTP status code
  -d, --date            display cache file date
  -l, --skipexpired     skip expired headers
  -v, --verbose         display whole request including headers
  -e, --expire          display cache file expire date
  -r, --request         display request time
  -p, --response        display response time
  -u, --showurl         DON'T display url
  -F FILENAME, --file=FILENAME
                        read all data from header file
  -S SEARCH, --search=SEARCH
                        search inside the header (unlike -P which searches in
                        url)
  -P PATTERN, --pattern=PATTERN
                        show only headers where url matches this pattern
  -C CACHEDIR, --cachedir=CACHEDIR
                        specify a non-default cache directory
dft:~# lscache -s -d -e -P '.*php.txt?'
[?] searching for .*php.txt? in url
[i] http://kroemeke.eu:80/php.txt?  200    2012-02-22 21:10:57    2012-02-23 21:10:57   
[?] Found 1 headers, 6 skipped.
dft:~# lscache -s -d -e -v -P '.*php.txt?'
[?] searching for .*php.txt? in url
[i] http://kroemeke.eu:80/php.txt?  200    2012-02-22 21:10:57    2012-02-23 21:10:57    
-------------------------
Last-Modified: Tue, 24 May 2011 17:26:11 GMT
ETag: "2908018-1c78-4a408e258b2c0"
Accept-Ranges: bytes
Cache-Control: max-age=86400, public
Expires: Thu, 23 Feb 2012 21:10:57 GMT
Vary: Accept-Encoding
Content-Encoding: gzip
Content-Type: text/plain

Host: kroemeke.eu
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:8.0) Gecko/20100101 Firefox/8.0 Iceweasel/8.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-us,en;q=0.5
Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7
X-Forwarded-For: 109.154.6.17
X-Varnish: 582572148
Accept-Encoding: gzip

 
[?] Found 1 headers, 6 skipped.
dft:~# lscache -s -d -e  -S '.*Gecko/20100101.*'
[?] searching for .*Gecko/20100101.* in header
[i] http://kroemeke.eu:80/gallery.html?  200    2012-02-22 21:10:32    2012-02-22 21:15:32   
[i] http://kroemeke.eu:80/projects.html?  200    2012-02-22 21:09:36    2012-02-22 21:14:36   
[i] http://kroemeke.eu:80/documents.html?  200    2012-02-22 21:10:31    2012-02-22 21:15:31   
[i] http://kroemeke.eu:80/lscache.html?  200    2012-02-22 21:09:38    2012-02-22 21:14:38   
[i] http://kroemeke.eu:80/index.html?  200    2012-02-22 21:10:36    2012-02-22 21:15:36   
[i] http://kroemeke.eu:80/php.txt?  200    2012-02-22 21:10:57    2012-02-23 21:10:57   
[i] http://kroemeke.eu:80/links.html?  200    2012-02-22 21:10:33    2012-02-22 21:15:33   
[?] Found 7 headers, 0 skipped.
dft:~# 

