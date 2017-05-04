import urlparse
import re

url = 'http://active.yueyin99.com/20170427ppbs/index.html'
print urlparse.urlparse(url)

url = 'http://69.46.86.252/max/3dsmax2014chinese-english64bit.rar'
print urlparse.urlparse(url)

pre_suffixPattern = re.compile(r"^http.*(?<!css|\.js|ico|png|gif|jpg|png|xml)$", re.I)
print re.match(pre_suffixPattern, url)

suffixPattern = re.compile(r"^http.*(?<=\.zip|\.rar|\.exe|\.apk|\.sis|sisx|\.jar|\.cab)$", re.I)
print True if re.match(suffixPattern, url) else False