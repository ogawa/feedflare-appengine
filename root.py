#!/usr/bin/env python
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class RootHandler(webapp.RequestHandler):
  def get(self):
    path_url = self.request.path_url
    self.response.out.write("""
<h1>Experimental FeedFlares</h1>

<ul>
<li><a href="%shatena">Hatena Bookmark</a></li>
</ul>

<p>maintained by <a href="http://blog.as-is.net/">Hirotaka Ogawa</a></p>
""" % path_url)

def main():
  application = webapp.WSGIApplication(
    [
      ('/', RootHandler),
      ],
    debug=False)
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
