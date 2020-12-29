#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Felipe Soares
"""

import requests
import json
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
import pyfiglet

ascii_banner = pyfiglet.figlet_format("DataCrypto Analytics")
print(ascii_banner)
#========================
criptomoeda = input('  | Create price chart and number of trades |'
                    '\n\n  | Twitter @DataCryptoML |'
                    '\n  | Github @datacryptoanalytics |'
                    '\n \nEnter the pair of cryptocurrencies listed on Binance: ')

print('\nThe cryptocurrency pair reported was: %s'
      '\n\nDataCrypto Analytics is scanning for values,'
      ' please wait a few seconds!' %(criptomoeda))


root_url = 'https://api.binance.com/api/v1/klines'

symbol = criptomoeda

interval = input('Enter the Timeframe (Example: 15m, 30m, 1h, 1d, 1M): ')

url = root_url + '?symbol=' + symbol + '&interval=' + interval

print(url)


# ===========
def get_bars(symbol, interva = interval ):
   url = root_url + '?symbol=' + symbol + '&interval=' + interval
   data = json.loads(requests.get(url).text)
   df = pd.DataFrame(data)
   df.columns = ['open_time',
                 'o', 'h', 'l', 'c', 'v',
                 'close_time', 'qav', 'num_trades',
                 'taker_base_vol', 'taker_quote_vol', 'ignore']
   df.index = [dt.datetime.fromtimestamp(x/1000.0) for x in df.close_time]
   return df

#============
criptomoeda = get_bars(criptomoeda)

criptomoeda_fechamento = criptomoeda['c'].astype('float')
criptomoeda_abertura = criptomoeda['o'].astype('float')
criptomoeda_num_trades = criptomoeda['num_trades'].astype('float')
criptomoeda_maxima = criptomoeda['h'].astype('float')
criptomoeda_minima = criptomoeda['l'].astype('float')
criptomoeda_volume = criptomoeda['v'].astype('float')
criptomoeda_datas_fechamento = criptomoeda['close_time'].astype('float')
criptomoeda_datas_abertura = criptomoeda['open_time'].astype('float')

#============  Indicadores
# Média movel de 14 dias do Fechamento
criptomoeda_fechamento_mediamovel = criptomoeda_fechamento.rolling(30).mean()
# Média movel de 30 dias do Fechamento
criptomoeda_fechamento_mediamovel100 = criptomoeda_fechamento.rolling(100).mean()
medias = criptomoeda_num_trades.rolling(12).mean()
# Retorno diário percentual
criptomoeda_fechamento_mediamovelDailyReturn = criptomoeda_fechamento.pct_change()
#print('Retorno Diario', criptomoeda_fechamento_mediamovelDailyReturn)
#print('\nMédia Movel 100 Periodos: \n%s' %(criptomoeda_fechamento_mediamovel100 ))
print('Média 100 periodos', criptomoeda_fechamento.mean())
print('Média num_trades', criptomoeda_num_trades.mean())
media = criptomoeda_fechamento.mean()
calc = criptomoeda_num_trades.mean()
#============  Criar Gráfico
#plt.style.use('ggplot')
plt.style.use('bmh')
plt.rcParams['figure.figsize'] = (9,5)
plt.rcParams['font.family'] = 'serif'

#============ Plotar indicadores
plt.subplot(2, 1, 1)
plt.plot(criptomoeda_fechamento, '-', color="black", linewidth=1)
plt.plot(criptomoeda_fechamento_mediamovel, '-', color="red", linewidth=1)
plt.plot(criptomoeda_fechamento_mediamovel100, '-', color="black", linewidth=1)
plt.legend(['Close', 'MA30', 'MA100'], loc=0)
plt.title('DataCrypto Analytics (@DataCryptoML)')
plt.ylabel('Price')

plt.subplot(2, 1, 2)
plt.plot(criptomoeda_num_trades, '-', color="black", linewidth=1)
plt.plot(medias, '-', color="red", linewidth=1)
plt.legend(['num_trades', 'MA12'], loc=0)
plt.xlabel('Github: @datacryptoanalytics', fontsize=9)
plt.ylabel('Number of Trades')
plt.gcf().autofmt_xdate()

plt.show()
