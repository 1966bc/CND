#!/usr/bin/python3
""" This is the engine module of CND."""

import sqlite3 as lite
import os
import sys

__author__ = "1966bc aka giuseppe costanzi"
__copyright__ = "Copyleft"
__credits__ = ["hal9000",]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "beta 1"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "2019-03-4"
__status__ = "Production"

class DBMS(object):
    def __init__(self, *args, **kwargs):
        super(DBMS, self).__init__()

       
    def get_connection(self,):

        con = lite.connect('cnd.db',isolation_level = 'IMMEDIATE')
        con.text_factory = lambda x: str(x, 'iso-8859-1')
        return con
        
        
    def read(self, fetch, sql, args=()):
       
        try:
            
            con = self.get_connection()

            cur = con.cursor()
        
            cur.execute(sql,args)

            if fetch == True:
                rs =  cur.fetchall()
            else:
                rs =  cur.fetchone()
            
            return rs

        except:
            print (sys.exc_info()[0])
            print (sys.exc_info()[1])
            print (sys.exc_info()[2])
            
        finally:
            try:
                cur.close()
                con.close()
            except:
                print (sys.exc_info()[0])
                print (sys.exc_info()[1])
                print (sys.exc_info()[2])

   
    def write(self, sql, args=()):
        try:
            con = self.get_connection() 
            cur = con.cursor()
            cur.execute(sql,args)
            con.commit()
            
        except:
            con.rollback()
            print (sys.exc_info()[0])
            print (sys.exc_info()[1])
            print (sys.exc_info()[2])
            
        finally:
            try:
                cur.close()
                con.close()
            except:
                print (sys.exc_info()[0])
                print (sys.exc_info()[1])
                print (sys.exc_info()[2])


    def get_fields(self,table):
        """Return fields name for the passed table ordered by field position"""

        try:

            columns = []
            ret = []

            sql = 'SELECT * FROM %s ' % table
            con = self.get_connection()
            cur = con.cursor()
            cur.execute(sql)

            for field in cur.description:
                columns.append(field[0])
            cur.close()
            
            for k,v in enumerate(columns):
                if k > 0:
                    ret.append(v)
            return ret
        except:
            print (sys.exc_info()[0])
            print (sys.exc_info()[1])
            print (sys.exc_info()[2])
            
        finally:
            try:
                cur.close()
                con.close()
            except:
                print (sys.exc_info()[0])
                print (sys.exc_info()[1])
                print (sys.exc_info()[2])

    def get_update_sql(self,table,pk):

        return "UPDATE %s SET %s =? WHERE %s =?"%(table," =?, ".join(self.get_fields(table)),pk)

    def get_insert_sql(self,table,n):

        #n = len(args)

        return "INSERT INTO %s(%s)VALUES(%s)"%(table,",".join(self.get_fields(table)), ",".join("?"*n))

    def get_selected(self,table,field,*args):
        """recive table name, pk and return a dictionary
       
        @param name: table,field,*args
        @return: dictionary
        @rtype: dictionary
        """
        
        d = {}
        sql = "SELECT * FROM %s WHERE %s =?" % (table,field)

        for k,v in enumerate(self.read(False,sql,args)):
            d[k]=v
            
        return d

 
               
def main():
    

    foo = DBMS()
    print (foo)

    sql = "SELECT name FROM sqlite_master WHERE type = 'table'"
    rs = foo.read(True, sql)
    if rs:
        for i in enumerate(rs):
            print (i)

    input('end')
    
    
if __name__ == "__main__":
    main()
