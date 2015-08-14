#!/user/bin/env python
#coding: utf-8

import os
import sys
import time
import math
import ConfigParser

reload(sys)
sys.setdefaultencoding('utf8')

class TimeFactor:
    def __init__(self, start, end, factor):
        self.is_default = (end == "+")
        self.start = float(start)
        if not self.is_default:
            self.end = float(end)
        self.factor = float(factor)

    def is_match(self, hour):
        hour = float(hour)
        if not self.is_default:
            return (self.start <= hour < self.end)
        else:
            return (self.start <= hour)

    def get_factor(self):
        return self.factor

class HotPicCalculator:
    """
    热度图片计算类
    """
    def __init__(self, timestamp):
        self.is_inited = False
        self.time_factors = []
        self.timestamp = int(timestamp)
    
    def load_conf(self, conf_file):
        cf = ConfigParser.ConfigParser()
        cf.read(conf_file)
        self.a = cf.getfloat("fixed", "a")
        self.b = cf.getfloat("fixed", "b")
        self.c = cf.getfloat("fixed", "c")
        self.d = cf.getfloat("fixed", "d")
        self.e = cf.getfloat("fixed", "e")
        self.f = cf.getfloat("fixed", "f")
        self.x = cf.getfloat("fixed", "x")

        time_factors = cf.options("time_factor")
        for factor in time_factors:
            hour = cf.get(factor, "hour")
            (start, end) = self._parse_hour_section(hour)
            factor = cf.getfloat(factor, "t")
            self.time_factors.append(TimeFactor(start, end, factor))

        self.is_inited = True

    def get_score(self, zan_num, comment_num, share_num, base, c_time):
        if not self.is_inited:
            return 1
        t = self._get_t(c_time)
        numerator = self.a * int(zan_num) + self.b * int(comment_num) + self.c * int(share_num)
        numerator += self.d
        denominator = math.pow(t + self.e, self.x)
        score = numerator / denominator * self.f + float(base)
        return score

    def _parse_hour_section(self, hour):
        hour_list = hour.split(",")
        return (hour_list[0], hour_list[1])

    def _get_hour_from_now(self, c_time):
        return int((self.timestamp - int(c_time))/3600)

    def _get_t(self, c_time):
        if not self.is_inited or len(self.time_factors) == 0:
            return 0
        hour = self._get_hour_from_now(c_time)
        sec = 0
        for factor in self.time_factors:
            if factor.is_match(hour):
                return factor.get_factor()
            sec += 1
        return 0

if __name__ == "__main__":
    cal = HotPicCalculator("1438499047")
    cal.load_conf("../conf/calculate_hot_pic.conf")
    print cal._get_t("1438499000")
    print cal.get_score(1, 2, 3, "100", "1438499000")
    print cal._get_t("1438495000")
    print cal.get_score(1, 2, 3, "100", "1438495000")
    print cal._get_t("1435466682")
    print cal.get_score(1, 2, 3, "100", "1435466682")
