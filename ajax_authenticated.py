#!/usr/bin/python2.7
#-*-coding:utf-8-*-


def ajax_authenticated(method):
    """Decorate methods with this to require that the user be logged in.

    If the user is not logged in, it will send User Authenticated Failed to cilent
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            if self.request.method in ("GET", "HEAD"):
                self.write({"status": "error", "msg": "User Authenticated Failed"})
                return
            raise tornado.web.HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper
