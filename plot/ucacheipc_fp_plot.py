#!/usr/bin/env python3
import numpy as np
import os, sys
sys.path.append("../data")
from head import *


# get and process data
original: pd.DataFrame = pd.read_excel(args.file, index_col=0)
processed = original.iloc[0:6]
# 只选中某些特定列，数据才有效
processed = processed[["168.wupwise", "171.swim", "172.mgrid", "177.mesa", "178.galgel", "179.art", "183.equake", "187.facerec", "188.ammp", "301.apsi"]]
head_list = processed.columns.tolist()    
# index_list = processed.index.tolist()
processed[head_list] = processed[head_list].div(processed.iloc[0][head_list]) # 除以第一行
processed_nrow = len(processed.index)   # 行数=3
processed_ncol = len(processed.columns)  # 列数=10

# 忽略第一行
processed = processed.iloc[1:]

f, (ax0, ax1) = plt.subplots(
  ncols=2, sharey=True, figsize=(5, 2),
  gridspec_kw={"width_ratios": [0.1,0.9], "wspace": 0,}
)

bar = ax0.bar(processed.index,
  processed.apply(np.mean, axis=1) * 100,
  color=colors
)   # 画平均，按照列求平均
ax0.set_xticks(processed.index, processed.index, rotation=90)
ax0.bar_label(bar, fmt="%.1f", rotation=90)
ax0.set_ylabel("相对性能")
ax0.set_title("平均", y=0.88, fontsize=8)
ax0.yaxis.grid(True)
ax0.yaxis.set_major_formatter(ticker.PercentFormatter())

x = np.arange(processed_ncol) # x = 0,1,2,3,4,5,6,7,8,9
width = 0.4
multiplier = 0.5

for (index, row) in processed.iterrows(): # 遍历行, index是行名，row是行数据
  offset = width * multiplier   # 0.2, 0.6, 1.0, 1.4
  bar = ax1.bar(x+offset, row * 100, width, label=index)
  ax1.yaxis.grid(True)
  # ax1.bar_label(bar, fmt="%.2f", rotation=90)
  multiplier += 1

# ax1.tick_params(axis='x', labelsize=8) 
ax1.legend(loc="upper left", ncol=processed_nrow, labels=["无优化", "开启所有优化"])
ax1.set_xticks(x+width*processed_nrow/2, processed.columns, rotation=90)
ax1.set_xlim(-0.3, processed_ncol)
ax1.set_ylim(40, processed.max().max() * 1.4 * 100)

ax1.set_yticks([40, 60, 80, 100])

import os
ext = ".svg"
plt.savefig(
  os.path.splitext(args.file)[0] + ext,
  bbox_inches="tight",
  transparent=True
)
