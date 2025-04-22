from tkinter import *
from tkinter import messagebox
import datetime as dt
from timeit import *
import numpy as np
import time
import sounddevice
import threading
import csv
import os
import pandas as pd
from tkinter import ttk


# initialisation de variables globales
frame = None
label_timer = None
sound_stream = None
name = ""

def csv_header():
    filename = "sessions_police.csv" 
    
    if not os.path.exists(filename):
        with open('sessions_police.csv', 'w', newline='') as fichier:
            tab=['Nom', 'Tirs', "Début_session", "Durée"]
            writer=csv.writer(fichier)
            writer.writerow(tab)

def export_sessions(tab):
    
    with open('sessions_police.csv', 'a', newline='') as fichier:
        writer=csv.writer(fichier)
        writer.writerow(tab)
       
def update_time():
    now = dt.datetime.now()
    time = now.strftime("%A %y %B / %H : %M")
    # On envoie la valeur du temps pour le réctualiser
    label_time.config(text=time)
    # Ici on va rafraichir le texte toutes les secondes
    window.after(1000, update_time)
        
def main_screen():
    global frame, entry, name, str_time, compteur
    # On commence par détruire la frame actuelle pour pouvoir afficher de nouvelles choses
    if frame:
        frame.destroy()
    
    # On recrée la frame pour afficher 
    frame = Frame(window, bg=font)
    
    
    label_title = Label(frame, text="Bienvenue sur l'application", font=("Arial", 28), bg=font, fg="white")
    label_title.pack()
    
    label_subtitle = Label(frame, text="Entrez votre nom", font=("Arial", 22), bg=font, fg="white")
    label_subtitle.pack(pady=20)
    
    entry = Entry(frame, font=("Arial, 20"), bg="white", fg=font)
    entry.pack(pady=25, fill=X)
    
    # Pour pouvoir entrer avec enter
    entry.bind("<Return>", lambda event: session())
        
    button = Button(frame, text="Démarrer la session", font=("Arial, 25"), bg="white", fg=font, command=session)
    button.pack(pady=15, fill=X)
    
    button_historique = Button(frame, text="Historique des sessions", font=("Arial", 15), bg="white", fg=font, command=show_history)
    button_historique.pack(pady=15, fill=X)
    
    # On vérifie s'il y a une session qui a eu lieu avant de revenir à l'écran principal
    if str_time != 0 :
        last_session = Label(frame, text=f"Dernière session : {name} \nDurée : {str_time} \nNombre de tirs : {compteur}", font=("Arial", 15), bg=font, fg="white")
        last_session.pack(pady=20)
        compteur = 0
        
    
    frame.pack(expand=YES)
    
    
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def show_history():
    global frame

    if frame:
        frame.destroy()

    frame = Frame(window, bg=font)
    frame.pack(expand=YES, fill=BOTH)

    label_title = Label(frame, text="Historique des sessions", font=("Arial", 25), bg=font, fg="white")
    label_title.pack(pady=10)

    filename = "sessions_police.csv"
    if not os.path.exists(filename):
        Label(frame, text="Aucune session enregistrée.", font=("Arial", 18), bg=font, fg="white").pack(pady=20)
        return

    df = pd.read_csv(filename)

    if df.empty:
        Label(frame, text="Aucune session enregistrée.", font=("Arial", 18), bg=font, fg="white").pack(pady=20)
        return

    # Ajouter une colonne de numérotation
    df.index = range(1, len(df) + 1)
    df.index.name = "Ligne"
    # Affichage du tableau (14 dernières sessions)
    try:
        # Sauvegarder les dates originales pour affichage
        df["Date_affichage"] = df["Début_session"]

        # Conversion des dates pour tri
        df["Début_session"] = pd.to_datetime(df["Début_session"], errors="coerce", format="%A %d %B / %H : %M")
        df = df.dropna(subset=["Début_session"])

        # Tri décroissant pour avoir les plus récentes en premier
        df_sorted = df.sort_values("Début_session", ascending=False).copy()

        # Garder les 14 dernières
        df_recent = df_sorted.head(14).copy()

        # Remettre la date sous forme de chaîne d'origine pour l'affichage
        df_recent["Début_session"] = df_recent["Date_affichage"]

        # Réindexation propre
        df_recent = df_recent.drop(columns=["Date_affichage"])
        df_recent.index = range(1, len(df_recent) + 1)
        df_recent.index.name = "Ligne"

        # Colonnes à afficher
        cols = ["Ligne", "Nom", "Tirs", "Début_session", "Durée"]
        tree = ttk.Treeview(frame, columns=cols, show="headings")
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, anchor=CENTER)

        for i, row in df_recent.iterrows():
            tree.insert("", "end", values=(i, *row.tolist()))

        tree.pack(pady=20, expand=YES, fill=BOTH)

    except Exception as e:
        Label(frame, text=f"Erreur lors de l'affichage du tableau : {e}", font=("Arial", 12), bg=font, fg="red").pack(pady=10)
        return



    try:
        df["Tirs"] = pd.to_numeric(df["Tirs"], errors="coerce").fillna(0).astype(int)
        df["Début_session"] = pd.to_datetime(df["Début_session"], errors="coerce", format="%A %d %B / %H : %M")

        # Trier, filtrer
        df = df.dropna(subset=["Début_session"])
        df = df[df["Tirs"] > 0].sort_values("Début_session")

        # Création d'une zone bas de page
        bottom_frame = Frame(frame, bg=font)
        bottom_frame.pack(fill=X, padx=20, pady=(0, 20))

        if df.empty:
            Label(bottom_frame, text="Aucune donnée de tir > 0 pour afficher un graphique.",
                  font=("Arial", 10), bg=font, fg="white").grid(row=0, column=0, columnspan=3)
        else:
            df["Tirs_cumulés"] = df["Tirs"].cumsum()
            df["Date_affichée"] = df["Début_session"].dt.strftime("%d/%m")

            fig, ax = plt.subplots(figsize=(6, 2.5))
            fig.tight_layout(pad=2.0)

            ax.plot(df["Date_affichée"], df["Tirs_cumulés"], marker='o', linestyle='-', color='blue')
            ax.set_title("Tirs cumulés en fonction du temps")
            ax.set_xlabel("Date")
            ax.set_ylabel("Tirs cumulés")
            ax.set_ylim(bottom=0)
            ax.set_xticks(df["Date_affichée"])
            ax.set_xticklabels(df["Date_affichée"], rotation=45)
            ax.grid(True)

            # Lignes horizontales d'usure
            ax.axhline(y=60, color='red', linestyle='--', linewidth=1.5, label='Usure 100 %')
            ax.axhline(y=54, color='orange', linestyle='--', linewidth=1.5, label='Usure 90 %')
            ax.axhline(y=48, color='yellow', linestyle='--', linewidth=1.5, label='Usure 80 %')



            ax.legend(loc='upper left')

            # Texte dates début / fin
            date_min = df["Date_affichée"].iloc[0]
            date_max = df["Date_affichée"].iloc[-1]
            ax.text(0.01, 0.95, f"Début : {date_min}", transform=ax.transAxes, fontsize=9, verticalalignment='top')
            ax.text(0.99, 0.95, f"Fin : {date_max}", transform=ax.transAxes, fontsize=9,
                    verticalalignment='top', horizontalalignment='right')

            # Affichage du graphique
            canvas = FigureCanvasTkAgg(fig, master=bottom_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=0, padx=10)

            # === Cadre d'alerte à droite ===
            alert_frame = Frame(bottom_frame, bg='white', bd=2, relief="solid")
            alert_frame.grid(row=0, column=1, padx=(20, 10), sticky="ns")

            # Calcul du pourcentage d'usure/ !! Valeur d'usure de 100% fixée à 60 !!
            usure_totale = 60
            
            usure_max = df["Tirs_cumulés"].max()
            usure_percent = (usure_max / usure_totale) * 100
            usure_text = f"Usure : {usure_percent:.1f}%"

            # Affichage du pourcentage avec couleur
            if usure_percent >= 100:
                couleur = 'red'
            elif usure_percent >= 80:
                couleur = 'orange'
            else:
                couleur = None  # pas d'affichage

            if couleur:
                Label(alert_frame, text=usure_text, font=("Arial", 12, "bold"), fg=couleur, bg='white').pack(padx=10, pady=(10, 5))

            if usure_percent > 90:
                Label(alert_frame, text="Plaques à changer", font=("Arial", 11, "bold"), fg='red', bg='white').pack(padx=10, pady=(5, 10))

            # Bouton accueil placé en colonne 2
            Button(bottom_frame, text="Accueil", font=("Arial", 15), bg="white", fg=font,
                   command=main_screen).grid(row=0, column=2, sticky='se', padx=10)

    except Exception as e:
        Label(frame, text=f"Erreur graphique : {e}", font=("Arial", 12), bg=font, fg="red").pack()



   # Button(frame, text="Accueil", font=("Arial", 15), bg="white", fg=font, command=main_screen).pack(pady=20)





def session():
    global frame, label_timer, start, timer_running, name, label_compteur, time_start_format
    
    #on récupère la valeur (le nom) contenur dans le "entry"
    name = entry.get()

    # Supprimer tout message d'erreur existant
    for widget in frame.winfo_children():
        if isinstance(widget, Label) and widget.cget("fg") == "red":
            widget.destroy()
    
    if not name.strip():
        error_label = Label(frame, text="Il faut entrer un nom d'utilisateur pour ouvrir une session", 
                    font=("Arial", 15, "bold"), fg="red", bg=font)

        error_label.pack(pady=10)
        return
    

    # On détruit la frame pour réinitialiser la page
    frame.destroy()
    frame = Frame(window, bg=font)

    label_title = Label(frame, text=f"Session de {name} en cours", font=("Arial", 25), bg=font, fg="white")
    label_title.grid(sticky="n")

    label_compteur = Label(frame, text="Nombre de tirs : 0", font=("Arial", 20), bg=font, fg="white")
    label_compteur.grid(pady=25)
    
    # Ajout du timer
    label_timer = Label(frame, text="0:00:00", font=("Arial", 20), bg=font, fg="white")
    label_timer.grid(pady=20)
    
    # Boutton pour arrêter la session
    button = Button(frame, text="Terminer la session", font=("Arial, 15"), bg="white", fg=font, command=stats)
    button.grid(pady=20)

    # On démarre le timer correctement
    start = default_timer()  # Réinitialise le début du timer
    timer_running = True
    # On run le timer pour le réactualiser toutes les secondes
    timer()
    
    time_start = dt.datetime.now()
    time_start_format = time_start.strftime("%A %y %B / %H : %M")
    tirs_thread = threading.Thread(target=start_sound_detection, daemon=True)
    tirs_thread.start()
    frame.pack(expand=YES)

def timer(): 
    global label_timer, timer_running, str_time
    
    # On ajoute cette condition pour éviter d'essayer d'actualiser le timer s'il ne tourne pas
    if not timer_running:
        return
    
    now = default_timer()-start
    #On definit les modules
    minutes, seconds = divmod(now, 60)
    hours, minutes = divmod(minutes, 60)
    str_time = "%d:%02d:%02d" % (hours, minutes, seconds)
    if label_timer.winfo_exists :
        label_timer.config(text=str_time, font=("Arial", 30, "bold"), bg="#222", fg="cyan", relief="solid", bd=2)
        # Ici on va rafraichir le texte toutes les secondes
        window.after(1000, timer)
    
def stats():
    global frame,timer_running, str_time, compteur, name, time_start_format
    
    stop_sound_detection()
    
    timer_running = False

    frame.destroy()
    
    # On recrée la frame pour afficher 
    frame = Frame(window, bg=font)
    frame.pack(expand=YES)
    csv_header()
    datas = [name, compteur, time_start_format, str_time]
    export_sessions(datas)
    
    label_save = Label(frame, text="Vos données ont bien été sauvegardées !", font=("Arial", 28), bg=font, fg="white")
    label_save.pack()
    
    label_stats = Label(frame, text="Voici les statistiques de votre session : ", font=("Arial", 24), bg=font, fg="white")
    label_stats.pack(pady=25)
    
    stats_affichage = Label(frame, text=f"Durée : {str_time} \n\nNombre de tirs : {compteur}", font=("Arial", 22), bg=font, fg="white")
    stats_affichage.pack(pady=12)
    
    # Bouton pour passer à l'écran d'après
    button_suivant = Button(frame, text="Suivant", font=("Arial", 20), bg="white", fg=font, command=main_screen)
    button_suivant.pack(pady=20)

    # On attend 7.5 secondes et on lance la page d'accueil
    window.after(30000, main_screen)
    
def sound(indata, frames, times, status):
    global label_compteur, compteur
    # indata, données fournies par le module : signal audio sous forme de nombre
    # frames, times, status sont aussi des données fournies par le module "sounddevice"
    # frames : nombre d'échantillions audio reçus
    # times : informations sur le timing des echantillions
    # status : informe sur la présence d'erreurs     

    sound_level = np.linalg.norm(indata)
    # calcul de la norme : intensité sonore 
    if sound_level > limit :
        compteur +=1
        if label_compteur.winfo_exists():
            window.after(0, label_compteur.config(text=f"Nombre de tirs : {compteur}"))
        time.sleep(0.2)

# Ancienne version de le fonction
# def start_sound_detection():
#     global sound_stream
#     sound_stream = sounddevice.InputStream(callback=sound, samplerate=frequence, channels=1)
#     sound_stream.start()

def start_sound_detection():
    global sound_stream
    try:
        sound_stream = sounddevice.InputStream(callback=sound, samplerate=frequence, channels=1)
        sound_stream.start()
        print("Détection sonore activée.")  # Debugging
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d'initialiser la détection sonore.\nVérifiez que votre microphone fonctionne.\nDétail : {e}")
        sound_stream = None  # On s'assure qu'aucune référence invalide ne persiste

# Ancienne version de le fonction
# def stop_sound_detection():
#     global sound_stream
#     if "sound_stream" in globals() and sound_stream is not None:
#         sound_stream.stop()
#         sound_stream.close()

def stop_sound_detection():
    global sound_stream
    if sound_stream is not None:
        try:
            sound_stream.stop()
            sound_stream.close()
            print("Détection sonore arrêtée.")  # Debugging
        except Exception as e:
            print(f"Erreur lors de l'arrêt du stream : {e}")

        
def on_closing():
    if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter l'application ?"):
        stop_sound_detection()
        window.destroy()

    
font = "#30384a"
# Application principale
window = Tk()
window.protocol("WM_DELETE_WINDOW", on_closing)

window.title("Compteur de tir")
# taille fenêtre
# window.geometry("1024x600")
window.state("zoomed")


window.minsize(1024, 600)
window.config(background=font)

# Ici on initialise des variables que l'on va utiliser plus tard pour éviter des problèmes en exécutant les fonctions
timer_running = False
str_time = 0
frame = None

# Variables pour le son
limit = 13
# Seuil de détection !!! Varie très fortement en fonction des micros, il faudra passer du temps à essayer de trouver la bonne valeur
delay = 0.05
# Delay utilisé pour séquencer le son
frequence = 48000
# "Combien de fois par seconde on prend une nouvelle mesure"
compteur = 0

# Ici on va charger l'image qui va rester en haut de la fenêtre 
# (on la place dans window afin qu'elle ne soit pas détruite lorsque l'on détruira la frame dans les fonctions)
window.image_pol = PhotoImage(file="polcie.png").subsample(6)
canvas_im_pol = Canvas(window, width=150, height=150, bg=font, bd=0, highlightthickness=0)
canvas_im_pol.create_image(75, 75, image=window.image_pol)
canvas_im_pol.image = window.image_pol
canvas_im_pol.place(relx=0, rely=0, anchor="nw")
# affichage de l'heure
label_time = Label(window, font=("Arial", 12), bg=font, fg="#d4d6de")
label_time.place(relx=0.999, rely=0.001, anchor="ne")

update_time()

main_screen()

window.mainloop()



# Menu supplémentaire pour consulter les données 
