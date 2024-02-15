from matplotlib import pyplot as plt
import pickle
from word_commonality import calc_commonality


def emoji_commonality(name_both: str = 'both', top_k: int = 5, figsize=(12, 12)):
    print('计算emoji_commonality')
    with open('temp_files/emoji_count.pkl', 'rb') as pf:
        dct = pickle.load(pf)
        d1_count = dct['d1']
        d2_count = dct['d2']
    common_df = calc_commonality(d1_count, d2_count)
    common_df.sort_values(by='commonality', ascending=False, inplace=True)
    plt.close('all')
    plt.rc('font', family='SimSun', size=15)
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    y = list(range(top_k - 1, -1, -1))
    plt.figure(1, figsize=figsize)
    plt.barh(y, common_df.iloc[:top_k, 3], color='C2')
    plt.yticks(y, common_df.iloc[:top_k, 0].tolist())
    plt.xlabel('emoji共有性', fontsize=20)
    plt.ylabel('emoji', fontsize=20)
    plt.title(f'{name_both} Top 5 emojis', fontsize=20)
    plt.savefig(f'figs/{name_both} emoji commonality.png')
    # plt.show()
    print('=' * 20)


if __name__ == '__main__':
    emoji_commonality()
