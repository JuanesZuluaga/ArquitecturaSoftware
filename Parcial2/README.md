# Diseño modificado
Buscaria que el json se guarde y este se pueda transportar a una url diferente con una funcion de carga que envie el json 
```
def historial(numero, factorial, etiqueta):
    payload = {
        "numero": numero,
        "factorial": factorial,
        "etiqueta": etiqueta
    }
    requests.post(URL_db, json=payload)
```
luego verifico si se me indica que tambien se quiere visualizar como esta el codigo por defecto o se elimina la funcion 
