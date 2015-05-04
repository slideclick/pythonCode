http://goldb.org/ystockquote.html

http://code.activestate.com/recipes/577989-yahoo-stock-information/



    proxy = urllib2.ProxyHandler({'http': proxyurl})# if you access HTTPS
    auth = urllib2.HTTPBasicAuthHandler()
    opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    
    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, stat)
    return urllib2.urlopen(url).read().strip().strip('"')    