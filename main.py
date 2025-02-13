import sounddevice
# j'ai recherché un module qui permettait d'écouter en continu, j'ai trouvé celui là, si vous connaissez mieux dites le moi
import numpy 
import time

limit = 3
# Seuil de détection !!! Varie très fortement en fonction des micros, il faudra passer du temps à essayer de trouver la bonne valeur
delay = 0.05
# Delai utilisé pour séquencer le son
frequence = 44100
# "Combien de fois par seconde on prend une nouvelle mesure"

compteur = 0

def sound(indata, frames, times, status):    
    global compteur
    sound_level = numpy.linalg.norm(indata)
    # "indata" : tableau numpy contenant les echantillons audios captés par le micro
    # chaque valeur représente une intensité sonore
    # tableau de forme (frames, channels), où frames est le nombre d’échantillons et 
    # channels est le nombre de canaux (1 pour mono, 2 pour stéréo...).
    if sound_level > limit :
        compteur +=1
        print(f"Un tir a été détecté : {compteur} tirs")
        time.sleep(0.2)
        
with sounddevice.InputStream(callback=sound, samplerate=frequence, channels=1):
    # "with sounddevice" permet d'ouvrir son micro et de capturer jusqu'à ce que l'onn sorte du with
    # callback appele la fonction sound() que j'ai crée plut^t et qui permet de capturer le son, de le transformer et de l'analyser
    # sampelrate= permet de définir la fréquence de capture
    # channel= permet de sélectionner un mode mono ou stéréo
    
    print("Ecoute en cours...")
    while True:
        # Boucle infinie (à arreter avec ctrl-c)
        continue
