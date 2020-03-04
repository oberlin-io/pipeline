# Manager
import yaml
from random import randint

class Manager(object):
    def __init__(self):
        '''
        with open('config.yaml', 'r') as f:
            self.conf = yaml.safe_load(f.read())
             = conf
            self.local_path = conf['local_path']
            '''

        with open('manager.yaml', 'r') as f:
            self.mgr = yaml.safe_load(f.read())

#class menu

class Topic(Manager):

    def __init__(self):
        super().__init__()

    def set_id(self):
        # Set hexidecimal _id for topic
        x = hex(1)[1:]

        while x in self.mgr.keys():
            x = hex( randint(1, 999) )[1:]

        self._id = x

    def get_id(self):
        return self._id

    def make_entry(self):
        pass

    def edit_entry(self):
        pass


testing = True
if testing:
    ex_topic = Topic()
    ex_topic.set_id()
    x = ex_topic.get_id()
    print(x)
