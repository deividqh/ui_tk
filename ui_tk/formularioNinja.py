import tkinter
class Formulario_Ninja():
    """ 
    Def: Clase que define un formulario tKinter para hacer una doble conexion cliente-servidor
    con sockets para poder enviar mensajes de texto y archivos y emojis en una red local.
    """                    
    # ____________________________
    # ==== Constructor de la clase
    def __init__(self, root, ancho=300, alto=150, posY=None, posX=None, descpos=''):
        """ 
        Def: Constructor de la clase Formulario_Ninja()
        [root]: ventana instanciada
        [ancho=300]: ancho de la ventana por defecto
        [alto=300]:  alto de la ventana por defecto
        [posY]=None: posicion Y inicial(altura) de la ventana. 
        Si se pasa None, situa la ventana a 100px de la esquina derecha abajo.
        [descpos]: ["up-down":"right-left"] ==> "u:l", "u:r", "d:r", "d:l", "c" 
        """
        self.PADY=100           # Desde la parte inferior de la pantalla al borde inferior de la ventana
        self.esExpandido=False  # Booleano para indicar si la ventana (formulario) está plegada
        # ___________________
        # ==== CACHA EL ROOT
        self.root = root        
        self.ancho=ancho
        self.alto=alto
        self.posY=posY      # posicion inicial x del formulario. 
        self.posX=posX      # posicion inicial y del formulario. 
        self.descpos=descpos
        # ==== Tamaño (ventana) xa geometry >>>
        # ===================================        
        self.formWidth = self.ancho
        self.formHeight = self.alto
        # ==== Posicion (ventana) xa geometry >>>
        # ====================================
        # Obtiene el tamaño de la pantalla Xa calcular la posicion (coorX, coorY) 
        self.screenWidth  = self.root.winfo_screenwidth()
        self.screenHeight = self.root.winfo_screenheight()
        pass
        # ________________________________
        # Posición inicial del Formulario
        # ================================
        # Configura la geometría inicial de la ventana (40 píxeles visibles en el ejeX) (derecha-Abajo-100)
        self.coorX = self.screenWidth - 40
        # ___________
        if posY==None:
            self.coorY = self.screenHeight - self.formHeight - self.PADY         # 100 de la barra inferior. 
        else:
            self.coorY = posY
        pass
        # ______________________
        # POSICIONAR FORMULARIO:  geometry => (str)" Ancho x Alto + coordenadaX + coordenadaY "
        # ======================
        self.root.geometry(f'{self.formWidth}x{self.formHeight}+{self.coorX}+{self.coorY}')
        pass
        # __________________
        # MOVER FORMULARIO:
        # ==================
        # Detecta el doble clic en la ventana para expandir o contraer
        self.root.bind('<Double-1>', self.formRoot_dblClick)
        # Al hacer doble clic, expandir o contraer la ventana

    # _______________________________________
    # DESCRIPCION DE POSICION:
    # =======================================
    def posicionDescForm(self):   
        if self.descpos=='':
            pass
        pass     
    
    # _______________________________________
    # EVENTO DOBLE CLICK SOBRE EL FORMULARIO:
    # =======================================
    def formRoot_dblClick(self, event):        
        if self.esExpandido:
            self.desplazar(mostrar_completa=False)
        else:
            self.desplazar(mostrar_completa=True)
    # _____________________________________________
    # Mueve la ventana con el metodo de root after
    # =============================================
    def desplazar(self, mostrar_completa=True):
        # global coorX, esExpandido
        if mostrar_completa:
            # Expande la ventana hacia el centro de la pantalla
            if self.coorX > self.screenWidth - self.formWidth - 10:
                self.coorX -= 10
                self.root.geometry(f'{self.formWidth}x{self.formHeight}+{self.coorX}+{self.coorY}')
                self.root.after(20, self.desplazar)
            else:
                self.esExpandido = True  # Indica que la ventana está completamente expandida
        else:       # Oculta la ventana(40 píxeles visibles)            
            if self.coorX < self.screenWidth - 40:
                self.coorX += 10
                self.root.geometry(f'{self.formWidth}x{self.formHeight}+{self.coorX}+{self.coorY}')
                self.root.after(20, self.desplazar, False)
            else:
                self.esExpandido = False  # Indica que la ventana está contraída

    # _____________________________________________
    # Abre una ventana con un mensaje tipo msgbox de vba arriba a la derecha
    # =============================================
    def msg_U_R(self, mensaje):
        ventana = tk.Tk()
        ventana.title("Nuevo Mensaje")
        ventana.geometry(f"200x100+{ventana.winfo_screenwidth() - 210}+10")  # Posicionar en la esquina superior derecha
        
        label = tk.Label(ventana, text=mensaje)
        label.pack(padx=20, pady=20)
        
        # Configura para que la ventana se cierre automáticamente después de 3 segundos
        ventana.after(3000, ventana.destroy)
        ventana.mainloop()

    # _____________________________________________
    # Función para mostrar una ventana emergente en la esquina inferior derecha
    # =============================================
    def msg_D_R(self, mensaje):
        ventana = tk.Tk()
        ventana.title("Nuevo Mensaje")

        # Obtener las dimensiones de la pantalla
        screen_width = ventana.winfo_screenwidth()
        screen_height = ventana.winfo_screenheight()

        # Posicionar en la esquina inferior derecha
        ventana.geometry(f"200x100+{screen_width - 210}+{screen_height - 150}")  

        label = tk.Label(ventana, text=mensaje)
        label.pack(padx=20, pady=20)
        
        # Configura para que la ventana se cierre automáticamente después de 3 segundos
        ventana.after(3000, ventana.destroy)
        ventana.mainloop()


    def toggle_expand(self):
        """ 
        Def: Función para expandir o contraer el frame de servidor.
        """
        # self.esExpandido = not getattr(self, "esExpandido", False)
        if self.esExpandido:
            self.root.geometry(f"{self.anchoIni}x{self.alto * 2}")
            self.btnToggle.config(text="Contraer")
        else:
            self.root.geometry(f"{self.anchoIni}x{self.alto}")
            self.btnToggle.config(text="Desplegar")