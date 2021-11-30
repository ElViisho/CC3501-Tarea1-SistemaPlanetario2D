# Sistema Planetario 2D
Programa que crea una representación gráfica en 2D, de un sistema planetario descrito
en un archivo `json`.

## Instalación y ejecución
Para poder utilizar la aplicación se necesitan instalar los paquetes requeridos por
el proyecto. Estos se encuentran en el archivo `requeriments.txt` y para instalarlos
se debe correr el comando:
```
pip install -r requeriments.txt
```

Para correr la aplicación, se debe hacer la llamada por consola ubicada en la carpeta de la aplicación:
```
python system_view.py bodies.json
```
Siendo `bodies.json` el archivo `json` donde está la información del sistema planetario. Se puede cambiar
el archivo del que se quiera sacar la información cambiando el último argumento de la llamada anterior.

## Uso
Una vez ejecutada la aplicación, se puede acercar la cámara a los objetos con **Z** y alejar con **X**.
Esta también se puede desplazar con **W**, **A**, **S** y **D**, dentro de una delimitación cerca del sistema.
Se puede seleccionar un cuerpo con las flechas izquierda y derecha, resaltándolo con un círculo blanco alrededor
de él. Al presionar **Enter**, se despliega información sobre el cuerpo seleccionado. Con esa misma tecla se
vuelve a ocultar la información. La información desplegada es genérica para todos los cuerpos.

## Estructura archivo `json`
El archivo `json` contiene una lista jerarquizada de cuerpos celestes que cumple con:
- Color que corresponde a un arreglo con el color en RGB.
- Radius que es el radio del cuerpo celeste.
- Distance es la distancia al cuerpo padre.
- Velocity es la velocidad de traslaci ́on con respecto a su padre, y su signo indica el sentido de rotación (sistema horario)
- Satellites corresponde a una lista de cuerpos celeste que orbitan alrededor, si no tiene se agrega ”Null”.
- El primer cuerpo debe representar la estrella del sistema que se ubicara en el centro, por lo que los datos de Velocity y Distance se ignoran en este caso.

Un ejemplo de archivo `json`:
```
[
    {
        "Color": [ 1, 1, 0 ],
        "Radius": 0.1,
        "Distance": 0.0,
        "Velocity": 0.0,
        "Satellites": [
            {
                "Color": [ 0.0, 0.2, 0.8 ],
                "Radius": 0.03,
                "Distance": 0.25,
                "Velocity": 0.4,
                "Satellites": [
                    {
                    "Color": [ 0.4, 0.4, 0.4 ],
                    "Radius": 0.01,
                    "Distance": 0.07,
                    "Velocity": -0.2,
                    "Satellites": "Null"
                    }
                ]
            },
            {
                "Color": [ 1, 0.3, 0.0 ],
                "Radius": 0.05,
                "Distance": 0.35,
                "Velocity": 0.5,
                "Satellites": "Null"
            }
        ]
    }
]
```
Esto representa una estrella con dos planetas, donde el primero de ellos tiene un satélite