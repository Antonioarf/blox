# -*- coding: utf-8 -*-
"""Classsificador_googlesheets.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NKclVptZP4pa6Hgswfmc7P7hoOtN3Qfb
"""

import pandas as pd;
import numpy as np
from stop_words import get_stop_words
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

import openpyxl
from openpyxl import Workbook
import xlsxwriter
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("ml-blox.json",scope)
client= gspread.authorize(creds)
sheet = client.open("eu").sheet1
headers = sheet.row_values(1)
classificar = sheet.col_values(1)

espm = sheet.get_all_records()
df = pd.DataFrame(espm)
colunas = df.columns

url = 'https://github.com/Antonioarf/blox/blob/master/excel/Book1.xlsx?raw=true'
df1 = pd.read_excel(url)
df1 = df1.loc[:, ~df1.columns.str.contains('^Unnamed')]
treino = df1.dropna()

def deletar_caracteres(coluna):
# coluna = coluna.replace("Humanidades e Linguagens","Humanidades, Artes e Linguagens").replace("Matemática e Computação","Matemática, Computação e Tecnologias de Informação e Comunicacão").replace("Ciências Sociais e Negócios","Ciências Sociais, Jornalismo e Informação").replace("Psicologia e Desenvolvimento","Psicologia e Desenvolvimento Pessoal").replace("Negócios e Administração","Administração e Negócios")
# coluna = coluna.replace("Ciências Sociais, Jornalismo e Informação",'1').replace("Saúde e Bem-Estar Social",'2').replace("Engenharia, Produção e Construção",'3').replace("Ciências Naturais",'4').replace('Humanidades, Artes e Linguagens','5').replace("Matemática, Computação e Tecnologias de Informação e Comunicacão",'6').replace("Direito",'7').replace("Educação",'8').replace("Psicologia e Desenvolvimento Pessoal",'9').replace("Serviços",'10').replace("Administração e Negócios",'11')
    
    return coluna
my_tags = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14']
# my_tags =[1,2,3,4,5,6,7,8,9,10,11]

from sklearn.linear_model import LogisticRegression
def machine (lista):
    X_train =  treino["materias"]
    y_train = deletar_caracteres(treino["ÁREA DO CONHECIMENTO"])
    X_test = lista
    logreg = Pipeline([('vect', TfidfVectorizer()),
                ('tfidf', TfidfTransformer()),
                ('clf', LogisticRegression(n_jobs=1, C=1e5)),
               ])
    logreg.fit(X_train, y_train)

#   %time

    y_pred = logreg.predict(X_test)

  # print('accuracy %s' % accuracy_score(y_pred, y_test))
  # print(classification_report(y_test, y_pred))
    return y_pred

resul = machine(classificar)
x=1
for e in resul:
    sheet.update_cell(x,2, e)
    x+=1