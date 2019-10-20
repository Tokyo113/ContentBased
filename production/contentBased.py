#coding:utf-8
'''
@Time: 2019/10/20 上午11:24
@author: Tokyo
@file: contentBased.py
@desc:完成user profile 和 online recommendation
'''
from __future__ import division
import os
import operator
import util.read as read
def get_up(item_cate, input_file):
    """
    user profile
    :param item_cate: dict  key:itemid, value:dict, key:category, value :weight
    :param input_file: user rating file
    Return:
    a dict
    key: userid  value[(category, ratio), (category2, ratio2)]
    """
    if not os.path.exists(input_file):
        return {}

    linenum = 0
    # 记录对于每一个userid,对于每一个类别的偏好得分
    record = {}
    up = {}
    score_thre = 4.0
    topk = 2
    fp = open(input_file)
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(",")
        if len(item) < 4:
            continue
        userid, itemid, rating, timestamp = item[0], item[1], float(item[2]), int(item[3])
        if rating < score_thre:
            continue
        if itemid not in item_cate:
            continue
        time_score = get_time_score(timestamp)

        if userid not in record:
            record[userid] = {}
        for fix_cate in item_cate[itemid]:
            if fix_cate not in record[userid]:
                record[userid][fix_cate] = 0
            record[userid][fix_cate] += rating*time_score*item_cate[itemid][fix_cate]

    fp.close()

    for userid in record:
        if userid not in up:
            up[userid] = []
        total_score = 0
        for zuhe in sorted(record[userid].items(), key=operator.itemgetter(1), reverse=True)[:topk]:
            up[userid].append((zuhe[0], zuhe[1]))
            total_score += zuhe[1]
        # 归一化
        for index in range(len(up[userid])):
            up[userid][index] = (up[userid][index][0],round(up[userid][index][1]/total_score, 3))

    return up



def get_time_score(timestamp):
    """

    :param timestamp: input timestamp
    Return:1427782288
    time score 时间差越小,得分越高
    """
    fix_time_stamp = 1427782288
    total_sec = 24*60*60
    delta = (fix_time_stamp - timestamp)/total_sec/100
    return round(1/(1+delta), 3)


def recom(cate_item_sort, up, userid, topk=10):
    """

    :param up:  user profile
    :param cate_item_sort:
    :param userid:
    :param topk: recom num
    Return:
    a dict
    key: userid, value: itemlist[itemid1, itemid2]
    """

    if userid not in up:
        return {}
    recom_result = {}
    if userid not in recom_result:
        recom_result[userid] = []
    for zuhe in up[userid]:
        # 不同偏好推荐的个数是不同的
        cate = zuhe[0]
        ratio = zuhe[1]
        num = int(topk*ratio)+1
        if cate not in cate_item_sort:
            continue
        recom_list = cate_item_sort[cate][:num]
        recom_result[userid] += recom_list

    return recom_result




def run_main():
    avg_score = read.get_avg_score("../data/ratings.csv")

    item_cate, cate_item_sort = read.get_item_cate(avg_score, "../data/movies.csv")

    user_profile = get_up(item_cate, "../data/ratings.csv")
    print(len(user_profile))
    print(user_profile["1"])
    result = recom(cate_item_sort, user_profile, "1")
    print(result)

if __name__ == '__main__':
    run_main()


