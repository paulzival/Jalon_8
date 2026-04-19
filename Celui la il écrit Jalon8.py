# Importer la bibliothèque
import sensor, time, pyb , math
from pyb import Pin, SPI
# Prérequis pour les moteur
tim12 = pyb.Timer(2, freq=100)
tim2X = pyb.Timer(4, freq=100)

p4 = pyb.Pin('P4', pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
p5 = pyb.Pin('P5', pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
p7 = pyb.Pin('P7', pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
p8 = pyb.Pin('P8', pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
M11 = tim12.channel(3, pyb.Timer.PWM, pin=p5)
M12 = tim12.channel(4, pyb.Timer.PWM, pin=p4)
M2X = tim2X.channel(1, pyb.Timer.PWM, pin=p7)
tim12.freq(100)
tim2X.freq(100)
#Prérequis communication SPI
cs = Pin("P3", Pin.OUT_PP, Pin.PULL_NONE)
spi = SPI(2, SPI.MASTER, polarity=1, phase=1, bits=8)
CTRL_REG1 = 0x20
CTRL_REG2 = 0x21
CTRL_REG3 = 0x22
CTRL_REG4 = 0x23
CTRL_REG5 = 0X24

OUT_X_L   = 0x28
OUT_X_H   = 0x29
OUT_Y_L   = 0x2A
OUT_Y_H   = 0x2B

fichier_x = open("cord_x.txt", "w")
fichier_y = open("cord_y.txt", "w")
#Fonction
def cmd_moteur(rapport_av_ar, vit_droite, vit_gauche):
    M2X.pulse_width_percent(rapport_av_ar)
    M11.pulse_width_percent(vit_droite)
    M12.pulse_width_percent(vit_gauche)
#Fonction spécifique a la communication SPI
def ecrire(adresse, valeur):
    cs.low()
    buf = bytearray([adresse, valeur])
    spi.write_readinto(buf, buf)
    cs.high()
def lire(adresse):
    cs.low()
    buf = bytearray([adresse | 0x80, 0x00])
    spi.write_readinto(buf, buf)
    cs.high()
    return buf[1]
# Fonction Initialiser
def init():
    ecrire(CTRL_REG1, 0x70)
    ecrire(CTRL_REG2, 0x00)
    ecrire(CTRL_REG3, 0x00)
    ecrire(CTRL_REG4, 0x0C)
    ecrire(CTRL_REG5, 0x40)
def lire_champ_magnetique():
    x_low = lire(OUT_X_L)
    x_high = lire(OUT_X_H)
    y_low = lire(OUT_Y_L)
    y_high = lire(OUT_Y_H)

    # Combine les octets en entiers 16 bits
    x = (x_high << 8) | x_low
    y = (y_high << 8) | y_low

    # Conversion en entiers signés
    if x >= 32768:
        x -= 65536
    if y >= 32768:
        y -= 65536
    #print("X: {}, Y: {}".format(x, y))

    # Écrit les valeurs dans le fichier
#    with open("CoordonneesXY.txt", "a") as fichier:
#        fichier.write("X: {}, Y: {}\n".format(x, y))
#        fichier.flush()  # Force l'écriture immédiate

  # Retourne les valeurs pour une utilisation ultérieure

    x +=3536
    y -=5141
    angle = math.atan2(y,x) * 180 / math.pi
    print (angle)


init()
i=0
while True :
    lire_champ_magnetique()
    i = i+1
    time.sleep_ms(500)  # Pause de 50 ms



