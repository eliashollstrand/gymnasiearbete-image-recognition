# Gymnasiearbete 2021 - Övervakningskamera med image recognition
Gymnasiearbete om image recognition med en övervakningskamera konstruerad m.h.a. Raspberry Pi samt komponenter. 

*Skapare: Elias Hollstrand & Vincent Nildén, Åva Gymnasium, TE19D*

## Filer
**capture.py** - Kod som körs på Raspberry Pi som lyssnar på förhöjd spänning från PIR sensorn och signalerar till webcam att spara en snapshot. Bilden skickas sedan till en Google Drive folder där bilden analyseras av ett Python script. 

**face_classifier.py** - Hämtar en förtränad model (ResNet50) och tränar om den på nya klasser som vi vill att kameran ska kunna identifiera (Ansikten). 

**detection.py** - Tillämpar den tränade modellen på en angiven bild och återger namn på den klass som identifierats i bilden, om någon funnits dvs. 

**test_all_images_per_class.py** - Samma funktion som detection.py men testar istället den tränade modellen på *alla* bilder i test-dataseten.

**check_for_new_files.py** - Kontrollerar om det läggs till några nya filer i Google Drive foldern och anropar isåfall funktionen "detect" i detection.py med den aktuella bilden som parameter.
