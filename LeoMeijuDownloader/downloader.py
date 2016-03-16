#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib
import urllib2
from cookielib import CookieJar
import re
import youtube_dl
import os
import time

from collector import Collector
from meiju import Episode
import logger


logger = logger.get_logger(__name__)

class Downloader:

    def __init__(self):
        pass

    def download_meiju_episode(self, collector, meiju_ename, season_id, episode_id, save_folder_path):

        # Check whether collector instance invalid
        if collector is None:
            logger.error("Collector instance is None")
            return

        # Check whether invalid input parameter
        if save_folder_path is None or len(save_folder_path) == 0:
            logger.error("Invalid folder path")
            return

        # Check whether need to create dir
        if not os.path.exists(save_folder_path):
            os.makedirs(save_folder_path)
            logger.debug("Create directory %s" % save_folder_path)

        # Check whether dir contains the Meiju folder
        if save_folder_path.find(meiju_ename.replace(" ", "_")) == -1:
            save_folder_path = os.path.join(save_folder_path, meiju_ename.replace(" ", "_"))
            if not os.path.exists(save_folder_path):
                os.makedirs(save_folder_path)

        # Check whether dir contains Season folder
        if save_folder_path.find("Season"+str(season_id)) == -1:
            save_folder_path = os.path.join(save_folder_path, "Season"+str(season_id))
            if not os.path.exists(save_folder_path):
                os.makedirs(save_folder_path)

        # Check whether download file already exists
        output_file_name = "Season" + str(season_id) + "Ep" + str(episode_id) + ".mp4"
        output_file_path = os.path.join(os.path.abspath(save_folder_path), output_file_name)
        if os.path.exists(output_file_path):
            logger.debug("File %s already exists, no need to download" % output_file_path)
            return

        # Get episode instace
        if meiju_ename in collector.meiju_ename_inst_dict:
            meiju_inst = collector.meiju_ename_inst_dict[meiju_ename]
            if season_id in meiju_inst.season_id_inst_dict:
                season_inst = meiju_inst.season_id_inst_dict[season_id]
                if episode_id in season_inst.episode_id_inst_dict:
                    episode_inst = season_inst.episode_id_inst_dict[episode_id]

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

                else:
                    logger.error("Failed to lookup Episode instance with Episode Id %d" % episode_id)
                    return
            else:
                logger.error("Failed to lookup Season instance with Season Id %d" % season_id)
                return
        else:
            logger.error("Failed to lookup Meiju with English name %s" % meiju_ename)
            return

    def download_meiju_season(self, collector, meiju_ename, season_id, save_folder_path):

        # Check whether collector is None
        if collector is None:
            logger.error("Collector instance is None")
            return

        # Check whether save folder path is invalid
        if save_folder_path is None or len(save_folder_path) == 0:
            logger.error("Invalid folder path")
            return

        # Check whether need to create dir
        if not os.path.exists(save_folder_path):
            os.makedirs(save_folder_path)
            logger.debug("Create directory %s" % save_folder_path)

        # Check whether dir contains the Meiju folder
        if save_folder_path.find(meiju_ename.replace(" ", "_")) == -1:
            save_folder_path = os.path.join(save_folder_path, meiju_ename.replace(" ", "_"))
            if not os.path.exists(save_folder_path):
                os.makedirs(save_folder_path)

        # Check whether dir contains Season folder
        if save_folder_path.find("Season"+str(season_id)) == -1:
            save_folder_path = os.path.join(save_folder_path, "Season"+str(season_id))
            if not os.path.exists(save_folder_path):
                os.makedirs(save_folder_path)

        # Get season instance
        if meiju_ename in collector.meiju_ename_inst_dict:
            meiju_inst = collector.meiju_ename_inst_dict[meiju_ename]
            if season_id in meiju_inst.season_id_inst_dict:
                season_inst = meiju_inst.season_id_inst_dict[season_id]

                # Download all episodes of the season
                for episode_inst in season_inst.episode_id_inst_dict.values():
                    self.download_meiju_episode(collector, meiju_ename, season_id,
                                                episode_inst.episode_id, save_folder_path)

                # Check whether there is some .mp4.part file exists, if yes, need to resume
                is_part_file_exist = True
                while is_part_file_exist == True:
                    is_part_file_exist = False
                    for episode_inst in season_inst.episode_id_inst_dict.values():
                        part_file_path = os.path.join(save_folder_path, "Season"+str(season_id)+"Ep"+str(episode_inst.episode_id)+".mp4.part")
                        if os.path.exists(part_file_path):
                            # Wait 10 seconds and then resume
                            is_part_file_exist = True
                            time.sleep(10)
                            self.download_meiju_episode(collector, meiju_ename, season_id, episode_inst.episode_id, save_folder_path)
            else:
                logger.error("Failed to lookup Season with Season Id %d" % season_id)
                return
        else:
            logger.error("Failed to lookup Meiju with English name %s" % meiju_ename)
            return

        logger.debug("Finished downloading all episods of Season %d" % season_inst.season_id)

    def download_meiju(self, collector, meiju_ename, save_folder_path):

        # Check whether Collector instance is None
        if collector is None:
            logger.error("Collector instance is None")
            return

        # Check whether save folder path is invalid
        if save_folder_path is None or len(save_folder_path) == 0:
            logger.error("Invalid folder path")
            return

        # Check whether need to create dir
        if not os.path.exists(save_folder_path):
            os.makedirs(save_folder_path)
            logger.debug("Create directory %s" % save_folder_path)

        # Check whether dir contains the Meiju folder
        if save_folder_path.find(meiju_ename.replace(" ", "_")) == -1:
            save_folder_path = os.path.join(save_folder_path, meiju_ename.replace(" ", "_"))
            if not os.path.exists(save_folder_path):
                os.makedirs(save_folder_path)

        # Get Meiju instance
        if meiju_ename in collector.meiju_ename_inst_dict:
            meiju_inst = collector.meiju_ename_inst_dict[meiju_ename]

            # Download all seaons for Meiju
            for season_inst in meiju_inst.season_id_inst_dict.values():
                self.download_meiju_season(collector, meiju_ename, season_inst.season_id, save_folder_path)
        else:
            logger.error("Failed to lookup Meiju with English name %s" % meiju_ename)
            return

if __name__ == "__main__":
    pass

