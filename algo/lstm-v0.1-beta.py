#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 20:48:46 2019

@author: Felipe Soares
"""
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import  Dense, Dropout, LSTM
import keras
import keras.backend as K
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

binance_historico = pd.read_csv('BTC-USD_Yahoo_5A.csv')
binance_historico.tail()
print(binance_historico.tail())

pd.set_option('display.float_format', '{:5f}'.format)
print(binance_historico.describe().transpose())

binance_historico.isnull().sum()

# Retira dados da nossa fucking tabela
binance_historico = binance_historico.dropna()
binance_historico.shape
print(binance_historico.shape)

plt.figure(figsize=(13,7))
sns.set_context('notebook', font_scale=1.5, rc= {'font.size':20,
                                                 'axes.titlesize':20,
                                                 'axes.labelsize':18})

sns.kdeplot(binance_historico['Open'], color = 'green')
sns.rugplot(binance_historico['Open'], color = 'red')
sns.distplot(binance_historico['Open'], color = 'green')
sns.set_style('darkgrid')

plt.xlabel('Distribuição do preço de abertura');

plt.figure(figsize=(13,7))
binance_historico.iloc[:,1].plot(label ='Abertura', color = 'red')
binance_historico.iloc[:,3].plot(label ='Fechamento', color = 'blue')
plt.ylabel('Preço de Abertura')
plt.xlabel('Periodo')
plt.title('Histórico de preço da Binance_Coin')
plt.legend();
plt.figure(figsize=(13,7))
binance_historico['Volume'].plot()
binance_historico.Volume.argmax()
#=================================================
binance_historico = pd.read_csv('BTC-USD_Yahoo_5A.csv')
binance_historico.dropna(inplace=True)
binance_treinamento = binance_historico.iloc[:,1:2].values
binance_treinamento[0:10]

min_scaler = MinMaxScaler(feature_range=(0,1))
binance_treinamento_normalizada = min_scaler.fit_transform(binance_treinamento)
binance_treinamento_normalizada[0:10]
# Previsão começa aqui caraio, arrumando dados da binance para prediction
previsores = []
preco_real = []
for i in range(90, len(binance_historico)):
    previsores.append(binance_treinamento_normalizada[i-90:i,0])
    preco_real.append(binance_treinamento_normalizada[i, 0])
print('Tamanho do Dataset criado de previsores', len(previsores))
print('\n')
previsores[0]

print('Tamanho do Dataset criado de previsores', len(preco_real))
print('\n')
preco_real[0]

previsores , preco_real = np.array(previsores), np.array(preco_real)
print('Formato Previsores', previsores.shape)
print('\n')
print('Formato Preco_real', preco_real.shape)
pd.concat([pd.DataFrame(previsores), pd.DataFrame(preco_real)], axis=1).head(10)

# Deixando os valores do treinamento em formato Keras
previsores = np.reshape(previsores, newshape= (previsores.shape[0], previsores.shape[1], 1))
previsores.shape
#=======================
# REGRESSOR COM REDE NEURAL RECORRENTE

# K.clear_session()
regressor = Sequential()
# Passa a flag return_sequences = True pois teremos mais uma camada conectada em nossa rede
regressor.add(LSTM(units= 100, return_sequences = True, input_shape = (previsores.shape[1], 1) ))
# Utilizada a técnica dropout com 0.3, assim teremos 30% dos neuronios 'desligados' aleatoriamente por passada
# Esta técninca de Dropout evita o ovefitting (quando o modelo aprende demais com os dados de treinamento)
regressor.add(Dropout(0.3))
regressor.add(LSTM(units=50, return_sequences = True))
regressor.add(Dropout(0.3))
regressor.add(LSTM(units=50, return_sequences = True))
regressor.add(Dropout(0.3))
regressor.add(LSTM(units=50, return_sequences = False))
regressor.add(Dropout(0.3))
# Agora passamos  a camada Densa ao modelo para ligar todos os neuronios da camada anterios
# Deixamos a função de ativação como linear pois estamos resolvendo um problema de regressão, porém como nosso dados
# estão normalizados entre 0 e 1, poderiamos  utilizar a  função sigmoid. pois esta também trabalha  no range de 0 e 1
regressor.add(Dense(units=1, activation = 'linear'))
# Deixamos o parâmetro metrics como mean_absolute_error pois os valores são mais fáceis de compreender (mesma escala)
regressor.compile(optimizer='adam', loss='mean_squared_error', metrics=['mean_absolute_error'])
regressor.fit(previsores, preco_real, epochs= 120, batch_size= 32)
regressor.summary()
print(regressor.summary)
#======= Carregando dados de teste
binance_test = pd.read_csv('BTC-USD_Yahoo_5A.csv')
print('Formato do arquivo de teste', binance_test.shape)
print('\n')
print('Primeiras linhas do Dataset')
binance_test.head()
binance_test.isnull().sum().max()
#====== Concatenar preços base para contemplar os 90 dados anteriores
preco_real_test = binance_test.iloc[:, 1:2].values
binance_completa = pd.concat((binance_historico['Open'], binance_test['Open']), axis=0)
binance_completa.shape
binance_completa.isnull().sum().max()
binance_completa.dropna(inplace=True)
#======= Variavel 'entradas'para contemplar dados anteriores(22 novo registros de teste + 90 anteriores)
entradas = binance_completa[len(binance_completa) - len(binance_test) - 90:].values
entradas.shape
entradas = entradas.reshape(-1,1)
entradas.shape
#======= Normalização dos dados teste: 3 observações iniciais já normalizadas
entradas = min_scaler.transform(entradas)
entradas[0:3]

X_teste = []
for i in range(90,112):
    # Inicia loop em 90
    X_teste.append(entradas[i-90:i,0])
X_teste = np.array(X_teste)
X_teste = np.reshape(X_teste, newshape=(X_teste.shape[0], X_teste.shape[1], 1))

print('Formato do Shape do X_teste')
print(X_teste.shape)

previsoes = regressor.predict(X_teste)
previsoes[0:10]
#====== Agora que você seguiu o pai até aqui nesse belo código, vamos reverter os valores para escala original
#====== Vou usar a função inverse_transform
previsoes = min_scaler.inverse_transform(previsoes)
previsoes[0:10]
previsoes.shape

print(previsoes.shape)

#================== Média de preços
print('Media precos reais', preco_real_test.mean())
print('Media previsoes', previsoes.mean())
print('Diferenca da media entre o valor_real e a previsao',round(previsoes.mean() - preco_real_test.mean(),2))
#=================== Grafico previsao
plt.figure(figsize=(13,8))
plt.plot(preco_real_test, color = 'red', label = 'Preco_real')
plt.plot(previsoes, color = 'blue', label = 'Previsoes')
plt.title('Previsao de precos Binance_Coin')
plt.legend()
plt.xlabel('Periodo')
plt.ylabel('Precos')
plt.show()
