#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import threading
import redis
import tornado.web


class OpenChannel(threading.Thread):

    def __init__(self, channel, host=None, port=None):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.redis = redis.StrictRedis(host=host or 'localhost', port=port or 6379)
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channel)

        self.output = []

    # lets implement basic getter methods on self.output, so you can access it like a regular list
    def __getitem__(self, item):
        with self.lock:
            return self.output[item]

    def __getslice__(self, start, stop=None, step=None):
        with self.lock:
            return self.output[start:stop:step]

    def __str__(self):
        with self.lock:
            return self.output.__str__()

    # thread loop
    def run(self):
        for message in self.pubsub.listen():
            with self.lock:
                self.output.append(message['data'])

    def stop(self):
        self._Thread__stop()


# add a method to the application that will return existing channels
# or create non-existing ones and then return them
class ApplicationMixin(object):

    def GetChannel(self, channel, host=None, port=None):
        if channel not in self.application.channels:
            self.application.channels[channel] = OpenChannel(channel, host, port)
            self.application.channels[channel].start()
        return self.application.channels[channel]


class ReadChannel(tornado.web.RequestHandler, ApplicationMixin):

    @tornado.web.asynchronous
    def get(self, channel):
        # get the channel
        channel = self.GetChannel(channel)
        # write out its entire contents as a list
        self.write('{}'.format(channel[:]))
        self.finish()  # not necessary?


class GetHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("Hello world")


application = tornado.web.Application([
    (r"/", GetHandler),
    (r"/channel/(?P<channel>\S+)", ReadChannel),
])

# add a dictionary containing channels to your application
application.channels = {}

if __name__ == '__main__':
    application.listen(8888)
    print 'running'
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass

    # clean up the subscribed channels
    for channel in application.channels:
        application.channels[channel].stop()
        application.channels[channel].join()
