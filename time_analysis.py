import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime


def time_ana(msg_file='msg.csv', figsize=(12, 8)):
    print('时域处理')
    data = pd.read_csv(f'input_data/{msg_file}', usecols=['StrTime']).dropna()
    data['date'] = data.apply(lambda x: x['StrTime'].split(' ')[0], axis=1)
    data['time'] = data.apply(lambda x: x['StrTime'].split(' ')[1], axis=1)
    data['year-month'] = data.apply(lambda x: '-'.join(x['date'].split('-')[:2]), axis=1)
    data['hour'] = data.apply(lambda x: x['time'].split(':')[0], axis=1)
    # 计算时间跨度
    date0 = datetime(*[int(each) for each in data.loc[0, 'date'].split('-')])
    date1 = datetime(*[int(each) for each in data.loc[data.shape[0] - 1, 'date'].split('-')])
    n_date = (date1 - date0).days + 1
    print(f"第一天：{date0.strftime('%Y-%m-%d')}\n最后一天：{date1.strftime('%Y-%m-%d')}\n"
          f"共计{n_date}天")
    # 月度数据
    data_yearmonth = data.groupby(by='year-month')['year-month'].count()
    # 时均数据
    data_hour = data.groupby(by='hour')['hour'].count() / n_date
    x1 = list(range(len(data_yearmonth)))
    plt.figure(1, figsize=figsize)
    plt.rc('font', family='SimSun', size=15)
    start, end = 0, 13 - date0.month
    for n_year in range(date1.year - date0.year + 1):
        plt.bar(x1[start:end], data_yearmonth.iloc[start:end])
        start = end
        end += 12
    months_ind = [each.split('-')[1] for each in data_yearmonth.index.to_list()]
    plt.xticks(x1, months_ind, rotation=60)
    plt.ylabel('消息条数')
    plt.savefig('figs/月度消息数量变化.png')
    plt.figure(2, figsize=figsize)
    x2 = list(range(24))
    plt.bar(x2, data_hour)
    plt.xticks(x2, data_hour.index)
    plt.xlabel('小时', fontsize=20)
    plt.ylabel('平均消息条数', fontsize=20)
    plt.savefig('figs/小时消息数量变化.png')
    print('=' * 20)


if __name__ == '__main__':
    time_ana()
