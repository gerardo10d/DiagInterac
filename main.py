import math
import numpy as np
from funciones import tablaBloqComp, graficar

# Materiales-----------------------

# Concreto
fc = 21  # MPa
Ec = 3900 * math.sqrt(fc)  # MPa  (variar la ecuacion)
ec = fc / Ec

# Acero
dBarra = 15.9  # mm diámetro de 5/8"
ABarra = 199  # mm2 área de 5/8"
nBarrasb = 3  # número de barras en el lado b
nBarrash = 4  # número de barras en el lado h
fy = 420  # MPa
Es = 200e3  # MPa
ey = fy / Es
esu = 0.1
estribos = True  # Estribos (True) o espiral (False)
dEstribo = 9.5  # mm siempre es de 3/8" el estribo en cols

# Sección columna-------------------
b = 300  # mm
h = 700  # mm
recubrimiento = 40  # mm
dc = recubrimiento + dEstribo + dBarra / 2  # mm
dc = 5 * math.ceil(dc / 5)  # Aplica un redondeo al múltiplo de 5 superior
d = h - dc  # mm
print(f'd: {d} mm. dc: {dc} ¿Redondear?')

# Puntos de P-M para verificar en el diagrama----------
Mx = np.array([30.0, 0])
Py = np.array([822.0, 0])

# Bloque de compresión
paso = 1  # Cada cuántos milímetros se modifica el bloque de compresión
fin = h  # Se analiza el bloque hasta el valor de h
M, P, fiMn, fiPn, hztalFiX, hztalFiY = tablaBloqComp(fin, paso, nBarrash, nBarrasb, b, h, fc, Ec, fy, Es, ABarra, dc, estribos)

graficar(M, P, fiMn, fiPn, hztalFiX, hztalFiY, Mx, Py)
