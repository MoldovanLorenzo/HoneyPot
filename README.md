Acesta este un honeypot scris in Python, care simuleaza un server SSH si salveaza date despre incercarile de conectare.
Are si o interfata grafica facuta cu tkinter, unde poti vedea loguri in timp real si statistici despre conexiuni.

Ce face aplicatia:
-Porneste un server pe portul 2222 care accepta conexiuni SSH
-Nu permite autentificarea, dar salveaza userul si parola
-Pastreaza logurile si le afiseaza intr-un chenar in interfata
-Salveaza toate datele(nume, parola, ip, data si ora) intr-un fisier CSV

<img width="1165" alt="Screenshot 2025-04-09 at 18 50 49" src="https://github.com/user-attachments/assets/4664363f-9cbe-45c5-a5da-f574e2fb484c" />

Ofera o pagia diferita cu statistici:
-Numar total conexiuni
-Ip-uri unice
-Parole folosite frecvent

<img width="694" alt="Screenshot 2025-04-09 at 18 50 21" src="https://github.com/user-attachments/assets/fe497bd8-155b-4e8d-a127-95febb1cfd60" />

Librari folosite:
-PARAMIKO pentru simularea serverului SSH
-SOCKET si THREADING pentru conexiunile multiple
-TKINTER pentru interfata grafica
-CSV si DATETIME pentru salvarea datelor

Cum se foloseste:
-Asigura-te ca ai fisierul "key".
-Rulează scriptul Python.
-Din interfata, apasa pe "porneste server".

-Vezi logurile live sau apasa pe "vezi statistici" pentru raportul în timp real.
<img width="1288" alt="Screenshot 2025-04-09 at 18 46 22" src="https://github.com/user-attachments/assets/8a8f2af7-6adf-4af7-9327-bc8002f7fde7" />


