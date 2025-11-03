from app import app, db
from sqlalchemy import text

with app.app_context():
    connection = db.engine.connect()
    try:
        # Primero agregar la columna sin UNIQUE
        connection.execute(text("ALTER TABLE bioanalista ADD COLUMN rif VARCHAR(20)"))
        print("✓ Columna 'rif' agregada a bioanalista")
        
        # Crear un índice único después
        connection.execute(text("CREATE UNIQUE INDEX idx_bioanalista_rif ON bioanalista(rif)"))
        print("✓ Índice único creado para 'rif'")
        
        connection.commit()
        print("\n✅ RIF agregado exitosamente a bioanalista")
    except Exception as e:
        print(f"Nota: {e}")
    finally:
        connection.close()
