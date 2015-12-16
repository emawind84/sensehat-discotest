from abc import ABCMeta, abstractmethod

class AbstractMonitor(object):
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def run(self):
        pass