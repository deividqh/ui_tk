import tkinter as tk
from tkinter import ttk  # Importa los componentes modernos
from ui_tk.Familia import Familia

""" 
• Mete los elementoes en level_2 por lo que tienes que definir la fila en el momento de la creación
del objeto y luego defines la posición y dibujas con draw.
• Funciona bien si la fila definida en la creación del widget  se cuadra con la fila en la matriz.

"""
class Nivel_2:
    def __init__(self, root, title="Formulario", ancho=300, alto=450, 
                 filas=None, cols_by_fila=1, padx=5, pady=5, shape=None):
        self.root = root
        self.root.title(title)
        self.padx = padx
        self.pady = pady
        self.level_2 = {}           # Diccionario de filas
        self.family = Familia()     # clase que relaciona grupos de widgets con un nombre vulgar.
        self.filas = None
        self.columnas = None        # Guarda el número de columnas (para shape)
        self.level_1 = tk.Frame(self.root)
        self.level_1.pack(fill="both", expand=True)
        
        
        # --- Procesar shape "filasxcolumnas" ---
        if shape is not None:
            try:
                filas_str, cols_str = shape.lower().split('x')
                self.filas = int(filas_str.strip())
                self.columnas = int(cols_str.strip())
                cols_by_fila = [self.columnas] * self.filas
            except ValueError:
                raise ValueError(f"Formato de shape inválido: '{shape}'. Use formato 'filasxcolumnas' (ej: '4x6')")
        
        if self.filas or (isinstance(cols_by_fila, list) and len(cols_by_fila) > 0):
            self._build_structure(cols_by_fila)

    def _build_structure(self, cols_config):
        for i, num_cols in enumerate(cols_config):
            if num_cols and num_cols > 0:
                frame_fila = tk.Frame(self.level_1)
                frame_fila.pack(fill="x", padx=self.padx, pady=self.pady)
                for col in range(num_cols):
                    frame_fila.grid_columnconfigure(col, weight=1)
                self.level_2[i] = frame_fila
            else:
                spacer = tk.Frame(self.level_1)
                spacer.pack(fill="x", pady=self.pady * 2)
                self.level_2[i] = spacer

    def row(self, index):
        return self.level_2.get(index)

    def add(self, widget, column, **kwargs):
        if 'sticky' not in kwargs:
            kwargs['sticky'] = "we"
        widget.grid(row=0, column=column, **kwargs)
        return widget

    def set_row(self, row, *items, **kwargs):
        if row not in self.level_2:
            raise ValueError(f"La fila {row} no existe.")
        added_widgets = []
        for column, item in enumerate(items):
            if self._is_empty_cell(item):
                continue
            new_widget = self.add(item, column, **kwargs)
            added_widgets.append(new_widget)
        return added_widgets
    
    def _is_empty_cell(self, item):
        return item is None or item == "_" or item == '-' or item == 'x'
    
    def frame(self):
        return self.level_1 if self.level_1 else None

    # ============================================================
    # MÉTODO draw / drow
    # ============================================================
    def draw(self, matrix):
        """
        ■ Recibe una matriz de widgets ya creados en sus respectivos masters (filas).        
        • Reglas por fila:
            - None o []: fila vacía. Se omite (la fila debe existir en la estructura).
            - list/tuple: se procesan los elementos.        
        • Reglas por elemento:
            - None, "_", "-", "x": celda vacía → frame vacío con padx.
            - "+": colspan del widget real más cercano a la izquierda (saltando solo "+").
                Si no hay widget a la izquierda → espacio vacío puro (se ignora).
            - Widget real: se posiciona con grid en la columna actual.
        """
        for i, row_data in enumerate(matrix):
            # ■ Fila vacía (None o lista vacía) 
            if row_data is None or (isinstance(row_data, (list, tuple)) and len(row_data) == 0):
                continue            
            if not isinstance(row_data, (list, tuple)):
                continue
            
            # ■ No se admiten filas dinámicas 
            if i not in self.level_2:
                raise IndexError(
                    f"La fila {i} no existe en la estructura. "
                    f"Filas disponibles: 0..{self.filas-1}. "
                    f"No se admiten filas dinámicas."
                )
            
            frame_fila = self.level_2[i]
            
            # ■ Si es un spacer, no se colocan widgets
            if not isinstance(frame_fila, tk.Frame):
                continue
            
            col_idx = 0
            placed = []  # Registro interno para manejar colspanes
            
            for item in row_data:
                # ── Celda vacía ──
                if item is None or item in ("_", "-", "x"):
                    empty_frame = tk.Frame(frame_fila, width=self.padx)
                    empty_frame.grid(row=0, column=col_idx, sticky="we")
                    col_idx += 1
                    placed.append({'type': 'empty', 'col': col_idx - 1})
                    continue
                
                # ── Colspan "+" ──
                if item == "+":
                    target = None
                    target_pos = None
                    
                    # Buscar último widget real a la izquierda (saltando solo otros "+")
                    for k in range(len(placed) - 1, -1, -1):
                        p = placed[k]
                        if p['type'] == 'widget':
                            target = p['widget']
                            target_pos = k
                            break
                        elif p['type'] == 'empty':
                            # Celda vacía en medio: no hay widget directo a la izquierda
                            break
                    
                    if target is not None:
                        old_span = placed[target_pos].get('span', 1)
                        new_span = old_span + 1
                        placed[target_pos]['span'] = new_span
                        target.grid_configure(columnspan=new_span)
                        col_idx += 1
                    # Si no hay widget → espacio vacío puro, se ignora
                    continue
                
                # ── Widget real ──
                item.grid(row=0, column=col_idx, sticky="we")
                placed.append({'type': 'widget', 'widget': item, 'col': col_idx, 'span': 1})
                col_idx += 1
        
        return self
    
    

# ==========================================
# EJEMPLO DE USO
# ==========================================
def checkbox_estado():
    # El método .get() obtiene el valor actual (1 si está marcado, 0 si no)
    if var_chk.get() == 1:
        checkbox.config(text="¡Casilla marcada!")
    else:
        checkbox.config(text="Casilla desmarcada")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x300")
    # Crear estructura: 5 filas x 6 columnas
    F1 = Nivel_2(root, shape="10x6", padx=15, pady=7)
    print(f"Filas: {F1.max_rows}, Columnas: {F1.columnas}")
    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
    # ■ Crear widgets • Es importante colocar la fila ro_row
    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
    lbl_nom  = tk.Label(F1.row(0), text='Nombre: ')
    txt_nom  = tk.Entry(F1.row(0))
    # ■ 
    lbl_ape1 = tk.Label(F1.row(1), text='Apellido1: ')
    txt_ape1 = tk.Entry(F1.row(1))
    lbl_ape2 = tk.Label(F1.row(1), text='Apellido2: ')
    txt_ape2 = tk.Entry(F1.row(1))
    # ■ 
    var_chk = tk.IntVar()
    checkbox = tk.Checkbutton(F1.row(2), text="soy CheckButton", variable=var_chk, command=checkbox_estado )
    # ■ 
    var_sc = tk.DoubleVar(value=5)
    slide = tk.Scale(F1.row(2), from_=0, to=10, resolution=1, variable=var_sc, orient=tk.HORIZONTAL, length=150, font=('Arial', 8))
    # ■ 
    combo = ttk.Combobox(F1.row(2), values=["dark_background", "ggplot", "bmh", "seaborn-v0_8-whitegrid"], state="readonly")
    combo.current(0)
    btn_add = tk.Button(F1.row(4), text="Añadir")
    btn_upt = tk.Button(F1.row(4), text="Actualiza")
    btn_del = tk.Button(F1.row(4), text="Borrar")
    scrollbar = tk.Scrollbar(F1.row(5), orient=tk.VERTICAL)
    listbox = tk.Listbox(F1.row(5), selectmode=tk.SINGLE)
    # ■■■■■■■■■■■■■■■■■■■■■■ 
    # ■ Matriz de dibujo
    # ■■■■■■■■■■■■■■■■■■■■■■ 
    matrix = [
        [lbl_nom,  txt_nom , '+'  , '+'  , '+'     ],  # Fila 0
        [lbl_ape1, txt_ape1, "+", lbl_ape2, txt_ape2  , '+'],  # Fila 1
        [combo, '_', slide , '_', checkbox, '_'],                                                    # Fila 2 (vacía)
        [listbox, '+', '+', '+', '+', '+'],                               
        [btn_add,  btn_upt,  "_", '_',  "_",  btn_del      ],  # Fila 4
    ]
    F1.draw(matrix)   
    # ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ 
    F1.frame().config(bg="lightgray")
    root.mainloop()

