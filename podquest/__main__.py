import click
import feedparser
from api import API
from downloader import Downloader
from pprint import pprint
import time
import requests

from PyInquirer import style_from_dict, Token, prompt, Separator


def progress_bar(percent, barLen=20, title=""):
    percentage = percent * 100
    bars = "=" * int(barLen * percent)
    return "\r{:25}[{:<{}}] {:.0f}%".format(title, bars, barLen, percentage)


def parse_feed(feed_url):
    feed = feedparser.parse(feed_url)
    return [{
        "podcast_title": feed["feed"]["title"],
        "title": entry["title"],
        "url": entry["links"][1]["href"],
    } for entry in feed["entries"]]


@click.group()
def cli():
    pass


@cli.command()
@click.argument("search_text")
def search(search_text):
    api = API()
    results = api.search(search_text)
    if not results:
        print("No Search Results Found")
        exit(1)

    questions = [{
        'type': 'list',
        'name': 'podcast',
        'message': 'Pick podcast if available',
        'choices': results,
    }]
    answers = prompt(questions)
    print(answers)


@cli.command()
@click.argument("url")
def download(url):
    feed = parse_feed(url)
    downloader = Downloader()
    for p in downloader.single_download(feed[0]):
        print(progress_bar(p, title=feed[0]["title"]), end="", flush=True)


        # with save(len(output)):
        #     for val in output:
        #         print("\033[2K{}".format(
        #             progress_bar(val)), flush=True)


if __name__ == '__main__':
    cli()
