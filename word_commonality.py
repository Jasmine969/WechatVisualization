from matplotlib import pyplot as plt
import pickle
from utils import calc_commonality


def word_commonality(name_both: str = 'both', top_k: int = 25, figsize=(10, 12)):
    print('计算word_commonality')
    with open('temp_files/keyword_count.pkl', 'rb') as pf:
        dct = pickle.load(pf)
        d1_kw = dct['d1']
        d2_kw = dct['d2']
    common_df = calc_commonality(d1_kw, d2_kw)
    common_df.sort_values(by='commonality', ascending=False, inplace=True)
    plt.rc('font', family='SimSun', size=15)
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    y = list(range(top_k - 1, -1, -1))
    plt.figure(1, figsize=figsize)
    plt.barh(y, common_df.iloc[:top_k, 3], color='C2')
    plt.yticks(y, common_df.iloc[:top_k, 0].tolist())
    plt.xlabel('词语共有性', fontsize=20)
    plt.ylabel('词语', fontsize=20)
    plt.title(f'{name_both} Top 25 words', fontsize=20)
    plt.savefig(f'figs/{name_both} commonality.png')
    print('=' * 20)


if __name__ == '__main__':
    word_commonality()
