from tkinter import *
from tkinter import messagebox
# from tkinter import ttk
# from tkinter import simpledialog
# import xlwt
import webbrowser
# from xlwt import Workbook
# import math
# import pickle
# from tkinter import filedialog
# import os
from numpy import var

from funciones import principal

# colores a utilizar-------------------------------------
azul_oscuro = "#2f354a"
azul_medio = "#1b5998"
naranja = "#fe9870"
claro = "#f2eddf"
fuente = ("Verdana", 10)
nombre = "Diseño a Flujo Libre"

# ----------------Interfaz gráfica-----------------------------

raiz = Tk()
raiz.title(nombre)
# raiz.iconbitmap('road16px.ico')

barraMenu = Menu(raiz, font=fuente)
raiz.config(menu=barraMenu, bg=azul_oscuro)

ancho_programa = 300
alto_programa = 500

ws = raiz.winfo_screenwidth()  # ancho pantalla
hs = raiz.winfo_screenheight()  # alto pantalla

x = ws / 2 - ancho_programa / 2
y = hs / 2 - alto_programa / 2

raiz.geometry('%dx%d+%d+%d' % (ancho_programa, alto_programa, x, y))

frame1 = Frame(raiz, width=300, height=500, bg=azul_oscuro)
# frame2 = Frame(raiz, width=550, height=500, bg=azul_oscuro)
# frame3 = Frame(frame2, width=350, height=80, bg=azul_oscuro)
# frame4 = Frame(frame2, bg=azul_oscuro)

# frame1.config(width=350, height=310)
# frame2.config(width=350, height=310)

frame1.pack(side="left")
# frame2.pack(side="left")
# frame3.pack()
# frame4.pack()

frame1.config(bd=10, relief="groove")
# frame2.config(bd=10, relief="groove")

# fc, dBarra, ABarra, nBarrasb, nBarrash, estribos, b, h
#  Entrada de fc
labelfc = Label(frame1, text="f'c (MPa):", bg=azul_oscuro, fg=claro, font=fuente)
labelfc.place(x=10, y=30)
entfc = Entry(frame1, width=8, justify="right", bg=azul_medio, fg=claro, font=fuente)
entfc.place(x=180, y=30)

#  Entrada de dBarra
labeldBarra = Label(frame1, text="Diámetro de barra (mm):", bg=azul_oscuro, fg=claro, font=fuente)
labeldBarra.place(x=10, y=80)
entdBarra = Entry(frame1, width=8, justify="right", bg=azul_medio, fg=claro, font=fuente)
entdBarra.place(x=180, y=80)

#  Entrada de ABarra
labelABarra = Label(frame1, text="Área de barra (mm2):", bg=azul_oscuro, fg=claro, font=fuente)
labelABarra.place(x=10, y=130)
entABarra = Entry(frame1, width=8, justify="right", bg=azul_medio, fg=claro, font=fuente)
entABarra.place(x=180, y=130)

#  Entrada de nBarrasb
labelnBarrasb = Label(frame1, text="Número de barras en b:", bg=azul_oscuro, fg=claro, font=fuente)
labelnBarrasb.place(x=10, y=180)
entnBarrasb = Entry(frame1, width=8, justify="right", bg=azul_medio, fg=claro, font=fuente)
entnBarrasb.place(x=180, y=180)

#  Entrada de nBarrash
labelnBarrash = Label(frame1, text="Número de barras en h:", bg=azul_oscuro, fg=claro, font=fuente)
labelnBarrash.place(x=10, y=230)
entnBarrash = Entry(frame1, width=8, justify="right", bg=azul_medio, fg=claro, font=fuente)
entnBarrash.place(x=180, y=230)

#  Entrada de b
labelb = Label(frame1, text="Dimensión b (mm):", bg=azul_oscuro, fg=claro, font=fuente)
labelb.place(x=10, y=280)
entb = Entry(frame1, width=8, justify="right", bg=azul_medio, fg=claro, font=fuente)
entb.place(x=180, y=280)

#  Entrada de h
labelh = Label(frame1, text="Dimensión h (mm):", bg=azul_oscuro, fg=claro, font=fuente)
labelh.place(x=10, y=330)
enth = Entry(frame1, width=8, justify="right", bg=azul_medio, fg=claro, font=fuente)
enth.place(x=180, y=330)

# Entrada de estribos
varOpcionTransversal = BooleanVar()
varOpcionTransversal.set(True)

labelTransversal = Label(frame1, text="Transversal:", bg=azul_oscuro, fg=claro, font=fuente)
labelTransversal.place(x=10, y=380)

rbutEstribos = Radiobutton(frame1, text="Estribos", variable=varOpcionTransversal,
                           value=True, bg=azul_oscuro, fg=claro, font=fuente)
rbutEstribos.config(activebackground=azul_oscuro, activeforeground=claro, selectcolor=azul_medio)
rbutEstribos.place(x=180, y=380)
rbutEspiral = Radiobutton(frame1, text="Espiral", variable=varOpcionTransversal, value=False, bg=azul_oscuro, fg=claro,
                          font=fuente)
rbutEspiral.config(activebackground=azul_oscuro, activeforeground=claro, selectcolor=azul_medio)
rbutEspiral.place(x=180, y=410)

# ----------------Botón de calcular-----------------------------
botCalcular = Button(frame1, text="Graficar", width=10,
                     command=lambda: llamarFunciones())
botCalcular.config(bg=claro, fg=azul_oscuro, activebackground=azul_oscuro, activeforeground=claro, font=fuente)
botCalcular.place(x=100, y=450)


# ----------------Funciones de menú------------------

def nuevo():
    entfc.delete(0, 'end')
    entdBarra.delete(0, 'end')
    entABarra.delete(0, 'end')
    entnBarrasb.delete(0, 'end')
    entnBarrash.delete(0, 'end')
    entb.delete(0, 'end')
    enth.delete(0, 'end')


def infoAdicional():
    ventana_info = Tk()
    ventana_info.title(nombre)
    ventana_info.config(bg=claro)
    ventana_info.resizable(0, 0)
    ancho_ventana = 300
    alto_ventana = 200

    wsv = ventana_info.winfo_screenwidth()  # ancho pantalla
    hsv = ventana_info.winfo_screenheight()  # alto pantalla
    xv = wsv / 2 - ancho_ventana / 2
    yv = hsv / 2 - alto_ventana / 2
    ventana_info.geometry('%dx%d+%d+%d' % (ancho_ventana, alto_ventana, xv, yv))

    texto1 = Label(ventana_info, text="Autores:" +
                                      "\n\nGerardo Andrés Dorado Jurado\nIngeniero Civil\nMagíster en Ingeniería de "
                                      "Pavimentos",
                   bg=claro, fg=azul_oscuro, font=fuente)
    texto2 = Label(ventana_info,
                   text="Nathalia Cerón Belalcázar\nIngeniera Civil\nMagíster en Estructuras",
                   bg=claro, fg=azul_oscuro, font=fuente)

    texto3 = Label(ventana_info, text="LinkedIn", fg=azul_medio, bg=claro, cursor="hand2", font=fuente)
    texto3.bind("<Button-1>", lambda e: webbrowser.open_new("www.linkedin.com/in/gadoradoj/"))

    texto1.pack()
    texto3.pack()
    texto2.pack()
    Label(ventana_info, text="Versión 2022", bg=claro, fg=azul_oscuro, font=fuente).pack()

    ventana_info.mainloop()


def avisoLicencia():
    messagebox.showinfo(nombre, "Programa de uso libre.")


def salirAplicacion():
    valor = messagebox.askokcancel("Salir", "¿Seguro que desea salir?")
    if valor:
        raiz.destroy()


# -------------------Barra de menús----------------------------

archivoMenu = Menu(barraMenu, tearoff=0, bg=azul_medio, fg=claro, font=fuente)
archivoMenu.add_command(label="Nuevo", command=nuevo)
# archivoMenu.add_command(label="Abrir", command=abrir)7
# archivoMenu.add_command(label="Guardar", command=guardar)
# archivoMenu.add_command(label="Exportar", command=exportar)
archivoMenu.add_separator()  # barra separadora
archivoMenu.add_command(label="Salir", command=salirAplicacion)

ayudaMenu = Menu(barraMenu, tearoff=0, bg=azul_medio, fg=claro, font=fuente)
ayudaMenu.add_command(label="Licencia", command=avisoLicencia)
ayudaMenu.add_command(label="Acerca de...", command=infoAdicional)

# Agrega los botones a la barra de menú
barraMenu.add_cascade(label="Archivo", menu=archivoMenu)
barraMenu.add_cascade(label="Ayuda", menu=ayudaMenu)


def llamarFunciones():
    try:
        principal(float(entfc.get()), float(entdBarra.get()), float(entABarra.get()), int(entnBarrasb.get()),
                  int(entnBarrash.get()), varOpcionTransversal.get(), float(entb.get()), float(enth.get()))
    except:
        pass


raiz.mainloop()
