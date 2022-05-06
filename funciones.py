import math
import numpy as np
from matplotlib import pyplot as plt


def tablaFibras(c, nBarrash, nBarrasb, b, h, fc, Ec, fy, Es, ABarra, dc):
    # Fibras para el concreto-------------
    eu = 0.003
    fiy = eu / c
    numFibConc = 10
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
    M = np.append(M, 0)  # Agrega 0 y el último elemento en P para completar con línea horizontal
    P = np.append(P, P[-1])  # Último elemento en P

    # Crear un vector de distancias entre los valores del vector fiPn y 0.75*el último valor de fiPn
    distancias = np.abs(fiPn - 0.75 * fiPn[-1])
    # Encontrar la posición de la menor de esas distancias
    # Los [0][0] al final son para devolver el número de la posición,
    # porque inicialmente es una tupla y luego es un array,
    # entonces se debe extraer dos veces.
    # La función np.where devuelve una tupla
    posMinDif = np.where(min(distancias) == distancias)[0][0]
    # Línea horizontal en 0.75 * fiPn
    hztalFiX = np.array([0., fiMn[posMinDif]])
    hztalFiY = np.array([0.75 * fiPn[-1], 0.75 * fiPn[-1]])

    return M, P, fiMn, fiPn, hztalFiX, hztalFiY


def graficar(x, y, x2, y2, x3, y3, x4, y4):
    fig, ax = plt.subplots()  # Crear la figura y los ejes
    ax.plot(x, y, color="blue", label="P - M")  # Dibujar línea
    ax.plot(x2, y2, color="orange", label=r"$\phi$Pn - $\phi$Mn")  # Dibujar línea
    ax.plot(x3, y3, color="orange")  # Dibujar línea horizontal complementaria
    ax.scatter(x4, y4, color="red")
    # ax.patch.set_facecolor("gray")
    # fig.patch.set_facecolor("gray")
    plt.title("Interacción P - M", size=20)
    plt.xlabel("M (kN.m)", size=16)
    plt.ylabel("P (kN)", size=16)
    plt.legend()
    plt.grid()
    plt.show()  # Mostrar el gráfico
