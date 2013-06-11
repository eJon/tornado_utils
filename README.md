tornado_utils
==============

some tornado utils helper


### [routes](https://github.com/thomashuang/tornado_utils/blob/master/route.py)

Here's a simple example.

    import tornado.web
    from route import route
    
    route.inithandlercls(BaseHandler)
    get = route.get
    post = route.post

    @get(r'/list')
    def list(self):
      self.write("list")

    @route('/blah')
    class SomeHandler(tornado.web.RequestHandler):
        pass

    t = tornado.web.Application(route.get_routes(), {'some app': 'settings'}
