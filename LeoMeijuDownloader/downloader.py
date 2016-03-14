#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib
import urllib2
from cookielib import CookieJar
import re
import youtube_dl

from collector import Collector
from meiju import Episode

class Downloader:

    def __init__(self):
        pass

    def download_meiju_episode(self, episode_inst, save_folder_path):
        episode_url = episode_inst.url
        cookiejar = CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
        values = {"log": "us02",
                  "pwd": "0000",
                  "redirect_to": episode_url,
                  "a": "login",
                  "Submit": "%E7%99%BB%E5%85%A5"}
        data = urllib.urlencode(values)
        response = opener.open(episode_url, data)
        soup = BeautifulSoup(response.read().replace("\n",""), "html.parser")

        # First we lookup videomega first
        iframe_tag_list = soup.find_all("iframe", src=re.compile("videomega"))
        for iframe_tag in iframe_tag_list:
            urlstr = iframe_tag["src"][:iframe_tag["src"].find("&")]
            #argv = ["-v", urlstr]
            #youtube_dl.main(argv)
            request = urllib2.Request(urlstr)
            request.add_header("Referer",
                               episode_url)
            request.add_header("User-Agent",
                               "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36")
            cookiejar = CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
            iframe_response = opener.open(request)
            print iframe_response.read()

            '''
            iframe_soup = BeautifulSoup(iframe_response.read(), "html.parser")
            source_tag = iframe_soup.find("source")
            video_url = source_tag["src"]
            print video_url

            # Get real video content
            request = urllib2.Request(video_url)
            request.add_header("Referer",
                                   iframe_tag["src"])
            request.add_header("User-Agent",
                               "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36")
            video_response = opener.open(request)
            meta = video_response.info()
            file_size = int(meta.getheaders("Content-Length")[0])
            print "file size: %d" % file_size
            '''

            '''
            is_continue = True
            retry_count = 0
            while is_continue == True and retry_count < 10:
                # Get IFrame content
                request = urllib2.Request(iframe_tag["src"])
                request.add_header("Referer",
                               episode_url)
                request.add_header("User-Agent",
                               "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36")
                cookiejar = CookieJar()
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
                iframe_response = opener.open(request)
                iframe_soup = BeautifulSoup(iframe_response.read(), "html.parser")
                source_tag = iframe_soup.find("source")
                video_url = source_tag["src"]

                # Get real video content
                request = urllib2.Request(video_url)
                request.add_header("Referer",
                                   iframe_tag["src"])
                request.add_header("User-Agent",
                               "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36")
                video_response = opener.open(request)

                f = open("tmp.mp4", 'wb')
                meta = video_response.info()
                file_size = int(meta.getheaders("Content-Length")[0])
                print "file size: %d" % file_size
                # if file seize is less than 10M, retry
                if file_size < 10000000:
                    retry_count += 1
                    time.sleep(5)
                    continue
                is_continue = False
                print "Downloading: %s Bytes: %s" % ("tmp.mp4", file_size)

                file_size_dl = 0
                block_sz = 8192
                while True:
                    buffer = video_response.read(block_sz)
                    if not buffer:
                        break

                    file_size_dl += len(buffer)
                    f.write(buffer)
                    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                    status = status + chr(8)*(len(status)+1)
                    print status,

                f.close()
                '''




    def download_meiju_season(self, season_inst, save_folder_path):
        pass

    def download_meiju(self, meiju_inst, save_folder_path):
        pass

if __name__ == "__main__":
    episode_inst = Episode()
    episode_inst.season_id = 5
    episode_inst.episode_id = 14
    episode_inst.url = "http://www.lm-us.com/%e7%a0%b4%e7%94%a2%e5%a7%90%e5%a6%b9-%e7%ac%ac5%e5%ad%a3%e7%ac%ac14%e9%9b%86-2-broke-girls-s5ep14-%e7%be%8e%e5%8a%87%e7%b7%9a%e4%b8%8a%e7%9c%8b"

    downloader = Downloader()
    downloader.download_meiju_episode(episode_inst, None)

