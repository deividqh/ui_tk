""" 
LOGICA DEL NEGOCY
Archivo donde quiero que estén los comands de los widgets creados 
Tengo que importar las bibliotecas que necesite.
"""
import tkinter as tk
from tkinter import messagebox, filedialog
import os
import json

def limpiar_textos(textos):
    """ A Eliminar. Solo de Muestra """
    for i, t in enumerate(textos):
        t.delete(0, tk.END)
        # t.insert(0, f"Hello Texto {i}")


# El primer parámetro es el título de la ventana y el segundo es el texto
def mostrar_alerta(texto_alerta):
    """ A Eliminar. Solo de Muestra """
    messagebox.showinfo("Titulo", texto_alerta)



def al_cambiar(estado_checkbox):
    if estado_checkbox.get():
        print("El checkbox está MARCADO")
    else:
        print("El checkbox está DESMARCADO")


