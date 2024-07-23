# Using command line do "pip install requests"
# Internet connection is required for the program to run
# The maximum capacity is 60 runs/min so try staying below it

from tkinter import *
import tkinter.font as font
import requests
import json
import os

api_codigo = os.getenv('OPENWEATHER_API_KEY')

ventana = Tk()
ventana.title("Condiciones Climáticas")

mifuente = font.Font(family='Helvetica', size=20, weight='bold')
mifuentegrande = font.Font(family='Helvetica', size=60, weight='bold')
mifuentepequeña = font.Font(family='Helvetica', size=15)

frame = LabelFrame(ventana)
frame.pack(padx=10, pady=10)

api_codigo = "3e048c850e7bcecc34437519ce82156a"
url_base = "https://api.openweathermap.org/data/2.5/weather?"

def obtener_datos_climaticos(ciudad, api_codigo):
    url_completo = url_base + "appid=" + api_codigo + "&q=" + ciudad
    respuesta = requests.get(url_completo)
    respuesta.raise_for_status()
    datos = respuesta.json()
    if datos.get('cod') != 200:
        raise KeyError("Ciudad no encontrada")
    return datos

def mostrar_datos(frame, datos):
    ciudadog = datos['name']
    pais = datos['sys']['country']
    temperatura_actual = round(datos['main']['temp'] - 273.15, 1)
    sensacion_termica = round(datos['main']['temp'] - 273.15, 1)
    clima = datos['weather'][0]['main']
    temperatura_minima = round(datos['main']['temp_min'] - 273.15, 1)
    temperatura_maxima = round(datos['main']['temp_max'] - 273.15, 1)

    etiqueta1 = Label(frame, text=f"{ciudadog}, {pais}")
    etiqueta1['font'] = mifuente
    etiqueta1.grid(column=1, row=0)

    etiqueta2 = Label(frame, text=f"{temperatura_actual} °C")
    etiqueta2['font'] = mifuentegrande
    etiqueta2.grid(column=1, row=1)

    frame3 = LabelFrame(frame)
    frame3.grid(column=1, row=2, pady=5)

    etiqueta3 = Label(frame3, text=f"Sensación Térmica {sensacion_termica} °C", anchor=W)
    etiqueta3['font'] = mifuentepequeña
    etiqueta3.grid(column=1, row=3, columnspan=2)

    etiqueta4 = Label(frame3, text=clima)
    etiqueta4['font'] = mifuente
    etiqueta4.grid(column=1, row=2)

    etiqueta5 = Label(frame3, text=f"Temperatura mínima/máxima: {temperatura_minima}°/{temperatura_maxima}°")
    etiqueta5['font'] = mifuentepequeña
    etiqueta5.grid(column=1, row=4)

def enviar(event=None):
    ventanaemergente = Toplevel()

    frame2 = LabelFrame(ventanaemergente)
    frame2.pack(padx=10, pady=10)

    ciudad = entry.get().strip()
    if not ciudad:
        etiqueta_error = Label(frame2, text="Por favor ingrese una ciudad.")
        etiqueta_error['font'] = mifuente
        etiqueta_error.grid(column=1, row=0)
        return

    entry.delete(0, END)

    try:
        datos = obtener_datos_climaticos(ciudad, api_codigo)
        mostrar_datos(frame2, datos)
    except requests.exceptions.RequestException as e:
        etiqueta_error = Label(frame2, text="Error al obtener datos: " + str(e))
        etiqueta_error['font'] = mifuente
        etiqueta_error.grid(column=1, row=0)
    except KeyError:
        etiqueta_error = Label(frame2, text="Ciudad no encontrada.")
        etiqueta_error['font'] = mifuente
        etiqueta_error.grid(column=1, row=0)

Label(frame, text="Ingrese el nombre de la ciudad:", font=mifuente).grid(column=1, row=0)
entry = Entry(frame)
entry['font'] = mifuente
entry.grid(column=0, row=1, columnspan=3, padx=10, pady=10, ipadx=50, ipady=5)
entry.bind('<Return>', enviar)  # Vincular la tecla Enter al evento enviar

button = Button(frame, text="Enviar", command=enviar)
button['font'] = mifuente
button.grid(column=1, row=2, ipadx=20, pady=10)

ventana.mainloop()
