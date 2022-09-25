Quellen
https://gitlab.server-kampert.de/Kampi/Raspberry-Pi/-/blob/master/Software/GPIO/Interrupt.py



Hardware:
https://www.elektronik-kompendium.de/sites/raspberry-pi/1907101.htm

Raspberry Pi 3 B
PIN 17 (+3,3 V)
PIN 18 (GPIO 24)


Deployment:

Secure copy (http://www.hypexr.org/linux_scp_help.php)

scp interrupt.py pi@192.168.178.52:/home/pi/dev/


# Abläufe
1. Pi protokolliert jede Zählerumdrehung durch den Magnetkontakt mit sekundengenauem Zeitstempel.
1. Jede Nacht werden aus den gesammelten Daten zwei Statistiken erzeugt: Gasverbrauch pro Tag und Gasverbrauch pro Stunde des Tages.
1. Diese Bilder und ein Nackup der gezippten Protokolldatei werden auf die Website hochgeladen.
1. Die Inhalte der Website liegen im Ordner web/


# Installation

* Verzeichnis web/ auf geeigneter Website hochladen
* interrupt.py und create_report_py auf dem Raspberry kopieren
* interrupt.py 'headless' starten
* Konfigdaten (u.a. FTP-Passwort) in create_report.py eintragen
* cron-Job für Start von create_report.py einrichten

