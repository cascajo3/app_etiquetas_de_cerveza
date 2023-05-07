# Aplicación de gestión de una DB de etiquetas de cerveza

Funcionamiento de la primera versión con una DB local:

![Vídeo](https://github.com/cascajo3/app_etiquetas_de_cerveza/blob/main/app/demo.gif)

Versión 1.0


*Sin imágenes por ahora*

También se ha hecho utilizando un archivo db en AWS que es público y simplemente se cambia la parte inicial del main por:


    url="url_del_elemento_público_de_s3"
    ruta_local="beer_labels.db"
    urllib.request.urlretrieve(url, ruta_local)
    # Crea una conexión a la base de datos SQLite local
    db = sqlite3.connect(ruta_local)


