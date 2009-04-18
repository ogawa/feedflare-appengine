#!/usr/bin/env python
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch
import json
import urllib

class HatenaHandler(webapp.RequestHandler):
  def get(self):
    path_url = self.request.path_url
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write("""<FeedFlareUnit>
  <Catalog>
    <Title>Save to hatena</Title>
    <Description>Save this item to the hatena bookmarking service.</Description>
  </Catalog>
  <DynamicFlare href="%s/${link}"/>
  <SampleFlare>
    <Text>Save to hatena</Text>
    <Link href="http://b.hatena.ne.jp/entry/{$link}" />
  </SampleFlare>
</FeedFlareUnit>
""" % path_url)

class HatenaFlareHandler(webapp.RequestHandler):
  def get(self, url):
    url = urllib.unquote(url)
    json_url = 'http://b.hatena.ne.jp/entry/json/%s' % url
    result = urlfetch.fetch(json_url)
    count = 0
    if result.status_code == 200:
      content = result.content[1:-1]
      if content != 'null':
        json_obj = json.read(content)
        count = int(json_obj['count'])
    text = 'Save to hatena'
    if count == 1:
      text += ' (' + str(count) + ' save)'
    elif count > 1:
      text += ' (' + str(count) + ' saves)'
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write("""<FeedFlare>
  <Text>%s</Text>
  <Link href="http://b.hatena.ne.jp/entry/%s" />
</FeedFlare>
""" % (text, url))

def main():
  application = webapp.WSGIApplication(
    [
      ('/hatena', HatenaHandler),
      (r'/hatena/(.+)', HatenaFlareHandler),
      ],
    debug=False)
  run_wsgi_app(application)

if __name__ == '__main__':
  main()