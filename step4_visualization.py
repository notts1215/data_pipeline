# -- coding: utf-8 --
"""
@Time : 2022/7/10 23:13
@Author : Notts XIANG
@Description : A simple Python script to read & visualize xlsx file.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import openpyxl


def main():
    """
    bar chart
    """
    df = pd.read_excel('./dwd_table.xlsx', sheet_name='Result 1')
    face_no = df['face_no']
    n, bins, patches = plt.hist(x=face_no, edgecolor='white', align='left', bins=max(face_no) + 1)
    plt.figure()
    dicts = {}
    for i in range(len(n)):
        dicts[i] = n[i]
    plt.bar(x=np.arange(min(face_no), max(face_no) + 1, 1), height=dicts.values(),
            edgecolor='white')  # make sure the bar is locate at each coordinate on x-axis
    for i in range(len(n)):
        plt.text(x=i, y=n[i] + 1, s=int(n[i]), horizontalalignment='center', fontsize=10)

    plt.xticks(np.arange(min(face_no), max(face_no), 1))  # specify each x-axis label
    plt.title('Histogram of face numbers detected')
    plt.xlabel('face numbers')
    plt.ylabel('count')
    plt.show()

    """
    pie chart
    """
    pie_lists = [0 for _ in range(len(n))]
    pie_desc = [i for i in range(len(n))]
    explodes = [0 for i in range(len(n))]
    explodes[10] = .2
    explodes[11] = .4
    explodes[12] = .6
    explodes[13] = .8
    for i in range(len(n)):
        pie_lists[i] = n[i] / 1000
    print(pie_lists)
    plt.pie(x=pie_lists,
            autopct="%.1f%%",
            radius=1.5,
            textprops={'fontsize': 10, 'color': 'k'},
            pctdistance=0.9,
            explode=explodes)
    plt.legend(pie_desc, loc=(1.4, .1))
    plt.show()


if __name__ == '__main__':
    main()
