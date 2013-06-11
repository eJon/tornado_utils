#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
__author__ = "Thomas"
__date__ = "2013-05-14"
__desc__ = "json util"
__version__ = "0.1"
"""

import json
import datetime
import decimal

class DataTimeEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")

        return json.JSONEncoder.default(self, obj)
    
class DecimalEncoder(json.JSONEncoder):
    def _iterencode(self, o, markers=None):
        if isinstance(o, decimal.Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return (str(o) for o in [o])
        return super(DecimalEncoder, self)._iterencode(o, markers)
