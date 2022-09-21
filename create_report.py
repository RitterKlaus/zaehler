from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('zaehler-20220908.csv', sep=';', names=['Impuls', 'Nummer', 'Label', 'Zeitpunkt'])
#df.set_index('Date',inplace=True)

#with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#    print(df)

# print(df.to_string())

print (df.dtypes)

df = df.drop(columns=['Impuls', 'Nummer', 'Label'])
df['Zeitpunkt'] = pd.to_datetime(df['Zeitpunkt'], format='%Y-%m-%d %H:%M:%S.%f')
df['Datum'] = pd.to_datetime(df['Zeitpunkt'], format='%Y-%m-%d')

print (df.dtypes)

#df['Date'] = pd.to_datetime(df['timestamp']).dt.date

df_gruppiert = df.groupby(pd.Grouper(key='Datum',freq='5D')).agg(summe=('Datum', 'count'))

print (df_gruppiert.dtypes)
print(df_gruppiert.to_string())


df_gruppiert.plot(kind = 'bar')
#plt.show()
plt.savefig('bild.png')