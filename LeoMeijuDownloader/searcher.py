#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from collector import Collector
import logger

logger = logger.get_logger(__name__)


class Searcher:

    def __init__(self):
        pass

    def search_meiju_list_by_english_name_keyword(self, collector, keyword_list):

        output_meiju_ename_list = []
        for meiju_inst in collector.meiju_inst_list:
            meiju_ename = meiju_inst.english_name
            for keyword in keyword_list:
                if re.search(keyword, meiju_ename, re.IGNORECASE):
                    output_meiju_ename_list.append(meiju_ename)
                    break
        return output_meiju_ename_list


