from bs4 import BeautifulSoup
import urllib
import urllib2
import cookielib
import re
import json
import os
import sys

from meiju import Meiju
from meiju import Season
from meiju import Episode
import logger


logger = logger.get_logger(__name__)


def dumper(obj):
    try:
        return obj.to_json()
    except:
        return obj.__dict__


class Collector:

    def __init__(self):
        self.init_url = "http://www.lm-us.com/"
        self.all_meiju_file_name = "All_Meiju.js"
        self.meiju_inst_list = []
        self.meiju_ename_inst_dict = {}

    def save_meiju_update_info(self, mix_name, meiju_url):
        logger.info("save_meiju_update_info() function entry. mix_name: %s, meiju_url: %s" % (mix_name, meiju_url))

        # Get the updated meiju instance
        new_meiju_inst = self.save_meiju_info()
        # Old meiju instance
        old_meiju_inst = self.meiju_ename_inst_dict[new_meiju_inst.english_name]
        for (season_id, season_inst) in new_meiju_inst.season_id_inst_dict.items():
            if not season_id in old_meiju_inst.season_id_inst_dict:
                sys.stdout.write("Found new Season %d in Meiju %s\n" % (season_id, new_meiju_inst.english_name))
            else:
                for (episode_id, episode_inst) in season_inst.episode_id_inst_dict.items():
                    if not episode_id in old_meiju_inst.season_id_inst_dict[season_id].episode_id_inst_dict:
                        sys.stdout.write("Found new Episode %d in Season %d in Meiju %s\n" %
                                         (episode_id, season_id, new_meiju_inst.english_name))

        # Save the new meiju instance
        self.meiju_ename_inst_dict[new_meiju_inst.english_name] = new_meiju_inst

    def save_all_meiju_update_info(self):
        logger.info("save_all_meiju_update_info() function entry")
        if not self.is_meiju_info_file_exist():
            sys.stdout.write("We detect that you haven't downloaded any Meiju info before, they will be downloaded now.\n")
            self.save_all_meiju_info()
            self.write_all_meiju_info_to_file()
            sys.stdout.write("All Meiju info has been downloaded successfully.\n")
        else:
            self.read_all_meiju_info_from_file()

            request = urllib2.Request(self.init_url)
            request.add_header("User-Agent",
                               "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36")
            response = urllib2.urlopen(request)
            resp_soup = BeautifulSoup(response.read(), 'html.parser')
            a_tag_list = resp_soup.find_all(href=re.compile("http://www.lm-us.com/\?p="))
            for a_tag in a_tag_list:
                mix_name = unicode(a_tag.string)
                meiju_url = a_tag['href']
                english_name = unicode(mix_name[:mix_name.rfind(" ")]).lstrip().rstrip()

                # To see if there is new Meiju
                if not english_name in self.meiju_ename_inst_dict:
                    sys.stdout.write("Found new Meiju: %s\n" % english_name)
                    meiju_inst = self.save_meiju_info(mix_name, meiju_url)
                    self.meiju_inst_list.append(meiju_inst)
                    self.meiju_ename_inst_dict[meiju_inst.english_name] = meiju_inst
                # If Meiju already exists, check the update seasons and episodes
                else:
                    self.save_meiju_update_info(mix_name, meiju_url)


    def save_all_meiju_info(self):
        logger.info("save_all_meiju_info() function entry")
        request = urllib2.Request(self.init_url)
        request.add_header("User-Agent",
                           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36")
        response = urllib2.urlopen(request)
        resp_soup = BeautifulSoup(response.read(), 'html.parser')
        a_tag_list = resp_soup.find_all(href=re.compile("http://www.lm-us.com/\?p="))
        for a_tag in a_tag_list:
            meiju_inst = self.save_meiju_info(unicode(a_tag.string), a_tag['href'])
            self.meiju_inst_list.append(meiju_inst)
            self.meiju_ename_inst_dict[meiju_inst.english_name] = meiju_inst

    def save_meiju_info(self, mix_name, meiju_url):
        logger.info("save_meiju_info() function entry. mix_name: %s, meiju_url: %s" % (mix_name, meiju_url))
        meiju_inst = Meiju()
        meiju_inst.mix_name = unicode(mix_name).lstrip().rstrip()
        meiju_inst.url = meiju_url

        # Get English Name and chinese name
        meiju_inst.english_name = unicode(meiju_inst.mix_name[:meiju_inst.mix_name.rfind(" ")]).lstrip().rstrip()
        meiju_inst.chinese_name = unicode(meiju_inst.mix_name[meiju_inst.mix_name.rfind(" "):]).lstrip().rstrip()
        logger.debug("Meiju english name: %s, chinese name: %s" % (meiju_inst.english_name, meiju_inst.chinese_name))

        # Get season and episode info
        request = urllib2.Request(meiju_inst.url)
        response = urllib2.urlopen(request)
        resp_soup = BeautifulSoup(response.read(), "html.parser")
        a_tag_list = resp_soup.find_all("a", title=re.compile("s[0-9]+ep[0-9]+", re.IGNORECASE))
        for a_tag in a_tag_list:
            regex = re.compile("s([0-9]+)ep([0-9]+)", re.IGNORECASE)
            match = regex.search(a_tag["title"])
            s_ep_pair = match.groups()

            if not str(int(s_ep_pair[0])) in meiju_inst.season_id_inst_dict:
                season_inst = Season()
                season_inst.season_id = int(s_ep_pair[0])
                meiju_inst.season_id_inst_dict[str(int(s_ep_pair[0]))] = season_inst
                meiju_inst.season_count += 1
                logger.debug("New season instance: %s" % str(season_inst))

            if not str(int(s_ep_pair[1])) in season_inst.episode_id_inst_dict:
                season_inst = meiju_inst.season_id_inst_dict[str(int(s_ep_pair[0]))]
                episode_inst = Episode()
                episode_inst.season_id = season_inst.season_id
                episode_inst.episode_id = int(s_ep_pair[1])
                episode_inst.url = a_tag["href"]
                season_inst.episode_id_inst_dict[str(int(s_ep_pair[1]))] = episode_inst
                season_inst.episode_count += 1
                logger.debug("New episode instance: %s" % str(episode_inst))

        return meiju_inst

    def write_all_meiju_info_to_file(self):
        file_hdlr = open(self.all_meiju_file_name, 'w')
        json.dump(self.meiju_inst_list, file_hdlr, default=dumper, indent=4)
        file_hdlr.close()

    def read_all_meiju_info_from_file(self):
        file_hdlr = open(self.all_meiju_file_name, 'r')
        meiju_dict_list = json.load(file_hdlr)

        self.meiju_inst_list = []
        self.meiju_ename_inst_dict = {}
        for meiju_dict_inst in meiju_dict_list:
            meiju_inst = Meiju()
            meiju_inst.mix_name = meiju_dict_inst["mix_name"]
            meiju_inst.english_name = meiju_dict_inst["english_name"]
            meiju_inst.chinese_name = meiju_dict_inst["chinese_name"]
            meiju_inst.season_count = meiju_dict_inst["season_count"]
            meiju_inst.url = meiju_dict_inst["url"]
            meiju_inst.season_id_inst_dict = {}
            for (season_id, season_dict_inst) in meiju_dict_inst["season_id_inst_dict"].items():
                season_inst = Season()
                season_inst.season_id = season_dict_inst["season_id"]
                season_inst.episode_count = season_dict_inst["episode_count"]
                season_inst.episode_id_inst_dict = {}
                for (episode_id, episode_dict_inst) in season_dict_inst["episode_id_inst_dict"].items():
                    episode_inst = Episode()
                    episode_inst.season_id = episode_dict_inst["season_id"]
                    episode_inst.episode_id = episode_dict_inst["episode_id"]
                    episode_inst.url = episode_dict_inst["url"]
                    season_inst.episode_id_inst_dict[episode_inst.episode_id] = episode_inst
                meiju_inst.season_id_inst_dict[season_inst.season_id] = season_inst
            self.meiju_inst_list.append(meiju_inst)
            self.meiju_ename_inst_dict[meiju_inst.english_name] = meiju_inst
        file_hdlr.close()

    def is_meiju_info_file_exist(self):
        if os.path.exists(self.all_meiju_file_name):
            return True
        return False

if __name__ == "__main__":
    collector = Collector()
    collector.save_all_meiju_info()
    collector.write_all_meiju_info_to_file()