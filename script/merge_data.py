#! /usr/bin/env python
#coding:utf-8
import json
import logging
import traceback
import sys
import codecs
import time
import hot_pic_calculator 

reload(sys)
sys.setdefaultencoding('utf-8')
class Tweet(object):
    def __init__(self):
        self.tid = 0
        self.uid = 0
        self.zan_num = 0
        self.comment_num = 0
        self.share_num = 0
        self.desc = []
        self.lon = 0.0
        self.lat = 0.0
        self.score = -1
        self.base_value = 100
        self.ctime = 0

def _get_content(resource_ids, resource_dict, imgs):
    content = []
    if resource_ids == None or resource_ids == 'NULL' or resource_ids == '':
        try:
            imgs = json.loads(imgs)
            for img in imgs:
                c = img.get('content', '') 
                if c:
                    content.append(c)
        except Exception, e:
            logging.info("get content error, e[%s]", e)
        return content

    resources_id_list = map(int, resource_ids.split(','))
    for rid in resources_id_list:
        content.append(resource_dict[rid])

    return content

def _load_resource(file):
    resource_dict = {} #resource_id:descri
    with open(file) as f:
        for index, line in enumerate(f):
            if index == 0:
                continue
            line = line.strip('\n')
            item = line.split('\t')
            resource_id = int(item[0])
            resource_dict[resource_id] = item[1]

    return resource_dict
            

def _load_tweet(file, resource_dict):
    tweet_dict = {}#tid:tweet
    with open(file) as f:
        logging.info("load tweet from [%s]" % (file))
        for index, line in enumerate(f):
            if index == 0:
                continue
            tweet = Tweet()
            line = line.strip('\n')
            item = line.split('\t')
            tid = int(item[0])
            tweet.tid = tid
            tweet.uid = int(item[1])
            #tweet.desc = _get_content(item[3], resource_dict, item[2])
            tweet.ctime = item[2]
            tweet.lon = float(item[4])
            tweet.lat = float(item[5])
            tweet.base_value = float(item[6])
            tweet.score = float(item[7])
            if tweet.lon < 1e-6 or tweet.lat < 1e-6:
                continue

            tweet_dict[tid] = tweet
    return tweet_dict

def _load_zan(file):
    zan_dict = {} #tid:number
    logging.info('load zan[%s]' % (file))
    with open(file) as f:
        for index, line in enumerate(f):
            if index == 0:
                continue
            line = line.strip('\n')
            item = line.split('\t')
            tid = int(item[0])
            if tid in zan_dict:
                zan_dict[tid] += 1
            else:
                zan_dict[tid] = 1
    return zan_dict 

def _load_comment(file):
    comment_dict = {}#poi_id: biz_area_id
    logging.info('load comment[%s]' % (file)) 
    with open(file) as f:
        for index, line in enumerate(f):
            if index == 0:
                continue
            line = line.strip('\n')
            item = line.split('\t')
            tid = int(item[1])
            if tid in comment_dict:
                comment_dict[tid] += 1
            else:
                comment_dict[tid] = 1
    return comment_dict

def _load_tweet_action(file):
    tweet_action_dict = {}#tid: count(action_type == 3)
    logging.info('load tweet_action[%s]' % (file)) 
    with open(file) as f:
        for index, line in enumerate(f):
            if index == 0:
                continue
            line = line.strip('\n')
            item = line.split('\t')
            tid = int(item[0])
            action_type = int(item[1])
            if action_type == 3: # 1:发布, 2:点赞, 3:分享
                if tid in tweet_action_dict:
                    tweet_action_dict[tid] += 1
                else:
                    tweet_action_dict[tid] = 1
    return tweet_action_dict

def _get_score(tweet):
    G = 1.8
    zan_num = int(tweet.zan_num)
    comment_num = int(tweet.comment_num)
    ctime = int(tweet.ctime)

    t = (time.time() - ctime)/3600.0

    score = (0.6*zan_num + 0.4*comment_num)/(t+2)**G

    return score

def merge_data(out_file, tweet_file, zan_file, comment_file, resource_file, tweet_action_file, hot_pic_conf):
    resource_dict = _load_resource(resource_file)
    tweet_dict = _load_tweet(tweet_file, resource_dict)
    zan_dict = _load_zan(zan_file)
    comment_dict = _load_comment(comment_file)
    tweet_action_dict = _load_tweet_action(tweet_action_file)
    score_calculator = hot_pic_calculator.HotPicCalculator(time.time())
    score_calculator.load_conf(hot_pic_conf)

    logging.info('total tweet: %d' % (len(tweet_dict)))
    #fp_out = codecs.open(out_file, 'w', "utf-8")
    fp_out = open(out_file, 'w')
    tweet_list = []
    for tid in tweet_dict:
        try:
            tweet = tweet_dict[tid]
            zan_num = zan_dict.get(tid, 0)
            tweet.zan_num = zan_num
            comment_num = comment_dict.get(tid, 0)
            tweet.comment_num = comment_num
            #tweet.score = _get_score(tweet)
            share_num = tweet_action_dict.get(tid, 0)
            tweet.share_num = share_num
            tweet.score = score_calculator.get_score(tweet.zan_num, tweet.comment_num, tweet.share_num, tweet.base_value, tweet.ctime)
            tweet_list.append(tweet)
        except Exception,e:
             logging.info(traceback.format_exc())
    tweet_list = sorted(tweet_list, key=lambda x:x.score)

    for tweet in tweet_list:
        #line = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (tweet.tid, tweet.type, tweet.f_catalog, tweet.s_catalog, ' '.join(tweet.tag), tweet.zan_num, tweet.comment_num, tweet.desc)
        #info = {}
        #info['tid'] = tweet.tid
        #info['lon'] = tweet.lon
        #info['lat'] = tweet.lat
        #info['score'] = tweet.score
        #line = '%s\n' % json.dumps(info)
        info = []
        info.append(tweet.tid)
        info.append(tweet.lon)
        info.append(tweet.lat)
        info.append(tweet.score)
        info.append(tweet.ctime)
        
        line = '\t'.join([str(i) for i in info])

        #logging.info('line:%s' % line)
        fp_out.write(line + "\n")
    fp_out.close()

def main():
    if 8 != len(sys.argv):
        logging.warning('cmd args is not equal to 8. error')
        exit(1)
    output_file = sys.argv[1]
    tweet_file = sys.argv[2]
    zan_file = sys.argv[3]
    comment_file = sys.argv[4]
    resource_file = sys.argv[5]
    tweet_action_file = sys.argv[6]
    hot_pic_conf = sys.argv[7]
    logging.info('merge_data: output[%s] tweet[%s] zan[%s] comment[%s] resource[%s] tweet_action[%s] hot_pic_conf[%s]' % (output_file, tweet_file, zan_file, comment_file, resource_file, tweet_action_file, hot_pic_conf))
    try:
        merge_data(output_file, tweet_file, zan_file, comment_file, resource_file, tweet_action_file, hot_pic_conf)
    except Exception as e:
        logging.warning(traceback.format_exc())
        exit(1)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%d %b %Y %H:%M:%S')
    main()
