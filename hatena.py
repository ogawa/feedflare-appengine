#!/usr/bin/env python
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch
import urllib
import json

class HatenaBookmarkFlare(webapp.RequestHandler):
  def get(self):
    url = self.request.get('url', default_value='')
    if url == '':
      self.get_flare_unit()
    else:
      self.get_flare_item(url)

  def get_flare_unit(self):
    path_url = self.request.path_url
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write("""<FeedFlareUnit>
  <Catalog>
    <Title>Save to hatena bookmark</Title>
    <Description>Save this item to the hatena bookmarking service.</Description>
  </Catalog>
  <DynamicFlare href="%s?url=${link}"/>
  <SampleFlare>
    <Text>Save to hatena bookmark (23 saves)</Text>
    <Link href="http://b.hatena.ne.jp/entry/{$link}" />
  </SampleFlare>
</FeedFlareUnit>
""" % path_url)

  def get_flare_item(self, url):
    count = 0
    json_url = 'http://b.hatena.ne.jp/entry/json/%s' % url
    try:
      result = urlfetch.fetch(json_url)
      if result.status_code == 200:
        content = result.content[1:-1]
        if content != 'null':
          json_obj = json.read(content)
          count = int(json_obj['count'])
    except:
      pass
    text = 'Save to hatena bookmark'
    if count == 1:
      text += ' (%d save)' % count
    elif count > 1:
      text += ' (%d saves)' % count
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write("""<FeedFlare>
  <Text>%s</Text>
  <Link href="http://b.hatena.ne.jp/entry/%s" />
</FeedFlare>
""" % (text, url))

class HatenaBookmarkFlareCompat(HatenaBookmarkFlare):
  def get(self, url):
    url = urllib.unquote(url)
    self.get_flare_item(url)

def main():
  application = webapp.WSGIApplication(
    [
      ('/hatena', HatenaBookmarkFlare),
      ('/hatena/(.+)', HatenaBookmarkFlareCompat),
      ],
    debug=False)
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
