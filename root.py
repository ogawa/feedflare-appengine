#!/usr/bin/env python
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class RootHandler(webapp.RequestHandler):
  def get(self):
    path_url = self.request.path_url
    self.response.out.write("""
<html>
<body>
<h1>FeedFlare-AppEngine</h1>

<dl>
<dt>code</dt><dd><a href="http://code.google.com/p/feedflare-appengine/">feedflare-appengine - Google Code</a></dd>
<dt>maintainer</dt><dd><a href="http://blog.as-is.net/">Hirotaka Ogawa</a></dd>
</dl>

<h2>FeedFlare Catalog</h2>
<ul>
<li><a href="%shatena">Hatena Bookmark</a></li>
<li><a href="%slivedoor">Livedoor Clip</a></li>
</ul>
</body>
</html>
""" % (path_url, path_url))

def main():
  application = webapp.WSGIApplication(
    [
      ('/', RootHandler),
      ],
    debug=False)
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
