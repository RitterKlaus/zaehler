#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Impulszähler
   Autor: Klaus Ritter, Lizenz: MIT
   für Taster zwischen GPIO 24 und 3,3 Volt (PIN 17 und 18)
   loggt auf die Konsole und in eine CSV-Datei
   geeignet z.B. zum Zählen von Impulsen eines Gas- oder Stromzählers
   verwendet Ideen von https://www.kampis-elektroecke.de/raspberry-pi/raspberry-pi-gpio/interrupts/
"""

import RPi.GPIO as GPIO
from datetime import datetime
import time

# Konfiguration
logdateiname = "zaehler.csv"
logaufconsole = True

# Globale Variable Counter definieren
counter = 0

# SoC als Pinreferenz waehlen
GPIO.setmode(GPIO.BCM)

# Pin 24 vom SoC als Input deklarieren und Pull-Down Widerstand aktivieren
GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

def loggen(counter):
    global logdateiname, logaufconsole

    f = open(logdateiname, "a")

    zeitpunkt = datetime.now()
    current_time = zeitpunkt.strftime("%Y-%m-%d %H:%M:%S.%f")
    f.write("impulse;" + str(counter) + ";timestamp;" + current_time +"\n")
    f.close()

    if (logaufconsole):
        print ("impuls: " + str(counter) + " timestamp: " + current_time)

# ISR
def Interrupt(Channel):
    # Zugriff auf globale Variablen
    global counter

    # Counter um eins erhoehen und loggen
    counter = counter + 1
    loggen(counter)


# Interrupt Event hinzufuegen. Pin 24, auf steigende Flanke reagieren und ISR "Interrupt" deklarieren
GPIO.add_event_detect(24, GPIO.RISING, callback = Interrupt, bouncetime = 200)

# Endlosschleife
print("Raspberry wartet auf Impulse.")
loggen(1)
try:
    while True:
	    time.sleep(1)
except KeyboardInterrupt:
    pass
