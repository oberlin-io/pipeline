# Manager
import yaml
from random import randint
import os

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



    def fs_sweep(self):
        '''fs/ directory and manager.yaml congruency.'''
        dirs = os.listdir('../fs/')
        pass

    def find_topic(self):

        x = input('Search string within topic names: ')
        for k, v in self.mgr.items():
            if x in v['topic'][0]['value']:
                print(k)
                print(v)
                print('\n')


class Topic(Manager):

    def __init__(self):
        super().__init__()

    def set_id(self):
        # Set hexidecimal _id for topic
        x = hex(1000)[1:]
        while x in self.mgr.keys():
            x = hex( randint(1001, 9999) )[1:]
        #self._id = x
        print(x)

    def get_id(self):
        return self._id

    def make_entry(self):
        pass



def main():
    MGR = Manager()
    for k, v in MGR.mgr.items():
        print(k)
        print(v)
        print('\n')

    menu = 'Pipeline Manager\n\n  f: Find Topic\n  h: Get an unused _id\n  x: Close'

    while True:
        print(menu)
        m = input()
        os.system('clear')
        if m == 'f':
            MGR.find_topic()
            m = input('Enter to return to menu')
        if m == 'h':
            Topic().set_id()
            m = input('Enter to return to menu')
        elif m == 'x':
            exit()
        os.system('clear')


if __name__ == '__main__': main()
