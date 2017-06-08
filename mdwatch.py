from time import sleep
from md2html import md2html
from hashlib import sha1
import sys
import os.path
import argparse

class FileWatcher(object):
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.last_hash = None

    def watch(self):
        hash = None
        
        with open(self.input_path, "rb") as f:
            hash = sha1(f.read()).digest()

        if self.last_hash != hash:
            self.last_hash = hash
            
            print("File changed, reprocessing...")
            
            md2html("My Title", self.input_path, self.output_path)
            
class MultipleFileWatcher(object):
    def __init__(self):
        self.watchers = []

    def add_file(self, input_path, output_path=None):
        if not output_path:
            output_path = os.path.splitext(input_path)[0] + ".html"

        watcher = FileWatcher(input_path, output_path)
        self.watchers.append(watcher)
        
    def watch(self):
        for watcher in self.watchers:
            watcher.watch()

if __name__ == "__main__":
    file_watcher = MultipleFileWatcher()
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", action='append')
    args = parser.parse_args()

    if not args.f:
        parser.error("Must have at least one -f")
    
    for item in args.f:
        split_item = item.split(',')
        
        file_watcher.add_file(*split_item)

    while True:
        file_watcher.watch()
        sleep(1)