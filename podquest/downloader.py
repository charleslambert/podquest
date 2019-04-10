from contextlib import contextmanager
from multiprocessing import Process, Queue
from pathlib import Path

import requests


@contextmanager
def save(l):
    yield
    print("\033[{}A".format(l), end="", flush=True)


def progress_bar(percent, barLen=20):
    percentage = percent * 100
    bars = "=" * int(barLen * percent)
    return "\r[{:<{}}] {:.0f}%".format(bars, barLen, percentage)


class Downloader:
    def __init__(self, download_dir=Path(Path.home(), "Podcast")):
        self.download_dir = download_dir
        self.download_dir.mkdir(parents=True, exist_ok=True)

    def create_download_path(self, download):
        dir_path = Path(self.download_dir, download["podcast_title"])
        dir_path.mkdir(parents=True, exist_ok=True)
        return Path(dir_path, download["title"]).with_suffix(".mp3")

    def single_download(self, download):
        req = requests.get(download["url"], stream=True)
        download_chunk = 0
        with open(self.create_download_path(download), 'wb') as f:
            for chunk in req.iter_content(chunk_size=1024):
                yield download_chunk / int(req.headers["content-length"])
                download_chunk += 1024
                f.write(chunk)

            yield 1

    def producer(self, id, queue, download, title):
        for progress in download:
            queue.put((id, progress, title))

    def muli_download(self, downloads):
        queue = Queue()

        downloads = [(self.single_download(d), d["title"]) for d in downloads]

        producers = [
            Process(target=self.producer, args=(i, queue, download, title))
            for i, (download, title) in enumerate(downloads)
        ]
        for p in producers:
            p.start()

        output = [0 for _ in range(len(init_vals))]

            while True:
                v = queue.get()
                output[v[0]] = v[1]
                if output.count(1.0) == len(output):
                    break
