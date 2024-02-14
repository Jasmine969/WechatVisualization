from parse_1 import parse
from word_cloud_2 import wc_main
from word_specificity import word_specificity
from emoji_specificity import emoji_specificity
from word_commonality import word_commonality
from emoji_commonality import emoji_commonality
from time_analysis import time_ana


def main(  # 下面这些文件都放在input_data目录下
        msg_file='msg.csv', emoji_file='emoji.txt',
        stopword_file='stopwords_hit_modified.txt',
        transform_file='transformDict.txt',
        user_dict_file='userDict.txt',
        # name_both是双方共同的名字，name1是自己的名字，name2是对方的名字
        name_both: str = 'both', name1: str = 'person 1', name2: str = 'person 2',
        top_k_word: int = 25, top_k_emoji: int = 5,
        min_count_word: int = 20, min_count_emoji: int = 1):
    parse(msg_file, emoji_file, stopword_file, transform_file, user_dict_file)
    wc_main(name_both, name1, name2)
    word_specificity(name1, name2, top_k_word, min_count_word)
    emoji_specificity(name1, name2, top_k_emoji, min_count_emoji)
    word_commonality(name_both, top_k_word)
    emoji_commonality(name_both, top_k_emoji)
    time_ana(msg_file)
    print('搞定了')


if __name__ == '__main__':
    main(min_count_word=2)
