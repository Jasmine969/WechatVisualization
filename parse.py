# encoding=utf-8
import jieba
import pandas as pd
from utils import contains
from tqdm import tqdm
from re import findall

"""
parse对消息进行分词。会分出词语和表情两列。
生成keywords.csv文件作为输出。
"""


def parse(msg_file='msg.csv', emoji_file='emoji.txt',
          stopword_file='stopwords_hit_modified.txt',
          transform_file='transformDict.txt',
          user_dict_file='userDict.txt', process_rows='all'):
    print('开始分词')
    records = pd.read_csv(
        f'input_data/{msg_file}', usecols=['IsSender', 'StrContent', 'StrTime']).dropna(how='any')
    # 如果有一条消息是乱码或者纯数字，直接删除之
    not_want_msg = ['<.+',  # 如<msg，<?xml
                    '^\d{1,}$'  # 纯数字，如验证码
                    ]
    records_not_want = records['StrContent'].apply(lambda x: contains(x, not_want_msg))
    records = records[~records_not_want]
    records.index = range(records.shape[0])
    emoji_eng2cn = pd.read_table(f'input_data/{emoji_file}').set_index('eng').to_dict()['cn']
    # 停词不是哈工大原版，删除了[]，使得微信表情能匹配到；添加了一些新词
    with open(f'input_data/{stopword_file}', 'r', encoding='utf-8') as f1:
        stop_words = set(f1.read().splitlines())
    transformDict = pd.read_table(f'input_data/{transform_file}'
                                  ).set_index('original').to_dict()['transformed']
    jieba.load_userdict(f'input_data/{user_dict_file}')
    if process_rows == 'all':
        process_rows = records.shape[0]
    result = []
    emoji_res = []
    records['keywords'] = [float('nan') for _ in range(records.shape[0])]
    records['emoji'] = [float('nan') for _ in range(records.shape[0])]
    # emoji_set = set()
    for i in tqdm(range(process_rows)):
        try:
            for word in jieba.cut(records.loc[i, 'StrContent'], use_paddle=True):  # 使用paddle模式
                # 不是停词，不是空白，是数字字母下划线汉字或者[]，不是纯数字(包括带小数点的)，不是单个英文字母
                if word not in stop_words and len(word.strip()) and \
                        findall('[\[\]一-龟a-zA-Z0-9]+', word) and \
                        not findall('^\d{1,}$|^\d{1,}\.\d{1,}$', word) and \
                        not findall('^[a-zA-Z]$', word):
                    if word in transformDict:
                        word = transformDict[word]
                    result.append(word)
            # 我发现jieba总是会把微信表情[Cry]分成[,Cry,]，因此人为把它们合起来
            for _ in range(result.count(']')):
                ind2 = result.index(']')
                if len(result) < 3:
                    break
                if result[ind2 - 2] != '[':
                    continue
                emoji_text = result[ind2 - 1]
                if emoji_text in emoji_eng2cn.keys():
                    # 如果是英文并且在字典中，就转换成中文
                    cur_emoji = '[' + emoji_eng2cn[emoji_text] + ']'
                else:
                    if findall('^[0-9a-zA-Z]+$', emoji_text):
                        # 如果emoji_text全部是字母数字并且不在emoji字典中，就删除后跳过
                        del result[ind2 - 2:ind2 + 1]
                        continue
                    cur_emoji = '[' + emoji_text + ']'  # 纯汉字
                del result[ind2 - 2:ind2 + 1]
                emoji_res.append(cur_emoji)
                # emoji_set.add(cur_emoji)
            records.loc[i, 'keywords'] = ', '.join(result)
            records.loc[i, 'emoji'] = ', '.join(emoji_res)
            result = []
            emoji_res = []
        except Exception as e:
            print(f'数据文件某行行有问题，异常为{e}。请检查生成的bug.csv，可以提交给开发者。')
            df_bug = records.loc[[i], :]
            df_bug.to_csv('bug.csv', index=None, encoding='utf_8_sig')
            raise e
    records.replace('', float('nan'), inplace=True)  # 方便后面dropna
    # 分词后，由于某些消息全是停词，使得分词为空，需要删去这部分
    records.dropna(how='all', subset=['keywords', 'emoji'], inplace=True)
    records.to_csv('temp_files/keywords.csv', index=None, encoding='utf_8_sig')
    # with open('emoji_set.txt', 'w') as f3:
    #     f3.write('\n'.join(emoji_set))
    print('=' * 20)


if __name__ == '__main__':
    parse()
