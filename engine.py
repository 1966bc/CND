#!/usr/bin/python3
""" This is the engine module of CND."""
import os
import sys
import inspect
from dbms import DBMS
from tools import Tools

__author__ = "1966bc aka giuseppe costanzi"
__copyright__ = "Copyleft"
__credits__ = ["hal9000",]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "beta 1"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "2019-03-4"
__status__ = "Production"

class Engine(DBMS, Tools):
    def __init__(self, *args, **kwargs):
        super(Engine, self).__init__()

        
        self.title = "CND-Italian National Classification of Medical Devices"

        self.version = self.get_version()

        platform = "Debian Release 9 (stretch) 64-bit"
        s = "%s ver %s\nwritten by\n1966bc\nMilk galaxy\nSolar System\nThird planet(Earth) Italy(Rome)\ngiuseppecostanzi@gmail.com\n%s"
        msg = (s % (self.title,self.version,platform))

        self.about = msg

        self.no_selected = "Attention!\nNo record selected!"
        self.mandatory = "Attention!\nField %s is mandatory!"
        self.delete = "Delete data?"
        self.ask_to_save = "Save data?"
        self.abort = "Operation aborted!"
        
        
    def __str__(self):
        return "class: %s" % (self.__class__.__name__, )


       
    def explode_dict(self, obj):
        #for debug...
        for k, v in obj.iteritems():
                print (k,v,type(v))

    def get_version(self):
        
        try:
            f = open('version', 'r')
            s = f.readline()
            f.close()
            return s
        except:
            print(inspect.stack()[0][3])
            print (sys.exc_info()[0])
            print (sys.exc_info()[1])
            print (sys.exc_info()[2])

    def get_dimensions(self):

        try:
            d = {}
            with open("dimensions", "r") as filestream:
                for line in filestream:
                    currentline = line.split(",")
                    d[currentline[0]] = currentline[1]
                      
            return d
        except:
            print(inspect.stack()[0][3])
            print (sys.exc_info()[0])
            print (sys.exc_info()[1])
            print (sys.exc_info()[2])                

   
def main():

    #testing some stuff

    print ("MRO:", [x.__name__ for x in Engine.__mro__])
   
    foo = Engine()

    print (foo)

    print (foo.get_connection())

    print (foo.title)

    
    input('end')
       
if __name__ == "__main__":
    main()
