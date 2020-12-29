#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para buscar sentimento de alguma criptomoeda no twitter
@author: Felipe Ssoares
"""
import matplotlib.pyplot as plt
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from textblob import TextBlob as tb
import tweepy
import numpy as np

consumer_key = 'SUA API KEY TWITTER'
consumer_secret = 'SUA API SECRET KEY TWITTER'

access_token = 'SEU ACCESS TOKEN'
access_token_secret = 'SEU ACCESS TOKEN'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#Variável que irá armazenar todos os Tweets com
#a palavra escolhida na função search da API
pesquisa = input('DataCrypto Analytics | Sentiment Algorithm |'
                    '\n\n | Twitter @DataCryptoML |'
                    '\n | Github @datacrypto-analytics |'
                    '\n\nQual palavra deseja calcular o sentimento no Twitter?'
                    '\n\nDigite aqui por favor: ')


public_tweets = api.search(pesquisa)

tweets = [] # Lista vazia para armazenar scores
for tweet in public_tweets:
    print(tweet.text,)
    analysis = tb(tweet.text)
    polarity = analysis.sentiment.polarity
    tweets.append(polarity)
    print(polarity)


print('================================='
      '\n\nA média calculada foi de: ' + str(np.mean(tweets)))



#============  Criar Gráfico
#plt.style.use('ggplot')
plt.style.use('bmh')
plt.rcParams['figure.figsize'] = (9,5)
plt.rcParams['font.family'] = 'serif'

#============ Plotar indicadores
plt.plot(tweets, '-', color="black", linewidth=1)
plt.legend(['Sentiment', 'MA30', 'MA100', 'Midpoint' ], loc=0)
plt.title('DataCrypto Analytics (@DataCryptoML)')
plt.ylabel('Sentiment')
'''
plt.subplot(2, 1, 2)
plt.plot(atr, '-', color="black", linewidth=1)
plt.legend(['ATR', 'MA12'], loc=0)
plt.xlabel('Github: @datacrypto-analytics', fontsize=9)
plt.ylabel('ATR(Volatilite)')
plt.gcf().autofmt_xdate()
'''
plt.show()
