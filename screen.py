from tkinter import *
import datetime as dt
from timeit import *

       
def update_time():
    now = dt.datetime.now()
    time = now.strftime("%A %y %B / %H : %M")
    # On envoie la valeur du temps pour le réctualiser
    label_time.config(text=time)
    # Ici on va rafraichir le texte toutes les secondes
    window.after(1000, update_time)
        
def main_screen():
    global frame, entry, timer_running, name, str_time
    
    timer_running = False
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
    
    button = Button(frame, text="Démarrer la session", font=("Arial, 25"), bg="white", fg=font, command=session)
    button.pack(pady=25, fill=X)
    
    # On vérifie s'il y a une session qui a eu lieu avant de revenir à l'écran principal
    if str_time != 0 :
        last_session = Label(frame, text=f"Dernière session : {name} \nDurée : {str_time}", font=("Arial", 15), bg=font, fg="white")
        last_session.pack(pady=20)
        
    
    frame.pack(expand=YES)

def session():
    global frame, label_timer, start, timer_running, name
    
    # On réinitialise l'affichage du timer
    label_timer = Label(frame, text="0:00:00", font=("Arial", 20), bg=font, fg="white")
    label_timer.pack()
    
    #on récupère la valeur (le nom) contenur dans le "entry"
    name = entry.get()
    
    # On détruit la frame pour réinitialiser la page
    frame.destroy()
    frame = Frame(window, bg=font)

    label_title = Label(frame, text=f"Session de {name} en cours", font=("Arial", 25), bg=font, fg="white")
    label_title.grid(pady=20)

    label_subtitle = Label(frame, text="Nombre de tirs : ", font=("Arial", 20), bg=font, fg="white")
    label_subtitle.grid(pady=20)
    
    # Ajout du timer
    label_timer = Label(frame, text="0:00:00", font=("Arial", 20), bg=font, fg="white")
    label_timer.grid(pady=20)

    # Boutton pour arrêter la session
    button = Button(frame, text="Terminer la session", font=("Arial, 15"), bg="white", fg=font, command=main_screen)
    button.grid(pady=20)
    frame.pack(expand=YES)

    frame.pack(expand=YES)

    # On démarre le timer correctement
    start = default_timer()  # Réinitialise le début du timer
    timer_running = True
    # On run le timer pour le réactualiser toutes les secondes
    timer()
    
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
        label_timer.config(text=str_time)
        # Ici on va rafraichir le texte toutes les secondes
        window.after(1000, timer)

font = "#30384a"
# Application principale
window = Tk()
window.title("Compteur de tir")
window.geometry("1024x600")
window.minsize(1024, 600)
window.config(background=font)

# Ici on initialise des variables que l'on va utiliser plus tard pour éviter des problèmes en exécutant les fonctions
timer_running = False
str_time = 0
frame = None

# Ici on va charger l'image qui va rester en haut de la fenêtre 
# (on la place dans window afin qu'elle ne soit pas détruite lorsque l'on détruira la frame dans les fonctions)
window.image_pol = PhotoImage(file="polcie.png").subsample(6)
canvas = Canvas(window, width=150, height=150, bg=font, bd=0, highlightthickness=0)
canvas.create_image(75, 75, image=window.image_pol)
canvas.image = window.image_pol
canvas.place(relx=0, rely=0, anchor="nw")
# affichage de l'heure
label_time = Label(window, font=("Arial", 12), bg=font, fg="#d4d6de")
label_time.place(relx=0.999, rely=0.001, anchor="ne")

update_time()

main_screen()

window.mainloop()
