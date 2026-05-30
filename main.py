# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
import tkinter as tk
from tkinter import ttk  # Importa los componentes modernos
import os               # SISTEMA OPERATIVO(PARA LIMPIAR LA TERMINAL)
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
from ui_tk.pestanas_dicc import Pestanas_by_Step 
from ui_tk.row_draw import Nivel_2
import logica_ui_tk as cmd

def main():
    """ Quiero poner una de pestañas y en cada pestaña un Frame al menos de prueba """

    ventana = tk.Tk()
    ventana.title("Sistema de Pestañas Secuenciales")
    # ventana.geometry("680x350")
    
    # ■■■■ ■■■■ ■■■■ ■■■■ ■■■■ ■■■■ ■■■■ ■■■■ ■■■■ ■■■■ ■■■■ ■■■■ ■■■■ ■■■■ ■■■■ 
    # Configuración de las pestañas a añadir. key es el nombre corto y value es el Título de la UI.
    configuracion_pestanas = {
        "dat": "Datos",
        "split": "Split",
        "alg": "Algoritmo/Modelo",
        "met": "Métricas",
        "graf": "Gráficas",
        'tab6': 'Tab 6',
        'tab7': 'Tab 7',
        'tab8': 'Tab 8',
    }
    a=1
    b=2
    TABS = Pestanas_by_Step(ventana, configuracion_pestanas, b_botones_cursor = True, mode_step=False)
    TABS.pack(fill="both", expand=True, padx=10, pady=10)

    # ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ 
    # FRAME PARA LA PESTAÑA DATOS
    F1 = Nivel_2(TABS.get_p('dat'), shape="5x6", padx=15, pady=7)     
    # ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ 
    # ■ WIDGETS
    lbl_nom  = tk.Label(F1.frame, text='Nombre: ', anchor='w')
    txt_nom  = tk.Entry(F1.frame)    
    lbl_ape1 = tk.Label(F1.frame, text='Apellido1: ', anchor='w')
    txt_ape1 = tk.Entry(F1.frame)
    lbl_ape2 = tk.Label(F1.frame, text='Apellido2: ', anchor='w')
    txt_ape2 = tk.Entry(F1.frame)    
    btn_add = tk.Button(F1.frame, text="Añadir")
    btn_upt = tk.Button(F1.frame, text="Actualiza")
    btn_del = tk.Button(F1.frame, text="Borrar")
    scrollbar = tk.Scrollbar(F1.frame, orient=tk.VERTICAL)
    listbox = tk.Listbox(F1.frame, yscrollcommand=scrollbar.set, selectmode=tk.SINGLE)

    # ■  MATRIZ
    matrix = [
        [lbl_nom,  txt_nom, "+", "+", "+", "_"       ],
        [lbl_ape1, txt_ape1, "_", lbl_ape2, txt_ape2 ],   
        ['-' , listbox, '+', '+', '+', '-'],              
        [],                                             
        [btn_add,  btn_upt, "+", "_", btn_del ],   
    ]
    # ■  DIBUJO
    F1.draw(matrix)

    # ______________________________________
    # ■ 'family' asocia nombre a grupo de widgets • • • (Opciona pero Recomendado) 
    F1.family.formar("textos", [txt_nom, txt_ape1, txt_ape2,])
    F1.family.formar("crud", [btn_add, btn_upt, btn_del,])
    # ______________________________________
    # ■ Aplica los comandos de los widgets limpiamente en otro archivo(cmd) • • • (Opciona pero Recomendado) 
    btn_del.config(command=lambda: cmd.limpiar_textos( F1.family.familiares('textos') ))
    btn_add.config(command=lambda: cmd.mostrar_alerta( "Texto de Alerta de Prueba" ))

    # ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ 
    # FRAME PARA LA PESTAÑA SPLIT
    F2 = Nivel_2(TABS.get_p('split'), shape="12x6", padx=15, pady=7)    
    # ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ 

    # • checkbutton
    chk_st = tk.BooleanVar(value=False)
    texto = "Boton de Check:"
    checkbox = ttk.Checkbutton( F2.frame, text=texto, variable = chk_st, command=lambda: cmd.chk_estado( chk_st ) )

    # • my_slide
    # l_slide, slide, v_slide = F2.my_slide(texto= texto, desde=0, hasta=10, valor_inicial=3,tipo_dato=tk.DoubleVar )
    slide_derecha = F2.my_slide(titulo="■ Ratio de Aprendizaje", desde=0, hasta=100, rel_coords="e")
    slide_arriba = F2.my_slide(titulo="■ Nivel de Ruido (db)", desde=0, hasta=10, rel_coords="n")
    slide_invisible = F2.my_slide(titulo="", desde=0, hasta=5, rel_coords="s")

    # • my_radio
    opciones_algoritmo = [
        {"texto": "Random Forest", "value": 1},
        {"texto": "XGBoost", "value": 2},
        {"texto": "Regresión Logística", "value": 3}
    ]
    titulo = "Selecciona un Algoritmo"
    radio_con_titulo = F2.my_radio(titulo=titulo, dicc_radio=opciones_algoritmo, orientacion="vertical" )

    # • my_radio
    opciones_booleanas = [{"texto": "Sí", "value": True}, {"texto": "No", "value": False}]
    radio_sin_titulo = F2.my_radio(titulo="", dicc_radio=opciones_booleanas, orientacion="horizontal")

    # • Combo
    content_combo = ["SVM", "Naivy Bayes", "LDA", "PCA", "Random Forest"]
    combo = ttk.Combobox(F2.frame, values=content_combo, state="readonly")
    combo.current(0)
    # ■  MATRIZ
    matrix_F2 = [
        [checkbox, '+', '+'],                                             
        [] , 
        [slide_derecha, '+', '+', '+'] ,
        [] ,
        [slide_arriba, '+', '+', '+'] ,
        [slide_invisible, '+', '+', '+'] ,
        [ '+', '+', '+', '+', '+', '+'] ,
        [radio_con_titulo, '_', '_', '_', '_'] ,
        [radio_sin_titulo] , 
        [combo] ,
    ]
    # ■  DIBUJO
    F2.draw(matrix = matrix_F2)

    # ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ 
    # FRAME PARA LA PESTAÑA ALGORITMOS
    F3 = Nivel_2(TABS.get_p('alg'), shape="6x3", padx=15, pady=20)    
    # ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ 

    # filedialog = F3.my_fileDialog(entry_width=35, )
    tit = "■ Configuración del Modelo"
    txt = "Cargar Pesos (.json)"
    fd_s = F3.my_fileDialog(titulo=tit,texto_boton=txt,rel_coords="w",filetypes=[("Archivos JSON", "*.json")] )
    fd_w = F3.my_fileDialog(texto_boton="Buscar CSV",rel_coords="w", filetypes=[("Archivos CSV", "*.csv")] )
    fd_e = F3.my_fileDialog(texto_boton="📂 Seleccionar Dataset",rel_coords="e",entry_width=35)
    matrix_F3 = [
        [] ,
        [fd_s, '+', '+'] ,                                             
        [] ,
        [fd_e, '+', '+'] ,
        [] ,
        [fd_w, '+', '+'] ,
    ]
    F3.draw(matrix = matrix_F3)
    
    # ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ 
    # FRAME PARA LA PESTAÑA 'METRICAS'
    # ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ 
    F4 = Nivel_2(TABS.get_p('met'), shape="6x6", padx=15, pady=7)    

    

    # ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ 
    # FRAME PARA LA PESTAÑA 'GRAFICOS'
    # ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ 
    F5 = Nivel_2(TABS.get_p('graf'), shape="6x6", padx=15, pady=7)    

    
    # ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ 
    # FRAME PARA LA PESTAÑA 'Tab6'
    # ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ 
    F6 = Nivel_2(TABS.get_p('tab6'), shape="1x1", padx=15, pady=7)    

    # Los datos se pueden sacar de un archivo csv, json, base de datos...
    # ahora creo unos datos sinteticos para mostrar el control 
    datos_ok = [
        (1, "Ana", "García", "López", "555-1234", "Madrid"),
        (1, "Marcos", "Rojas", "Márquez", "3333-1234", "Vigo"),
        (1, "María", "Saturno", "Obradoiro", "353-1234", "Murcia"),
        (2, "Juan", "Pérez", "Gómez", "111-1234", "Las Palmas de Gran Canaria"),
    ]
    titulo = "■ Demostración de My_Tree con Datos Sintenticos y cabeceras manuales."
    # En caso de que no se metan cabeceras, se escribiran igualmente los datos sinteticos
    cab = ["ID", "Nombre", "Ape-1", "Ape-2", "Teléfono", "Ciudad"]    
    poscion_textos = [["Nombre", "_", "_"],[],["Ape-1", "+", "Ape-2", "+"],["Ciudad", "+","Teléfono"] ]
    arbol = F6.my_tree(titulo=titulo, cabeceras=cab, datos=datos_ok, textos = poscion_textos )    
    matrix_F6 = [
        [arbol,] ,
    ]
    F6.draw(matrix = matrix_F6)

    # ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ 
    # FRAME PARA LA PESTAÑA 'Tab7'
    # ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ 
    # import pandas as pd
    # import csv  # Importamos la librería estándar para detectar cabeceras
    # from tkinter import messagebox

    F7 = Nivel_2(TABS.get_p('tab7'), shape="2x2", padx=15, pady=7)    

    acciones_crud = [
        ("Add", lambda: cmd.saludar("add") ), "+", '_', 
        ("Borrar", lambda: cmd.saludar("borrar") ), '_', 
        ("Actulizar", lambda: cmd.saludar("update") ), "+"
    ]

    # • My_Tree sin textos y vacío para cargar.    
    # arbol_visor = F7.my_tree(titulo="■ Visor Dinámico de Datos")
    titulo="■ Visor Dinámico de Datos"
    # arbol_visor = F7.my_tree( titulo = titulo, textos=None,  acciones=acciones_crud,)
    poscion_textos = [[1, "+", "_"],[],[2, "+", 3, "+"],[0,] ]
    arbol_visor = F7.my_tree( titulo = titulo, 
                            textos={}, 
                            textos_height=None,    # No pone altura maxima
                            acciones=acciones_crud,)
    # d_texto = None 
    fd_dataset = F7.my_fileDialog(titulo="■ Origen de Datos", 
                                texto_boton="📂 Cargar Archivo",
                                filetypes=[("Archivos CSV","*.csv")],
                                rel_coords="e",                                 
                                command=lambda ruta: cmd.accion_file_d_to_treeview(ruta, arbol_visor)) # ► ¡CABLEADO DIRECTO!
    pass
    matrix = [
        [fd_dataset, "+"],
        [arbol_visor, "+"]
    ]
    F7.draw(matrix=matrix)

    # ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ 
    # FRAME PARA LA PESTAÑA 'Tab7'
    F8 = Nivel_2(TABS.get_p('tab8'), shape="2x2", padx=15, pady=20)    
    # ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ 
    titulo = "■ Visor dinamico de csv con My_Tree y FileDialog integrado ■"
    poscion_textos = [[1, "+", "_"],[],[2, "+", 3, "+"],[0,] ]
    acciones_crud = [
        ("Add", lambda: cmd.saludar("add") ), "+", '_', 
        ("Borrar", lambda: cmd.saludar("borrar") ), '_', 
        ("Actulizar", lambda: cmd.saludar("update") ), "+"
    ]
    tree_csv = F8.my_tree_csv(titulo = titulo, 
                                textos={}, 
                                textos_height=200,                                 
                                acciones = acciones_crud,
                                )                     
    matrix = [
        [tree_csv, "+"]
    ]
    F8.draw(matrix=matrix)

    # • • • — — — • • •
    ventana.mainloop()
    # • • • — — — • • •



# █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ 
# █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ 
# • • • • • • • • • • • • • • • • • INICIO • • • • • • • • • • • • • • • • • • • 
# █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ 
# █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ 
if __name__ == "__main__":
    # • Limpio la terminal 
    os.system('cls')    
    main() 
