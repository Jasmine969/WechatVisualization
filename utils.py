import re
from collections import Counter
import pandas as pd


def contains(text: str, checklist: list) -> bool:
    """
    # 判断一段文本是否有一堆字符串之一
    # 比如字符串s中是否含有“你”、“我”、“他”这些词
    :param text: 被检查的文本
    :param checklist: 包含“你”、“我”、“他”的列表
    :return: 逻辑值，表示是否包含
    """
    res = [bool(re.findall(each, text)) for each in checklist]
    return any(res)


def calc_specificity(d1: Counter, d2: Counter):
    d1_df = pd.DataFrame({'name': d1.keys(), 'count': d1.values()})
    d2_df = pd.DataFrame({'name': d2.keys(), 'count': d2.values()})
    all_df = pd.merge(d1_df, d2_df, how='outer', on='name', suffixes=['_x', '_y'])
    all_df.fillna(0, inplace=True)
    # (4,0)>(100,96)所以x-y不行。(4,0)>(1,0),所以(x-y)/(x+y)不行
    # 这边用的是(x-y)/(x+y)*max(x,y)
    all_df['specificity'] = all_df.apply(
        lambda x: (x['count_x'] - x['count_y']) / (
                x['count_x'] + x['count_y']) * max(x['count_x'], x['count_y']), axis=1)
    all_df['count'] = all_df['count_x'] + all_df['count_y']
    return all_df


def calc_commonality(d1: Counter, d2: Counter):
    d1_df = pd.DataFrame({'name': d1.keys(), 'count': d1.values()})
    d2_df = pd.DataFrame({'name': d2.keys(), 'count': d2.values()})
    common_df = pd.merge(d1_df, d2_df, how='inner', on='name', suffixes=['_x', '_y'])
    common_df['commonality'] = 2 / (1 / common_df['count_x'] + 1 / common_df['count_y'])
    return common_df
