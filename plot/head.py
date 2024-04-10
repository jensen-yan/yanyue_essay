import typing
import pandas as pd
import numpy as np
import matplotlib.style as style
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.stats import gmean
import argparse
import pathlib

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", nargs="?", type=pathlib.Path,help="the path to xlsx file")
parser.add_argument("-o","--output",nargs="?", type=pathlib.Path,help="name of outputfile")
args = parser.parse_args()
if args.file is None and args.output is None:
    print("the path to xlsx file or name of outputfile")
    exit(0)

style.use("seaborn-v0_8-white")
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["savefig.dpi"] = 300
# https://stackoverflow.com/questions/13831549/get-matplotlib-color-cycle-state
# https://matplotlib.org/stable/gallery/color/color_cycle_default.html
# get default prop_cycle
prop_cycle = plt.rcParams["axes.prop_cycle"]
colors: typing.List[str] = prop_cycle.by_key()["color"] # type: ignore

