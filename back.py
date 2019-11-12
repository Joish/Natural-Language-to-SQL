from flask import Flask, request,redirect
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api,reqparse
from json import dumps
from flask_jsonpify import jsonify
from werkzeug import secure_filename
import os
import subprocess
from sqlalchemy import create_engine

import MySQLdb
import pandas as pd
import nltk
from nltk.corpus import wordnet
from difflib import SequenceMatcher

from sqlupload import replace

import sqlupload as sp

app = Flask(__name__)
api = Api(app)

CORS(app)

parser = reqparse.RequestParser()
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 19:32:37 2018

@author: Joish
"""
cn=[]
utl = []
def checker(q):
    test = q
    test = test.lower()
    test = test.split()
    
    low=[]
    for c in cn:
        # print ("*****************************")
        # print (c.lower())
        low.append(c.lower())
    

    print ('qwerty',low)
    te ={}
    for words in test:
        for word in low:
            print (words , word)
            seq=SequenceMatcher(None,words,word)
            d = seq.ratio()
            if d>.60:
                te[test.index(words)]=word
                break
            print (d)

    print (te)   
    for key,value in te.items():
        utl.append(value)
        test[key] = value
        
    return " ".join(test)

result={}

def SqlGen(q): 

    db = MySQLdb.connect("localhost","root","joish@123","nlp2sql" )  # Open database connection

    cursor = db.cursor()  # prepare a cursor object using cursor() method
    cursor.execute("desc data") # execute SQL query using execute() method.
    data = cursor.fetchall()

    column_name=[]
    column_dt={}

    for col in range (len(data)):
        column_name.append(data[col][0].lower())
        column_dt[data[col][0]] = data[col][1].lower()

    cursor.execute("select * from data") # execute SQL query using execute() method.
    data = cursor.fetchall()    
    df = pd.DataFrame(list(data))
    df.columns = column_name
    
    df = df.apply(lambda x: x.astype(str).str.lower())  #convert entire dataframe to lower case

    nlp = q
    nlp = nlp.lower()
    nlp_list = list(nlp.split(" "))
    nlp_list_c = nlp_list[:]
    
    inCloumnName=[]
    inCloumnValue={}
    
    remove_list=[]
    
    def remove(elearr):
        for val in elearr:
            try:
                nlp_list_c.remove(val)
            except:
                pass
        remove_list.clear()
        
    def getMeaning(word):
        synonyms = []
        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                synonyms.append(l.name())
        return synonyms
    
    map_list = []
    def getRelativity(k,meani_dict,copy_list):
        for word1 in copy_list:
            for word2 in meani_dict:
                seq = SequenceMatcher(None,word1,word2)
                d = seq.ratio()*100
                print (word1+" "+word2+"->"+str(int(d)))
                if (int(d)>=60):
                    map_list.append(k)
                    
    
    def Fnresult(q1,q2):
        result['q1'] = q1
        result['q2'] = q2
        
        value = list(set(result.values()))
        #print("_______________________________________________")
        #print("POSSIBLE QUERY:")
        #print("_______________________________________________")
        #print("\n")
        for res in value:
            if(res != None):
                print (res)
        print("_______________________________________________")
            
    for words in nlp_list_c:
        try:
            int(words)
            if nlp_list_c[nlp_list_c.index(words)+1] == "to":
                x= words
                check_list = [nlp_list_c[nlp_list_c.index(words)-1],nlp_list_c[nlp_list_c.index(words)-2],nlp_list_c[nlp_list_c.index(words)-3]]
                for some in check_list:
                    if some in column_name:
                        x=" ".join(nlp_list_c[nlp_list_c.index(x):nlp_list_c.index(x)+3])
                        inCloumnValue.setdefault(some, []).append(x)
                        x = x.split()
                        remove_list.append(some)
                        remove_list.append(x[0])
                        remove_list.append(x[1])
                        remove_list.append(x[2])               
        except:
            pass
        
    remove(remove_list)
    
    for words in nlp_list_c:
        if words in column_name:
            inCloumnName.append(words)
            remove_list.append(words)
    
    remove(remove_list)
            
    for words in column_name:
        for word in nlp_list_c:
            if word in list(df[words]):
                inCloumnValue.setdefault(words, []).append(word)
                remove_list.append(word)
    
    remove(remove_list)
                
    temp_arr=[]
    
    for key in inCloumnValue.keys():
        try:
            if(int(inCloumnValue[key][0])):
                if len(inCloumnValue[key]) == 2:
                    #print ("asd")
                    inCloumnValue[key] = [str(key+" between "+inCloumnValue[key][0]+" and "+inCloumnValue[key][1])]
                #print ("t"+key)
                elif len(inCloumnValue[key]) >= 3:
                    #print ("3")
                    for value in range (len(inCloumnValue[key])):
                        temp_arr.append(str(key)+'='+inCloumnValue[key][value])
                    inCloumnValue[key] = [" or ".join(temp_arr)]
                    temp_arr.clear()
                
                elif len(inCloumnValue[key]) == 1:
                    inCloumnValue[key] = [str(key)+"="+inCloumnValue[key][0]]
                             
        except:
            if 'to' in inCloumnValue[key][0]:
                #print ("e"+key)
                inCloumnValue[key][0] = (str(key +" between "+inCloumnValue[key][0]).replace("to" , "and"))
                #print (inCloumnValue[key][0])
            else:
                length = len(inCloumnValue[key])
                if length == 1:
                    inCloumnValue[key] = [str(key)+"= '"+inCloumnValue[key][0]+"'"]
                else:
                    for value in range (length):
                        temp_arr.append(str(key)+"= '"+inCloumnValue[key][value]+"'")
                    inCloumnValue[key] = [" or ".join(temp_arr)]
                    temp_arr.clear()
    
    meaning={}
    map_meaning = {'maximum' :'max','max' : 'max','minimum' : 'min','min' :'min','count':'count','distinct' : 'distinct','unique' : 'distinct'}
    meaning_list = ['maximum','minimum','distinct','count','max','min','unique']
    
    for word in meaning_list:                
        meaning[word] = getMeaning(word)
        
    for key in meaning.keys():
        ss = set(nlp_list_c).intersection(meaning[key])
        if (len(ss)>=1):
            ind = nlp_list.index(list(ss)[0])
            manu = nlp_list[ind+1:]
            manu = list(set(inCloumnName).intersection(manu))
            find = []
            for words in manu:
                find .append(nlp_list.index(words))
            try:
                inCloumnName[inCloumnName.index(nlp_list[min(find)])] = str(map_meaning[key])+"("+ str(nlp_list[min(find)]) +")"
            except:
                return redirect("http://localhost:4200/bad_request")
        else:
            pass
           # map_list.append(key)
            
        #getRelativity(key,meaning[key],nlp_list_c)
        
    #set(map_list)
    
    '''for words in inCloumnValue.keys():
        if words in inCloumnName:
            inCloumnName.remove(words)'''
            
    #tagged_sentences = nltk.pos_tag(nlp_list_c)
    #ne_chunked_sents = nltk.ne_chunk(tagged_sentences)
                
    if len(inCloumnName)==0 and len(inCloumnValue)==0:
        print ("your query didnt match the database.....PLEASE TrY AGAIN")
        query1 = "your query didnt match the database.....PLEASE TrY AGAIN"

        Fnresult(query1,None)

    elif len(inCloumnName)==0 and len(inCloumnValue)>0:
        where = []
        for value in inCloumnValue.values():
             where.append(value[0])
        query1 = "SELECT * FROM DATA WHERE "+ " and ".join(where)+";"
        query2 = "SELECT * FROM DATA WHERE "+ " or ".join(where)+";"
        
        Fnresult(query1,query2)
        
    elif len(inCloumnName)>0 and len(inCloumnValue)==0:
        select = inCloumnName
        query1 = "SELECT "+" , ".join(select)+" FROM DATA"+";"
        
        Fnresult(query1,None)
        
    elif len(inCloumnName)>0 and len(inCloumnValue)>0:
        select = inCloumnName
        where = []
        for value in inCloumnValue.values():
             where.append(value[0])
        query1 = "SELECT "+" , ".join(select)+" FROM DATA WHERE "+ " and ".join(where)+";"
        query2 = "SELECT "+" , ".join(select)+" FROM DATA WHERE "+ " or ".join(where)+";"
        
        Fnresult(query1,query2)
        
    else:
        print ("PLEASE TRY AGAIN")
        query1 = "PLEASE TRY AGAIN"

        Fnresult(query1,None)

    db.close()

    return result

# questions = pd.read_csv("sharmila-sales_questions.csv")

# for question in questions['questions']:
#     print (question)
#     SqlGen(checker(question))
    
#question = input("Question:")
#SqlGen(checker(question)) 

#print(column_name)
#print (result)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)),"upload")
ALLOWED_EXTENSIONS = set(['csv'])
print (UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def hello():
    return jsonify({'text':'Hello World!'})

    

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            f = request.files['file']
            ext = (str(f.filename)).split(".")
            print (ext)
            if 'csv' in ext:
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
                filen = (os.path.join(os.path.dirname(os.path.abspath(__file__)),"upload"))+"\\"+f.filename
                df2 = pd.read_csv(filen,encoding='latin-1')
                #print (df2)
                ret = replace(filen)
                cn.clear()
                for li in list(df2):
                    cn.append(li)
                #SqlGen(checker(l[0]))
                return redirect("http://localhost:4200/generator")
                #df2 = pd.read_csv()
            else:
                return redirect("http://localhost:4200/bad_request")
        except:
            return redirect("http://localhost:4200/bad_request")


@app.route('/query', methods = ['GET', 'POST'])
def query():
    if request.method == 'POST':
        text = request.form['text']
        #processed_text = text.upper()
        print ("------"+str(len(text)))
        if len(text)==0:
            #jav.append("your query didnt match the database.....PLEASE TrY AGAIN")
            return redirect("http://localhost:4200/empty")
        else:
            damn = SqlGen(checker(text))
            #return jsonify(damn)
            return redirect("http://localhost:4200/generator")
        


class CloumnValues(Resource):
    def get(self):
        #print ("1234567890",cn)
        return jsonify(cn)

class Result(Resource):
    def get(self):
        #print (result)
        resultt = list(set(result.values()))
        jav = []
        for r in resultt:
            if r!=None:
                jav.append(r)
        if (len(jav)==0):
            jav.append("Please Try some Query...")
        return jsonify(jav)

class QueryResult(Resource):
    def get(self):
        resultt = list(set(result.values()))
        jav = []
        for r in resultt:
            if r!=None:
                jav.append(r)

        answer = []
        
        print("********************************")
        for j in jav:
            print (j)
            db = MySQLdb.connect("localhost","root","joish@123","nlp2sql" )  # Open database connection

            cursor = db.cursor()  # prepare a cursor object using cursor() method
            try:
                cursor.execute(j) # execute SQL query using execute() method.
                data = cursor.fetchall()
                answer.append(data)
            except:
                answer.append('Error')
                print ("Error in sql")

        print("********************************")
        return jsonify(answer)

       
# class Upload(Resource):
#     def post(self):
#         print request.files
#         # checking if the file is present or not.
#         if 'file' not in request.files:
#         return "No file found"
        
#         file = request.files['file']
#         file.save("static/test.jpg")
#         return "file successfully saved"


# class Employees_Name(Resource):
#     def get(self, employee_id):
#         print('Employee id:' + employee_id)
#         result = {'data': {'id':1, 'name':'Balram'}}
#         return jsonify(result)    


api.add_resource(CloumnValues, '/columnvalues') # Route_1
api.add_resource(Result, '/result') # Route_1
api.add_resource(QueryResult, '/query_result') # Route_1


# api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3


if __name__ == '__main__':
   app.run(port=5002)