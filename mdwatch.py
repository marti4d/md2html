from time import sleep
from md2html import md2html
from hashlib import sha1
import sys
import os.path

# class FileWatcher(object):
    # def __init__(self, input_path, output_path):
        # self.input_path = input_path
        # self.output_path = output_path
        # self.last_hash = None

    # def watch(self):
        # hash = None
        
        # with open(self.input_path, "rb") as f:
            # hash = sha1(f.read()).digest()

        # if self.last_hash != hash:
            # self.last_hash = hash
            
            # print("File changed, reprocessing...")
            
            # md2html("My Title", self.input_path, self.output_path)

class FileWatcher(object):
    def __init__(self, i, o):
        print i
        print o
    
    def watch(self):
        pass
            
class MultipleFileWatcher(object):
    def __init__(self, paths):
        watchers = []

        if isinstance(paths, basestring):
            input_path = str(paths)
            output_path = os.path.splitext(input_path)[0] + ".html"
            watcher = FileWatcher(input_path, output_path)
            watchers.append(watcher)

        elif isinstance(paths, tuple):
            input_path = str(paths[0])
            output_path = str(paths[1])
            watcher = FileWatcher(input_path, output_path)
            watchers.append(watcher)

        else:
            for item in paths:
                if isinstance(item, basestring):
                    input_path = str(item)
                    output_path = os.path.splitext(input_path)[0] + ".html"
                    watcher = FileWatcher(input_path, output_path)
                    watchers.append(watcher)
                
                elif isinstance(item, tuple):
                    input_path = str(item[0])
                    output_path = str(item[1])
                    watcher = FileWatcher(input_path, output_path)
                    watchers.append(watcher)

        self.watchers = watchers
        
    def watch(self):
        for watcher in self.watchers:
            watcher.watch()

watcher = MultipleFileWatcher(("readme.md", "poop.html"))
while True:
    watcher.watch()
    sleep(1)