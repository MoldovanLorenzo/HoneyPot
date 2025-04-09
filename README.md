Acesta este un mic honeypot scris in Python, care simuleaza un server SSH si salveaza date despre incercarile de conectare.
Are si o interfata grafica facuta cu tkinter, unde poti vedea loguri in timp real si statistici despre conexiuni.

Ce face aplicatia:
-Porneste un server pe portul 2222 care accepta conexiuni SSH
-Nu permite autentificarea, dar salveaza userul si parola
-Pastreaza logurile si le afiseaza intr-un chenar in interfata
-Salveaza toate datele(nume, parola, ip, data si ora) intr-un fisier CSV

Ofera o pagia diferita cu statistici:
-Numar total conexiuni
-Ip-uri unice
-Parole folosite frecvent

Librari folosite:
-PARAMIKO pentru simularea serverului SSH
-SOCKET si THREADING pentru conexiunile multiple
-TKINTER pentru interfata grafica
-CSV si DATETIME pentru salvarea datelor

Cum se foloseste:
-Asigura-te ca ai fisierul "key".
-Rulează scriptul Python.
-Din interfata, apasa pe "porneste server".
-Vezi logurile live sau apasa pe `vezi statistici" pentru raportul în timp real.
