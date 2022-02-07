# Gymnasiearbete 2021 - Övervakningskamera med image recognition
## Skapare: Elias Hollstrand & Vincent Nildén, Åva Gymnasium, TE19D
Gymnasiearbete om image recognition med en övervakningskamera konstruerad m.h.a. Raspberry Pi samt komponenter. 

**Funktion:** Den konstuerade övervakningskameran detekterar rörelse och tar bild som sedan analyseras utifrån en Siamese neural network modell vars uppgift är att verifiera vare sig bilden innehåller ansiktet av en verifierad användare eller inte. Bilden skickas till en app som visar de senast detekterade bilderna samt vad som detekterats i dem. 

## Filer
**capture.py** - Kod som körs på Raspberry Pi som lyssnar på förhöjd spänning från PIR sensorn och signalerar till webcam att spara en snapshot. Bilden skickas sedan till en Google Drive folder.

**fetch_image.py** - Gör anrop med Google Drive API och hämtar nya bilder från mappen dit Raspberry Pi:n laddar upp till. Anropar sedan funktionen detect() från *detect.py*.

**detect.py** - Tillämpar den tränade modellen på en angiven bild och återger namnet på den verifierade användaren utifall att bilden innehåller dess ansikte, annars "Unknown".

**app.py** - Kör en Flask app på localhost som visar de senast detekterade bilderna samt vad som detekterats i dem. Strukturen på HTML-sidan är sådan som anges utav *index.html* i mappen *templates*. 

**preprocess.py & layers.py** - Nödvändiga funktioner
