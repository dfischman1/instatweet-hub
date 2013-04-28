#!/usr/local/bin/python
import threading


def continuousUpdate():    
    print 'fischman'
    s = threading.Timer(1.0, continuousUpdate)
    s.start()

if __name__=='__main__':
    continuousUpdate()
