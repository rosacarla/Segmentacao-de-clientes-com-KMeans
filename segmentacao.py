# -*- coding: utf-8 -*-
"""Segmentacao.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_5c0uI2v4oZZmzqAsHHnUKqD_jqQFKTx

# Segmentação de dados
## Autora: Carla Edila Silveira
## Dataset: Vendas por Fatura, disponível em: https://drive.google.com/file/d/14T8yNDk_XNsKATT3bP7f2RrMS1ydZWFg/view
## Data: 15/07/2022
"""

import pandas as pd
import numpy as np #funcoes numericas, matematicas, vetores, matrizes
from datetime import datetime as dt
from sklearn.cluster import KMeans #importa biblioteca de pra analise de cluster

tabela = pd.read_csv('/content/sample_data/vendas-por-fatura.csv')
#link dataset: https://drive.google.com/file/d/14T8yNDk_XNsKATT3bP7f2RrMS1ydZWFg/view

tabela.head(10)

tabela.info()
#transformar data de tipo texto pra data
#tratar dados ausentes, eliminar 
#transformar nros de tipo texto pra numero

tabela.dropna(subset=['ID Cliente']) 
#eliminados os dados faltantes

tabela['Data da fatura'].values[0]
#mostra 1o. valor da coluna

tabela['Data da fatura'] = tabela['Data da fatura'].apply(lambda x: dt.strptime(x, '%m/%d/%Y %H:%M:%S'))

tabela['Valor'] = tabela['Valor'].apply(lambda x: float(x.replace(',','.')))

tabela['Ticket Medio'] = tabela['Valor'] / tabela['Quantidade']

tabela.head()

tabela['Valor'].hist(bins=50, range=(-1000,1000))
#plota grafico de histograma com 50 barras e range de -1000 a 1000

tabela[tabela['Valor']<0]

tabela['Valor'].max()
#mostra valor maximo

tabela[tabela['Valor']==tabela['Valor'].max()]
#mostra valor maximo da coluna Valor

tabela['Quantidade'].max()
#mostra maior valor da tabela

tabela = tabela[tabela['Valor']>0]

tabela.info()

np.unique(tabela['ID Cliente'])
#mostra array de valores unicos

len(np.unique(tabela['ID Cliente']))
#conta valore unicos

tabela['Data da fatura'].min()

tabela['Data da fatura'].max()

t1 = tabela.pivot_table(index='ID Cliente',values='N° da fatura',aggfunc='count').reset_index()
#t1 é tabela temporaria com calculo da frequencia relativa de cada cliente na base de dados
#resetados os indices da tabela

t1.head()
#mostra tabela tratada

tabela.columns

t1.columns = ['ID Cliente', 'Frq']

t1.join(tabela[['ID Cliente', 'País']], lsuffix=['ID Cliente'], rsuffix=['ID Cliente'])

t2 = pd.merge(t1,tabela,how='left',on='ID Cliente')

t3 = t2.pivot_table(index='ID Cliente',values=['Quantidade','Valor','Ticket Medio','Frq'], aggfunc='mean')
#mostra frequencia do cliente, qunantidade, valor, ticket medio e media de valor

t3

modelo = KMeans(5).fit(t3)
#modelo de clusterização em 5 grupos/classes

modelo.labels_.shape
#mostra quantidade de rotulos das classes

t4 = t2.pivot_table(index='ID Cliente',values=['Quantidade','Valor','Ticket Medio','Frq'], aggfunc='mean').reset_index()

t4['Cluster'] = modelo.labels_

t4
#mostra tabela t4

t4[(t4['Valor']<1000)&(t4['Frq']<10)].plot.scatter(x='Frq',y='Valor',c= 'Cluster', cmap='magma')
#plota grafico

t4[(t4['Valor']<1000)&(t4['Frq']<10)].boxplot(column='Frq',by='Cluster')
#plota boxplot da frequencia de Valor

"""0"""