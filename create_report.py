"""Erstellt Grafiken aus den von interrupt.py gesammelten Daten
   Autor: Klaus Ritter, Lizenz: MIT
"""

from datetime import datetime
from datetime import timedelta
import pandas as pd
import matplotlib.pyplot as plt
import ftplib
import zaehlerconfig
import logging

logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logdateiname = "zaehler.csv"

# Hilfreiche Befehle
# print(df.to_string())
# print(df.dtypes)
# print (df_gruppiert.dtypes)
# print(df_gruppiert.to_string())
# plt.show()

############################# Daten vorbereiten ###############################
# CSV-Datei in Pandas einlesen, Spaltentitel definieren
df = pd.read_csv(logdateiname, sep=';', names=['Impuls', 'Nummer', 'Label', 'Zeitpunkt'])

# unnötige Spalten löschen
df = df.drop(columns=['Impuls', 'Nummer', 'Label'])

# Zeitpunkt-Spalte in das richtige Format bringen
df['Zeitpunkt'] = pd.to_datetime(df['Zeitpunkt'], format='%Y-%m-%d %H:%M:%S.%f')
df['Datum'] = pd.to_datetime(df['Zeitpunkt'], format='%Y-%m-%d')

############################# Summe nach Datum (Tag) ###############################
# Summe pro Tag bilden (gruppieren)
logger.debug('Tage gruppieren')
df_gruppiert_datum = df.groupby(pd.Grouper(key='Datum',freq='5D')).agg(summe=('Datum', 'count'))

# Diagramm erstellen
gas_nach_datum = df_gruppiert_datum.plot(kind = 'bar', fontsize=8, xlabel = 'Datum', ylabel = 'Zählimpulse', legend = False)

# Beschriftung der x-Achse in ein schönes Format bringen
x_labels = df_gruppiert_datum.index.strftime('%d.%m.')
gas_nach_datum.set_xticklabels(x_labels)

# Ergebnis als Bild speichern
plt.savefig('web/img/diagramm_gas_pro_tag.png')

############################# Summe nach Datum (letzte 30 Tage) ###############################
# Summe pro Tag bilden (gruppieren)
logger.debug('Tage gruppieren (letzte 30 Tage)')
heute = datetime.today().strftime('%Y-%m-%d') # das Skript sollte erst nach Mitternacht laufen
vor30tagen =  (datetime.today() + timedelta(days=-30)).strftime('%Y-%m-%d') 
df_letzte_30_tage = df[(df['Datum'] > vor30tagen) & (df['Datum'] < heute)]
df_gruppiert_datum = df_letzte_30_tage.groupby(pd.Grouper(key='Datum',freq='D')).agg(summe=('Datum', 'count'))

# Diagramm erstellen
gas_nach_datum = df_gruppiert_datum.plot(kind = 'bar', fontsize=8, xlabel = 'Datum', ylabel = 'Zählimpulse', legend = False)

# Beschriftung der x-Achse in ein schönes Format bringen
x_labels = df_gruppiert_datum.index.strftime('%d.%m.')
gas_nach_datum.set_xticklabels(x_labels)

# Ergebnis als Bild speichern
plt.savefig('web/img/diagramm_gas_pro_tag_letzte_30.png')

############################# Summe nach Tageszeit ###############################
# Summe pro Tag bilden (gruppieren)
logger.debug('Tageszeit gruppieren')
df_gruppiert_tageszeit = df.groupby(df['Zeitpunkt'].dt.hour).count()

# unnötige Spalten löschen
df_gruppiert_tageszeit = df_gruppiert_tageszeit.drop(columns=['Datum'])

# Diagramm erstellen
gas_nach_tageszeit = df_gruppiert_tageszeit.plot(kind = 'bar', fontsize=8, xlabel = 'Stunde', ylabel = 'Zählimpulse', legend = False)

# Ergebnis als Bild speichern
plt.savefig('web/img/diagramm_gas_pro_stunde.png')

############################# Summe nach Tageszeit (gestern) ###############################
# Summe pro Tag bilden (gruppieren)
logger.debug('Tageszeit gruppieren')
bereich_start =  (datetime.today() + timedelta(days=-5)).strftime('%Y-%m-%d') 
bereich_ende =  (datetime.today() + timedelta(days=-4)).strftime('%Y-%m-%d') 
df_gestern = df[(df['Datum'] > bereich_start) & (df['Datum'] < bereich_ende)]
df_gruppiert_tageszeit = df_gestern.groupby(pd.Grouper(key='Datum',freq='30min')).count()

# Diagramm erstellen
gas_nach_tageszeit = df_gruppiert_tageszeit.plot(kind = 'bar', fontsize=8, xlabel = 'Stunde', ylabel = 'Zählimpulse', legend = False)

# Ergebnis als Bild speichern
plt.savefig('web/img/diagramm_gas_pro_stunde_gestern.png')

############################# Dateien hochladen ###############################
logger.debug('FTP-Upload startet')
session = ftplib.FTP(zaehlerconfig.ftp_adress, zaehlerconfig.ftp_username, zaehlerconfig.ftp_password)
file = open('web/img/diagramm_gas_pro_tag.png','rb')                  
session.storbinary('STOR img/diagramm_gas_pro_tag.png', file)   
file.close()
file = open('web/img/diagramm_gas_pro_tag_letzte_30.png','rb')                  
session.storbinary('STOR img/diagramm_gas_pro_tag_letzte_30.png', file)   
file.close()
file = open('web/img/diagramm_gas_pro_stunde.png','rb')                  
session.storbinary('STOR img/diagramm_gas_pro_stunde.png', file)   
file.close()  
file = open('web/img/diagramm_gas_pro_stunde_gestern.png','rb')                  
session.storbinary('STOR img/diagramm_gas_pro_stunde_gestern.png', file)   
file.close()                             
session.quit()
logger.debug('FTP-Upload beendet')