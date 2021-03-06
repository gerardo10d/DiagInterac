import math
import numpy as np
from matplotlib import pyplot as plt


def tablaFibras(c, nBarrash, nBarrasb, b, h, fc, Ec, fy, Es, ABarra, dc):
    # Fibras para el concreto-------------
    eu = 0.003
    fiy = eu / c
    numFibConc = 50
    Ai = b * h / numFibConc
    yi = np.arange(1, numFibConc + 1, 1)
    # ei = np.zeros(numFibConc)
    si = np.zeros(numFibConc)

    hFibra = h / numFibConc
    yi = h / 2 - yi * hFibra + hFibra / 2
    ei = fiy * (c - (h / 2 - yi))
    for i in range(len(ei)):
        si[i] = min(max(Ec * ei[i], 0), fc)
    Aisi = Ai * si
    Aiyisi = Aisi * yi

    # Fibras para el acero---------------
    numFibAcero = nBarrash
    filasBarras = np.ones(nBarrash) * 2
    filasBarras[0], filasBarras[-1] = nBarrasb, nBarrasb
    AiAcero = filasBarras * ABarra
    yiAcero = np.zeros(nBarrash)
    yiExtremo = h / 2 - dc
    yiAcero[0], yiAcero[-1] = yiExtremo, -yiExtremo
    numVecesResta = math.ceil(nBarrash / 2) - 1
    distanciaEntreBarrasEnH = (h - 2 * dc) / (nBarrash - 1)
    for i in range(1, numVecesResta + 1):
        yiAcero[i] = yiExtremo - i * distanciaEntreBarrasEnH
        yiAcero[-1 - i] = -yiAcero[i]

    # print(yiAcero)
    # yiAcero = np.array([h / 2 - dc, 0, -(h / 2 - dc)])

    eiAcero = fiy * (c - (h / 2 - yiAcero))
    siAcero = np.zeros(numFibAcero)
    for i in range(len(eiAcero)):
        siAcero[i] = min(max(Es * eiAcero[i], -fy), fy)
    AisiAcero = AiAcero * siAcero
    AiyisiAcero = AisiAcero * yiAcero

    # print(AiyisiAcero)

    P = (sum(Aisi) + sum(AisiAcero)) / 1e3  # kN
    M = (sum(Aiyisi) + sum(AiyisiAcero)) / 1e6  # kN.m

    return P, M, abs(eiAcero[-1])


def tablaBloqComp(fin, paso, nBarrash, nBarrasb, b, h, fc, Ec, fy, Es, ABarra, dc, estribos):
    filasTabla = int(fin / paso)
    M, P, es, fi = np.zeros(filasTabla), np.zeros(filasTabla), np.zeros(filasTabla), np.zeros(filasTabla)
    i = 0
    for c in range(paso, fin + paso, paso):
        P[i], M[i], es[i] = tablaFibras(c, nBarrash, nBarrasb, b, h, fc, Ec, fy, Es, ABarra, dc)
        if estribos:  # Estribos
            if es[i] >= 5e-3:
                fi[i] = 0.9
            elif es[i] <= 2e-3:
                fi[i] = 0.65
            else:
                fi[i] = 0.65 + (es[i] - 2e-3) * 250 / 3
        else:  # Espiral
            if es[i] >= 5e-3:
                fi[i] = 0.9
            elif es[i] <= 2e-3:
                fi[i] = 0.75
            else:
                fi[i] = 0.75 + (es[i] - 2e-3) * 50
        i += 1

    fiMn = fi * M
    fiPn = fi * P
    M = np.append(M, 0)  # Agrega 0 y el ??ltimo elemento en P para completar con l??nea horizontal
    P = np.append(P, P[-1])  # ??ltimo elemento en P

    # Crear un vector de distancias entre los valores del vector fiPn y 0.75*el ??ltimo valor de fiPn
    distancias = np.abs(fiPn - 0.75 * fiPn[-1])
    # Encontrar la posici??n de la menor de esas distancias
    # Los [0][0] al final son para devolver el n??mero de la posici??n,
    # porque inicialmente es una tupla y luego es un array,
    # entonces se debe extraer dos veces.
    # La funci??n np.where devuelve una tupla
    posMinDif = np.where(min(distancias) == distancias)[0][0]
    # L??nea horizontal en 0.75 * fiPn
    hztalFiX = np.array([0., fiMn[posMinDif]])
    hztalFiY = np.array([0.75 * fiPn[-1], 0.75 * fiPn[-1]])

    return M, P, fiMn, fiPn, hztalFiX, hztalFiY


def graficar(x, y, x2, y2, x3, y3, x4, y4):
    fig, ax = plt.subplots()  # Crear la figura y los ejes
    ax.plot(x, y, color="blue", label="P - M")  # Dibujar l??nea
    ax.plot(x2, y2, color="orange", label=r"$\phi$Pn - $\phi$Mn")  # Dibujar l??nea
    ax.plot(x3, y3, color="orange")  # Dibujar l??nea horizontal complementaria
    ax.scatter(x4, y4, color="red")
    # ax.patch.set_facecolor("gray")
    # fig.patch.set_facecolor("gray")
    plt.title("Interacci??n P - M", size=20)
    plt.xlabel("M (kN.m)", size=16)
    plt.ylabel("P (kN)", size=16)
    plt.legend()
    plt.grid()
    plt.show()  # Mostrar el gr??fico


def principal(fc, dBarra, ABarra, nBarrasb, nBarrash, estribos, b, h):
    # Materiales-----------------------

    # Concreto
    # fc = 21  # MPa
    Ec = 3900 * math.sqrt(fc)  # MPa  (variar la ecuacion)
    ec = fc / Ec

    # Acero
    # dBarra = 15.9  # mm di??metro de 5/8"
    # ABarra = 199  # mm2 ??rea de 5/8"
    # nBarrasb = 3  # n??mero de barras en el lado b
    # nBarrash = 4  # n??mero de barras en el lado h
    fy = 420  # MPa
    Es = 200e3  # MPa
    ey = fy / Es
    esu = 0.1
    # estribos = True  # Estribos (True) o espiral (False)
    dEstribo = 9.5  # mm siempre es de 3/8" el estribo en cols

    # Secci??n columna-------------------
    # b = 300  # mm
    # h = 700  # mm
    recubrimiento = 40  # mm
    dc = recubrimiento + dEstribo + dBarra / 2  # mm
    dc = 5 * math.ceil(dc / 5)  # Aplica un redondeo al m??ltiplo de 5 superior
    d = h - dc  # mm
    # print(f'd: {d} mm. dc: {dc} ??Redondear?')

    # Puntos de P-M para verificar en el diagrama----------
    Mx = np.array([30.0, 0])
    Py = np.array([822.0, 0])

    # Bloque de compresi??n
    paso = 1  # Cada cu??ntos mil??metros se modifica el bloque de compresi??n
    fin = int(h)  # Se analiza el bloque hasta el valor de h
    M, P, fiMn, fiPn, hztalFiX, hztalFiY = tablaBloqComp(fin, paso, nBarrash, nBarrasb, b, h, fc, Ec, fy, Es, ABarra,
                                                         dc, estribos)
    # print(M, P, fiMn, fiPn)
    graficar(M, P, fiMn, fiPn, hztalFiX, hztalFiY, Mx, Py)
