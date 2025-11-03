from app import app, db, Usuario

with app.app_context():
    admin = Usuario.query.filter_by(username='admin').first()
    if admin:
        # Actualizar campos faltantes
        admin.nombre_completo = 'Administrador del Sistema'
        admin.activo = True
        db.session.commit()
        print("✅ Usuario admin actualizado correctamente")
        print(f"Username: {admin.username}")
        print(f"Email: {admin.email}")
        print(f"Nombre completo: {admin.nombre_completo}")
        print(f"Rol: {admin.rol}")
        print(f"Activo: {admin.activo}")
    else:
        print("❌ No se encontró el usuario admin")
