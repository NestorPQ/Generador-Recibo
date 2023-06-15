import os

# import mysql.connector
from reportlab.lib.utils import ImageReader
from tkinter import *
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors


from tkinter import ttk
from tkinter.ttk import Combobox



recibo_actual = 100

def limpiar_campos():
    combo_tipo_moneda.current(0)
    entry_nombre.delete(0, END)
    entry_monto_cancelado.delete(0, END)
    entry_saldo_cuenta.delete(0, END)
    entry_monto_total.delete(0, END)
    entry_descripcion.delete(0, END)


def crear_factura():
    global recibo_actual



    # Obtener los valores de los campos de entrada
    nombre = entry_nombre.get()
    simbolo_monetario = combo_tipo_moneda.get()
    monto_cancelado = entry_monto_cancelado.get()
    saldo_cuenta = entry_saldo_cuenta.get()
    monto_total = entry_monto_total.get()
    descripcion = entry_descripcion.get().strip()



    # Validar que se hayan ingresado todos los campos
    if not nombre or not monto_cancelado or not saldo_cuenta or not monto_total or not descripcion:
        messagebox.showerror("Error", "Por favor, complete todos los campos.")
        return


    # Verificar si el directorio existe, de lo contrario, crearlo
    directorio = "./Boletas/"
    if not os.path.exists(directorio):
        os.makedirs(directorio)

    # Crear el archivo PDF
    c = canvas.Canvas(f"{directorio}{nombre}_{recibo_actual}.pdf", pagesize=letter)

    # Agregar la descripción de la empresa
    c.setFont("Helvetica-Bold", 14)
    c.drawString(140, 750, "Quique Ronceros Fotografía")
    c.setFont("Helvetica", 12)
    c.drawString(140, 730, "Av. Alva Maurtua #500 - 2do piso Chincha Alta")
    c.drawString(140, 710, "Celular: +51 934 668 775")
    c.drawString(140, 690, "Email: quiqueronceros@gmail.com")

    # Agregar el número del recibo
    c.setFont("Helvetica-Bold", 16)
    c.drawString(450, 750, f"Recibo #{recibo_actual}")

    # Actualizar el número del recibo
    recibo_actual += 1

    # Agregar el logotipo
    #ruta_logo = os.path.join(sys._MEIPASS, "isotipo.png")
    ruta_logo = "isotipo.png"

    logo = ImageReader(ruta_logo)
    c.drawImage(logo, 50, 680, width=60, height=80)



    # Crear la tabla de detalles de la factura
    descripcion_words = descripcion.split()  # Dividir el texto en palabras
    descripcion_lines = []
    current_line = ""
    max_line_width = 70  # Ancho máximo de línea (puedes ajustar este valor)

    for word in descripcion_words:
        if len(current_line) + len(word) + 1 <= max_line_width:  # Verificar si la palabra cabe en la línea actual
            current_line += word + " "
        else:
            descripcion_lines.append(current_line.strip())  # Agregar la línea actual a la lista de líneas
            current_line = word + " "

    if current_line:  # Agregar la última línea si aún hay contenido en current_line
        descripcion_lines.append(current_line.strip())

    # Crear la tabla de detalles de la factura
    tabla = [
        ["Descripción de la compra:", "\n".join(descripcion_lines)],  # Unir las líneas con saltos de línea
        ["Nombre:", nombre],
        ["Monto cancelado:", f"{simbolo_monetario}{monto_cancelado}"],
        ["Saldo a cuenta:", f"{simbolo_monetario}{saldo_cuenta}"],
        ["Monto total:", f"{simbolo_monetario}{monto_total}"]
    ]

    estilos = [
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),

        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('BACKGROUND', (1, 0), (1, 0), colors.white),

        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]

    tabla_estilo = Table(tabla, style=TableStyle(estilos))
    tabla_height = len(
        descripcion_lines) * 20  # Calcular la altura de la tabla basada en la cantidad de líneas de la descripción

    # Calcular la posición vertical de la tabla
    tabla_y = 550 - tabla_height  # Ajustar la posición vertical de la tabla

    tabla_estilo.wrapOn(c, 400, 200)
    tabla_estilo.drawOn(c, 50, tabla_y)

    # ...

    # Guardar y cerrar el archivo PDF
    c.save()

    # Mostrar mensaje de éxito
    messagebox.showinfo("Éxito", "La factura ha sido generada ")

def cerrar_aplicacion():
    window.destroy()


# Crear la ventana principal
window = Tk()
window.title("Generador de recibo")
window.geometry("540x400")

# Crear el cuadro de combinación
combo_tipo_moneda = ttk.Combobox(window, values=["S/ ", "$ ", "€ ", "¥ "], font=("Helvetica", 14), state="readonly")


# Crear los campos de entrada y etiquetas
label_nombre = Label(window, text="Nombres y Apellidos:", font=("Helvetica", 14))
label_nombre.grid(row=0, column=0, padx=20, pady=10, sticky=W)
entry_nombre = Entry(window, font=("Helvetica", 14))
entry_nombre.grid(row=0, column=1, padx=20, pady=10)

# Etiqueta y selección del tipo de moneda
label_tipo_moneda = Label(window, text="Tipo de Moneda:", font=("Helvetica", 14))
label_tipo_moneda.grid(row=5, column=0, padx=20, pady=10, sticky=W)
combo_tipo_moneda = Combobox(window, values=["S/ ", "$ ", "€ ", "¥ "], font=("Helvetica", 14), state="readonly")
combo_tipo_moneda.current(0)
combo_tipo_moneda.grid(row=5, column=1, padx=20, pady=10, sticky=W)


label_monto_cancelado = Label(window, text="Monto Cancelado:", font=("Helvetica", 14))
label_monto_cancelado.grid(row=1, column=0, padx=20, pady=10, sticky=W)
entry_monto_cancelado = Entry(window, font=("Helvetica", 14))
entry_monto_cancelado.grid(row=1, column=1, padx=20, pady=10)

label_saldo_cuenta = Label(window, text="Saldo a Cuenta:", font=("Helvetica", 14))
label_saldo_cuenta.grid(row=2, column=0, padx=20, pady=10, sticky=W)
entry_saldo_cuenta = Entry(window, font=("Helvetica", 14))
entry_saldo_cuenta.grid(row=2, column=1, padx=20, pady=10)

label_monto_total = Label(window, text="Monto Total:", font=("Helvetica", 14))
label_monto_total.grid(row=3, column=0, padx=20, pady=10, sticky=W)
entry_monto_total = Entry(window, font=("Helvetica", 14))
entry_monto_total.grid(row=3, column=1, padx=20, pady=10)

label_descripcion = Label(window, text="Descripción de la compra:", font=("Helvetica", 14))
label_descripcion.grid(row=4, column=0, padx=20, pady=10, sticky=W)
entry_descripcion = Entry(window, font=("Helvetica", 14))
entry_descripcion.grid(row=4, column=1, padx=20, pady=10)


# Crear los botones
btn_generar_factura = Button(window, text="Generar Recibo", command=crear_factura, font=("Helvetica", 14))
btn_generar_factura.grid(row=6, column=0, padx=20, pady=10)

btn_nueva_factura = Button(window, text="Nueva Recibo", command=limpiar_campos, font=("Helvetica", 14))
btn_nueva_factura.grid(row=6, column=1, padx=20, pady=10, sticky=E)

# Ejecutar la interfaz
window.mainloop()
