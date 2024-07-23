# Using command line do "pip install requests"
# Internet connection is required for the program to run
# The maximum capacity is 60 runs/min so try staying below it

from tkinter import *
import tkinter.font as font
import requests
import json

ventana = Tk()
ventana.title("Condiciones Climáticas")

mifuente = font.Font(family='Helvetica', size=20, weight='bold')
mifuentegrande = font.Font(family='Helvetica', size=60, weight='bold')
mifuentepequeña = font.Font(family='Helvetica', size=15)

frame = LabelFrame(ventana)
frame.pack(padx=10, pady=10)

def enviar():
    ventanaemergente = Toplevel()

    frame2 = LabelFrame(ventanaemergente)
    frame2.pack(padx=10, pady=10)

    ciudad = entry.get()
    entry.delete(0, END)

    url_completo = url_base + "appid=" + api_codigo + "&q=" + ciudad

    try:
        respuesta = requests.get(url_completo)
        respuesta.raise_for_status()
        x = respuesta.json()
        if x.get('cod') != 200:
            raise KeyError
    except requests.exceptions.RequestException as e:
        etiqueta_error = Label(frame2, text="Error al obtener datos ups: " + str(e))
        etiqueta_error['font'] = mifuente
        etiqueta_error.grid(column=1, row=0)
        return
    except KeyError:
        etiqueta_error = Label(frame2, text="Ciudad no encontrada.")
        etiqueta_error['font'] = mifuente
        etiqueta_error.grid(column=1, row=0)
        return

    ciudadog = x['name']
    pais = x['sys']['country']
    temperatura_actual = round(x['main']['temp'] - 273.15, 1)
    sensacion_termica = round(x['main']['temp'] - 273.15, 1)
    clima = x['weather'][0]['main']
    temperatura_minima = round(x['main']['temp_min'] - 273.15, 1)
    temperatura_maxima = round(x['main']['temp_max'] - 273.15, 1)

    etiqueta1 = Label(frame2, text=ciudadog + ", " + pais)
    etiqueta1['font'] = mifuente
    etiqueta1.grid(column=1, row=0)

    etiqueta2 = Label(frame2, text=str(temperatura_actual) + " °C")
    etiqueta2['font'] = mifuentegrande
    etiqueta2.grid(column=1, row=1)

    frame3 = LabelFrame(frame2)
    frame3.grid(column=1, row=2, pady=5)

    etiqueta3 = Label(frame3, text="Sensación Térmica " + str(sensacion_termica) + " °C", anchor=W)
    etiqueta3['font'] = mifuentepequeña
    etiqueta3.grid(column=1, row=3, columnspan=2)

    etiqueta4 = Label(frame3, text=clima)
    etiqueta4['font'] = mifuente
    etiqueta4.grid(column=1, row=2)

    etiqueta5 = Label(frame3, text="Temperatura mínima/máxima: " + str(temperatura_minima) + "°/" + str(temperatura_maxima) + "°")
    etiqueta5['font'] = mifuentepequeña
    etiqueta5.grid(column=1, row=4)

api_codigo = "3e048c850e7bcecc34437519ce82156a"

url_base = "https://api.openweathermap.org/data/2.5/weather?"

Label(frame, text="Ingrese el nombre de la ciudad:", font=mifuente).grid(column=1, row=0)
entry = Entry(frame)
entry['font'] = mifuente
entry.grid(column=0, row=1, columnspan=3, padx=10, pady=10, ipadx=50, ipady=5)

button = Button(frame, text="Enviar", command=enviar)
button['font'] = mifuente
button.grid(column=1, row=2, ipadx=20, pady=10)

ventana.mainloop()
