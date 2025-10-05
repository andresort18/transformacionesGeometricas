import tkinter as tk

class TraslacionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Traslación de un cuadrado")

        # Canvas para dibujar
        self.canvas = tk.Canvas(root, width=900, height=600, bg="white")
        self.canvas.pack()

        # Dibujar un cuadrado (guardo el id para poder moverlo)
        self.size = 100
        self.square = self.canvas.create_rectangle(0, 0, self.size, self.size, fill="red")

        # Controles para ingresar coordenadas
        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="X:").grid(row=0, column=0)
        self.entry_x = tk.Entry(frame, width=7)
        self.entry_x.grid(row=0, column=1)

        tk.Label(frame, text="Y:").grid(row=0, column=2)
        self.entry_y = tk.Entry(frame, width=7)
        self.entry_y.grid(row=0, column=3)

        self.btn = tk.Button(frame, text="Mover", command=self.mover)
        self.btn.grid(row=0, column=4, padx=5)

    def mover(self):
        try:
            # Leer valores de entrada
            x = int(self.entry_x.get())
            y = int(self.entry_y.get())

            # Reubicar el cuadrado
            self.canvas.coords(self.square, x, y, x + self.size, y + self.size)
        except ValueError:
            print("Por favor ingresa números válidos.")

# Ejecutar programa
root = tk.Tk()
app = TraslacionApp(root)
root.mainloop()