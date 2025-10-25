import tkinter as tk
import json
import math

pantalla = tk.Tk()
pantalla.title('Rotar figura 2D')
pantalla.geometry('900x700')
pantalla.configure(bg='white')

# --- Variables globales ---
puntos_originales = []
puntos_rotados = []

# --- Funciones ---
def cargar_figura():
    """Carga la figura desde figura_guardada.json y la dibuja"""
    global puntos_originales
    try:
        with open("figura_guardada.json", "r") as f:
            datos = json.load(f)
            puntos_originales = datos.get("puntos", [])
    except FileNotFoundError:
        etiqueta_estado.config(text="⚠️ No se encontró 'figura_guardada.json'", fg="red")
        return
    except Exception as e:
        etiqueta_estado.config(text=f"Error al leer JSON: {e}", fg="red")
        return

    if not puntos_originales:
        etiqueta_estado.config(text="⚠️ La figura no contiene puntos.", fg="red")
        return

    etiqueta_estado.config(text="✅ Figura cargada correctamente.", fg="green")
    dibujar_figura(puntos_originales, color="blue")


def dibujar_figura(puntos, color="blue"):
    """Dibuja la figura en el canvas"""
    canvas.delete("all")

    origen_x = 700 / 2
    origen_y = 500 / 2
    escala = 20

    # Rejilla
    for i in range(0, 701, int(escala)):
        color_linea = "lightgray" if i != origen_x else "black"
        canvas.create_line(i, 0, i, 500, fill=color_linea)
    for j in range(0, 501, int(escala)):
        color_linea = "lightgray" if j != origen_y else "black"
        canvas.create_line(0, j, 700, j, fill=color_linea)

    # Números
    rango = int((700 / 2) / escala)
    for n in range(-rango, rango + 1):
        if n != 0:
            x = origen_x + n * escala
            canvas.create_text(x, origen_y + 10, text=str(n), fill="black", font=("Arial", 8))
            y = origen_y - n * escala
            canvas.create_text(origen_x + 15, y, text=str(n), fill="black", font=("Arial", 8))

    # Figura
    coords = []
    for (x, y) in puntos:
        cx = origen_x + x * escala
        cy = origen_y - y * escala
        coords.extend([cx, cy])
        canvas.create_oval(cx - 4, cy - 4, cx + 4, cy + 4, fill="red")
        canvas.create_text(cx + 12, cy - 10, text=f"({x},{y})", fill="black", font=("Arial", 9))

    if len(coords) >= 4:
        canvas.create_polygon(coords, outline=color, fill="", width=2)


def rotar_figura():
    """Rota la figura sobre su centro, sin trasladarla"""
    global puntos_rotados

    if not puntos_originales:
        etiqueta_estado.config(text="⚠️ Primero cargue una figura.", fg="red")
        return

    try:
        grados = float(entry_grados.get())
    except ValueError:
        etiqueta_estado.config(text="⚠️ Ingrese un número válido de grados.", fg="red")
        return

    # Calcular el centro de la figura
    xs = [p[0] for p in puntos_originales]
    ys = [p[1] for p in puntos_originales]
    centro_x = sum(xs) / len(xs)
    centro_y = sum(ys) / len(ys)

    rad = math.radians(grados)
    cos_t = math.cos(rad)
    sin_t = math.sin(rad)

    puntos_rotados = []
    for (x, y) in puntos_originales:
        # Trasladar al origen
        x_rel = x - centro_x
        y_rel = y - centro_y

        # Rotar
        xr = x_rel * cos_t - y_rel * sin_t
        yr = x_rel * sin_t + y_rel * cos_t

        # Volver a trasladar al centro original
        xr += centro_x
        yr += centro_y

        puntos_rotados.append((round(xr, 2), round(yr, 2)))

    dibujar_figura(puntos_rotados, color="orange")
    etiqueta_estado.config(text=f"🔄 Figura rotada {grados}° sobre su centro", fg="orange")


# --- Interfaz ---
label_titulo = tk.Label(pantalla, text="Rotar figura guardada", font=("Arial", 16, "bold"), bg='white', fg='black')
label_titulo.pack(pady=10)

canvas = tk.Canvas(pantalla, width=700, height=500, bg="white", highlightbackground="black")
canvas.pack(pady=20)

frame_controles = tk.Frame(pantalla, bg="white")
frame_controles.pack(pady=10)

boton_cargar = tk.Button(frame_controles, text="Cargar figura guardada", command=cargar_figura,
                         bg="white", fg="black", width=20, relief="solid", borderwidth=1)
boton_cargar.grid(row=0, column=0, padx=10, pady=5)

label_grados = tk.Label(frame_controles, text="Grados a rotar:", bg="white", fg="black")
label_grados.grid(row=0, column=1, padx=10)

entry_grados = tk.Entry(frame_controles, width=10)
entry_grados.grid(row=0, column=2, padx=5)

boton_rotar = tk.Button(frame_controles, text="Rotar figura", command=rotar_figura,
                        bg="white", fg="black", width=15, relief="solid", borderwidth=1)
boton_rotar.grid(row=0, column=3, padx=10)

etiqueta_estado = tk.Label(pantalla, text="", bg="white", fg="black", font=("Arial", 11, "bold"))
etiqueta_estado.pack(pady=10)

pantalla.mainloop()
