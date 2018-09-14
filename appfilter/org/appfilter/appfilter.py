import os
import sys
import queue
from org.appfilter.singleapkparse import SingleAPKParse
import threading
import time


MAX_THREAD = 12
DELETE_TEMP_FOLDER = True
APKProcess_Queue = queue.Queue()

'''

'''
class AppFilter(object):

    def __init__(self,papkdir,poutputdir):
        self.apkdir = papkdir
        self.outputdir = poutputdir
        self.threads = []
        self.prepare_and_parse()


    def worker(self):
        global APKProcess_Queue
        global DELETE_TEMP_FOLDER
        while not APKProcess_Queue.empty():
            apk_file_path = APKProcess_Queue.get()
            apk_file_name = os.path.split(apk_file_path)[1]
            apk_file_dir = os.path.split(apk_file_path)[0]
            SingleAPKParse(apk_file_name, apk_file_dir, self.outputdir,DELETE_TEMP_FOLDER)
            time.sleep(1)
            APKProcess_Queue.task_done()


    def prepare_and_parse(self):
        # assert all the input is a directory or a file
        if not (os.path.isfile(self.apkdir) or os.path.isdir(self.apkdir)):
            print("Input: "+self.apkdir+" is not a path for a directory of a file")
            sys.exit(-1)

        if not (os.path.isdir(self.outputdir)):
            print("Output directory is not created or not valid file path")
            sys.exit(-1)


        # loop all files under the directory
        for r, d, f in os.walk(self.apkdir):
            for file in f:
                if ".apk" in file:
                    APKProcess_Queue.put(os.path.join(r,file))

        # set max thread and start each thread
        for i in range(MAX_THREAD):
            thread = threading.Thread(target=self.worker)
            thread.start()
            self.threads.append(thread)


        for thread in self.threads:
            thread.join()


if __name__ == '__main__':
    AppFilter("F:/app/医疗健康","F:/app/医疗健康out")