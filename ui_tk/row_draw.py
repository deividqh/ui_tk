import tkinter as tk
from tkinter import ttk             # Importa los componentes modernos
from tkinter import filedialog
import os

import pandas as pd
import numpy as np


# █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ 
class My_FileDialog(ttk.Frame):
    """
    Widget compuesto (KISS). Hereda de ttk.Frame (invisible).
    Si se pasa 'titulo', genera un ttk.LabelFrame interno.
    Contiene un Entry y un Botón para buscar archivos con soporte para comandos de evento.
    """
    def __init__(self, parent, texto_boton="Buscar", titulo="", rel_coords="e",
                 title_dialog="Seleccionar Archivo", initialdir=None, filetypes=None, entry_width=40, command=None):
        
        super().__init__(parent)
        
        # Validamos coordenadas relativas
        self.rel_coords = rel_coords.lower().strip()
        if self.rel_coords not in ["n", "s", "e", "w"]:
            self.rel_coords = "e"

        # Guardamos el comando de evento (callback)
        self._command = command

        # ==========================================
        # 1. CONTENEDOR INTELIGENTE
        # ==========================================
        if titulo and titulo.strip() != '':
            self.box = ttk.LabelFrame(self, text=titulo)
            self.box.pack(fill="both", expand=True, padx=2, pady=2)
        else:
            self.box = self

        # ==========================================
        # 2. CONFIGURACIÓN DEL DIÁLOGO BÁSICO
        # ==========================================
        self.var_ruta = tk.StringVar(value="")
        self._title_dialog = title_dialog
        self._dir_inicial = initialdir if initialdir else os.path.dirname(os.path.abspath(__file__))
        self._tipos = filetypes if filetypes else [
            ("Todos los archivos", "*.*"),
            ("Archivos JSON", "*.json"),
            ("Archivos CSV", "*.csv"),
            ("Archivos de texto", "*.txt")
        ]

        # ==========================================
        # 3. WIDGETS INTERNOS DIRECTAMENTE EN LA CAJA
        # ==========================================
        self.entry = ttk.Entry(self.box, textvariable=self.var_ruta, width=entry_width)
        self.btn = ttk.Button(self.box, text=texto_boton, command=self._abrir_dialogo)

        # ==========================================
        # 4. EMPAQUETADO CARDINAL SIMPLE
        # ==========================================
        if self.rel_coords == "n":
            self.btn.pack(side="top", pady=(2, 0))
            self.entry.pack(side="top", fill="x", expand=True, pady=(0, 2))
        elif self.rel_coords == "s":
            self.entry.pack(side="top", fill="x", expand=True, pady=(2, 0))
            self.btn.pack(side="top", pady=(0, 2))
        elif self.rel_coords == "w":
            self.btn.pack(side="left", padx=(5, 5))
            self.entry.pack(side="left", fill="x", expand=True) 
        else: # "e"
            self.entry.pack(side="left", fill="x", expand=True) 
            self.btn.pack(side="left", padx=(5, 5))
            
    # ■■■■ MÉTODOS PÚBLICOS E INTERNOS ■■■■

    def _abrir_dialogo(self):
        ruta = filedialog.askopenfilename(
            title=self._title_dialog,
            initialdir=self._dir_inicial,
            filetypes=self._tipos
        )
        if ruta:
            self.var_ruta.set(ruta)
            self.entry.xview_moveto(1) # Scroll al final para ver el nombre
            
            # 🔄 ¡MAGIA REACTIVA! Si hay una función vinculada, la disparamos pasándole la ruta
            if self._command and callable(self._command):
                self._command(ruta)

    def set_command(self, nuevo_comando):
        """ Asigna o cambia dinámicamente la función que se ejecuta al seleccionar un archivo. """
        self._command = nuevo_comando

    def get_ruta(self):
        return self.var_ruta.get()

    def set_ruta(self, nueva_ruta):
        self.var_ruta.set(nueva_ruta)    

# █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █
class My_Slide(ttk.Frame):
    """
    Widget compuesto (KISS). Hereda de ttk.Frame (invisible).
    Si se pasa 'texto_label', genera un ttk.LabelFrame interno.
    """
    def __init__(self, parent, tipo_dato=tk.IntVar, tipo_slide="scale", 
                 texto_label='', valor_inicial=5, desde=0, hasta=10, rel_coords="e"):
        
        super().__init__(parent)
        
        self.valor_ini = valor_inicial 
        self.from_ = desde
        self.to_ = hasta
        self.tipo_dato_cls = tipo_dato  
        
        self.rel_coords = rel_coords.lower().strip()
        if self.rel_coords not in ["n", "s", "e", "w"]:
            self.rel_coords = "e"

        # ==========================================
        # 1. CONTENEDOR INTELIGENTE (IGUAL QUE MY_RADIO)
        # ==========================================
        if texto_label and texto_label.strip() != '':
            self.box = ttk.LabelFrame(self, text=texto_label)
            # Se empaqueta llenando el espacio, con un poco de margen interior
            self.box.pack(fill="both", expand=True, padx=2, pady=2)
        else:
            self.box = self

        # ==========================================
        # 2. VARIABLE Y FORMATEO
        # ==========================================
        self.valor_objeto = self.tipo_dato_cls(value=valor_inicial)

        def _formatear(val):
            if self.tipo_dato_cls == tk.DoubleVar:
                return f"{float(val):.2f}"
            else:
                return f"{int(float(val))}"

        # ==========================================
        # 3. WIDGETS INTERNOS DIRECTAMENTE EN LA CAJA
        # ==========================================
        self.lbl_valor = ttk.Label(self.box, text=_formatear(valor_inicial))
        
        tipo_slide_limpio = tipo_slide.lower().strip()
        if tipo_slide_limpio == 'slide':
            self.obj = tk.Scale(
                self.box, from_=desde, to=hasta, 
                variable=self.valor_objeto, orient=tk.HORIZONTAL,
                showvalue=False,
                command=lambda val: self.lbl_valor.config(text=_formatear(val))
            )
        else:
            self.obj = ttk.Scale(
                self.box, from_=desde, to=hasta, 
                variable=self.valor_objeto, orient=tk.HORIZONTAL,
                command=lambda val: self.lbl_valor.config(text=_formatear(val))
            )

        # ==========================================
        # 4. EMPAQUETADO CARDINAL SIMPLE (SIN EXPANSIÓN VERTICAL)
        # ==========================================
        if self.rel_coords == "n":
            self.lbl_valor.pack(side="top", pady=(2, 0))
            self.obj.pack(side="top", fill="x", pady=(0, 2))
        elif self.rel_coords == "s":
            self.obj.pack(side="top", fill="x", pady=(2, 0))
            self.lbl_valor.pack(side="top", pady=(0, 2))
        elif self.rel_coords == "w":
            self.lbl_valor.pack(side="left", padx=(5, 5))
            self.obj.pack(side="left", fill="x", expand=True) # expand solo horizontal
        else: # "e"
            self.obj.pack(side="left", fill="x", expand=True) # expand solo horizontal
            self.lbl_valor.pack(side="left", padx=(5, 5))

        # Propiedad simulada por compatibilidad
        # self.lbl_texto = ttk.Label(self, text="")

    # ■■■■ MÉTODOS PÚBLICOS DE COMUNICACIÓN (INTACTOS) ■■■■
    
    def get_valor(self):
        """ Devuelve el valor del slide en su formato correcto. """
        return self.valor_objeto.get()

    def set_valor(self, valor):
        """ Pone un valor programáticamente y actualiza el label. """
        if self.from_ <= valor <= self.to_: 
            self.valor_objeto.set(valor)
            if self.tipo_dato_cls == tk.DoubleVar:
                self.lbl_valor.config(text=f"{float(valor):.2f}")
            else:
                self.lbl_valor.config(text=f"{int(float(valor))}")

    def reset(self):
        """ Pone el Scale en su valor inicial. """
        if self.valor_ini is not None: 
            self.set_valor(self.valor_ini)

# █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █
class My_Listbox(ttk.Frame):
    """
    Widget compuesto que hereda de Frame. 
    Contiene un Listbox con Scrollbar y, opcionalmente, controles de navegación y estado.
    """
    def __init__(self, parent, datos=None, b_botones=True, b_registro=True, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.b_botones = b_botones
        self.b_registro = b_registro

        # ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ 
        # 1. LISTBOX Y SCROLLBAR (SIEMPRE PRESENTES)
        # ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ 
        self.frm_list = ttk.Frame(self)
        self.frm_list.pack(fill="both", expand=True)
        
        self.scroll = ttk.Scrollbar(self.frm_list, orient="vertical")
        self.listbox = tk.Listbox(self.frm_list, selectmode=tk.SINGLE, yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.listbox.yview)
        
        self.listbox.pack(side="left", fill="both", expand=True)
        self.scroll.pack(side="right", fill="y")
        
        self.listbox.bind("<<ListboxSelect>>", self._actualizar_status)
        
        # ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ 
        # 2. CONTROLES INFERIORES (BOTONES Y/O REGISTRO)
        # ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ 
        # Solo creamos la fila de abajo si al menos uno de los controles fue solicitado
        if self.b_botones or self.b_registro:
            self.frm_bottom = ttk.Frame(self)
            self.frm_bottom.pack(fill="x", pady=(2, 0))
            
            # ■ 1. Empaquetamos los botones a los extremos si fueron solicitados
            if self.b_botones:
                self.btn_first = ttk.Button(self.frm_bottom, text="<<", width=4, command=self._go_first)
                self.btn_prev  = ttk.Button(self.frm_bottom, text="<",  width=4, command=self._go_prev)
                self.btn_next  = ttk.Button(self.frm_bottom, text=">",  width=4, command=self._go_next)
                self.btn_last  = ttk.Button(self.frm_bottom, text=">>", width=4, command=self._go_last)
                
                # Izquierda
                self.btn_first.pack(side="left", padx=(0, 2))
                self.btn_prev.pack(side="left")
                # Derecha
                self.btn_last.pack(side="right")
                self.btn_next.pack(side="right", padx=(0, 2))
            
            # ■ 2. Empaquetamos el centro (Label de estado o Espaciador invisible)
            if self.b_registro:
                self.lbl_status = ttk.Label(self.frm_bottom, text="0 de 0", anchor="center")
                # Al empaquetarlo con expand=True después de los botones, rellena el centro exacto
                self.lbl_status.pack(side="left", fill="both", expand=True)
            elif self.b_botones:
                # Si hay botones pero NO registro, metemos el espaciador para empujar los botones
                lbl_spacer = ttk.Label(self.frm_bottom, text="")
                lbl_spacer.pack(side="left", fill="both", expand=True)
                
        # ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ 
        # CARGA DE DATOS INICIAL
        # ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ 
        if datos is not None:
            self.load_data(datos)

    # ■■■■ MÉTODOS PÚBLICOS ■■■■    
    def load_data(self, datos: list):
        """ Limpia el listbox, inserta nuevos datos y selecciona el primero. """
        self.listbox.delete(0, tk.END)
        for d in datos:
            self.listbox.insert(tk.END, d)
        
        if datos:
            self._seleccionar_indice(0)
        else:
            self._actualizar_status()

    # ■■■■ LÓGICA PRIVADA Y NAVEGACIÓN ■■■■
    def _actualizar_status(self, event=None):
        """ Actualiza el label solo si b_registro es True. """
        if not self.b_registro:
            return
            
        total = self.listbox.size()
        if total == 0:
            self.lbl_status.config(text="0 de 0")
            return
            
        seleccion = self.listbox.curselection()
        actual = (seleccion[0] + 1) if seleccion else 0
            
        self.lbl_status.config(text=f"{actual} de {total}")

    def _seleccionar_indice(self, idx):
        """ Mueve la selección programáticamente y actualiza la vista. """
        total = self.listbox.size()
        if total == 0: return
        
        if idx < 0: idx = 0
        if idx >= total: idx = total - 1
        
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(idx)
        self.listbox.activate(idx)
        self.listbox.see(idx) # El scroll persigue al registro
        
        self._actualizar_status()

    # ■ Funciones de navegación (Seguras de llamar aunque los botones no existan)
    def _go_first(self): self._seleccionar_indice(0)
    def _go_last(self):  self._seleccionar_indice(self.listbox.size() - 1)
    def _go_prev(self):
        sel = self.listbox.curselection()
        if sel: self._seleccionar_indice(sel[0] - 1)
    def _go_next(self):
        sel = self.listbox.curselection()
        if sel: 
            self._seleccionar_indice(sel[0] + 1)
        elif self.listbox.size() > 0:
            self._seleccionar_indice(0)


# █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █
class My_Tree(ttk.Frame):
    """
    Widget compuesto (Frame).
    Contiene un Treeview, botones de navegación (opcionales) y un formulario dinámico 
    autogenerado a partir de d_textos, todo integrado en un único bloque sólido.
    """
    def __init__(self, parent, 
                        titulo="", 
                        cabeceras=None, 
                        datos=None, 
                        b_botones=True, 
                        b_registro=True, 
                        d_textos=None, 
                        **kwargs):
        super().__init__(parent, **kwargs)
        
        self.cabeceras = list(cabeceras) if cabeceras else []
        self.datos = datos if datos else []
        self.b_botones = b_botones
        self.b_registro = b_registro
        self.d_textos = d_textos
        
        self.dicc_entries = {}  # Guardará { indice_cabecera: widget_Entry }

        # ==========================================
        # 1. TÍTULO (OPCIONAL)
        # ==========================================
        if titulo:
            self.lbl_titulo = ttk.Label(self, text=titulo, font=("Arial", 10, "bold"))
            self.lbl_titulo.pack(side="top", fill="x", pady=(0, 5))
            
        # ==========================================
        # 2. TREEVIEW Y SCROLL
        # ==========================================
        self.frm_tree = ttk.Frame(self)
        self.frm_tree.pack(fill="both", expand=True)
        
        self.scroll = ttk.Scrollbar(self.frm_tree, orient="vertical")
        self.tree = ttk.Treeview(self.frm_tree, yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.tree.yview)
        
        self.tree.pack(side="left", fill="both", expand=True)
        self.scroll.pack(side="right", fill="y")
        
        self.tree.bind("<<TreeviewSelect>>", self._al_seleccionar)
        
        # ==========================================
        # 3. CONTROLES INFERIORES CENTRADOS
        # ==========================================
        if self.b_botones or self.b_registro:
            self.frm_bottom = ttk.Frame(self)
            self.frm_bottom.pack(fill="x", pady=(5, 0))
            
            # Sub-frame para mantener todo agrupado y centrado
            self.frm_center = ttk.Frame(self.frm_bottom)
            self.frm_center.pack(anchor="center")
            
            if self.b_botones:
                self.btn_first = ttk.Button(self.frm_center, text="<<", width=4, command=self._go_first)
                self.btn_prev  = ttk.Button(self.frm_center, text="<",  width=4, command=self._go_prev)
                self.btn_next  = ttk.Button(self.frm_center, text=">",  width=4, command=self._go_next)
                self.btn_last  = ttk.Button(self.frm_center, text=">>", width=4, command=self._go_last)
                
                # Empaquetamos los de la izquierda
                self.btn_first.pack(side="left", padx=(0, 2))
                self.btn_prev.pack(side="left")
            
            if self.b_registro:
                self.lbl_status = ttk.Label(self.frm_center, text="0 de 0", anchor="center")
                # Solo aplicamos el padx=15 si hay botones empujando a los lados
                pad_x = 15 if self.b_botones else 0
                self.lbl_status.pack(side="left", padx=pad_x)
                
            if self.b_botones:
                # Empaquetamos los de la derecha
                self.btn_next.pack(side="left")
                self.btn_last.pack(side="left", padx=(2, 0))

        # ==========================================
        # 4. FORMULARIO INTEGRADO (Contenedor)
        # ==========================================
        self.frm_form = ttk.Frame(self)
        self.frm_form.pack(fill="x", pady=(10, 0))

        # ==========================================
        # CONFIGURACIÓN INICIAL DE COLUMNAS Y DATOS
        # ==========================================
        self._configurar_columnas()
        self._construir_formulario()
        if self.datos:
            self.load_data(self.datos)

    # ■■■■ MÉTODOS PÚBLICOS ■■■■

    def set_feature_names(self, cabeceras):
        """ Valida y asigna nuevas cabeceras """
        if not isinstance(cabeceras, (list, tuple)):
            raise ValueError("Las cabeceras deben ser una lista o tupla.")
        if not all(isinstance(c, str) for c in cabeceras):
            raise ValueError("Todos los elementos de las cabeceras deben ser strings.")
            
        self.cabeceras = list(cabeceras)
        self._configurar_columnas()
        self._construir_formulario()

    def load_data(self, datos: list):
        """ Limpia e inserta datos. """
        self.datos = datos if datos else []
        self._configurar_columnas()  
        self._construir_formulario() 
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for d in self.datos:
            valores = d if isinstance(d, (list, tuple)) else (d,)
            self.tree.insert("", tk.END, values=valores)
            
        self._actualizar_status()

    def get_textos(self) -> list:
        """ 
        Devuelve un array con los valores actuales de los Entry.
        Garantiza que el orden sea exactamente el de lectura de tu matriz (fila por fila)
        y devuelve únicamente los campos que tengan un registro real.
        """
        if self.d_textos is None: return []
        
        cab_efectivas = self._obtener_cabeceras_efectivas()
        d_trabajo = self._obtener_d_trabajo(cab_efectivas)

        valores = []
        
        # Recorremos la matriz fila por fila, elemento por elemento
        for r, row_data in enumerate(d_trabajo):
            for c, val_crudo in enumerate(row_data):
                val = self._resolver_indice(val_crudo, cab_efectivas)
                
                if isinstance(val, int) and val in self.dicc_entries:
                    valores.append(self.dicc_entries[val].get())
                    
        return valores
                    
        return valores

    # ■■■■ LÓGICA PRIVADA ■■■■

    def _construir_formulario(self):
        """ Construye internamente el Grid de Labels y Entries basándose en la MATRIZ d_textos. """
        if self.d_textos is None: return
            
        cab_efectivas = self._obtener_cabeceras_efectivas()
        if not cab_efectivas: return 
            
        # Limpieza por si venimos de un repintado dinámico
        for widget in self.frm_form.winfo_children():
            widget.destroy()
        self.dicc_entries.clear()

        d_trabajo = self._obtener_d_trabajo(cab_efectivas)
        max_row, max_col = self._obtener_dimensiones(d_trabajo)
        
        # Configuramos los pesos de las columnas de la rejilla interna
        for c in range((max_col + 1) * 2):
            self.frm_form.columnconfigure(c, weight=1 if c % 2 != 0 else 0)

        # Iteramos de forma limpia por índice y contenido de la matriz
        for r, row_data in enumerate(d_trabajo):
            last_entry = None  
            
            for c, val_crudo in enumerate(row_data):
                val = self._resolver_indice(val_crudo, cab_efectivas)
                col_real = c * 2 
                
                if isinstance(val, int) and 0 <= val < len(cab_efectivas):
                    lbl = ttk.Label(self.frm_form, text=f"{cab_efectivas[val]}:")
                    lbl.grid(row=r, column=col_real, sticky="e", padx=(5, 2), pady=2)
                    
                    ent = ttk.Entry(self.frm_form, state="readonly")
                    ent.grid(row=r, column=col_real + 1, sticky="we", padx=(0, 5), pady=2)
                    
                    self.dicc_entries[val] = ent 
                    last_entry = ent  
                    
                elif val == '+':
                    if last_entry:
                        # Hacemos colspan expandiendo el último Entry registrado de esta fila
                        span_actual = last_entry.grid_info().get('columnspan', 1)
                        last_entry.grid_configure(columnspan=span_actual + 2)


    def _al_seleccionar(self, event=None):
        """ Al clicar un registro, vuelca los datos en los Entries. """
        self._actualizar_status()
        
        seleccion = self.tree.selection()
        if not seleccion or not self.dicc_entries: return
        
        valores = self.tree.item(seleccion[0])['values']
        
        for idx, ent in self.dicc_entries.items():
            if idx < len(valores):
                ent.config(state="normal")
                ent.delete(0, tk.END)
                ent.insert(0, str(valores[idx]))
                ent.config(state="readonly")

    def _actualizar_status(self):
        if not self.b_registro: return
        total = len(self.tree.get_children())
        if total == 0:
            self.lbl_status.config(text="0 de 0")
            return
        seleccion = self.tree.selection()
        if seleccion:
            indice = self.tree.index(seleccion[0]) + 1
            self.lbl_status.config(text=f"{indice} de {total}")
        else:
            self.lbl_status.config(text=f"0 de {total}")

    # (Lógica de _go_first, _go_last, _go_prev, _go_next omitida para no ser redundante, 
    # usa el mismo motor de índices que My_Listbox pero aplicado a self.tree.get_children())
    def _seleccionar_indice(self, idx):
        hijos = self.tree.get_children()
        if not hijos: return
        idx = max(0, min(idx, len(hijos) - 1))
        item_id = hijos[idx]
        self.tree.selection_set(item_id)
        self.tree.focus(item_id)
        self.tree.see(item_id)
        self._al_seleccionar()

    def _go_first(self): self._seleccionar_indice(0)
    def _go_last(self): self._seleccionar_indice(len(self.tree.get_children()) - 1)
    def _go_prev(self):
        sel = self.tree.selection()
        if sel: self._seleccionar_indice(self.tree.index(sel[0]) - 1)
    def _go_next(self):
        sel = self.tree.selection()
        if sel: self._seleccionar_indice(self.tree.index(sel[0]) + 1)
        elif self.tree.get_children(): self._seleccionar_indice(0)


    # ■■■■ LÓGICA PRIVADA PARA UI ■■■■

    def _resolver_indice(self, valor, cab_efectivas):
        """ Traduce el valor tolerando mayúsculas y tildes. """
        if isinstance(valor, int): return valor
        if isinstance(valor, str):
            val_str = valor.strip().lower()
            if val_str in ['+', 'x']: return '+'
            if val_str in ['_', '']: return '_'
                
            import unicodedata
            def quitar_tildes(s):
                return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
                
            val_norm = quitar_tildes(val_str)
            for i, cab in enumerate(cab_efectivas):
                if quitar_tildes(str(cab).strip().lower()) == val_norm:
                    return i
        return '_'

    def _configurar_columnas(self):
        """ Aplica las reglas visuales a las columnas del TreeView """
        cols_a_mostrar = self._obtener_cabeceras_efectivas()
        self.tree.config(columns=tuple(cols_a_mostrar))
        
        if not cols_a_mostrar:
            self.tree.config(show="") 
        else:
            self.tree.config(show="headings")
            for i, cab in enumerate(cols_a_mostrar):
                self.tree.heading(cols_a_mostrar[i], text=cab)
                self.tree.column(cols_a_mostrar[i], width=100, anchor="w")

    def _obtener_dimensiones(self, d_trabajo):
        """ Devuelve las dimensiones máximas (max_row, max_col) de la matriz de disposición. """
        if not d_trabajo: 
            return 0, 0
        max_row = len(d_trabajo) - 1
        max_col = max((len(row) for row in d_trabajo), default=0) - 1
        return max_row, max_col
    
    def _obtener_d_trabajo(self, cab_efectivas):
        """ Retorna la matriz de trabajo. Si es {} o [], genera una secuencia hacia abajo. """
        if self.d_textos == {} or self.d_textos == []:
            return [[i] for i in range(len(cab_efectivas))]
        return self.d_textos
    
    def _obtener_cabeceras_efectivas(self):
        """ Decide si usar las cabeceras dadas o generar 'col0', 'col1'... """
        if self.cabeceras:
            return self.cabeceras
        elif self.datos and len(self.datos) > 0:
            num_cols = len(self.datos[0]) if isinstance(self.datos[0], (list, tuple)) else 1
            return [f"col{i}" for i in range(num_cols)]
        return []

# █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █
class My_TreeCSV(ttk.Frame):
    """
    Macro-Widget compuesto. Hereda de ttk.Frame (o ttk.LabelFrame si hay título).
    Contiene un My_FileDialog en la parte superior y un My_Tree en la inferior.
    Carga automáticamente el CSV seleccionado en el TreeView.
    """
    def __init__(self, parent, 
                titulo="", 
                texto_boton="Buscar CSV",   
                initialdir=None, 
                entry_width=40,
                b_botones=True, b_registro=True, d_textos=None, **kwargs):
        
        super().__init__(parent, **kwargs)

        # ==========================================
        # 1. CONTENEDOR INTELIGENTE
        # ==========================================
        if titulo and titulo.strip() != '':
            self.box = ttk.LabelFrame(self, text=titulo)
            self.box.pack(fill="both", expand=True, padx=2, pady=2)
        else:
            self.box = self

        # Por defecto, filtramos por CSV
        # if not filetypes:
        #     filetypes = [("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]

        # ==========================================
        # 2. FILE DIALOG (Panel Superior)
        # ==========================================
        self.file_dialog = My_FileDialog(
            parent=self.box,
            texto_boton=texto_boton,
            titulo="", 
            rel_coords="e",
            title_dialog="Seleccionar Archivo CSV",
            initialdir=initialdir,
            filetypes=[("Archivos CSV","*.csv")],
            entry_width=entry_width,
            command=self._cargar_csv_automatico
        )
        # Empaquetamos arriba, sin expandir en vertical
        self.file_dialog.pack(side="top", fill="x", padx=5, pady=(5, 5))

        # ==========================================
        # 3. TREEVIEW (Panel Inferior)
        # ==========================================
        self.tree = My_Tree(
            parent=self.box,
            titulo=titulo, 
            b_botones=b_botones,
            b_registro=b_registro,
            d_textos=d_textos
        )
        # Empaquetamos debajo, forzando a expandirse en todas direcciones
        self.tree.pack(side="top", fill="both", expand=True, padx=5, pady=(0, 5))

    # ■■■■ LÓGICA INTERNA AUTOMÁTICA ■■■■

    def _cargar_csv_automatico(self, ruta_fichero):
        """ Se dispara solo cuando el usuario selecciona un archivo en el FileDialog. """
        if not ruta_fichero: 
            return 
            
        import pandas as pd
        import csv
        from tkinter import messagebox

        try:
            # 1. Detectamos cabecera
            tiene_cabecera = True
            with open(ruta_fichero, 'r', encoding='utf-8') as f:
                muestra = f.read(2048)
                try:
                    tiene_cabecera = csv.Sniffer().has_header(muestra)
                except csv.Error:
                    pass
            
            # 2. Leemos con Pandas
            if tiene_cabecera:
                df = pd.read_csv(ruta_fichero)
                nuevas_cabeceras = df.columns.tolist()
            else:
                df = pd.read_csv(ruta_fichero, header=None)
                nuevas_cabeceras = [f"col{i}" for i in range(df.shape[1])]
            
            # 3. Inyectamos
            nuevos_datos = df.values.tolist()
            self.tree.set_feature_names(nuevas_cabeceras)
            self.tree.load_data(nuevos_datos)
            
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error de lectura", f"No se pudo leer el archivo CSV.\n\nDetalle: {e}")

    # ■■■■ MÉTODOS PÚBLICOS DE PUENTE ■■■■
    # Exponemos los métodos clave para que interactúes con él fácilmente desde fuera
    
    def get_textos(self):
        """ Devuelve los textos del formulario (si lo hay). """
        return self.tree.get_textos()
        
    def get_ruta(self):
        """ Devuelve la ruta seleccionada. """
        return self.file_dialog.get_ruta()


# █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █
class My_Radio(ttk.Frame):
    """
    Crea un componente My_Radio con Label(titulo) en un LabelFrame.
    Gestiona su propia variable de control automáticamente.

    - dicc_radio: array de diccionarios [{'texto': 'op1', 'value': 1}, ...]
    - orientacion: "vertical" (por defecto) u "horizontal"
    - titulo: Si entra titulo se crea un Titulo en el LabelFrame.
    """
    def __init__(self, parent, dicc_radio, titulo="", orientacion="vertical", **kwargs):
        # Iniciamos el Frame base (transparente y sin bordes por naturaleza)
        super().__init__(parent, **kwargs)

        self.dicc_radio = dicc_radio
        self.radios = []

        # ==========================================
        # 1. CONTENEDOR INTELIGENTE
        # ==========================================
        if titulo:
            # Si hay título, creamos la caja nativa con borde y texto
            self.box = ttk.LabelFrame(self, text=titulo)
            self.box.pack(fill="both", expand=True)
        else:
            # Si no hay título, el contenedor será este mismo Frame invisible
            self.box = self

        # ==========================================
        # 2. DETECTOR AUTOMÁTICO DE VARIABLE
        # ==========================================
        if self.dicc_radio and len(self.dicc_radio) > 0:
            primer_valor = self.dicc_radio[0].get("value", "")
            
            if isinstance(primer_valor, bool):
                self.var = tk.BooleanVar()
            elif isinstance(primer_valor, int):
                self.var = tk.IntVar()
            elif isinstance(primer_valor, float):
                self.var = tk.DoubleVar()
            else:
                self.var = tk.StringVar()
            
            # Seleccionamos la primera opción por defecto
            self.var.set(primer_valor)
        else:
            self.var = tk.StringVar()

        # ==========================================
        # 3. CONSTRUCCIÓN DE RADIOBUTTONS
        # ==========================================
        for item in self.dicc_radio:
            texto = item.get("texto", "Opción")
            valor = item.get("value", texto)
            
            # ¡OJO! Se empaquetan dentro de 'self.box'
            rb = tk.Radiobutton(self.box, text=texto, value=valor, variable=self.var)
            
            if orientacion.lower() == "horizontal":
                rb.pack(side="left", padx=(5, 10), pady=5)
            else:
                rb.pack(side="top", anchor="w", padx=5, pady=2)
                
            self.radios.append(rb)

    # ■■■■ MÉTODOS PÚBLICOS FUNCIONALES ■■■■
    
    def get_valor(self):
        """ Devuelve el valor numérico/texto de la opción seleccionada. """
        return self.var.get()

    def set_valor(self, valor):
        """ Cambia la selección programáticamente. """
        self.var.set(valor)

    def set_command(self, comando):
        """ 
        Asigna una función que se disparará automáticamente al cambiar de opción. 
        Ejemplo: mi_radio.set_command(lambda: print(mi_radio.get_valor()))
        """
        for rb in self.radios:
            rb.config(command=comando)
    

# █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █
class Familia:
    def __init__(self):
        self.d_family = {}  # { 'nombre': [widgets] }

    def __call__(self, nombre_familia: str = None):
        """ 
        Permite usar la instancia como una función: F() o F('nombre')
        Llama internamente a la visualización.
        """
        self.view(nombre_familia)

    def view(self, nombre_familia: str = None):
        """
        Lógica de impresión en consola.
        """
        if nombre_familia:
            if nombre_familia in self.d_family:
                print(f"\n[ DETALLE FAMILIA: '{nombre_familia}' ]")
                print(f"{'Índice':<8} | {'Tipo':<15} | {'Nombre ID':<15} | {'Texto/Valor'}")
                print("-" * 65)
                for i, w in enumerate(self.d_family[nombre_familia]):
                    tipo = type(w).__name__
                    nombre_id = w.winfo_name()
                    
                    info = ""
                    try:
                        if isinstance(w, (tk.Button, tk.Label, tk.Checkbutton)):
                            info = w.cget("text")
                        elif isinstance(w, tk.Entry):
                            info = w.get()
                    except:
                        info = "n/a"
                    
                    info = str(w)

                    print(f"{i:<8} | {tipo:<15} | {nombre_id:<15} | {info}")
            else:
                print(f"⚠️ La familia '{nombre_familia}' no existe.")
        else:
            print("\n[ RESUMEN DE TODAS LAS FAMILIAS ]")
            print(f"{'Nombre Familia':<20} | {'Nº Widgets'}")
            print("-" * 45)
            for fam, lista in self.d_family.items():
                print(f"{fam:<20} | {len(lista)}")

    # ■■■■ Crea / Elimina lista de widgets en una 'nombre_familia'
    def formar(self, nombre_familia: str, widgets: list = [], b_del: bool = False):
        if nombre_familia not in self.d_family and not b_del:
            self.d_family[nombre_familia] = []
        
        if b_del:
            """ Borrar """
            if nombre_familia in self.d_family:
                for w in widgets:
                    if w in self.d_family[nombre_familia]:
                        self.d_family[nombre_familia].remove(w)
        else:
            """ Crear """
            for w in widgets:
                if w not in self.d_family[nombre_familia]:
                    self.d_family[nombre_familia].append(w)
            pass
        pass
        self.view(nombre_familia)
    
    # ■■■■ Devuelve los widget de la familia  
    def familiares(self, nombre_familia: str) -> list:
        return self.d_family.get(nombre_familia, [])

    # ■■■■ Pone estilo comun a todos los widget de la familia.
    def style_family(self, nombre_familia: str, **kwargs):
        for w in self.familiares(nombre_familia):
            try:
                w.config(**kwargs)
            except tk.TclError:
                pass

    # ■■■■ Activa / Des-activa los widget de 'nombre_familia'
    def active_family(self, nombre_familia: str, activa: bool = True):
        estado = "normal" if activa else "disabled"
        for w in self.familiares(nombre_familia):
            try:
                w.config(state=estado)
            except tk.TclError:
                pass 

    def clean_family(self, nombre_familia: str):
        for w in self.familiares(nombre_familia):
            if isinstance(w, tk.Entry):
                w.delete(0, tk.END)
            elif isinstance(w, tk.Text):
                w.delete("1.0", tk.END)
            elif isinstance(w, tk.Listbox):
                w.delete(0, tk.END)

# ██████████████████████████████████████████
# ██       EJEMPLO DE USO DE FAMILIA      ██
# ██████████████████████████████████████████
# if __name__ == "__main__":
#     root = tk.Tk()
#     F = Familia()
#     Frame1 = tk.Frame(root, background='#111111')
#     Frame1.pack()
#     btn_add = tk.Button(Frame1, text="Añadir")
#     btn_add.pack()
#     btn_del = tk.Button(Frame1, text="Borrar")
#     btn_del.pack()
#     txt_nom = tk.Entry(root)
#     txt_nom.pack(padx=10, pady=10)
#     txt_nom.insert(0, "Juan")
#     # Registro
#     F.formar('botones_control', [ btn_add , btn_del ])
#     F.formar('entradas', [txt_nom])
#     F.familiares('botones_control')[0].config(bg="lightgray")
#     # --- PRUEBAS DE LLAMADA DIRECTA ---
#     F('botones_control')        # Esto funciona gracias a __call__
#     F()                         # Muestra el resumen

#     root.mainloop() # Cerramos la ventana de test

# █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █
# █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █
# █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █
class Nivel_2:
    """ 
    • Crea un Frame Formulario e inserta los widgets con un dibujo ( draw() )
    • Mete los elementoes en level_1 por lo que NO tienes que definir la fila en el momento de la creación.
    • De esta forma al definir el objeto puedo pasarle simplemente frame (level_1)
      dibujas el formulario con draw y ahí se define la posición definitiva de los widgets. 
    • Es mas cuadrado que row_fix porque define cada espacio.
    """
    def __init__(self,  contenedor, 
                        shape=None,
                        title="Formulario", 
                        ancho=300, alto=450, 
                        padx=5, pady=5 ):
        self.contenedor = contenedor
        """ contenedor del Frame que vamos a crear. """
        self.padx = padx
        self.pady = pady
        """ Distancia horizontal y vertical entre widgets, y filas vacías y columnas vacías. """
        self.level_1 = tk.Frame(self.contenedor)
        """ frame contenedor principal. se obtiene con frame()  """
        self.level_1.pack(fill="both", expand=True, padx=self.padx, pady=pady)
        self.level_2 = {}      # Diccionario de filas existentes (metadatos)
        """ diccionario de frames fila contenidos en level_1  """
        self.filas = None
        """ Numero de filas del frame """        
        self.columnas = None   
        """ Numero de columnas del frame """        
        self._draw_map = []    
        """ Mapa de posiciones tras draw() """        
        self.family = Familia()
        """ Clase familia para hacer agrupaciones de widgets custom """        
        
        # ■ ■  Procesar shape "filasxcolumnas" 
        if shape is not None:
            try:
                filas_str, cols_str = shape.lower().split('x')
                self.filas = int(filas_str.strip())
                self.columnas = int(cols_str.strip())
                #  [6] * 5 = [6,6,6,6,6] ... lo uso como validación: 
                cols_by_fila = [self.columnas] * self.filas
            except ValueError:
                raise ValueError(f"Formato de shape inválido: '{shape}'. Use formato 'filasxcolumnas' (ej: '4x6')")
        pass        
        # Construye level_1 y level_2
        if self.filas or (isinstance(cols_by_fila, list) and len(cols_by_fila) > 0):
            self._construye_estructura_levels(cols_by_fila)

    def _construye_estructura_levels(self, cols_config):
        """
        Configura level_1 como grid maestro.
        level_2[i] registra metadatos de cada fila.
        """
        for i, num_cols in enumerate(cols_config):
            if num_cols and num_cols > 0:
                self.level_1.grid_rowconfigure(i, weight=0, minsize=self.pady)
                self.level_2[i] = {'row': i, 'cols': num_cols, 'type': 'active'}
            else:
                # Fila vacía: dejamos espacio reservado
                self.level_1.grid_rowconfigure(i, weight=0, minsize=self.pady * 2)
                self.level_2[i] = {'row': i, 'cols': 0, 'type': 'spacer'}
        
        # Configurar columnas en level_1
        max_cols = max((c for c in cols_config if isinstance(c, int)), default=0)
        for col in range(max_cols):
            self.level_1.grid_columnconfigure(col, weight=1)
    
    @property
    def frame(self):
        return self.level_1 if self.level_1 else None

    def row(self, index):
        """
        ■ Siempre devuelve level_1.
        Todos los widgets se crean como hijos del mismo contenedor.
        El posicionamiento real lo hace draw().
        """
        return self.level_2.get(index)

    def _add(self, widget, column, row=0, **kwargs):
        """
        ■ posiciona en level_1.
        """
        if 'sticky' not in kwargs:
            kwargs['sticky'] = "we"
        widget.grid(in_=self.level_1, row=row, column=column, **kwargs)
        return widget

    def _set_row(self, row, *items, **kwargs):
        """
        ■ posiciona widgets en una fila específica de level_1.
        """
        if row not in self.level_2:
            raise ValueError(f"La fila {row} no existe.")
        added_widgets = []
        for column, item in enumerate(items):
            if self._is_empty_cell(item):
                continue
            widget = item
            widget.grid_forget()
            widget.grid(in_=self.level_1, row=row, column=column, sticky="we", **kwargs)
            added_widgets.append(widget)
        return added_widgets
    
    def _is_empty_cell(self, item):
        return item is None or item == "_" or item == '-' 
    
    def draw(self, matrix):
        """
        • Recibe una matriz de widgets (todos hijos de level_1).
        • La posición en la matriz PREVALECE sobre cualquier grid anterior.
        • Guarda un mapa interno self._draw_map con la situación final.
        """
        self._draw_map = []
        try:
            for row_idx, row_data in enumerate(matrix):
                if self._skip_row(row_data, row_idx):
                    continue
                pass
                col_idx = 0
                placed = []     # Tracking interno para colspan
                for item in row_data:
                    if self._is_empty_cell(item):
                        placed.append(self._celda_vacia(row_idx, col_idx))
                    elif item == "+":
                        self._colspan(placed)
                    else:
                        # VALIDACIÓN DE TIPO
                        # Nota: Cambia 'ClaseBaseWidget' por la clase real de tu framework 
                        # (ej. tk.Widget, QWidget, o tu propia clase padre).
                        if not isinstance(item, tk.Widget):
                            # raise TypeError(
                            #     f"Tipo de dato inválido en fila {row_idx}, columna {col_idx}. "
                            #     f"Se esperaba un Widget, pero se recibió: {type(item).__name__} (Valor: {item})"
                            # )
                            continue
                        
                        placed.append(self._widget_real(item, row_idx, col_idx))
                    col_idx += 1
            return self
        except TypeError as te:
            # Aquí capturamos el error de tipo que lanzamos arriba (o cualquier otro TypeError)
            print(f"[Error de Tipo en draw]: {te}")
            # Puedes decidir si quieres silenciar el error, registrarlo en un log, o relanzarlo:
            raise 
        except Exception as e:
            # Captura de seguridad para cualquier otro error inesperado (ej. matrix no es iterable)
            print(f"[Error Inesperado en draw]: Ha ocurrido un fallo general: {e}")
            raise

    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■ 
    # ■ MÉTODOS MODULARES (KISS)
    # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■ 

    def _skip_row(self, row_data, row_idx):
        """ ■ Decide si una fila del matrix debe saltarse."""
        if row_data is None or (isinstance(row_data, (list, tuple)) and len(row_data) == 0):
            return True
        if not isinstance(row_data, (list, tuple)):
            return True
        if row_idx not in self.level_2:
            raise IndexError(
                f"La fila {row_idx} no existe en la estructura. "
                f"Filas disponibles: 0..{self.filas-1}."
            )
        if self.level_2[row_idx]['type'] == 'spacer':
            return True
        return False

    def _celda_vacia(self, row_idx, col_idx):
        """ ■ Crea un frame vacío, lo posiciona y registra el tracking."""
        empty_frame = tk.Frame(self.level_1, width=self.padx)
        empty_frame.grid(in_=self.level_1, row=row_idx, column=col_idx, sticky="we")

        self._draw_map.append({
            'fila': row_idx, 'columna': col_idx,
            'widget': empty_frame, 'tipo': 'empty', 'span': 1
        })
        return {'type': 'empty', 'widget': empty_frame, 'col': col_idx, 'span': 1}

    def _colspan(self, placed):
        """ ■ Extiende el span del último widget real a la izquierda."""
        target = None
        target_pos = None

        for k in range(len(placed) - 1, -1, -1):
            p = placed[k]
            if p['type'] == 'widget':
                target = p['widget']
                target_pos = k
                break
            elif p['type'] == 'empty':
                break

        if target is not None:
            new_span = placed[target_pos].get('span', 1) + 1
            placed[target_pos]['span'] = new_span
            target.grid_configure(columnspan=new_span)

            for m in self._draw_map:
                if m['widget'] is target:
                    m['span'] = new_span
                    break

    def _widget_real(self, item, row_idx, col_idx):
        """ ■ Posiciona un widget real en el grid, registra el tracking y automatiza pesos."""
        item.grid_forget()
        
        comportamiento_sticky = "we"
        
        # Validación limpia usando isinstance 
        if isinstance(item, (My_Tree, My_TreeCSV, My_Listbox, tk.Listbox, ttk.Treeview, tk.Text, tk.Canvas)):
            comportamiento_sticky = "nsew"
            
            # ■■ ¡LA MAGIA DE LA AUTOMATIZACIÓN! ■■
            # Si el widget es expandible, le damos peso automáticamente a su fila
            self.level_1.rowconfigure(row_idx, weight=1)

        item.grid(in_=self.level_1, row=row_idx, column=col_idx, sticky=comportamiento_sticky)

        self._draw_map.append({
            'fila': row_idx, 'columna': col_idx,
            'widget': item, 'tipo': 'widget', 'span': 1
        })
        return {'type': 'widget', 'widget': item, 'col': col_idx, 'span': 1}

    # ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■  
    # ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■  
    # ■■■■■■■ WIDGETS CUSTOM
    # ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■  
    # ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■ ■■■  
    def my_fileDialog(self, texto_boton="Buscar", titulo="", rel_coords="e", 
                      title_dialog="Seleccionar Archivo", initialdir=None, filetypes=None, 
                      entry_width=40, command=None):
        """
        Crea un My_FileDialog compacto.
        Si se le pasa un 'titulo', dibuja un LabelFrame; si no, es invisible.
        """
        file_dialog = My_FileDialog(
            parent=self.frame,
            texto_boton=texto_boton,
            titulo=titulo,
            rel_coords=rel_coords,
            title_dialog=title_dialog,
            initialdir=initialdir,
            filetypes=filetypes,
            entry_width=entry_width,
            command = command
        )
        return file_dialog
    
    def my_slide(self, titulo= "—■—",desde= 0,hasta= 20,valor_inicial= 5,tipo_slide= "scale",
                        tipo_dato= tk.IntVar,
                        rel_coords='w'
                        ):
        """
        Crea un objeto My_Slide(clase interna) con sus widgets asociados ( lbl_texto , slide, lbl_valor).
         • tipo_slide: 'scale' (ttk.Scale) o 'slide' (tk.Scale). El tipo de control que se usará para el slide. 'scale' es más moderno, 'slide' es más clásico.
         • tipo_dato: tk.IntVar, tk.DoubleVar o tk.BooleanVar. El tipo de variable de control que se usará para almacenar el valor del slide. Esto afecta el formato del valor mostrado en lbl_valor.
         • texto: El texto que se mostrará en el label del slide. 
         • rel_coords: es una tupla de dos elementos.
                      representan la posición relativa de los widgets no slide ,label y valor en ese orden.
                      pej: (w,e): label w, valor e; (w,w): label w concatenado valor e + widget
                      (n,e): label n, valor e(ocupa 2 filas )
         """                
        slide = My_Slide(
            parent = self.frame,    
            texto_label= titulo,
            desde=desde,
            hasta=hasta,
            valor_inicial=valor_inicial, 
            tipo_slide=tipo_slide,
            tipo_dato=tk.IntVar,
            rel_coords=rel_coords                
        )
        # Devolvemos los widgets para que el usuario los distribuya en la matriz            
        # return slide.lbl_texto, slide.obj, slide.lbl_valor
        return slide

    def my_listbox(self, datos=None, b_botones=True, b_registro=True):
        """
        Instancia y devuelve el componente My_Listbox, el cual ya es un Frame.
        """
        # Se lo asignamos directamente al grid (self.frame, que es level_1)
        listbox = My_Listbox(parent=self.frame, 
                            datos=datos, 
                            b_botones=b_botones, 
                            b_registro=b_registro)
        # Devolvemos el propio objeto, que es un Frame y será procesado perfectamente por draw()
        return listbox
    
    def my_tree(self, titulo="", cabeceras=None, datos=None, b_botones=True, b_registro=True, d_textos=None):
        """
        Crea un componente TreeView de ttk con opciones b_botones / b_registro /  b_textos
        """
        treeview = My_Tree( parent=self.frame,
                                titulo=titulo, 
                                cabeceras=cabeceras, 
                                datos=datos,
                                d_textos=d_textos,
                                b_botones=b_botones, b_registro=b_registro
        )
        return treeview

    def my_radio(self, dicc_radio, titulo="", orientacion="vertical"):
        """
        Crea un componente My_Radio.
        - dicc_radio: array de diccionarios [{'texto': 'op1', 'value': 1}, ...]
        - orientacion: "vertical" (por defecto) u "horizontal"
        """
        radio = My_Radio(
            parent=self.frame,
            dicc_radio=dicc_radio,
            titulo=titulo,
            orientacion=orientacion
        )
        return radio

    def my_tree_csv(self, titulo="", 
                    texto_boton="Buscar CSV", rel_coords_fd="e", title_dialog="Seleccionar Archivo", 
                    initialdir=None, filetypes=None, entry_width=40,
                    cabeceras=None, datos=None, b_botones=True, b_registro=True, d_textos=None):
        """
        Crea un Macro-Componente: FileDialog + TreeView.
        Carga automáticamente el CSV seleccionado en la tabla y genera el formulario.
        """
        nuevo_tree_csv = My_TreeCSV(
            parent=self.frame,
            titulo=titulo,
            texto_boton=texto_boton,
            # rel_coords_fd=rel_coords_fd,
            # title_dialog=title_dialog,
            initialdir=initialdir,
            # filetypes=filetypes,
            entry_width=entry_width,
            # cabeceras=cabeceras,
            # datos=datos,
            b_botones=b_botones,
            b_registro=b_registro,
            d_textos=d_textos
        )
        return nuevo_tree_csv


# ██████████████████████████████████████████
# ██       EJEMPLO DE USO DE NIVEL_2      ██
# ██████████████████████████████████████████
# if __name__ == "__main__":
#     root = tk.Tk()
#     # root.geometry("800x300")
#     # ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ 
#     # Estructura: 
#     F1 = Nivel_2(root, shape="5x6", padx=15, pady=7)
#     print(f"Filas: {F1.filas}, Columnas: {F1.columnas}")
#     # ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ 
#     # ■ Todos los widgets se crean en level_1 (frame devuelve level_1 siempre)
#     # ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ 
#     lbl_nom  = tk.Label(F1.frame, text='Nombre: ', anchor='w')
#     txt_nom  = tk.Entry(F1.frame)
#     lbl_ape1 = tk.Label(F1.frame, text='Apellido1: ')
#     txt_ape1 = tk.Entry(F1.frame)
#     lbl_ape2 = tk.Label(F1.frame, text='Apellido2: ')
#     txt_ape2 = tk.Entry(F1.frame)
#     btn_add = tk.Button(F1.frame, text="Añadir")
#     btn_upt = tk.Button(F1.frame, text="Actualiza")
#     btn_del = tk.Button(F1.frame, text="Borrar")
#     scrollbar = tk.Scrollbar(F1.frame, orient=tk.VERTICAL)
#     listbox = tk.Listbox(F1.frame, yscrollcommand=scrollbar.set, selectmode=tk.SINGLE)
#     lbl_sc = tk.Label(F1.frame, text='Slide Val: ')
#     var_sc = tk.DoubleVar(value=5)
#     scale = tk.Scale(F1.frame, from_=0, to=10, resolution=1, variable=var_sc, orient=tk.HORIZONTAL, length=150, font=('Arial', 8))
#     # ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ 
#     # ■ Matriz que dicta la posición FINAL (prevalencia)
#     #    Da igual en qué fila los creaste con row(), draw() los manda donde toca
#     # ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ 
#     matrix = [
#         [lbl_nom,  txt_nom, "+", "+", "+", "_"       ],   # Fila 0
#         [lbl_ape1, txt_ape1, "_", lbl_ape2, txt_ape2 ],   
#         ['-' , listbox, '+', '+', '+', '-'],
#         [lbl_sc, scale, '+', '+', '+', '+', '+'],
#         [btn_add,  btn_upt, "+", "_", btn_del ],
#     ]    
#     F1.draw(matrix)
#     # ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ 
#     print("\n--- MAPA DE DRAW ---")
#     for entry in F1._draw_map:
#         print(entry)
#     # ______________________
#     F1.frame().config(bg="lightgray")
#     # ______________________
#     F1.family.formar("textos", [txt_nom, txt_ape1, txt_ape2,])
#     F1.family.formar("crud", [btn_add, btn_upt, btn_del,])
#     # ______________________
#     textos = F1.family.familiares('textos')
#     for i, t in enumerate(textos):
#         t.delete(0, tk.END)
#         t.insert(1, f"Hello Texto {i}")
#     # █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ 
#     root.mainloop()
#     # █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ █ ■ 