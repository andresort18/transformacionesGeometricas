import tkinter as tk
import json  # agregado para guardar la figura en un archivo

pantalla = tk.Tk()
pantalla.title('Dibujar figuras 2D')
pantalla.geometry('900x700')

# variables
puntos = []

#declaracion de funciones
def agregar_vector():
    try:
        x = int(entry_x.get())
        y = int(entry_y.get())
        puntos.append((x, y))  
        # para Limpiar entradas
        entry_x.delete(0, tk.END)
        entry_y.delete(0, tk.END)
        print("Punto agregado:", (x, y)) 
        
        texto = "Vectores ingresados:\n"
        for i, (px, py) in enumerate(puntos, start=1):
            texto += f"{i}. ({px}, {py})\n"

        etiqueta_vectores.config(text=texto)
        if not etiqueta_vectores.winfo_ismapped():
            etiqueta_vectores.pack(pady=5, before=boton_listo)
    except ValueError:
        print("Ingrese solo números enteros.")

def mostrar_siguiente(): 
    # Oculta elementos de la primera parte
    entry_x.pack_forget()
    entry_y.pack_forget()
    boton_agregar.pack_forget()
    boton_listo.pack_forget()
    label_titulo.pack_forget()
    label_x.pack_forget()
    label_y.pack_forget()

    # Muestra la siguiente parte (definir tamaño)
    label_titulo2.pack(side="top", pady=10)
    label_tam.pack()
    entry_tam.pack()
    boton_listo2.pack()

def mostrar_siguiente2(): 
    # Muestra tamaño seleccionado
    tam = entry_tam.get()
    etiqueta_tam.config(text=f"Tamaño seleccionado: {tam}")
    etiqueta_tam.pack(pady=5)

    # Oculta elementos y muestra el botón para dibujar
    entry_tam.pack_forget()
    boton_listo2.pack_forget()
    label_titulo2.pack_forget()
    label_tam.pack_forget()

    label_titulo3.pack()
    boton_dibujar.pack()

def dibujar():
    # Oculta parte anterior y muestra el canvas
    label_titulo3.pack_forget()
    boton_dibujar.pack_forget()
             
    boton_guardar.pack()

    canvas = tk.Canvas(pantalla, width=700, height=600, bg="gray20")
    canvas.pack(pady=20)

    # Centro del plano
    origen_x = 700 / 2
    origen_y = 500 / 2
    escala = 20  
   
    # Dibuja líneas verticales (rejilla)
    for i in range(0, 701, int(escala)):
        color = "black" if i != origen_x else "white"
        canvas.create_line(i, 0, i, 500, fill=color)

    # Dibuja líneas horizontales
    for j in range(0, 501, int(escala)):
        color = "black" if j != origen_y else "white"
        canvas.create_line(0, j, 700, j, fill=color)

    # Dibuja números de coordenadas
    rango = int((700 / 2) / escala)
    for n in range(-rango, rango + 1):
        if n != 0:
            x = origen_x + n * escala
            canvas.create_text(x, origen_y + 10, text=str(n), fill="white", font=("Arial", 8))
            
            y = origen_y - n * escala
            canvas.create_text(origen_x + 15, y, text=str(n), fill="white", font=("Arial", 8))

    # Dibuja los puntos ingresados
    coords = []
    for (x, y) in puntos:
        cx = origen_x + x * escala
        cy = origen_y - y * escala
        coords.extend([cx, cy])
        canvas.create_oval(cx - 4, cy - 4, cx + 4, cy + 4, fill="red")
        canvas.create_text(cx + 12, cy - 10, text=f"({x},{y})", fill="yellow", font=("Arial", 9))

    # Si hay al menos 2 vectores, dibuja la figura (polígono)
    if len(coords) >= 4:
        canvas.create_polygon(coords, outline="cyan", fill="", width=2)

    canvas.create_text(100, 20, text="   Figura con vectores", fill="white", font=("Arial", 12, "bold"))

def guardar_figura():
    # Guarda la figura creada
    global figura_funcion

    try:
        tam = float(entry_tam.get()) if entry_tam.get() else 1
    except ValueError:
        tam = 1

    datos = {
        "puntos": puntos.copy(),
        "tamano": tam
    }

    # Guarda la figura también en un archivo JSON para trasladar.py
    with open("figura_guardada.json", "w") as f:
        json.dump(datos, f)

    print("Figura procesada y guardada correctamente:", datos)
    etiqueta_guardado.config(
        text=" Figura guardada correctamente en 'figura_guardada.json'",
        fg="black",
        font=("Arial", 11, "bold")
    )
    etiqueta_guardado.pack(pady=10)

# --- Entradas y etiquetas ---
entry_x = tk.Entry(pantalla)
entry_y = tk.Entry(pantalla)
entry_tam = tk.Entry(pantalla)
etiqueta_tam = tk.Label(pantalla, text="")

#titulos
label_titulo = tk.Label(pantalla, text="Para iniciar a dibujar nuestra figura ingresemos nuestros vectores")
label_titulo.pack(side="top", pady=10)

label_titulo2 = tk.Label(pantalla, text="Ahora definamos el tamaño")
label_titulo3 = tk.Label(pantalla, text="perfecto, ya esta listo para dibujar")

etiqueta_vectores = tk.Label(pantalla, text="Vectores ingresados:\n", justify="left")

etiqueta_guardado = tk.Label(pantalla, text="", fg="black", font=("Arial", 11, "bold"))

label_x = tk.Label(pantalla, text="eje X:")
label_x.pack()
entry_x.pack()

label_y = tk.Label(pantalla, text="eje Y:")
label_y.pack()
entry_y.pack()

label_tam = tk.Label(pantalla, text="Tamaño:")

# botones utilizados
boton_agregar = tk.Button(pantalla, text="agregar vector",width=20, command=agregar_vector)
boton_agregar.pack(pady=10)

boton_listo = tk.Button(pantalla, text="listo", command=mostrar_siguiente)
boton_listo.pack(pady=10)

boton_listo2 = tk.Button(pantalla, text="listo", command=mostrar_siguiente2)

boton_dibujar = tk.Button(pantalla, text="Dibujar figura", command= dibujar)

boton_guardar = tk.Button(pantalla, text="Guardar figura", command=guardar_figura)

pantalla.mainloop()
