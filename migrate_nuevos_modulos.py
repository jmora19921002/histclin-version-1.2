"""
Script para migrar la base de datos con los nuevos módulos agregados
Ejecutar: python migrate_nuevos_modulos.py
"""

from app import app, db
from app import (
    Proveedor, Cita, TurnoMedico, Recordatorio,
    Prescripcion, PlantillaPrescripcion,
    Cama, RondaMedica, SignosVitales, PreAlta,
    Mensaje, NotaCompartida, Alerta, Comunicado,
    RecepcionPaciente, PlantillaDocumento, ConfiguracionAlerta
)

def migrate():
    with app.app_context():
        print("Creando nuevas tablas en la base de datos...")
        
        try:
            # Crear todas las tablas nuevas
            db.create_all()
            print("✓ Tablas creadas exitosamente")
            
            # Crear algunos datos de ejemplo opcionales
            print("\n¿Deseas crear datos de ejemplo? (s/n)")
            respuesta = input().lower()
            
            if respuesta == 's':
                crear_datos_ejemplo()
            
            print("\n✓ Migración completada exitosamente")
            
        except Exception as e:
            print(f"✗ Error durante la migración: {e}")
            import traceback
            traceback.print_exc()

def crear_datos_ejemplo():
    """Crear algunos datos de ejemplo para los nuevos módulos"""
    
    print("\nCreando datos de ejemplo...")
    
    # Ejemplo: Proveedor
    if not Proveedor.query.first():
        proveedor = Proveedor(
            rif="J-12345678-9",
            razon_social="Farmacia Central C.A.",
            contacto="Juan Pérez",
            telefono="0212-1234567",
            email="contacto@farmaciacentral.com",
            direccion="Av. Principal, Caracas",
            tipo="medicamentos"
        )
        db.session.add(proveedor)
        print("  ✓ Proveedor de ejemplo creado")
    
    # Ejemplo: Cama
    if not Cama.query.first():
        for i in range(1, 11):
            cama = Cama(
                numero=f"CAMA-{i:02d}",
                piso=f"Piso {(i-1)//5 + 1}",
                tipo="general" if i <= 8 else "UCI",
                ocupada=False
            )
            db.session.add(cama)
        print("  ✓ 10 camas de ejemplo creadas")
    
    # Ejemplo: Plantilla de Documento
    if not PlantillaDocumento.query.first():
        plantilla = PlantillaDocumento(
            nombre="Receta Médica Estándar",
            tipo="receta",
            contenido_html="""
            <div style="padding: 20px;">
                <h2>RECETA MÉDICA</h2>
                <p><strong>Paciente:</strong> {{paciente_nombre}}</p>
                <p><strong>Fecha:</strong> {{fecha}}</p>
                <hr>
                <h3>Medicamentos:</h3>
                {{medicamentos}}
                <hr>
                <p>{{observaciones}}</p>
                <div style="margin-top: 50px;">
                    <p>_______________________</p>
                    <p>Firma del Médico</p>
                </div>
            </div>
            """,
            variables='["paciente_nombre", "fecha", "medicamentos", "observaciones"]'
        )
        db.session.add(plantilla)
        print("  ✓ Plantilla de receta de ejemplo creada")
    
    try:
        db.session.commit()
        print("\n✓ Datos de ejemplo creados exitosamente")
    except Exception as e:
        db.session.rollback()
        print(f"\n✗ Error al crear datos de ejemplo: {e}")

if __name__ == '__main__':
    print("=" * 60)
    print("MIGRACIÓN DE BASE DE DATOS - NUEVOS MÓDULOS")
    print("=" * 60)
    print("\nEste script agregará las siguientes tablas:")
    print("  - Proveedores")
    print("  - Citas y Agenda")
    print("  - Prescripciones")
    print("  - Camas y Hospitalización ampliada")
    print("  - Mensajes y Comunicación")
    print("  - Recepción de Pacientes")
    print("  - Plantillas y Configuración")
    print("\n¿Deseas continuar? (s/n)")
    
    respuesta = input().lower()
    if respuesta == 's':
        migrate()
    else:
        print("Migración cancelada")
