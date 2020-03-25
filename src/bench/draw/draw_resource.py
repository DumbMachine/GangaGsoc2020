import json
import matplotlib.pyplot as plt

from glob import glob

files = [
    '../benchmarks/postgres-resources.json',
    '../benchmarks/mongo-resources.json',
]

def convert_to_float(item):
    return float(item) if "-" not in item else None

def net_io_usage():
    filename = f"../benchmarks/*-resources.json"
    files = glob(filename)
    plot_points = {}
    for file in files:
        data = json.load(open(file, 'r'))['stats']
        net_io = []
        for (i, j) in [i['NET I/O'].replace("0B", "0").split("/") for i in data if "--" not in i['NET I/O']]:
            if i == '':
                i = 0
            else:
                if "kB" in i:
                    i = float(i.replace("kB", "")) # for kbs
                elif "MB" in i:
                    i = float(i.replace("MB", ""))*1024 # for kbs
                elif "GB" in i:
                    i = float(i.replace("GB", ""))*1024*1024 # for kbs

            if j == '':
                j = 0
            else:
                if "kB" in j:
                    j = float(j.replace("kB", "")) # for kbs
                elif "MB" in j:
                    j = float(j.replace("MB", ""))*1024 # for kbs
                elif "GB" in j:
                    j = float(j.replace("GB", ""))*1024*1024 # for kbs
#             net_io.append([i, j])
            net_io.append(i)

        plot_points[file.split("/")[-1].split("-")[0]] = net_io

    if plot_points:
        print(1)
        for key in plot_points.keys():
            plt.plot(plot_points[key], label=key)

        plt.title("net_io_usage")
        plt.legend(loc="upper left")
        plt.savefig(f"../images/NETIO.png", dpi=100)
        plt.clf()

def mem_cpu_usage():

    filename = f"../benchmarks/*-resources.json"
    files = glob(filename)
    plot_points = {}
    for file in files:
        data = json.load(open(file, 'r'))['stats']
        mem_usage_total=[]
        for mem in [i['MEM USAGE/LIMIT'].split("/")[0] for i in data]:
            mem = mem.strip()
            if mem=="--":
                mem=None
            elif mem == '':
                mem = 0
            else:
                if "kiB" in mem:
                    mem = float(mem.replace("kiB", "")) # for kbs
                elif "MiB" in mem:
                    mem = float(mem.replace("MiB", ""))*1024 # for kbs
                elif "GiB" in mem:
                    mem = float(mem.replace("GiB", ""))*1024*1024 # for kbs
            mem_usage_total.append(mem)
        plot_points[file.split("/")[-1].split("-")[0]] = mem_usage_total

    if plot_points:
        print(1)
        for key in plot_points.keys():
            plt.plot(plot_points[key], label=key)

        plt.title("mem_cpu_usage")
        plt.legend(loc="upper left")
        plt.savefig(f"../images/MEM_USAGE.png", dpi=100)
        plt.clf()

def plot_cpu_usage_percent():
    filename = f"../benchmarks/*-resources.json"
    files = glob(filename)
    plot_points = {}
    for file in files:
        data = json.load(open(file, 'r'))['stats']
        mem_usage_percent = [convert_to_float(i['CPU %'][:-1]) for i in data]
        plot_points[file.split("/")[-1].split("-")[0]] = mem_usage_percent

    if plot_points:

        for key in plot_points.keys():
            plt.plot(plot_points[key], label=key)

        plt.title("cpu_usage_percent")
        plt.legend(loc="upper left")
        plt.savefig(f"../images/cpu_usage_percent.png", dpi=100)
        plt.clf()
def plot_mem_usage_percent():
    filename = f"../benchmarks/*-resources.json"
    files = glob(filename)
    plot_points = {}
    for file in files:
        data = json.load(open(file, 'r'))['stats']
        mem_usage_percent = [convert_to_float(i['MEM %'][:-1]) for i in data]
        plot_points[file.split("/")[-1].split("-")[0]] = mem_usage_percent

    if plot_points:

        for key in plot_points.keys():
            plt.plot(plot_points[key], label=key)

        plt.title("mem_usage_percent")
        plt.legend(loc="upper left")
        plt.savefig(f"../images/mem_usage_percent.png")
        plt.clf()


def block_io_usage():
    filename = f"../benchmarks/*-resources.json"
    files = glob(filename)
    plot_points = {}
    for file in files:
        data = json.load(open(file, 'r'))['stats']
        net_io = []
        for (i, j) in [i['BLOCK I/O'].replace("0B", "0").split("/") for i in data if "--" not in i['NET I/O']]:
            if i == '':
                i = 0
            else:
                if "kB" in i:
                    i = float(i.replace("kB", "")) # for kbs
                elif "MB" in i:
                    i = float(i.replace("MB", ""))*1024 # for kbs
                elif "GB" in i:
                    i = float(i.replace("GB", ""))*1024*1024 # for kbs

            if j == '':
                j = 0
            else:
                if "kB" in j:
                    j = float(j.replace("kB", "")) # for kbs
                elif "MB" in j:
                    j = float(j.replace("MB", ""))*1024 # for kbs
                elif "GB" in j:
                    j = float(j.replace("GB", ""))*1024*1024 # for kbs
#             net_io.append([i, j])
            net_io.append(i)

        plot_points[file.split("/")[-1].split("-")[0]] = net_io

    if plot_points:
        print(1)
        for key in plot_points.keys():
            plt.plot(plot_points[key], label=key)

        plt.title("block_io_usage")
        plt.legend(loc="upper left")
        plt.savefig(f"../images/BLOCK.png", dpi=100)
        plt.clf()

net_io_usage()
mem_cpu_usage()
block_io_usage()
plot_cpu_usage_percent()
plot_mem_usage_percent()