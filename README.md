# Gymnasiearbete 2021 - Övervakningskamera med image recognition
Gymnasiearbete om image recognition med en övervakningskamera konstruerad m.h.a. Raspberry Pi samt komponenter. 

*Skapare: Elias Hollstrand & Vincent Nildén, Åva Gymnasium, TE19D*

## Filer
**capture.py** - Kod som körs på Raspberry Pi som lyssnar på förhöjd spänning från PIR sensorn och signalerar till webcam att spara en snapshot. Bilden skickas sedan till en mapp på en FTP-server där bilden analyseras av ett Python script.

**modeltraining.py** - Hämtar en förtränad model och tränar om den på nya klasser som vi vill att kameran ska kunna identifiera. 

**detection.py** - Tillämpar den tränade modellen på en angiven bild och återger namn på den klass som identifierats i bilden, om någon funnits dvs.

**labels.txt** - Lista med alla de klasser som modellen är tränad på.
