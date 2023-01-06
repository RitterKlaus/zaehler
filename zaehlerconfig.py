# Bitte tragen Sie hier Ihre Daten ein!
ftp_username = 'username'
ftp_password = 'passwort'
ftp_adress = 'example.com'

# Konfiguration zum Gas-Tarif
gas_anbieter = 'Energieversorgung Musterstadt GmbH'
gas_cent_pro_kwh = 4.8655 # Stand: Juni 2022
gas_faktor = 10.757  # "Faktor" kWh pro m³ aus der letzten Gasrechnung, auch "Zustandszahl mal Abrechnungsbrennwert"
# Beispiel:
# Zählerstand alt =   4.340,735 m³
# Zählerstand neu =   6.262,757 m³
# Differenz       =   1.922,022 m³
# Differenz * Faktor ergibt
# Verbrauch       = 20.675,191 kWh
gas_zaehler_impuls_m3 = 0.01
