import tkinter as tk
import json
from tkinter import messagebox

class TraslacionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Traslación de figura guardada")

        #  Cargar figura desde el archivo JSON 
        try:
            with open("figura_guardada.json", "r") as f:
                self.figura = json.load(f)
        except FileNotFoundError:
            messagebox.showwarning(
                "Aviso",
                "⚠️ No se encontró el archivo 'figura_guardada'.\n\n"
                "Ejecuta primero 'dibujar figura' para crear y guardar una figura."
            )
            # En caso de no existir el archivo, usamos una figura base (cuadrado)
            self.figura = {"puntos": [(0, 0), (2, 0), (2, 2), (0, 2)], "tamano": 1}

        self.puntos = self.figura["puntos"]

        # Crear el canvas donde se dibujará la figura 
        self.canvas = tk.Canvas(root, width=900, height=600, bg="white")
        self.canvas.pack()

        # Parámetros para el dibujo
        self.escala = 20
        self.origen_x = 450
        self.origen_y = 300

        # Dibujar la figura inicial
        self.figura_id = self.dibujar_figura(self.puntos)

        # Controles para ingresar los desplazamientos
        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="Mover en X:").grid(row=0, column=0)
        self.entry_x = tk.Entry(frame, width=7)
        self.entry_x.grid(row=0, column=1)

        tk.Label(frame, text="Mover en Y:").grid(row=0, column=2)
        self.entry_y = tk.Entry(frame, width=7)
        self.entry_y.grid(row=0, column=3)

        # Botón para ejecutar la traslación
        self.btn = tk.Button(frame, text="Trasladar", command=self.mover)
        self.btn.grid(row=0, column=4, padx=5)

    def dibujar_figura(self, puntos):
        """Dibuja la figura a partir de los puntos dados."""
        coords = []
        for (x, y) in puntos:
            cx = self.origen_x + x * self.escala
            cy = self.origen_y - y * self.escala
            coords.extend([cx, cy])
            self.canvas.create_oval(cx - 3, cy - 3, cx + 3, cy + 3, fill="red")
            self.canvas.create_text(cx + 12, cy - 10, text=f"({x},{y})", fill="black", font=("Arial", 9))
        return self.canvas.create_polygon(coords, outline="blue", fill="", width=2)

    def mover(self):
        """Lee los valores de entrada y traslada la figura."""
        try:
            dx = int(self.entry_x.get())
            dy = int(self.entry_y.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa números válidos.")
            return

        # Calcula los nuevos puntos trasladados
        self.puntos = [(x + dx, y + dy) for (x, y) in self.puntos]

        # Limpia el canvas y redibuja la figura actualizada
        self.canvas.delete("all")
        self.figura_id = self.dibujar_figura(self.puntos)


root = tk.Tk()
app = TraslacionApp(root)
root.mainloop()