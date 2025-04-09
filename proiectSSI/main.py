import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import socket
import paramiko
import threading
import os
import csv
from datetime import datetime


loguri = []
serverPornit = False
socketServer = None
conexiuniTotal = 0
paroleFolosite = {}
ipUnice = set()

def CreareCsv():
    if not os.path.exists("utilizatori.csv"):
        with open("utilizatori.csv", "w",newline="") as f:
            iesireCsv = csv.writer(f)
            iesireCsv.writerow(["timp","ip","nume","parola"])
class serverSSH(paramiko.ServerInterface):
    def __init__(self, adresaIp):
        self.adresaIp = adresaIp

    def check_auth_password(self, nume: str, parola: str) -> int:
        global conexiuniTotal, paroleFolosite
        mesaj = f"incercare autentificare: {nume} cu parola: {parola}"
        print(mesaj)
        loguri.append(mesaj)
        conexiuniTotal += 1
        paroleFolosite[parola] = paroleFolosite.get(parola, 0) + 1
        actualizareInterfata()
        with open("utilizatori.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.adresaIp, nume, parola])
        return paramiko.AUTH_FAILED

def conectiune(socketClient, adresaClient):
    transport = paramiko.Transport(socketClient)
    with open('key', 'r') as key_file:
        cheieServer = paramiko.RSAKey.from_private_key(key_file)
    transport.add_server_key(cheieServer)
    ssh = serverSSH(adresaClient[0])
    try:
        transport.start_server(server=ssh)
    except Exception as e:
        mesaj = f"eroare: {adresaClient}: {e}"
        print(mesaj)
        loguri.append(mesaj)
        actualizareInterfata()



def pornesteServer():
    global serverPornit, socketServer
    socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socketServer.bind(('', 2222))
    socketServer.listen(100)
    serverPornit = True
    loguri.append("server pornit")
    actualizareInterfata()

    while serverPornit:
        try:
            socketServer.settimeout(1.0)
            socketClient, adresaClient = socketServer.accept()
            ipUnice.add(adresaClient[0])
            mesaj = f"conectiune de la {adresaClient[0]}:{adresaClient[1]}"
            print(mesaj)
            loguri.append(mesaj)
            actualizareInterfata()
            t = threading.Thread(target=conectiune, args=(socketClient, adresaClient))
            t.start()
        except socket.timeout:
            continue
        except Exception as e:
            loguri.append(f"eroare: {e}")
            actualizareInterfata()
            break

def opresteServer():
    global serverPornit, socketServer
    serverPornit = False
    if socketServer:
        try:
            socketServer.close()
            loguri.append("server oprit")
        except Exception as e:
            loguri.append(f"eroare: {e}")
    actualizareInterfata()

def actualizareInterfata():
    textLog.configure(state='normal')
    textLog.delete(1.0, tk.END)
    for linie in loguri[-100:]:
        textLog.insert(tk.END, linie + "\n")
    textLog.see(tk.END)
    textLog.configure(state='disabled')

def actualizeazaStatistici():
    labelTotal.config(text=f"total conexiuni: {conexiuniTotal}")
    labelIp.config(text=f"ip uri unice: {len(ipUnice)}")
    topParole = sorted(paroleFolosite.items(), key=lambda x: x[1], reverse=True)[:5]
    textParole = "\n".join([f"{p:<15}  {c} ori" for p, c in topParole]) or "inca nicio parola."
    labelListaParole.config(text=textParole)
    root.after(2000, actualizeazaStatistici)

def schimbaPagina(pagina):
    pagina.tkraise()

root = tk.Tk()
root.title("honeypot")
root.geometry("700x600")

notebook = tk.Frame(root)
notebook.pack()
paginaLoguri = tk.Frame(notebook)
paginaStatistici = tk.Frame(notebook)

for pagina in (paginaLoguri, paginaStatistici):
    pagina.grid(row=0, column=0, sticky='nsew')

titluLoguri = tk.Label(paginaLoguri, text="Loguri server", font=("Helvetica", 16, "bold"))
titluLoguri.pack(pady=(10, 0))
textLog = ScrolledText(paginaLoguri, width=80, height=30, state='disabled')
textLog.pack(padx=10, pady=10)
frameButoane = tk.Frame(paginaLoguri)
frameButoane.pack(pady=5)
butonStart = tk.Button(frameButoane, text="porneste server", command=lambda: threading.Thread(target=pornesteServer, daemon=True).start())
butonStart.pack(side=tk.LEFT, padx=5)
butonStop = tk.Button(frameButoane, text="opreste server", command=opresteServer)
butonStop.pack(side=tk.LEFT, padx=5)
butonStatistici = tk.Button(frameButoane, text="vezi statistici", command=lambda: schimbaPagina(paginaStatistici))
butonStatistici.pack(side=tk.LEFT, padx=5)
paginaStatistici.grid_columnconfigure(0, weight=1)
paginaStatistici.grid_rowconfigure(1, weight=1)
titluStatistici = tk.Label(paginaStatistici, text="Statistici", font=("Helvetica", 20, "bold"))
titluStatistici.grid(row=0, column=0, pady=(10, 0), sticky="n")
frameStatistici = tk.Frame(paginaStatistici)
frameStatistici.grid(row=1, column=0, padx=20, pady=20, sticky="n")
labelTotal = tk.Label(frameStatistici, text="total conexiuni: 0", font=('Arial', 15, 'bold'), anchor="w")
labelTotal.grid(row=0, column=0, sticky="w", pady=5)
labelIp = tk.Label(frameStatistici, text="ip unice: 0", font=('Arial', 15, 'bold'), anchor="w")
labelIp.grid(row=1, column=0, sticky="w", pady=5)
labelParole = tk.Label(frameStatistici, text="parole frecvente:", font=('Arial', 15, 'bold'), anchor="w", justify="left")
labelParole.grid(row=2, column=0, sticky="w", pady=5)
labelListaParole = tk.Label(frameStatistici, text="", font=('Arial', 15), justify="left", anchor="w")
labelListaParole.grid(row=3, column=0, sticky="w", pady=5)

schimbaPagina(paginaLoguri)
actualizeazaStatistici()
root.mainloop()
