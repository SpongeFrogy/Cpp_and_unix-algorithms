import matplotlib.pyplot as plt
from cycler import cycler


def plot_settings():
    plt.rcParams["axes.facecolor"] = '#0d1117'
    plt.rcParams["axes.titlecolor"] = "#eef7f4"
    plt.rcParams["figure.facecolor"] = '#0d1117'

    # plt.rcParams['figure.figsize'] = [7.0, 3.0]
    plt.rcParams['figure.dpi'] = 100

    # plt.rcParams["axes.spines.bottom.color"]
    # plt.rcParams["axes.spines.left"] = '#0d1117'
    plt.rcParams["axes.spines.right"] = False
    plt.rcParams["axes.spines.top"] = False

    plt.rcParams["axes.edgecolor"] = "#eef7f4"

    plt.rcParams["xtick.color"] = '#eef7f4'
    plt.rcParams["ytick.color"] = '#eef7f4'


    plt.rcParams["axes.labelcolor"] = '#eef7f4'

    plt.rcParams["grid.color"] = '#eef7f4'

    plt.rcParams["legend.frameon"] = False
    plt.rcParams["legend.labelcolor"] = "#eef7f4"

    plt.rcParams['axes.prop_cycle'] = cycler(color=['g', 'r', 'b', 'y', 'w'])