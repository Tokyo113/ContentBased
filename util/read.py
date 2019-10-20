#coding:utf-8
'''
@Time: 2019/10/20 上午10:26
@author: Tokyo
@file: read.py
@desc: some util function
基于内容的推荐
1.item profile---get item cate
2.user profile---
'''

from __future__ import division
import os
import operator
def get_avg_score(input_file):
    """

    :param input_file:  user ratings file
    Return:
    a dict
    key: itemid,  value:avg_score
    """
    if not os.path.exists(input_file):
        return {}
    linenum = 0
    record = {}
    avg_score = {}
    fp = open(input_file)
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(",")
        if len(item) < 4:
            continue
        userid, itemid, rating = item[0], item[1], float(item[2])

        if itemid not in record:
            # 记录总得分和打分人数
            record[itemid] = [0, 0]
        record[itemid][0] += rating
        record[itemid][1] += 1
    fp.close()
    for itemid in record:
        avg_score[itemid] = round(record[itemid][0]/record[itemid][1], 3)
    return avg_score



def get_item_cate(avg_score, input_file):
    """
    获得每一个item的类别,以及每一个类别对应的item按照平均得分的倒排
    :param avg_score: a dict key: itemid, value:rating score
    :param input_file: item info file
    Return:
    a dict: key:itemid,  value: a dict: key--cate  value--weight
    a dict: key--cate, value--[itemid1, itemid2, itemid3...]
    """

    if not os.path.exists(input_file):
        return {}, {}

    linenum = 0
    item_cate = {}
    record = {}
    cate_item_sort = {}
    topk = 100
    fp = open(input_file)
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(",")
        if len(item) < 3:
            continue
        itemid = item[0]
        cate_str = item[-1]
        cate_list = cate_str.strip().split("|")
        ratio = round(1/len(cate_list), 3)
        if itemid not in item_cate:
            item_cate[itemid] = {}
        for fix_cate in cate_list:
            item_cate[itemid][fix_cate] = ratio
    fp.close()

    for itemid in item_cate:
        for cate in item_cate[itemid]:
            if cate not in record:
                # 记录每一个种类下所有item 的平均评分
                record[cate] = {}
            itemid_rating_score = avg_score.get(itemid, 0)
            record[cate][itemid] = itemid_rating_score

    for cate in record:
        if cate not in cate_item_sort:
            cate_item_sort[cate] = []
        # 按照平均得分从高到低排序
        for zuhe in sorted(record[cate].items(), key=operator.itemgetter(1), reverse=True)[:topk]:
            cate_item_sort[cate].append(zuhe[0])

    return item_cate, cate_item_sort


if __name__ == '__main__':
    avg_score = get_avg_score("../data/ratings.csv")
    # print(len(avg_score))
    # print(avg_score["31"])
    item_cate, cate_item_sort = get_item_cate(avg_score, "../data/movies.csv")
    print(item_cate["1"])
    print(cate_item_sort["Children"])