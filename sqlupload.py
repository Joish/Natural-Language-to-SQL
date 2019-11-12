# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 10:39:18 2018

@author: Joish
"""

from sqlalchemy import create_engine
import pandas as pd
from multiprocessing import Process


def replace(filename):
    engine = create_engine("mysql://root:joish@123@localhost/nlp2sql")
    con = engine.connect()
    df = pd.read_csv(filename,encoding="latin-1")

    
    #print ("-------------")
    #print (df)
    df.to_sql(name='data',con=con,if_exists='replace',index=False)
    #print ("After df")
    con.close()
    #return "sucess"

if __name__ == '__main__':
    p = Process(target=replace)
    p.start()
    p.join()