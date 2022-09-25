from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import ftplib
import zaehlerconfig

# Hilfreiche Befehle
# print(df.to_string())
# print(df.dtypes)
# print (df_gruppiert.dtypes)
# print(df_gruppiert.to_string())
# plt.show()

############################# Daten vorbereiten ###############################
# CSV-Datei in Pandas einlesen, Spaltentitel definieren
df = pd.read_csv('zaehler.csv', sep=';', names=['Impuls', 'Nummer', 'Label', 'Zeitpunkt'])

# unnötige Spalten löschen
df = df.drop(columns=['Impuls', 'Nummer', 'Label'])

# Zeitpunkt-Spalte in das richtige Format bringen
df['Zeitpunkt'] = pd.to_datetime(df['Zeitpunkt'], format='%Y-%m-%d %H:%M:%S.%f')
df['Datum'] = pd.to_datetime(df['Zeitpunkt'], format='%Y-%m-%d')

############################# Summe nach Datum (Tag) ###############################
# Summe pro Tag bilden (gruppieren)
df_gruppiert_datum = df.groupby(pd.Grouper(key='Datum',freq='5D')).agg(summe=('Datum', 'count'))

# Diagramm erstellen
gas_nach_datum = df_gruppiert_datum.plot(kind = 'bar', xlabel = 'Datum', ylabel = 'Zählimpulse', legend = False)

# Beschriftung der x-Achse in ein schönes Format bringen
x_labels = df_gruppiert_datum.index.strftime('%d.%m.')
gas_nach_datum.set_xticklabels(x_labels)

# Ergebnis als Bild speichern
plt.savefig('web/img/diagramm_gas_pro_tag.png')

############################# Summe nach Tageszeit ###############################
# Summe pro Tag bilden (gruppieren)

df_gruppiert_tageszeit = df.groupby(df['Zeitpunkt'].dt.hour).count()
# unnötige Spalten löschen
df_gruppiert_tageszeit = df_gruppiert_tageszeit.drop(columns=['Datum'])

print(df_gruppiert_tageszeit.to_string())
print(df_gruppiert_tageszeit.dtypes)

# Diagramm erstellen
gas_nach_tageszeit = df_gruppiert_tageszeit.plot(kind = 'bar', xlabel = 'Stunde', ylabel = 'Zählimpulse', legend = False)

# Ergebnis als Bild speichern
plt.savefig('web/img/diagramm_gas_pro_stunde.png')

############################# Dateien hochladen ###############################
session = ftplib.FTP(zaehlerconfig.ftp_adress, zaehlerconfig.ftp_username, zaehlerconfig.ftp_password)
file = open('web/img/diagramm_gas_pro_tag.png','rb')                  
session.storbinary('STOR img/diagramm_gas_pro_tag.png', file)   
file.close()
file = open('web/img/diagramm_gas_pro_stunde.png','rb')                  
session.storbinary('STOR img/diagramm_gas_pro_stunde.png', file)   
file.close()                                  
session.quit()