#!/usr/bin/python2.7
#-*-coding:utf-8-*-

"""
__author__ = "Thomas"
__date__ = "2013-05-16"
__desc__ = "handler route RSETFUL"
__version__ = "0.1"
"""

import tornado.web

class route:
    """
    decorates RequestHandlers and builds up a list of routables handlers

    Tech Notes (or "What the *@# is really happening here?")
    --------------------------------------------------------

    Everytime @route('...') is called, we instantiate a new route object which
    saves off the passed in URI.  Then, since it's a decorator, the function is
    passed to the route.__call__ method as an argument.  We save a reference to
    that handler with our uri in our class level routes list then return that
    class to be instantiated as normal.

    Later, we can call the classmethod route.get_routes to return that list of
    tuples which can be handed directly to the tornado.web.Application
    instantiation.

    Example
    -------
    route.inithandlercls(BaseHandler)
    get = route.get
    post = route.post

    @get(r'/list')
    def list(self):
    self.write("list")
    
    @route("/index")
    class AjaxHandler(BaseHandler):
        def get(self):
            self.write("index")

    my_routes = route.get_routes()

    Credit
    -------
    Jeremy Kelley - initial work
    Peter Bengtsson - redirects, named routes and improved comments
    Ben Darnell - general awesomeness
    Thomas Huang - add get post function like handler
    """

    _routes = []

    @classmethod
    def inithandlercls(cls, handlercls):
        cls.BaseHandler = handlercls

    def __init__(self, uri):
        self._uri = uri

    def __call__(self, _handler):
        """gets called when we class decorate"""
        self._routes.append((self._uri, _handler))
        return _handler

    @classmethod
    def get(cls, route):
        def make_handler (handle, *args, **kwargs):
            class Handler (cls.BaseHandler):
                @tornado.web.authenticated
                def get (self, *args, **kwargs):
                    handle(self, *args, **kwargs)
            cls._routes.append((route, Handler))
            return Handler
        return make_handler

    @classmethod
    def post(cls, route):
        def make_handler (handle, *args, **kwargs):
            class Handler (cls.BaseHandler):
                @tornado.web.authenticated
                def post (self, *args, **kwargs):
                    handle(self, *args, **kwargs)
            cls._routes.append((route, Handler))
            return Handler
        return make_handler

    @classmethod
    def get_routes(cls):
        return cls._routes

# route_redirect provided by Peter Bengtsson via the Tornado mailing list
# and then improved by Ben Darnell.
# Use it as follows to redirect other paths into your decorated handler.
#
#   from routes import route, route_redirect
#   route_redirect('/smartphone$', '/smartphone/')
#   route_redirect('/iphone/$', '/smartphone/iphone/', name='iphone_shortcut')
#   @route('/smartphone/$')
#   class SmartphoneHandler(RequestHandler):
#        def get(self):
#            ...


def route_redirect(from_, to, name=None):
    route._routes.append(tornado.web.url(
        from_,
        tornado.web.RedirectHandler,
        dict(url=to),
        name=name ))
