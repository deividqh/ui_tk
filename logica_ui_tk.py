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



def chk_estado(estado_checkbox):
    if estado_checkbox.get():
        print("El checkbox está MARCADO")
    else:
        print("El checkbox está DESMARCADO")


def act_cargar_archivo(ruta_fichero):
        # print(fd_dataset.get_ruta() + "-" + fd_dataset.entry.get())
        if not ruta_fichero: 
            return 
        print(f"Analizando y leyendo dataset desde: {ruta_fichero}")
        try:
            # =========================================================
            # 1. HUSMEAR EL ARCHIVO (DETECTAR CABECERA)
            # =========================================================
            tiene_cabecera = True # Asumimos True por defecto
            # Abrimos solo un pedacito del archivo para no saturar la memoria
            with open(ruta_fichero, 'r', encoding='utf-8') as f:
                muestra = f.read(2048) # Leemos los primeros 2048 bytes
                try:
                    tiene_cabecera = csv.Sniffer().has_header(muestra)
                except csv.Error:
                    # Si el Sniffer falla (ej. hay muy pocos datos), asumimos que sí tiene
                    pass
            # =========================================================
            # 2. LEER CON PANDAS SEGÚN LO DETECTADO
            # =========================================================
            if tiene_cabecera:
                # Si tiene cabecera, leemos normal
                df = pd.read_csv(ruta_fichero)
                nuevas_cabeceras = df.columns.tolist()
            else:
                # Si NO tiene cabecera, le avisamos a Pandas con header=None 
                # para que no se coma la primera fila de datos.
                df = pd.read_csv(ruta_fichero, header=None)
                # Como no hay cabeceras reales, Pandas las llama 0, 1, 2...
                # Nosotros generamos nombres bonitos: "col0", "col1", "col2"...
                nuevas_cabeceras = [f"col{i}" for i in range(df.shape[1])]
            # =========================================================
            # 3. EXTRAER DATOS E INYECTAR EN LA UI
            # =========================================================
            nuevos_datos = df.values.tolist()
            # Inyectamos
            arbol_visor.set_feature_names(nuevas_cabeceras)
            arbol_visor.load_data(nuevos_datos)
            print(f"Carga exitosa: {'Con' if tiene_cabecera else 'Sin'} cabeceras detectadas.")
        except Exception as e:
            print(f"Error al procesar el archivo: {e}")
            messagebox.showerror("Error de lectura", f"No se pudo leer el archivo CSV.\n\nDetalle: {e}")