#!/usr/bin/python

from pprint import pprint
from subprocess import check_output,Popen,PIPE,CalledProcessError,STDOUT
import time
import os

class Tasks:
    objects = []
    global box

    def int_to_time(self, seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return '{:02d}:{:02d}:{:02d}'.format(h, m, s)

    def get_process_name(self, pid):
        p = Popen(["ps -o cmd --no-headers -p {}".format( pid )], stdout=PIPE, shell=True)
        return str(p.communicate()[0]).rstrip()


    def monitor(self, window_name, pid):
        exists = 0
        for task in self.objects:
            if task.window_name == window_name:
                task.spent_time = task.spent_time + 1
                exists = 1;
        if not exists:
            if pid:
                process_name = self.get_process_name( pid )
            else:
                process_name = "NaN"
            self.objects.append ( Task( window_name, process_name ))

    def list(self):
        for task in self.objects:
            print '{:s} --- {:s} --- {:s} '.format( task.process_name, task.window_name, self.int_to_time( task.spent_time) )

    def get_process_list(self):
        list = {}
        for task in self.objects:
            list[ task.process_name ] = 1
        return list.keys()

    def get_tasks_group_by_process(self):
        for process_name in self.get_process_list():
            total_time = 0;
            for task in self.objects:
                if task.process_name == process_name:
                    total_time = total_time + task.spent_time
            print '{:s} --- {:s}'.format( process_name, self.int_to_time(total_time) )
            self.get_process_tasks(process_name)


    def get_process_tasks(self, process_name ):
        for task in self.objects:
            if task.process_name == process_name:
                print '\t{:s} --- {:s}'.format( task.window_name, self.int_to_time( task.spent_time ) )



class Task:
    process_name = None
    window_name = None
    spent_time  = 0

    def __init__(self, window_name=None, process_name=None):
        self.window_name = window_name
        self.process_name = process_name


t = Tasks();
while True:
    try:
        out = check_output(['/usr/bin/xdotool', 'getwindowfocus','getwindowpid','getwindowname'],stderr=STDOUT).split('\n')
        ( process_pid, window_name ) = (out[0], out[1])
    except CalledProcessError as e:
        ( process_pid, window_name ) = (0, e.output.rstrip())

    t.monitor(window_name, process_pid)
    t.get_tasks_group_by_process()
    time.sleep(1)
