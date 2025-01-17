import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox

def gauss_jordan_paso_a_paso(aumentada):
    pasos = []
    filas, columnas = aumentada.shape

    for i in range(filas):
        pasos.append(f"Paso {i+1}: Hacer el pivote en la fila {i+1} igual a 1")
        pivote = aumentada[i, i]
        if pivote != 0:
            aumentada[i] = aumentada[i] / pivote
        pasos.append(aumentada.copy())

        pasos.append(f"Hacer ceros en la columna {i+1} para las demás filas:")
        for j in range(filas):
            if j != i:
                factor = aumentada[j, i]
                aumentada[j] = aumentada[j] - factor * aumentada[i]
                pasos.append(f"Fila {j+1} - ({factor}) * Fila {i+1}")
                pasos.append(aumentada.copy())

    pasos.append("Matriz reducida en forma escalonada:")
    pasos.append(aumentada.copy())

    soluciones = []
    for i in range(len(aumentada)):
        soluciones.append(f"x{i+1} = {aumentada[i, -1]}")

    return pasos, soluciones

def mostrar_resultados(pasos, soluciones, inicial):
    resultados = tk.Toplevel()
    resultados.title("Resultados del Método Gauss-Jordan")
    resultados.configure(bg="#f5f5f5")

    title_label = tk.Label(resultados, text="Resultados del Método Gauss-Jordan", font=("Helvetica", 16, "bold"), bg="#f5f5f5")
    title_label.pack(pady=10)

    text_area = tk.Text(resultados, wrap=tk.WORD, font=("Courier", 12), bg="#ffffff", fg="#333333")
    text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    text_area.insert(tk.END, "Matriz inicial:\n")
    text_area.insert(tk.END, np.array2string(inicial) + "\n\n")

    for paso in pasos:
        if isinstance(paso, str):
            text_area.insert(tk.END, paso + "\n")
        else:
            text_area.insert(tk.END, np.array2string(paso) + "\n")

    text_area.insert(tk.END, "\nSoluciones:\n")
    for solucion in soluciones:
        text_area.insert(tk.END, solucion + "\n")

    text_area.config(state=tk.DISABLED)

def resolver():
    try:
        n = int(entry_n.get())
        matriz_aumentada = []
        for i in range(n):
            fila = matriz_entradas[i].get().split()
            matriz_aumentada.append([float(x) for x in fila])

        matriz_aumentada = np.array(matriz_aumentada, dtype=float)
        inicial = matriz_aumentada.copy()
        pasos, soluciones = gauss_jordan_paso_a_paso(matriz_aumentada)
        mostrar_resultados(pasos, soluciones, inicial)
    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error: {e}")

def crear_interfaz():
    global entry_n, matriz_entradas

    matriz_entradas = []

    root = tk.Tk()
    root.title("Método Gauss-Jordan")
    root.geometry("900x700")
    root.configure(bg="#f5f5f5")

    title_label = tk.Label(root, text="Método Gauss-Jordan", font=("Helvetica", 20, "bold"), bg="#f5f5f5", fg="#333333")
    title_label.pack(pady=20)

    frame = ttk.Frame(root, padding="10")
    frame.pack(expand=True, fill=tk.BOTH)

    ttk.Label(frame, text="Número de ecuaciones:", font=("Helvetica", 12)).grid(row=0, column=0, sticky=tk.W, pady=5)
    entry_n = ttk.Entry(frame, width=10, font=("Helvetica", 12))
    entry_n.grid(row=0, column=1, sticky=tk.W, pady=5)

    def generar_campos():
        for widget in frame.winfo_children()[2:]:
            widget.destroy()

        try:
            n = int(entry_n.get())
            matriz_entradas.clear()

            ttk.Label(frame, text="Ingrese los términos independientes separado por espacio:", font=("Helvetica", 12)).grid(row=1, column=0, columnspan=2, pady=10)

            for i in range(n):
                ttk.Label(frame, text=f"Ecuación {i+1}:", font=("Helvetica", 12)).grid(row=i+2, column=0, sticky=tk.W, pady=5)
                entrada = ttk.Entry(frame, width=50, font=("Helvetica", 12))
                entrada.grid(row=i+2, column=1, sticky=tk.W, pady=5)
                matriz_entradas.append(entrada)

            ttk.Button(frame, text="Resolver", command=resolver, style="Accent.TButton").grid(row=n+3, column=0, columnspan=2, pady=20)
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido de ecuaciones.")

    ttk.Button(frame, text="Generar Campos", command=generar_campos, style="Accent.TButton").grid(row=0, column=2, padx=10, pady=5)

    style = ttk.Style()
    style.configure("Accent.TButton", font=("Helvetica", 12), padding=5)

    root.mainloop()

if __name__ == "__main__":
    crear_interfaz()
