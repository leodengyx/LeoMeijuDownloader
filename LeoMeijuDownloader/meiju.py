import json


class Episode:

    def __init__(self):

        self.season_id = 0
        self.episode_id = 0
        self.url = u""

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, intent=4)

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __unicode__(self):
        return "season_id:[%d] episode_id:[%d] url:[%s]" % \
               (self.season_id, self.episode_id, self.url)

class Season:

    def __init__(self):
        self.season_id = 0
        self.episode_count = 0
        self.episode_id_inst_dict = {}

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, intent=4)

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __unicode__(self):
        return "season_id:[%d] episode_count:[%d]" % \
               (self.season_id, self.episode_count)

class Meiju:

    def __init__(self):

        self.mix_name = u""
        self.english_name = u""
        self.chinese_name = u""
        self.season_count = 0
        self.season_id_inst_dict = {}
        self.url = u""

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, intent=4)

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __unicode__(self):
        return "mix_name:[%s] e_name:[%s] c_name:[%s] season_count:[%d] url:[%s]" % \
               (self.mix_name, self.english_name, self.chinese_name, self.season_count, self.url)



