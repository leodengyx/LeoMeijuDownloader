from bs4 import BeautifulSoup
import urllib
import urllib2
import cookielib
import re
import json

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
        self.meiju_inst_list = json.load(file_hdlr)
        file_hdlr.close()

if __name__ == "__main__":
    collector = Collector()
    collector.save_all_meiju_info()
    collector.write_all_meiju_info_to_file()