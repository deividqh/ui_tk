import tkinter as tk
from tkinter import ttk


class StepByStab(ttk.Frame):
    """Notebook secuencial configurable mediante un diccionario {clave: titulo}
    Permite avanzar y bloquear pestañas tanto por código (claves) como por interfaz (índices).
    """

    def __init__(self, contenedor, configuracion_pestanas, b_botones=True):
        """ 
        contenedor: el contenedor del Frame de Pestañas.
        configuracion_pestanas: un diccionario key = slug:str , value = 'Titulo de las Pestañas'
        b_botones: True, muestra botones para avanzar y bloquear. False no los muestra.
        """
        super().__init__(contenedor)

        if not configuracion_pestanas:
            raise ValueError("El diccionario de configuración no puede estar vacío.")

        # Separamos las claves y los títulos manteniendo el orden estricto de inserción
        self.claves  = list(configuracion_pestanas.keys())
        self.titulos = list(configuracion_pestanas.values())
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.pestanas = []
        self._crear_pestanas()
        self.blok_from(1) # Bloquea todo menos la primera al iniciar

        # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
        # PANEL DE CONTROL INTEGRADO (opcional)
        # ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
        if b_botones:
            self._crear_panel_control()

    def _crear_pestanas(self):
        """ ■ Crea las pestañas introducidas en la configuración. """
        for titulo in self.titulos:
            pestana = ttk.Frame(self.notebook)
            self.notebook.add(pestana, text=titulo)
            self.pestanas.append(pestana)

    def get_p(self, identificador):
        """■ Devuelve el Frame de la pestaña buscando por índice (int), clave (str) o título (str)."""
        # 1. Búsqueda por Índice Numérico (ideal para controles dinámicos de la interfaz)
        if isinstance(identificador, int):
            if 0 <= identificador < len(self.pestanas):
                return self.pestanas[identificador]
        
        elif isinstance(identificador, str):
            # 2. Búsqueda por Clave Custom (Prioritaria por código)
            if identificador in self.claves:
                indice = self.claves.index(identificador)
                return self.pestanas[indice]
            
            # 3. Búsqueda por Título Visible
            if identificador in self.titulos:
                indice = self.titulos.index(identificador)
                return self.pestanas[indice]

        raise ValueError(f"No se encontró la pestaña con el identificador: '{identificador}'")

    def go_next(self, identificador_actual):
        """ ■ Avanza a la siguiente pestaña basándose en cualquier identificador de la actual."""
        pestana_actual = self.get_p(identificador_actual)
        indice_actual = self.pestanas.index(pestana_actual)
        
        siguiente_indice = indice_actual + 1
        if siguiente_indice < len(self.pestanas):
            siguiente_pestana = self.pestanas[siguiente_indice]
            self.notebook.tab(siguiente_pestana, state="normal")
            self.notebook.select(siguiente_pestana)

    def blok_from(self, indice_inicial):
        """ ■ Bloquea todas las pestañas a partir del índice numérico indicado."""
        for indice in range(indice_inicial, len(self.pestanas)):
            self.notebook.tab(self.pestanas[indice], state="disabled")
    
    def _crear_panel_control(self):
        """ ■ Crea los botones de avanzar y bloquear empaquetados en la parte inferior."""
        panel_control = ttk.Frame(self)
        panel_control.pack(fill="x", padx=10, pady=10)

        # Botón Avanzar: Detecta la pestaña actual dinámicamente y avanza
        btn_avanzar = ttk.Button(
            panel_control,
            text="Validar y Avanzar ➡️",
            command=lambda: self.go_next(self.notebook.index("current"))
        )
        btn_avanzar.pack(side="left", padx=5, expand=True, fill="x")

        # Botón Bloquear: Bloquea todo el camino que esté por delante de la pestaña actual
        btn_bloquear = ttk.Button(
            panel_control,
            text="🔒 Bloquear Siguientes",
            command=lambda: self.blok_from(self.notebook.index("current") + 1)
        )
        btn_bloquear.pack(side="left", padx=5, expand=True, fill="x")


# --- ENTORNO DE PRUEBA ---
# def main():
#     ventana = tk.Tk()
#     ventana.title("Sistema de Pestañas Secuenciales")
#     ventana.geometry("680x350")

#     # Tu configuración limpia en un solo sitio
#     config = {
#         "dat": "Datos",
#         "split": "Split",
#         "alg": "Algoritmo/Modelo",
#         "met": "Métricas",
#         "graf": "Gráficas"
#     }

#     TABs = StepByStab(ventana, config)
#     TABs.pack(fill="both", expand=True, padx=10, pady=10)

#     # --- INYECTANDO CONTROLES EN LAS PESTAÑAS (Usando tus llaves custom) ---
    
#     # Pestaña Datos
#     p_datos = TABs.get_p("dat")
#     ttk.Label(p_datos, text="📂 Configuración de Datos del Modelo", font=("Arial", 11, "bold")).pack(pady=10)
#     ttk.Entry(p_datos).pack(pady=5)

#     # Pestaña Split
#     p_split = TABs.get_p("split")
#     ttk.Label(p_split, text="✂️ Proporción del Split (Train/Test)", font=("Arial", 11, "bold")).pack(pady=10)
#     ttk.Scale(p_split, from_=0, to=100, orient="horizontal").pack(fill="x", padx=30, pady=5)

#     # Pestaña Algoritmo
#     p_alg = TABs.get_p("alg")
#     ttk.Label(p_alg, text="🤖 Selección de Algoritmo", font=("Arial", 11, "bold")).pack(pady=10)


#     # --- PANEL DE CONTROL GLOBAL (Los botones de antes) ---
#     panel_control = ttk.Frame(ventana)
#     panel_control.pack(fill="x", padx=10, pady=10)

#     # Botón Avanzar: Detecta la pestaña actual dinámicamente y avanza
#     btn_avanzar = ttk.Button(
#         panel_control,
#         text="Validar y Avanzar ➡️",
#         command=lambda: TABs.go_next(
#             TABs.notebook.index("current")
#         )
#     )
#     btn_avanzar.pack(side="left", padx=5, expand=True, fill="x")

#     # Botón Bloquear: Bloquea todo el camino que esté por delante de la pestaña actual
#     btn_bloquear = ttk.Button(
#         panel_control,
#         text="🔒 Bloquear Siguientes",
#         command=lambda: TABs.blok_from(
#             TABs.notebook.index("current") + 1
#         )
#     )
#     btn_bloquear.pack(side="left", padx=5, expand=True, fill="x")

#     ventana.mainloop()


# if __name__ == "__main__":
#     main()