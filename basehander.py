#!/usr/bin/python2.7
#-*-coding:utf-8-*-

"""
Author: Thomas
Date : 2013-05-08
Desc : web base handlers
"""

import tornado.web
import tornado.escape


class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        # return self.get_secure_cookie('uid')
        user_json = self.get_secure_cookie("member_auth")
        if user_json:
            return tornado.escape.json_decode(user_json)
        else:
            return None

    def set_default_headers(self):
        self.set_header('Server', '')

    def form(self, name):
        """"""
        return self.get_argument(name, default=None)
    
    def set_flask(self, status, message):
        """用来处理错误信息"""
        self._flask = {'status' : status, 'msg' : message}
    
    def get_flask(self):
        return self._flask
    
    flask = property(get_flask, set_flask)

    def write_error(self, status_code, **kwargs):
        #handler 404
        if status_code == 404: 
            self.write("Not Found 404 Page") 
            return 
        #hander 405
        if status_code == 405: 
            self.write('method not found') 
            return 
      
        # if status_code == 500: 
        #     self.write('oh, shit happens')
        #     return
