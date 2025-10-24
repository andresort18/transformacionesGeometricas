import tkinter as tk
import json
from tkinter import messagebox

class TraslacionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Traslación de figura guardada")

        #  Cargar figura desde archivo JSON
        try:
            with open("figura_guardada.json", "r") as f:
                self.figura = json.load(f)
        except FileNotFoundError:
            messagebox.showwarning(
                "Aviso",
                "⚠️ No se encontró el archivo 'figura_guardada.json'.\n\n"
                "Ejecuta primero 'dibujar_figura.py' para crear y guardar una figura."
            )
            # Si no existe el archivo, usamos una figura base (cuadrado)
            self.figura = {"puntos": [(0, 0), (2, 0), (2, 2), (0, 2)], "tamano": 1}

        self.puntos = self.figura["puntos"]

        # Canvas para dibujo 
        self.canvas = tk.Canvas(root, width=900, height=600, bg="white")
        self.canvas.pack()

        # Parámetros de dibujo
        self.escala = 25  # Tamaño de cada unidad
        self.origen_x = 450
        self.origen_y = 300

        # Dibuja plano cartesiano y figura inicial
        self.dibujar_plano_cartesiano()
        self.figura_id = self.dibujar_figura(self.puntos)

        # Controles de traslación
        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="Mover en X:").grid(row=0, column=0)
        self.entry_x = tk.Entry(frame, width=7)
        self.entry_x.grid(row=0, column=1)

        tk.Label(frame, text="Mover en Y:").grid(row=0, column=2)
        self.entry_y = tk.Entry(frame, width=7)
        self.entry_y.grid(row=0, column=3)

        self.btn = tk.Button(frame, text="Trasladar", command=self.mover)
        self.btn.grid(row=0, column=4, padx=5)

    def dibujar_plano_cartesiano(self):
        """Dibuja cuadrícula y ejes principales."""
        ancho = 900
        alto = 600
        paso = self.escala

        # Cuadrícula gris
        for x in range(0, ancho, paso):
            self.canvas.create_line(x, 0, x, alto, fill="#eaeaea")
        for y in range(0, alto, paso):
            self.canvas.create_line(0, y, ancho, y, fill="#eaeaea")

        # Ejes X y Y
        self.canvas.create_line(0, self.origen_y, ancho, self.origen_y, fill="black", width=2)
        self.canvas.create_line(self.origen_x, 0, self.origen_x, alto, fill="black", width=2)

        # Etiquetas numéricas
        rango_x = range(-int(ancho/(2*paso)), int(ancho/(2*paso)) + 1)
        rango_y = range(-int(alto/(2*paso)), int(alto/(2*paso)) + 1)
        for i in rango_x:
            x = self.origen_x + i * paso
            if 0 < x < ancho:
                self.canvas.create_text(x, self.origen_y + 10, text=str(i), fill="gray", font=("Arial", 8))
        for j in rango_y:
            y = self.origen_y - j * paso
            if 0 < y < alto:
                self.canvas.create_text(self.origen_x + 15, y, text=str(j), fill="gray", font=("Arial", 8))

    def dibujar_figura(self, puntos):
        """Dibuja figura con sus vértices etiquetados."""
        coords = []
        for (x, y) in puntos:
            cx = self.origen_x + x * self.escala
            cy = self.origen_y - y * self.escala
            coords.extend([cx, cy])
            self.canvas.create_oval(cx - 3, cy - 3, cx + 3, cy + 3, fill="red")
            self.canvas.create_text(cx + 12, cy - 10, text=f"({x},{y})", fill="black", font=("Arial", 9))
        return self.canvas.create_polygon(coords, outline="blue", fill="", width=2)

    def mover(self):
        """Traslada la figura en el plano cartesiano."""
        try:
            dx = int(self.entry_x.get())
            dy = int(self.entry_y.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa números válidos.")
            return

        #  Actualiza los puntos trasladados 
        self.puntos = [(x + dx, y + dy) for (x, y) in self.puntos]

        #  Recentrar si la figura se sale del canvas
        min_x = min(p[0] for p in self.puntos)
        max_x = max(p[0] for p in self.puntos)
        min_y = min(p[1] for p in self.puntos)
        max_y = max(p[1] for p in self.puntos)

        # Si la figura se aleja demasiado, movemos el origen
        if abs(max_x) > 15 or abs(min_x) > 15 or abs(max_y) > 10 or abs(min_y) > 10:
            self.origen_x = 450 - int((min_x + max_x)/2 * self.escala)
            self.origen_y = 300 + int((min_y + max_y)/2 * self.escala)

        # Redibuja 
        self.canvas.delete("all")
        self.dibujar_plano_cartesiano()
        self.figura_id = self.dibujar_figura(self.puntos)


root = tk.Tk()
app = TraslacionApp(root)
root.mainloop()
