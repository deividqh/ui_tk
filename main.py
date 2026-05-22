# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
import tkinter as tk
from tkinter import ttk  # Importa los componentes modernos
import os               # SISTEMA OPERATIVO(PARA LIMPIAR LA TERMINAL)
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
from ui_tk.pestanas_dicc import StepByStab 
from ui_tk.row_draw import Nivel_2
import comandos_ui_tk as cmd

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
    }
    a=1
    b=2
    TABS = StepByStab(ventana, configuracion_pestanas, b_botones = True)
    TABS.pack(fill="both", expand=True, padx=10, pady=10)

    # ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ 
    # FRAME PARA LA PESTAÑA DATOS
    # ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ 

    F1 = Nivel_2(TABS.get_p('dat'), shape="5x6", padx=15, pady=7)     

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
    # ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ 
    F2 = Nivel_2(TABS.get_p('split'), shape="5x6", padx=15, pady=7)    
    # ■ WIDGETS
    # •
    estado_checkbox = tk.BooleanVar(value=False)
    checkbox = ttk.Checkbutton( F2.frame, text="Boton de Check:", variable = estado_checkbox, 
                                command=lambda: cmd.al_cambiar( estado_checkbox ) )
    # • 
    l_slide, slide, v_slide = F2.my_slide(texto="■ Split (Train/Test)", 
                                          desde=0, hasta=10, 
                                          valor_inicial=3,
                                          tipo_dato=tk.DoubleVar
                                          )
    # ■  MATRIZ
    matrix_F2 = [
        [] ,
        [checkbox, '+', '+'],                                             
        [ '+', '+', '+', '+', '+', '+'] ,
        [l_slide, slide, '+', '+', '+', v_slide] ,
        [ '+', '+', '+', '+', '+', '+'] ,
    ]
    # ■  DIBUJO
    F2.draw(matrix = matrix_F2)

    # ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ 
    # FRAME PARA LA PESTAÑA ALGORITMOS
    # ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ 
    F3 = Nivel_2(TABS.get_p('alg'), shape="6x6", padx=15, pady=7)    

    # ■ manera de meter el fileDialog, obteniendo el texto y el botón.
    fd_texto, fd_boton = F3.my_fileDialog(entry_width=35, b_split=True)
    matrix_F3 = [
        ['+', '+', '+', '+', '+', '_'] ,
        [fd_boton, fd_texto],                                             
        [] ,
    ]
    F3.draw(matrix = matrix_F3)
    
    # ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ 
    # FRAME PARA LA PESTAÑA 'METRICAS'
    # ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ ■■ 
    F4 = Nivel_2(TABS.get_p('met'), shape="6x6", padx=15, pady=7)    

    # Los datos se pueden sacar de un archivo csv, json, base de datos...
    # ahora creo unos datos sinteticos para mostrar el control 
    datos_ok = [
        (1, "Ana", "García", "López", "555-1234", "Madrid"),
        (1, "Marcos", "Rojas", "Márquez", "3333-1234", "Vigo"),
        (1, "María", "Saturno", "Obradoiro", "353-1234", "Murcia"),
        (2, "Juan", "Pérez", "Gómez", "111-1234", "Las Palmas de Gran Canaria"),
    ]
    # En caso de que no se metan cabeceras, se escribiran igualmente los datos sinteticos
    cab = ["ID", "Nombre", "Apellido 1", "Apellido 2", "Teléfono", "Ciudad"]    
    # posicion de los textos.
    dicc = {'A0': cab[0], 'B0': "Nombre",  'C0': '+',       'D0': '+' ,  
            'A1': cab[2], 'B1': "+" , 	   'C1': cab[3],    'D1': '+' , 
            'A2': "_",    'B2': "Ciudad",  'C2': cab[4],    'D2': cab[5] , 
    } 
    titulo = "■ BDatos de Clientes"
    mi_tabla = F4.my_tree(titulo=titulo, cabeceras=cab, datos=datos_ok, d_textos = dicc )    
    arbol_not_features = F4.my_tree(titulo="■■",  datos=datos_ok, d_textos = dicc )    
    arbol_vacio = F4.my_tree(titulo="•vacio•" )    
    
    btn_set_cab = tk.Button(F4.frame, text="Inyectar Cabeceras", 
                            command=lambda: arbol_vacio.set_feature_names(["A", "B", "C"]))
    matrix_F4 = [
        # [arbol_not_features] ,
        [arbol_vacio, '+', '+', '+', '+', '+'],                                             
        [btn_set_cab],                                             
        # [mi_tabla, '+', '+', '+', '+', '+'] ,
    ]

    F4.draw(matrix = matrix_F4)

    # Le damos a la fila 2 de F4 la capacidad de absorber el espacio sobrante en vertical
    # F4.frame.rowconfigure(2, weight=1)
    F4.frame.rowconfigure(0, weight=1)

    # btn_del.config(command=lambda: cmd.limpiar_textos(  ))
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
