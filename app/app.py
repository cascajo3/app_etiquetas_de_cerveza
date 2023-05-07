from kivy.config import Config
Config.set('graphics', 'resizable', 0)
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
import sqlite3
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.config import Config
from kivy.uix.image import Image
from kivy.clock import Clock
import math
from kivy.uix.widget import Widget



class ResultsWindow(Popup):
    MAX_CLICKS = 5 # Límite de clics antes de borrar

    num_clicks = 0 # Variable de clase para contar los clics
    def __init__(self, result,db, **kwargs):
        super().__init__(**kwargs)
        num_results = len(result)
        self.title = f"Resultados de búsqueda ({num_results})"
        # Calcular el valor de size_hint_y a partir de num_results
        size_hint_y = 0.22*(num_results+1)
        #size_hint_y = 0.4*(num_results+1)
        layout = GridLayout(cols=4, size_hint_y=size_hint_y, row_force_default=True, row_default_height=70)
        def delete_label(name):
            self.num_clicks += 1
            if self.num_clicks == self.MAX_CLICKS:
                cursor = db.cursor()
                cursor.execute("DELETE FROM etiquetas_cerveza WHERE nombre=?", (name,))
                db.commit()
                cursor.close()
                self.dismiss() # Cerrar el pop-up después de borrar el registro
            else:
                # Mostrar mensaje con la cantidad de clics restantes necesarios
                remaining_clicks = self.MAX_CLICKS - self.num_clicks
                message = f"Para eliminar el registro, debes tocar {remaining_clicks} veces más"

        for row in result:
            layout.add_widget(Label(text='Nombre:'))
            layout.add_widget(Label(text=row[0]))

            layout.add_widget(Label(text='Compañía:'))
            layout.add_widget(Label(text=row[1]))

            layout.add_widget(Label(text='Tipo:'))
            layout.add_widget(Label(text=row[2]))

            layout.add_widget(Label(text='País:'))
            layout.add_widget(Label(text=row[4]))
            
            layout.add_widget(Label(text='Región:'))
            layout.add_widget(Label(text=row[5]))
            empty_widget = Widget(size_hint_y=0.1)
            layout.add_widget(empty_widget)
            delete_button = Button(text='Eliminar', size_hint=(0.3, 0.8), font_size=15)
            delete_button.bind(on_press=lambda _, name=row[0]: delete_label(name))
            layout.add_widget(delete_button)
            line1 = Label(text='------------------------', color=(1, 0.5, 0, 1))
            line2 = Label(text='------------------------', color=(1, 0.5, 0, 1))
            line3 = Label(text='------------------------', color=(1, 0.5, 0, 1))
            line4 = Label(text='------------------------', color=(1, 0.5, 0, 1))
            layout.add_widget(line1)
            layout.add_widget(line2)
            layout.add_widget(line3)
            layout.add_widget(line4)
        
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(layout)

        self.content = scroll_view

class BeerLabelDatabaseApp(App):
    
    def build(self):
        self.icon='logocervezasdeetiqueta.png'
        # Crea una conexión a la base de datos SQLite local
        db = sqlite3.connect('beer_labels.db')
        
        # Crea una tabla para almacenar las etiquetas de cerveza
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS etiquetas_cerveza
                          (nombre TEXT, compania TEXT, tipo TEXT, imagen TEXT, pais TEXT, region TEXT)''')
        db.commit()

        # Define una función que agrega una etiqueta de cerveza a la base de datos
        def add_label(name, company, type, image, country, region):
            cursor = db.cursor()
            sql = "INSERT INTO etiquetas_cerveza (nombre, compania, tipo, imagen, pais, region) VALUES (?, ?, ?, ?, ?, ?)"
            values = (name, company, type, image, country, region)
            cursor.execute(sql, values)
            db.commit()
            cursor.close()

        # Define una función que busca una etiqueta de cerveza por nombre en la base de datos
        def search_label(name, company, tipo, country, region):
            cursor = db.cursor()
            sql = "SELECT * FROM etiquetas_cerveza WHERE 1=1"
            values = []
            if name:
                sql += " AND nombre LIKE ?"
                values.append('%'+name+'%')
            if company:
                sql += " AND compania LIKE ?"
                values.append('%'+company+'%')
            if tipo:
                sql += " AND tipo LIKE ?"
                values.append('%'+tipo+'%')
            if country:
                sql += " AND pais LIKE ?"
                values.append('%'+country+'%')
            if region:
                sql += " AND region LIKE ?"
                values.append('%'+region+'%')
            sql += " ORDER BY nombre"
            cursor.execute(sql, values)
            result = cursor.fetchall()
            cursor.close()
            return result

        # Define la interfaz de usuario
        layout = GridLayout(cols=2)
        # Agregar un Widget BoxLayout centrado con el título de la base de datos
        layout.add_widget(BoxLayout(size_hint=(None, 2), size=(10, 10)))
        title_label = Label(text='Etiquetas de cerveza', font_size=30, size_hint_x=None, width=300)
        layout.add_widget(title_label)

        layout.add_widget(Label(text='Nombre de la etiqueta:'))
        name_input = TextInput(multiline=False)
        layout.add_widget(name_input)

        layout.add_widget(Label(text='Compañía:'))
        company_input = TextInput(multiline=False)
        layout.add_widget(company_input)

        layout.add_widget(Label(text='Tipo de cerveza:'))
        type_input = TextInput(multiline=False)
        layout.add_widget(type_input)

        layout.add_widget(Label(text='Imagen:'))
        image_input = TextInput(multiline=False)
        layout.add_widget(image_input)

        layout.add_widget(Label(text='País de origen:'))
        country_input = TextInput(multiline=False)
        layout.add_widget(country_input)

        layout.add_widget(Label(text='Región:'))
        region_input = TextInput(multiline=False)
        layout.add_widget(region_input)

        # Define los botones para agregar y buscar etiquetas
        def add_label_button(instance):
            name = name_input.text
            company = company_input.text
            type = type_input.text
            image = image_input.text
            country = country_input.text
            region = region_input.text
            add_label(name, company, type, image, country, region)
            name_input.text = ''
            company_input.text = ''
            type_input.text = ''
            image_input.text = ''
            country_input.text = ''
            region_input.text = ''
            
        def search_label_button(instance):
            name = name_input.text
            company = company_input.text
            type = type_input.text
            country = country_input.text
            region = region_input.text
            result = search_label(name,company,type,country,region)
            if len(result) == 0:
                # Si no se encuentra ninguna etiqueta en la base de datos, muestra un mensaje de error
                error_popup = Popup(title='Error', content=Label(text='No se encontró la etiqueta de cerveza'), size_hint=(None, None), size=(400, 400))
                error_popup.open()
            else:
                # Si se encuentra una o más etiquetas, muestra la ventana de resultados
                results_popup = ResultsWindow(result=result,db=db)
                results_popup.open()
            name_input.text = ''
            company_input.text = ''
            type_input.text = ''
            image_input.text = ''
            country_input.text = ''
            region_input.text = ''

        layout.add_widget(Label(text=''))
        add_button = Button(text='Agregar', size_hint_x=None, width=300,background_color=(1, 0.5, 0, 1))
        add_button.bind(on_press=add_label_button)
        layout.add_widget(add_button)

        layout.add_widget(Label(text=''))
        search_button = Button(text='Buscar', size_hint_x=None, width=300,background_color=(0, 1, 0, 1))
        search_button.bind(on_press=search_label_button)
        layout.add_widget(search_button)
        Config.set('graphics', 'resizable', True)
        # Crea un Image widget para mostrar el logo de la cuenta
        logo_image = Image(source='logocervezasdeetiqueta.png', size_hint=(0, 4), width=100, keep_ratio=True, allow_stretch=False, pos_hint={"x": 0, "y": 1})
        layout.add_widget(logo_image)
        return layout


if __name__ == '__main__':
    BeerLabelDatabaseApp().run()
