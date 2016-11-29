#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import argparse
import sys, os

# parse html
import lxml.html
import datetime


MAGIC_KEY = "BD1UO2FFu9QAAAAAAAAETAAAAAcAAAASAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAQACAAEAAAgACAAAABAAKAAAAAAAAAAAAABABKAAAAIAAECQAAAAAgCAAAgAAIAAAAMAAAAAAAAABAFEAACAkAAAAAAAIAAAAAAAAAAEAEAAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAA"

def load_html(q, tweet_max=None, tweet_min=None):
    r_url = "https://twitter.com/i/search/timeline"
    r_headers = {
        "User-Agent": "Mozilla/5.0",
    }
    r_params = {
        "q": "%23" + q,
        "max_position": None,
    }
    if tweet_max is not None: # always equal to (tweet_min is not None)
        r_params["max_position"] = "TWEET-{}-{}-".format(tweet_min, tweet_max) + MAGIC_KEY
    # print(r_params["max_position"])
    data = requests.get(r_url, params=r_params, headers=r_headers)

    json = data.json()
    if "message" in json:
        print(json["message"])
        sys.exit(2)
    # try:
    #     print("-"*21)
    #     print("Loaded {} messages...".format(json["new_latent_count"]))
    # except Exception as e:
    #     raise

    return json



def parse_html(data):
    html = lxml.html.document_fromstring(data)
    records = list()

    tweets = html.xpath("//li[contains(concat(' ', normalize-space(@class), ' '), ' stream-item ')]")
    for tweet in tweets:
        timestamp = int( tweet.xpath("./div[1]//small/a/span/@data-time")[0] )
        message = tweet.xpath(".//div[@class='js-tweet-text-container']/p")[0]
        record = {
            "tweet_id"   : tweet.xpath("./@data-item-id")[0],
            "created_at" : datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'),
            "user"       : tweet.xpath("./div[1]/@data-screen-name")[0],
            "nikname"    : tweet.xpath("./div[1]/@data-name")[0],
            "message"    : message.text_content(),
            "hashtags"   : message.xpath(".//a[contains(concat(' ', normalize-space(@class), ' '), ' twitter-hashtag ')]//strong/text()"),
            "reply_to"   : message.xpath(".//a[contains(concat(' ', normalize-space(@class), ' '), ' twitter-atreply ')]//b/text()"),
            "reply_to_id": message.xpath(".//a[contains(concat(' ', normalize-space(@class), ' '), ' twitter-atreply ')]/@data-mentioned-user-id"),
            "ulrs"       : message.xpath(".//a/@data-expanded-url"),
            "reply"      : tweet.xpath(".//span[contains(concat(' ', normalize-space(@class), ' '), ' ProfileTweet-action--reply '   )]/span/@data-tweet-stat-count")[0],
            "retweets"   : tweet.xpath(".//span[contains(concat(' ', normalize-space(@class), ' '), ' ProfileTweet-action--retweet ' )]/span/@data-tweet-stat-count")[0],
            "likes"      : tweet.xpath(".//span[contains(concat(' ', normalize-space(@class), ' '), ' ProfileTweet-action--favorite ')]/span/@data-tweet-stat-count")[0],
            "lang"       : tweet.xpath(".//div[@class='js-tweet-text-container']/p/@lang")[0],
            # "permalink" : tweet.xpath("./div[1]/@data-permalink-path")[0],
        }
        # print(record["tweet_id"])
        """
        for tag, value in record.items():
            if tag == "message":
                value = value.replace("\n", " ")
                if len(value) > 184:
                    value = "{:.184}***".format(value)
            print("{:>11}: {}".format(tag, value))
        print("-"*200)
        """
        records.append(record)

    return records


def main(argv):
    # init -----------------------------------------------------------------
    work_dir = os.path.dirname(os.path.realpath(__file__))
    cache_dir = work_dir + "/data"
    if not os.path.isdir(cache_dir):
        os.mkdir(cache_dir)

    # read arg -------------------------------------------------------------
    parser = argparse.ArgumentParser(description='Twitter crawler v0.9')
    parser.add_argument('hashtag', type=str, nargs='*',
                        help='a hashtag to collect messages (without hash `#` sign)')
    parser.add_argument('--from', type=str, default=None,
                        help='tweet id to continue breaked process from (not realised yet)')
    args = parser.parse_args()

    if len(args.hashtag) == 0:
        parser.print_help()
        sys.exit(2)
    hashtag = args.hashtag[0]
    if len(args.hashtag) > 1:
        print("INFO: Only one hashtag can be processed at once, using `#{}`.".format(hashtag))

    file_name = "{}/{}.json".format(cache_dir, hashtag)
    if getattr(args, "from") == None:
        if os.path.isfile(file_name) == True:
            print("ERROR: File `{}.json` already exists, can't overwrite!".format(hashtag))
            sys.exit(2)
    else:
        if os.path.isfile(file_name) == True:
            print("INFO: File `{}.json` has been found, append new data.".format(hashtag))

    # load data ------------------------------------------------------------
    print("Loading... ", end="")
    tweet_cnt = 0
    tweet_max = None
    tweet_min = None
    while True:
        html = load_html(hashtag, tweet_max, tweet_min)
        if html["new_latent_count"] == 0:
            print(" Done.")
            break

        tweets = parse_html(html["items_html"])
        with open(file_name, 'a') as f:
            for tweet in tweets:
                json.dump(tweet, f, sort_keys=True)
                f.write("\n")

        # only for the first data load
        if tweet_max is None:
            tweet_max = int(tweets[0]["tweet_id"])
            for tweet in tweets:
                tweet_id = int(tweet["tweet_id"])
                if tweet_id > tweet_max:
                    tweet_max = tweet_id
        # every iteration
        tweet_min = tweet_max
        for tweet in tweets:
            tweet_id = int(tweet["tweet_id"])
            if tweet_id < tweet_min:
                tweet_min = tweet_id

        tweet_cnt += html["new_latent_count"]
        print(" {}...".format(tweet_cnt), end="")
        sys.stdout.flush()

    print("\n")

if __name__ == "__main__":
    main(sys.argv[1:])
