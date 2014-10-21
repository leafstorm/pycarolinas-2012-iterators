# tornado-gen.py
# adapted from the Tornado documentation

from tornado import gen

TRANSLOC = "http://api.transloc.com/1.1/"
TRANSLOC_AGENCIES = TRANSLOC + "agencies.json"

class TwitterTimeline(RequestHandler):
    @asynchronous
    @gen.engine
    def get(self):
        http_client = AsyncHTTPClient()

        response = yield gen.Task(http_client.fetch,
                                  TRANSLOC_AGENCIES)
        agencies = json.loads(response.body)['data']

        self.render("agencies.html", agencies=agencies)
