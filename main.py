import sounddevice
# j'ai recherché un module qui permettait d'écouter en continu, j'ai trouvé celui là, si vous connaissez mieux dites le moi
import numpy 
import time

limit = 3
# Seuil de détection !!! Varie très fortement en fonction des micros, il faudra passer du temps à essayer de trouver la bonne valeur
delay = 0.05
# Delay utilisé pour séquencer le son
frequence = 44100
# "Combien de fois par seconde on prend une nouvelle mesure"

compteur = 0

def sound(indata, frames, times, status):
    # indata, données fournies par le module : signal audio sous forme de nombre
    # frames, times, status sont aussi des données fournies par le module "sounddevice"
    # frames : nombre d'échantillions audio reçus
    # times : informations sur le timing des echantillions
    # status : informe sur la présence d'erreurs     
    global compteur
    sound_level = numpy.linalg.norm(indata)
    # calcul de la norme : intensité sonore 
    
    if sound_level > limit :
        compteur +=1
        print(f"Un tir a été détecté : {compteur} tirs")
        time.sleep(0.2)
        
with sounddevice.InputStream(callback=sound, samplerate=frequence, channels=1):
    # "with sounddevice" permet d'ouvrir son micro et de capturer jusqu'à ce que l'on sorte du with
    # callback appele la fonction sound() que j'ai crée plutôt et qui permet de capturer le son, de le transformer et de l'analyser
    # samplerate= permet de définir la fréquence de capture
    # channel= permet de sélectionner un mode mono ou stéréo
    
    print("Ecoute en cours...")
    while True:
        # Boucle infinie (à arreter avec ctrl-c)
        continue
