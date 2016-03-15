#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib
import urllib2
from cookielib import CookieJar
import re
import youtube_dl
import os
import threading

from collector import Collector
from meiju import Episode
import logger


logger = logger.get_logger(__name__)

'''
def thread_func(downloader, episode_inst, season_dir_path):
    logger.debug("Thread %s starting." % threading.currentThread().getName())
    downloader.download_meiju_episode(episode_inst, season_dir_path)
    logger.debug("Thread %s end." % threading.currentThread().getName())
'''

class Downloader:

    def __init__(self):
        pass

    def download_meiju_episode(self, episode_inst, save_folder_path):

        # Check whether episode instance invalid
        if episode_inst is None:
            logger.error("Episode instance is None")
            return

        # Check whether invalid input parameter
        if save_folder_path is None or len(save_folder_path) == 0:
            logger.error("Invalid folder path")
            return

        # Check whether need to create dir
        if not os.path.exists(save_folder_path):
            os.makedirs(save_folder_path)
            logger.debug("Create directory %s" % save_folder_path)

        # Check whether download file already exists
        output_file_name = "Season" + str(episode_inst.season_id) + "Ep" + str(episode_inst.episode_id) + ".mp4"
        output_file_path = os.path.join(os.path.abspath(save_folder_path), output_file_name)
        if os.path.exists(output_file_path):
            logger.debug("File %s already exists, no need to download" % output_file_path)
            return

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
            logger.debug("Videomega URL: %s" % urlstr)
            logger.debug("Save to file %s" % output_file_path)

            # Use youtube-dl to download the video
            argv = ["-o", unicode(output_file_path), urlstr]
            try:
                youtube_dl.main(argv)
            except:
                logger.error("Error downloading the video")

    def download_meiju_season(self, season_inst, save_folder_path):

        # Check whether season instance is None
        if season_inst is None:
            logger.error("Season Instance is None")
            return

        # Check whether save folder path is invalid
        if save_folder_path is None or len(save_folder_path) == 0:
            logger.error("Invalid folder path")
            return

        # Check whether need to create dir
        if not os.path.exists(save_folder_path):
            os.makedirs(save_folder_path)
            logger.debug("Create directory %s" % save_folder_path)

        # Check whether need to create Season folder
        season_dir_name = "Season" + str(season_inst.season_id)
        season_dir_path = os.path.join(save_folder_path, season_dir_name)
        if not os.path.exists(season_dir_path):
            os.makedirs(season_dir_path)
            logger.debug("Create directory %s for season" % season_dir_path)

        # Download all episodes of the season
        for episode_inst in season_inst.episode_id_inst_dict.values():
            self.download_meiju_episode(episode_inst, season_dir_path)
            '''
            thread_inst = threading.Thread(name="S"+str(episode_inst.season_id)+"Ep"+str(episode_inst.episode_id),
                                           target=thread_func,
                                           args=(self, episode_inst, season_dir_path))
            thread_list.append(thread_inst)
            thread_inst.setDaemon(True)
            thread_inst.start()
        for thread_inst in thread_list:
            thread_inst.join()
            '''

        logger.debug("Finished downloading all episods of Season %d" % season_inst.season_id)

    def download_meiju(self, meiju_inst, save_folder_path):

        # Check whether season instance is None
        if meiju_inst is None:
            logger.error("Meiju Instance is None")
            return

        # Check whether save folder path is invalid
        if save_folder_path is None or len(save_folder_path) == 0:
            logger.error("Invalid folder path")
            return

        # Check whether need to create dir
        if not os.path.exists(save_folder_path):
            os.makedirs(save_folder_path)
            logger.debug("Create directory %s" % save_folder_path)

        # Check whether need to create Meiju folder
        meiju_dir_name = meiju_inst.english_name.replace(" ", "_")
        meiju_dir_path = os.path.join(save_folder_path, meiju_dir_name)
        if not os.path.exists(meiju_dir_path):
            os.makedirs(meiju_dir_path)
            logger.debug("Create directory %s for Meiju" % meiju_dir_path)

        # Download all seaons for Meiju
        for season_inst in meiju_inst.season_id_inst_dict.values():
            self.download_meiju_season(season_inst, meiju_dir_path)

if __name__ == "__main__":
    episode_inst = Episode()
    episode_inst.season_id = 5
    episode_inst.episode_id = 14
    episode_inst.url = "http://www.lm-us.com/%e7%a0%b4%e7%94%a2%e5%a7%90%e5%a6%b9-%e7%ac%ac5%e5%ad%a3%e7%ac%ac14%e9%9b%86-2-broke-girls-s5ep14-%e7%be%8e%e5%8a%87%e7%b7%9a%e4%b8%8a%e7%9c%8b"

    downloader = Downloader()
    downloader.download_meiju_episode(episode_inst, "C:\Github")

