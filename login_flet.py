import flet as ft
import json
import os
from database_config import db_manager
from dashboard_flet import main as dashboard_main

CONFIG_FILE = "db_config.json"

def cargar_configuracion():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return None

def guardar_configuracion(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def main(page: ft.Page):
    page.title = "Login - Medisoft"
    page.window_width = 500
    page.window_height = 600
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    config = cargar_configuracion()
    
    # --- Campos de conexión ---
    host = ft.TextField(label="Host", value=db_manager.host)
    puerto = ft.TextField(label="Puerto", value=str(db_manager.port))
    usuario_bd = ft.TextField(label="Usuario BD", value=db_manager.user)
    password_bd = ft.TextField(label="Contraseña BD", password=True, can_reveal_password=True, value=db_manager.password)
    dbname = ft.TextField(label="Base de Datos", value=db_manager.database)
    
    # --- Campos de login ---
    usuario = ft.TextField(label="Usuario")
    password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True)
    mensaje = ft.Text(value="", color="red")

    def aplicar_config():
        db_manager.host = host.value
        db_manager.port = int(puerto.value)
        db_manager.user = usuario_bd.value
        db_manager.password = password_bd.value
        db_manager.database = dbname.value

    def probar_conexion(e):
        aplicar_config()
        if db_manager.connect():
            guardar_configuracion({
                'host': db_manager.host,
                'port': db_manager.port,
                'user': db_manager.user,
                'password': db_manager.password,
                'database': db_manager.database
            })
            mensaje.value = "Conexión exitosa. Configuración guardada."
            mensaje.color = "green"
        else:
            mensaje.value = "No se pudo conectar a la base de datos."
            mensaje.color = "red"
        page.update()

    def crear_bd(e):
        aplicar_config()
        try:
            db_manager.create_database()
            db_manager.create_tables()
            guardar_configuracion({
                'host': db_manager.host,
                'port': db_manager.port,
                'user': db_manager.user,
                'password': db_manager.password,
                'database': db_manager.database
            })
            mensaje.value = "Base de datos y tablas creadas. Configuración guardada."
            mensaje.color = "green"
        except Exception as ex:
            mensaje.value = f"Error al crear la base de datos: {str(ex)}"
            mensaje.color = "red"
        page.update()

    def login(e):
        from werkzeug.security import check_password_hash
        db_manager.connect()
        query = "SELECT * FROM usuario WHERE username = %s"
        params = (usuario.value,)
        result = db_manager.execute_query(query, params)
        if result and len(result) > 0:
            usuario_db = result[0]
            if check_password_hash(usuario_db["password_hash"], password.value):
                nombre = usuario_db.get("nombre_completo", usuario.value)
                rol = usuario_db.get("rol", "usuario")
                page.clean()
                dashboard_main(page, usuario_nombre=nombre, usuario_rol=rol)
            else:
                mensaje.value = "Usuario o contraseña incorrectos"
                mensaje.color = "red"
                page.update()
        else:
            mensaje.value = "Usuario o contraseña incorrectos"
            mensaje.color = "red"
            page.update()
    def mostrar_registro(e):
        page.clean()
        nuevo_usuario = ft.TextField(label="Nuevo usuario")
        nuevo_email = ft.TextField(label="Email")
        nuevo_nombre = ft.TextField(label="Nombre completo")
        nuevo_password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True)
        nuevo_rol = ft.TextField(label="Rol")
        mensaje_registro = ft.Text(value="", color="red")

        def registrar_usuario(ev):
            from werkzeug.security import generate_password_hash
            db_manager.connect()
            query = "INSERT INTO usuario (username, email, password_hash, rol, nombre_completo, activo) VALUES (%s, %s, %s, %s, %s, %s)"
            params = (
                nuevo_usuario.value,
                nuevo_email.value,
                generate_password_hash(nuevo_password.value),
                nuevo_rol.value,
                nuevo_nombre.value,
                True
            )
            try:
                db_manager.execute_query(query, params)
                mensaje_registro.value = "Usuario registrado exitosamente."
                mensaje_registro.color = "green"
            except Exception as ex:
                mensaje_registro.value = f"Error: {str(ex)}"
                mensaje_registro.color = "red"
            page.update()

        page.add(
            ft.Column([
                ft.Text("Registro de Usuario", size=18, weight=ft.FontWeight.BOLD),
                nuevo_usuario,
                nuevo_email,
                nuevo_nombre,
                nuevo_password,
                nuevo_rol,
                ft.ElevatedButton("Registrar", on_click=registrar_usuario),
                ft.ElevatedButton("Volver al Login", on_click=lambda _: page.clean() or main(page)),
                mensaje_registro
            ], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        from werkzeug.security import check_password_hash
        if not config:
            aplicar_config()
        db_manager.connect()
        query = "SELECT * FROM usuario WHERE username = %s"
        params = (usuario.value,)
        result = db_manager.execute_query(query, params)
        if result and len(result) > 0:
            usuario_db = result[0]
            if check_password_hash(usuario_db["password_hash"], password.value):
                nombre = usuario_db.get("nombre_completo", usuario.value)
                rol = usuario_db.get("rol", "usuario")
                page.clean()
                dashboard_main(page, usuario_nombre=nombre, usuario_rol=rol)
            else:
                mensaje.value = "Usuario o contraseña incorrectos"
                mensaje.color = "red"
                page.update()
        else:
            mensaje.value = "Usuario o contraseña incorrectos"
            mensaje.color = "red"
            page.update()

    # Layouts
    elementos = []
    if not config:
        elementos.extend([
            ft.Text("Parámetros de Base de Datos", size=18, weight=ft.FontWeight.BOLD),
            host, puerto, usuario_bd, password_bd, dbname,
            ft.Row([
                ft.ElevatedButton("Probar Conexión", on_click=probar_conexion),
                ft.ElevatedButton("Crear Base de Datos", on_click=crear_bd)
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider()
        ])
    else:
        # Aplicar config a db_manager
        db_manager.host = config['host']
        db_manager.port = config['port']
        db_manager.user = config['user']
        db_manager.password = config['password']
        db_manager.database = config['database']
    elementos.extend([
        ft.Text("Login de Usuario", size=18, weight=ft.FontWeight.BOLD),
        usuario, password,
        ft.Row([
            ft.ElevatedButton("Iniciar Sesión", on_click=login),
            ft.ElevatedButton("Registro", on_click=mostrar_registro)
        ], alignment=ft.MainAxisAlignment.CENTER),
        mensaje
    ])
    page.add(ft.Column(elementos, tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER))

if __name__ == "__main__":
    import flet
    flet.app(target=main) 