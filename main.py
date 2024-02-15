from parse import parse
from word_cloud import wc_main
from word_specificity import word_specificity
from emoji_specificity import emoji_specificity
from word_commonality import word_commonality
from emoji_commonality import emoji_commonality
from time_analysis import time_ana
import os
import yaml


def main(  # 下面这些文件都放在input_data目录下
        msg_file='msg.csv', emoji_file='emoji.txt',
        stopword_file='stopwords_hit_modified.txt',
        transform_file='transformDict.txt',
        user_dict_file='userDict.txt',
        # name_both是双方共同的名字，name1是自己的名字，name2是对方的名字
        name_both: str = 'both', name1: str = 'person 1', name2: str = 'person 2',
        p_word_specificity=None, p_emoji_specificity=None,
        p_word_commonality=None, p_emoji_commonality=None,
        p_time_analysis=None,
        process_rows='all'
):
    if not os.path.exists('figs'):
        os.mkdir('figs')
    if not os.path.exists('temp_files'):
        os.mkdir('temp_files')
    parse(msg_file, emoji_file, stopword_file, transform_file, user_dict_file, process_rows)
    wc_main(name_both, name1, name2)
    word_specificity(name1, name2, **p_word_specificity)
    emoji_specificity(name1, name2, **p_emoji_specificity)
    word_commonality(name_both, **p_word_commonality)
    emoji_commonality(name_both, **p_emoji_commonality)
    time_ana(msg_file, **p_time_analysis)
    print('搞定了')


if __name__ == '__main__':
    with open('config.yml', 'r', encoding='utf-8') as f:
        p = yaml.safe_load(f)
    main(
        msg_file=p['msg_file'],
        emoji_file=p['emoji_file'],
        stopword_file=p['stopword_file'],
        transform_file=p['transform_file'],
        user_dict_file=p['user_dict_file'],
        name_both=p['name_both'], name1=p['name1'], name2=p['name2'],
        p_word_specificity=p['word_specificity'],
        p_emoji_specificity=p['emoji_specificity'],
        p_word_commonality=p['word_commonality'],
        p_emoji_commonality=p['emoji_commonality'],
        p_time_analysis=p['time_analysis'],
        process_rows=p['process_rows']
    )
