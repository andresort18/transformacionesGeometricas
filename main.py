import tkinter as tk
import subprocess

from tkinter import Menu
from PIL import Image, ImageTk
def opcion1():
    print("Opción 1 seleccionada")

def opcion2():
    print("Opción 2 seleccionada")

def abrir_trasladar():
    subprocess.Popen(["python", "traslacion.py"])

def abrir_dibujar():
    subprocess.Popen(["python", "dibujarFigura.py"])       

#ventana principal
root = tk.Tk()
root.title("Traslación y Rotación de Figuras 2D")
root.geometry("900x600")

#menu de opciones 
menu_opciones = Menu(root)
opciones_menu = Menu(menu_opciones, tearoff=0)
opciones_menu.add_command(label="Opción 1", command=opcion1)
opciones_menu.add_command(label="Opción 2", command=opcion2)

menu_opciones.add_cascade(label="Opciones", menu=opciones_menu)
root.config(menu=menu_opciones)

titulo = tk.Label(root, text="Traslación y Rotación de Figuras 2D", font=("Arial", 20, "bold"))
titulo.pack(pady=20)

# imagen de la interfaz
imagen = Image.open("traslacion_rotacion.png")
imagen = imagen.resize((700, 300))  # Ajustar tamaño al espacio
imagen_tk = ImageTk.PhotoImage(imagen)

marco_imagen = tk.Label(root, image=imagen_tk, relief="solid")
marco_imagen.pack(pady=20)

#botones
btn_dibujar_figu = tk.Button(root, text="Dibujar figura", width=30,command=abrir_dibujar)
btn_dibujar_figu.pack(pady=10)

frame_botones = tk.Frame(root)
frame_botones.pack(pady=20)

btn_trasladar = tk.Button(frame_botones, text="Trasladar", width=30,command=abrir_trasladar)
btn_trasladar.pack(side="left", padx=40)

btn_rotar = tk.Button(frame_botones, text="Rotar", width=30)
btn_rotar.pack(side="right", padx=40)
root.mainloop()
