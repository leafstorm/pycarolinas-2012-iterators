# tornado-async.py
# from the Tornado documentation

TRANSLOC = "http://api.transloc.com/1.1/"
TRANSLOC_AGENCIES = TRANSLOC + "agencies.json"

class TwitterTimeline(RequestHandler):
    @asynchronous
    def get(self):
        http_client = AsyncHTTPClient()
        http_client.fetch(TRANSLOC_AGENCIES,
                          callback=self.on_fetch)

    def on_fetch(self, response):
        agencies = json.loads(response.body)['data']

        self.render("agencies.html", agencies=agencies)

