import feedparser
from pprint import pprint
import time
from contextlib import contextmanager
import sys


@contextmanager
def save(l):
    yield
    print("\033[{}A".format(l), end="", flush=True)



from multiprocessing import Process, Queue


def progress_bar(percent, barLen=20):
    percentage = percent * 100
    bars = "=" * int(barLen * percent)
    return "\r[{:<{}}] {:.0f}%".format(bars, barLen, percentage)


def producer(init_percent, id, queue):
    percent = init_percent
    while percent < 1:
        queue.put((id, percent))
        percent += 0.1
        time.sleep(0.5)

    queue.put((id, 1.0))


init_vals = [0.1, 0.2, 0.3]

queue = Queue()

producers = [
    Process(target=producer, args=(val, i, queue))
    for i, val in enumerate(init_vals)
]
for p in producers:
    p.start()

output = [0 for _ in range(len(init_vals))]

while True:
    v = queue.get()
    output[v[0]] = v[1]
    with save(len(output)):
        for val in output:
            print("\033[2K{}".format(progress_bar(val)), flush=True)
    if output.count(1.0) == len(output):
        break
