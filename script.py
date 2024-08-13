import pyodbc
import tkinter as tk
from tkinter import messagebox


# Clase para manejar la conexión a la base de datos
def get_connection():
    connection = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=DESKTOP-LO6U7DV;"
        "DATABASE=productos;"
        "Trusted_Connection=yes;"
    )
    return connection


# Clase Producto
class Producto:
    def __init__(self, id, nombre, precio, cantidad_en_stock, categoria):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.cantidad_en_stock = cantidad_en_stock
        self.categoria = categoria


# Funciones CRUD
def crear_producto(producto):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Productos (Nombre, Precio, CantidadEnStock, Categoria) VALUES (?, ?, ?, ?)",
        (
            producto.nombre,
            producto.precio,
            producto.cantidad_en_stock,
            producto.categoria,
        ),
    )
    conn.commit()
    conn.close()


def leer_productos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Productos")
    productos = cursor.fetchall()
    conn.close()
    return [Producto(row[0], row[1], row[2], row[3], row[4]) for row in productos]


def actualizar_producto(producto):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Productos SET Nombre=?, Precio=?, CantidadEnStock=?, Categoria=? WHERE Id=?",
        (
            producto.nombre,
            producto.precio,
            producto.cantidad_en_stock,
            producto.categoria,
            producto.id,
        ),
    )
    conn.commit()
    conn.close()


def eliminar_producto(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Productos WHERE Id=?", (id,))
    conn.commit()
    conn.close()


# Funciones para la interfaz gráfica
def agregar_producto():
    nombre = entry_nombre.get()
    precio = float(entry_precio.get())
    cantidad_en_stock = int(entry_cantidad.get())
    categoria = entry_categoria.get()
    producto = Producto(None, nombre, precio, cantidad_en_stock, categoria)
    crear_producto(producto)
    messagebox.showinfo("Éxito", "Producto creado con éxito.")
    limpiar_campos()
    mostrar_productos()


def mostrar_productos():
    for widget in frame_productos.winfo_children():
        widget.destroy()

    productos = leer_productos()
    for p in productos:
        tk.Label(
            frame_productos,
            text=f"ID: {p.id}, Nombre: {p.nombre}, Precio: {p.precio}, Cantidad: {p.cantidad_en_stock}, Categoría: {p.categoria}",
        ).pack()


def actualizar_producto_ui():
    id = int(entry_id.get())
    nombre = entry_nombre.get()
    precio = float(entry_precio.get())
    cantidad_en_stock = int(entry_cantidad.get())
    categoria = entry_categoria.get()
    producto = Producto(id, nombre, precio, cantidad_en_stock, categoria)
    actualizar_producto(producto)
    messagebox.showinfo("Éxito", "Producto actualizado con éxito.")
    limpiar_campos()
    mostrar_productos()


def eliminar_producto_ui():
    id = int(entry_id.get())
    eliminar_producto(id)
    messagebox.showinfo("Éxito", "Producto eliminado con éxito.")
    limpiar_campos()
    mostrar_productos()


def limpiar_campos():
    entry_id.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_precio.delete(0, tk.END)
    entry_cantidad.delete(0, tk.END)
    entry_categoria.delete(0, tk.END)


# Configuración de la ventana principal
root = tk.Tk()
root.title("Gestión de Productos")

# Creación de campos y botones
tk.Label(root, text="ID (solo para actualizar/eliminar):").grid(
    row=0, column=0, padx=10, pady=5, sticky="w"
)
entry_id = tk.Entry(root)
entry_id.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Nombre:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Precio:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_precio = tk.Entry(root)
entry_precio.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Cantidad en Stock:").grid(
    row=3, column=0, padx=10, pady=5, sticky="w"
)
entry_cantidad = tk.Entry(root)
entry_cantidad.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Categoría:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
entry_categoria = tk.Entry(root)
entry_categoria.grid(row=4, column=1, padx=10, pady=5)

tk.Button(root, text="Crear Producto", command=agregar_producto).grid(
    row=5, column=0, padx=10, pady=5
)
tk.Button(root, text="Actualizar Producto", command=actualizar_producto_ui).grid(
    row=5, column=1, padx=10, pady=5
)
tk.Button(root, text="Eliminar Producto", command=eliminar_producto_ui).grid(
    row=5, column=2, padx=10, pady=5
)

# Marco para mostrar productos
frame_productos = tk.Frame(root)
frame_productos.grid(row=0, column=3, rowspan=6, padx=10, pady=5, sticky="n")

tk.Button(root, text="Mostrar Productos", command=mostrar_productos).grid(
    row=6, column=3, padx=10, pady=5
)

root.mainloop()
