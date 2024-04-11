#!/usr/bin/env python3
import numpy as np
import os, sys
sys.path.append("../data")
from head import *


# get and process data
original: pd.DataFrame = pd.read_excel(args.file, index_col=0)
processed = original
# 只选中某些特定列，数据才有效
processed = processed[["164.gzip", "175.vpr.0", "175.vpr.1", "176.gcc", "181.mcf", "186.crafty", "197.parser", "254.gap", "256.bzip2", "300.twolf"]]
head_list = processed.columns.tolist()
processed[head_list] = processed[head_list].div(processed.iloc[0][head_list]) # 除以第一行
processed_nrow = len(processed.index)   # 行数=3
processed_ncol = len(processed.columns)  # 列数=10

# 根据mode 选择 switch case
if args.mode == 0:  # all opt
  processed = processed.iloc[[1,2]]
elif args.mode == 1:
  processed = processed.iloc[[1,3]]
elif args.mode == 2:
  processed = processed.iloc[[1,4]]
elif args.mode == 3:
  processed = processed.iloc[[1,5]]
elif args.mode == 4:
  processed = processed.iloc[[1,6]]
else:
  processed = processed.iloc[[1,2]]
# processed = processed.iloc[[1,3]]

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
# ax1.legend(loc="upper left", ncol=processed_nrow)
# 根据mode设置legend 内容
if args.mode == 0:
  ax1.legend(loc="upper left", ncol=processed_nrow, labels=["无优化", "开启所有优化"])
elif args.mode == 1:
  ax1.legend(loc="upper left", ncol=processed_nrow, labels=["无优化", "放松缓存行优化"])
elif args.mode == 2:
  ax1.legend(loc="upper left", ncol=processed_nrow, labels=["无优化", "放松条件跳转优化"])
elif args.mode == 3:
  ax1.legend(loc="upper left", ncol=processed_nrow, labels=["无优化", "压缩指令优化"])
elif args.mode == 4:
  ax1.legend(loc="upper left", ncol=processed_nrow, labels=["无优化", "变长缓存行优化"])
else:
  ax1.legend(loc="upper left", ncol=processed_nrow, labels=["无优化", "开启所有优化"])

ax1.set_xticks(x+width*processed_nrow/2, processed.columns, rotation=90)
ax1.set_xlim(-0.3, processed_ncol)
ax1.set_ylim(0, processed.max().max() * 1.4 * 100)

ax1.set_yticks([0, 20, 40, 60, 80, 100])

import os
ext = ".svg"
plt.savefig(
  os.path.splitext(args.file)[0] + (str(args.mode) if args.mode is not None else "") + ext,
  bbox_inches="tight",
  transparent=True
)
