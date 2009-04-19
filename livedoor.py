#!/usr/bin/env python
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch
import json

class LivedoorClipHandler(webapp.RequestHandler):
  def get(self):
    path_url = self.request.path_url
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write("""<FeedFlareUnit>
  <Catalog>
    <Title>Save to livedoor clip</Title>
    <Description>Save this item to the "livedoor clip" bookmarking service.</Description>
  </Catalog>
  <DynamicFlare href="%s/${link}"/>
  <SampleFlare>
    <Text>Save to livedoor clip</Text>
    <Link href="http://clip.livedoor.com/redirect?link={$link}" />
  </SampleFlare>
</FeedFlareUnit>
""" % path_url)

class LivedoorClipItemHandler(webapp.RequestHandler):
  def get(self, url):
    count = 0
    json_url = 'http://api.clip.livedoor.com/json/comments?link=%s' % url
    try:
      result = urlfetch.fetch(json_url)
      if result.status_code == 200:
        content = result.content
        json_obj = json.read(content)
        if json_obj['isSuccess'] == 1:
          count = int(json_obj['total_clip_count'])
    except:
      pass
    text = 'Save to livedoor clip'
    if count == 1:
      text += ' (%d save)' % count
    elif count > 1:
      text += ' (%d saves)' % count
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write("""<FeedFlare>
  <Text>%s</Text>
  <Link href="http://clip.livedoor.com/redirect?link=%s" />
</FeedFlare>
""" % (text, url))

def main():
  application = webapp.WSGIApplication(
    [
      ('/livedoor', LivedoorClipHandler),
      (r'/livedoor/(.+)', LivedoorClipItemHandler),
      ],
    debug=False)
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
