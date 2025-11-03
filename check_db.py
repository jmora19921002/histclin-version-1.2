from app import app, db, Usuario
from werkzeug.security import generate_password_hash

print("=== Verificando Base de Datos ===\n")

with app.app_context():
    try:
        # Verificar si existen usuarios
        usuarios = Usuario.query.all()
        print(f"Total de usuarios en la BD: {len(usuarios)}")
        
        if usuarios:
            print("\nUsuarios existentes:")
            for u in usuarios:
                print(f"  - Username: {u.username}, Email: {u.email}, Rol: {u.rol}, Activo: {u.activo}")
        else:
            print("\n⚠️ No hay usuarios en la base de datos")
            respuesta = input("\n¿Deseas crear un usuario administrador? (s/n): ")
            if respuesta.lower() == 's':
                username = input("Username: ")
                email = input("Email: ")
                password = input("Password: ")
                nombre_completo = input("Nombre completo: ")
                
                nuevo_usuario = Usuario(
                    username=username,
                    email=email,
                    password_hash=generate_password_hash(password),
                    rol='administrador',
                    nombre_completo=nombre_completo,
                    activo=True
                )
                
                db.session.add(nuevo_usuario)
                db.session.commit()
                print("\n✅ Usuario administrador creado exitosamente")
                print(f"Username: {username}")
                print(f"Email: {email}")
        
        # Verificar estructura de tabla Usuario
        print("\n=== Estructura de tabla Usuario ===")
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        columns = inspector.get_columns('usuario')
        print("Columnas:")
        for col in columns:
            print(f"  - {col['name']}: {col['type']}")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPosible solución: La base de datos podría estar corrupta o no inicializada")
        print("Ejecuta: python init_db.py")
