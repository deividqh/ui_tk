import tkinter as tk

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
    def family(self, nombre_familia: str, widgets: list = [], b_del: bool = False):
        if nombre_familia not in self.d_family and not b_del:
            self.d_family[nombre_familia] = []
        
        if b_del:
            if nombre_familia in self.d_family:
                for w in widgets:
                    if w in self.d_family[nombre_familia]:
                        self.d_family[nombre_familia].remove(w)
        else:
            for w in widgets:
                if w not in self.d_family[nombre_familia]:
                    self.d_family[nombre_familia].append(w)
    
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

# ==========================================
# TEST OPERATIVO
# ==========================================
# if __name__ == "__main__":
#     root = tk.Tk()

#     Frame1 = tk.Frame(root, background='#111111')
#     Frame1.pack()
#     F = Familia()

#     btn_add = tk.Button(Frame1, text="Añadir")
#     btn_add.pack()
#     btn_del = tk.Button(Frame1, text="Borrar")
#     btn_del.pack()
#     txt_nom = tk.Entry(root)
#     txt_nom.pack(padx=10, pady=10)
#     txt_nom.insert(0, "Juan")

#     # Registro
#     F.family('botones_control', [ btn_add , btn_del ])
#     F.family('entradas', [txt_nom])


#     F.familiares('botones_control')[0].config(bg="lightgray")


#     # --- PRUEBAS DE LLAMADA DIRECTA ---
#     F('botones_control')        # Esto funciona gracias a __call__
#     F()                         # Muestra el resumen

#     # root.withdraw() # Cerramos la ventana de test
#     root.mainloop() # Cerramos la ventana de test