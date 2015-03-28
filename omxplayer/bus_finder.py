import os.path
import time
from glob import glob
from logging import getLogger

logger = getLogger(__name__)


class BusFinder(object):
    def __init__(self):
        self.path = self.find_address_file()

    def get_address(self):
        self.wait_for_file()
        logger.debug('Opening file at %s' % self.path)
        with open(self.path, 'r') as f:
            logger.debug('Opened file at %s' % self.path)
            self.address = f.read().strip()
            logger.debug('Address \'%s\' parsed from file' % self.address)
        return self.address

    def find_address_file(self):
        dbus_files = []
        while not dbus_files:
            # filter is used here as glob doesn't support regexp :(
            isnt_pid_file = lambda path: not path.endswith('.pid')
            possible_address_files = glob('/tmp/omxplayerdbus.*')
            possible_address_files = filter(isnt_pid_file,
                                            possible_address_files)
            possible_address_files.sort(key=lambda path: os.path.getmtime(path))
            time.sleep(0.5)

        return dbus_files[-1]

    def wait_for_path_to_exist(self):
        while not os.path.isfile(self.path):
            time.sleep(0.5)

    def wait_for_dbus_address_to_be_written_to_file(self):
        while not os.path.getsize(self.path):
            time.sleep(0.5)

    def wait_for_file(self):
        if self.path:
            self.wait_for_path_to_exist()
        else:
            self.find_address_file()
        self.wait_for_dbus_address_to_be_written_to_file()
