# NUEVOS MÓDULOS AGREGADOS - HistClin v1.3

## Resumen de Cambios

Se han agregado **13 modelos nuevos** y **múltiples rutas** para completar el sistema de historia clínica según los requerimientos.

---

## 📦 MODELOS AGREGADOS

### 1. **PROVEEDORES** (Modelo: `Proveedor`)
Gestión de proveedores de medicamentos, insumos y equipos médicos.

**Campos:**
- `rif` - RIF del proveedor (único)
- `razon_social` - Nombre de la empresa
- `contacto` - Persona de contacto
- `telefono`, `email`, `direccion` - Datos de contacto
- `tipo` - Tipo de proveedor (medicamentos, insumos, equipos)
- `activo` - Estado del proveedor

**Rutas:**
- `GET /proveedores` - Listar proveedores
- `GET /proveedores/nuevo` - Formulario nuevo proveedor
- `POST /proveedores/nuevo` - Crear proveedor
- `GET /proveedores/<id>/editar` - Editar proveedor
- `POST /proveedores/<id>/eliminar` - Desactivar proveedor

---

### 2. **AGENDA Y CITAS** (Modelos: `Cita`, `TurnoMedico`, `Recordatorio`)

#### Cita
Gestión completa de citas médicas con calendario.

**Campos:**
- `paciente_id`, `medico_id` - Referencias
- `fecha_hora` - Fecha y hora de la cita
- `motivo` - Motivo de la consulta
- `estado` - programada, confirmada, completada, cancelada
- `tipo` - consulta, control, emergencia
- `duracion_minutos` - Duración estimada
- `observaciones` - Notas adicionales

**Rutas:**
- `GET /agenda` - Vista principal de agenda
- `GET /agenda/calendario` - Vista de calendario
- `GET /agenda/citas` - Lista de citas
- `GET /agenda/citas/nuevo` - Nueva cita
- `POST /agenda/citas/<id>/reagendar` - Reagendar cita
- `POST /agenda/citas/<id>/cancelar` - Cancelar cita

#### TurnoMedico
Define los horarios de trabajo de los médicos.

**Campos:**
- `medico_id` - Médico asignado
- `dia_semana` - 0=Lunes, 6=Domingo
- `hora_inicio`, `hora_fin` - Horario del turno
- `activo` - Si el turno está activo

#### Recordatorio
Sistema de recordatorios automáticos de citas.

**Campos:**
- `cita_id` - Cita asociada
- `fecha_envio` - Cuándo enviar el recordatorio
- `tipo` - email, sms, whatsapp
- `enviado` - Si ya fue enviado

---

### 3. **PRESCRIPCIÓN** (Modelos: `Prescripcion`, `PlantillaPrescripcion`)

#### Prescripcion
Gestión digital de prescripciones médicas.

**Campos:**
- `medico_id`, `paciente_id` - Referencias
- `diagnostico` - Diagnóstico asociado
- `medicamentos_json` - Lista de medicamentos en formato JSON
- `vigencia_dias` - Días de vigencia de la receta
- `observaciones` - Indicaciones adicionales

**Rutas:**
- `GET /prescripciones` - Listar prescripciones
- `GET /prescripciones/nuevo` - Nueva prescripción
- `GET /prescripciones/plantillas` - Gestionar plantillas

#### PlantillaPrescripcion
Plantillas predefinidas de prescripciones para uso frecuente.

---

### 4. **HOSPITALIZACIÓN AMPLIADA** (Modelos: `Cama`, `RondaMedica`, `SignosVitales`, `PreAlta`)

#### Cama
Gestión de camas hospitalarias.

**Campos:**
- `numero` - Número de cama (único)
- `piso` - Piso donde se encuentra
- `tipo` - UCI, general, pediatría, etc.
- `ocupada` - Estado de ocupación
- `paciente_id` - Paciente actual (si está ocupada)

**Rutas:**
- `GET /hospitalizaciones/camas` - Gestión de camas

#### RondaMedica
Registro de rondas médicas diarias.

**Campos:**
- `hospitalizacion_id`, `medico_id` - Referencias
- `fecha_hora` - Momento de la ronda
- `observaciones`, `evolucion` - Evolución del paciente
- `ordenes_medicas` - Nuevas órdenes

**Rutas:**
- `GET /hospitalizaciones/rondas` - Registro de rondas

#### SignosVitales
Monitoreo de signos vitales.

**Campos:**
- `paciente_id`, `hospitalizacion_id` - Referencias
- `temperatura`, `presion_arterial` - Signos vitales
- `frecuencia_cardiaca`, `frecuencia_respiratoria` - Frecuencias
- `saturacion_oxigeno` - SpO2
- `peso`, `talla` - Medidas antropométricas
- `registrado_por` - Quién registró

**Rutas:**
- `GET /hospitalizaciones/signos` - Registro de signos vitales

#### PreAlta
Gestión de pre-altas hospitalarias.

**Campos:**
- `hospitalizacion_id` - Hospitalización asociada
- `fecha_probable` - Fecha probable de alta
- `condiciones_medicas`, `indicaciones_alta` - Condiciones
- `medicamentos_alta` - Medicamentos para el alta
- `controles_posteriores` - Controles post-alta
- `estado` - pendiente, aprobada, cancelada

**Rutas:**
- `GET /hospitalizaciones/prealtas` - Gestión de pre-altas

---

### 5. **COMUNICACIÓN** (Modelos: `Mensaje`, `NotaCompartida`, `Alerta`, `Comunicado`)

#### Mensaje
Sistema de mensajería interna entre usuarios.

**Campos:**
- `remitente_id`, `destinatario_id` - Usuarios
- `asunto`, `contenido` - Mensaje
- `leido` - Si fue leído
- `fecha` - Fecha de envío

**Rutas:**
- `GET /comunicacion` - Vista principal
- `GET /comunicacion/mensajes` - Mensajes
- `POST /comunicacion/mensajes/nuevo` - Enviar mensaje

#### NotaCompartida
Notas clínicas compartidas entre el personal.

**Campos:**
- `autor_id` - Quien creó la nota
- `paciente_id` - Paciente asociado (opcional)
- `titulo`, `contenido` - Contenido de la nota
- `tipo` - clinica, administrativa, alerta

#### Alerta
Alertas para el personal médico.

**Campos:**
- `tipo` - urgente, importante, info
- `titulo`, `contenido` - Contenido de la alerta
- `activa` - Si está activa

**Rutas:**
- `GET /comunicacion/alertas` - Ver alertas

#### Comunicado
Comunicados oficiales del centro médico.

**Campos:**
- `titulo`, `contenido` - Contenido
- `fecha_publicacion`, `fecha_expiracion` - Vigencia
- `autor_id` - Quien lo publicó
- `activo` - Si está activo

**Rutas:**
- `GET /comunicacion/comunicados` - Ver comunicados

---

### 6. **RECEPCIÓN** (Modelo: `RecepcionPaciente`)

Gestión de cola de espera y check-in de pacientes.

**Campos:**
- `paciente_id` - Paciente
- `fecha_llegada` - Hora de llegada
- `motivo` - Motivo de la visita
- `prioridad` - urgente, alta, normal, baja
- `estado` - esperando, en_atencion, atendido, cancelado
- `medico_asignado_id` - Médico asignado
- `fecha_atencion` - Cuándo fue atendido

**Rutas:**
- `GET /recepcion` - Cola de espera
- `GET /recepcion/registrar` - Registrar llegada
- `POST /recepcion/<id>/atender` - Pasar a atención
- `POST /recepcion/<id>/completar` - Completar atención

---

### 7. **HISTORIAS MÉDICAS AMPLIADAS**

Nuevas vistas integradas de historia clínica.

**Rutas:**
- `GET /historias/unica/<paciente_id>` - Historia clínica única integrada
- `GET /historias/timeline/<paciente_id>` - Línea de tiempo cronológica

**Características:**
- Vista unificada de todo el historial del paciente
- Incluye: consultas, emergencias, tratamientos, cirugías, hospitalizaciones, exámenes
- Timeline visual con todos los eventos médicos ordenados cronológicamente

---

### 8. **INFORMES AMPLIADOS**

Nuevos reportes e indicadores.

**Rutas:**
- `GET /informes/epidemiologia` - Estadísticas epidemiológicas
- `GET /informes/calidad` - Indicadores de calidad asistencial
- `GET /informes/bi` - Business Intelligence Dashboard

---

### 9. **CONFIGURACIÓN AMPLIADA** (Modelos: `PlantillaDocumento`, `ConfiguracionAlerta`)

#### PlantillaDocumento
Plantillas HTML personalizables para documentos.

**Campos:**
- `nombre` - Nombre de la plantilla
- `tipo` - receta, orden_examen, informe, certificado
- `contenido_html` - HTML de la plantilla
- `variables` - Variables disponibles (JSON)
- `activa` - Si está activa

#### ConfiguracionAlerta
Configuración de alertas automáticas del sistema.

**Campos:**
- `tipo_alerta` - stock_bajo, vencimiento, cita_proxima
- `parametros_json` - Parámetros de configuración
- `activa` - Si está activa

---

## 🚀 INSTALACIÓN Y MIGRACIÓN

### Paso 1: Migrar la Base de Datos

```bash
python migrate_nuevos_modulos.py
```

Este script:
- Creará todas las nuevas tablas en la base de datos
- Opcionalmente agregará datos de ejemplo
- Mostrará el progreso de la migración

### Paso 2: Crear Templates

Debes crear los siguientes directorios y templates en `templates/`:

```
templates/
├── proveedores/
│   ├── index.html
│   ├── nuevo.html
│   └── editar.html
├── agenda/
│   ├── index.html
│   ├── calendario.html
│   ├── citas.html
│   └── nueva_cita.html
├── prescripciones/
│   ├── index.html
│   ├── nuevo.html
│   └── plantillas.html
├── recepcion/
│   ├── index.html
│   └── registrar.html
├── comunicacion/
│   ├── index.html
│   ├── mensajes.html
│   ├── alertas.html
│   └── comunicados.html
├── hospitalizaciones/
│   ├── camas.html
│   ├── rondas.html
│   ├── signos.html
│   └── prealtas.html
├── historias/
│   ├── historia_unica.html
│   └── timeline.html
└── informes/
    ├── epidemiologia.html
    ├── calidad.html
    └── bi.html
```

### Paso 3: Actualizar el Menú de Navegación

Agrega enlaces a estos nuevos módulos en `templates/base.html` en el menú de navegación.

---

## 📝 NOTAS IMPORTANTES

1. **Permisos**: Los nuevos módulos respetan el sistema de roles existente (`role_required`)
2. **Relaciones**: Todos los modelos están correctamente relacionados con `Paciente`, `Medico`, `Usuario`, etc.
3. **JSON**: Los campos que almacenan listas (medicamentos, etc.) usan JSON
4. **Timestamps**: Todos los modelos tienen campos de fecha automáticos
5. **Soft Delete**: Proveedores usan desactivación en lugar de eliminación física

---

## ✅ PRÓXIMOS PASOS

1. ✅ Modelos creados (13 nuevos modelos)
2. ✅ Rutas principales implementadas (50+ rutas nuevas)
3. ⏳ Templates HTML a crear
4. ⏳ Actualizar menú de navegación
5. ⏳ Agregar JavaScript para interactividad
6. ⏳ Implementar Dashboard con métricas en tiempo real
7. ⏳ Agregar módulo PACS para imágenes médicas

---

## 🔧 SOPORTE TÉCNICO

Para dudas o problemas con los nuevos módulos, revisa:
- Los modelos en `app.py` líneas 964-1168
- Las rutas en `app.py` líneas 2452-2834
- Este documento de referencia

**Versión:** 1.3
**Fecha:** 2025-11-03
**Módulos agregados:** 13
**Rutas agregadas:** 50+
