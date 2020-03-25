import json
import matplotlib.pyplot as plt

files = [
    '../benchmarks/postgres.json',
    '../benchmarks/mongo.json',
]

# Single plots
data = []
for file in files:
    _data = json.load(open(file, 'r'))['push']
    data.append(_data)

    plt.plot(_data[1:], label=f"{file.split('/')[-1][:-5]}")
    # plt.plot(_data[:], label=f"{file.split('/')[-1][:4]}")

plt.title(f"{file.split('/')[-1]} Benchmarking")
plt.xlabel("iterations")
plt.ylabel("time (in seconds)")
plt.legend(loc="upper left")
plt.savefig(f'total_time.png')




# start of the single plot
plt.clf()
plt.plot(data[0][1:])
plt.title(f"Postgres Benchmarking")
plt.xlabel("iterations")
plt.ylabel("time (in seconds)")
plt.legend(loc="upper left")
plt.savefig(f'postgres_time.png')
plt.clf()
# end of the single plot

# start of the single plot
plt.plot(data[1][1:])
plt.title(f"Mongo Benchmarking")
plt.xlabel("iterations")
plt.ylabel("time (in seconds)")
plt.legend(loc="upper left")
plt.savefig(f'mongo_time.png')
plt.clf()
# end of the single plot