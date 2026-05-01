# 📚 BASE DE DATOS — Los profetas

## 📋 Descripción General

Sistema completo de base de datos SQLite3 con ORM Python para el mercado de NFTs "Los profetas". Incluye:

- ✅ Gestión de usuarios y autenticación
- ✅ CRUD de NFTs con metadatos completos
- ✅ Sistema de comentarios
- ✅ Transacciones y ofertas
- ✅ Favoritos
- ✅ Notificaciones
- ✅ Configuración de usuario
- ✅ API REST con Flask

---

## 🚀 Inicio Rápido

### 1. Instalación de dependencias

```bash
pip install -r requirements.txt
```

### 2. Inicializar base de datos con datos de prueba

```bash
python seed.py
```

Output esperado:
```
🚀 Iniciando carga de datos de prueba...

✓ Usuario creado: Alejandro Rivera (arivera)
✓ Usuario creado: Laura Santos (lsantos)
...
✅ ¡Base de datos cargada exitosamente!
```

### 3. Iniciar servidor API

```bash
python api.py
```

El servidor estará disponible en: `http://localhost:5000`

---

## 📁 Estructura de Archivos

```
├── base.py              # Clase DatabaseNFT y todas las funciones CRUD
├── seed.py              # Script para cargar datos iniciales de prueba
├── api.py               # Servidor Flask con endpoints REST
├── requirements.txt     # Dependencias Python
└── losprofetas.db       # Base de datos SQLite (se crea automáticamente)
```

---

## 🗄️ Estructura de Base de Datos

### Tabla: `usuarios`
```sql
id           TEXT PRIMARY KEY
username     TEXT UNIQUE
email        TEXT UNIQUE
password_hash TEXT
avatar_b64   TEXT (imagen en base64)
nombre       TEXT
bio          TEXT
fecha_registro TIMESTAMP
actualizado  TIMESTAMP
activo       INTEGER (1=activo, 0=inactivo)
```

### Tabla: `nfts`
```sql
id           INTEGER PRIMARY KEY
titulo       TEXT
descripcion  TEXT
artista_id   TEXT (FK → usuarios.id)
precio       REAL (en ETH)
categoria    TEXT (art, music, collectible, photo)
color_inicio TEXT (hex)
color_fin    TEXT (hex)
imagen_url   TEXT
imagen_b64   TEXT (imagen en base64)
tags         TEXT (JSON array)
regalias     REAL (% de regalías)
likes        INTEGER
fecha_creacion TIMESTAMP
actualizado  TIMESTAMP
```

### Tabla: `comentarios`
```sql
id           INTEGER PRIMARY KEY
nft_id       INTEGER (FK → nfts.id)
usuario_id   TEXT (FK → usuarios.id)
contenido    TEXT
fecha_creacion TIMESTAMP
likes        INTEGER
```

### Tabla: `transacciones`
```sql
id           INTEGER PRIMARY KEY
nft_id       INTEGER (FK → nfts.id)
vendedor_id  TEXT (FK → usuarios.id)
comprador_id TEXT (FK → usuarios.id)
cantidad     REAL (en ETH)
tipo         TEXT (compra, intercambio, oferta)
estado       TEXT (completada, pendiente, cancelada)
fecha        TIMESTAMP
```

### Tabla: `ofertas`
```sql
id           INTEGER PRIMARY KEY
nft_id       INTEGER (FK → nfts.id)
usuario_id   TEXT (FK → usuarios.id)
monto        REAL (en ETH)
mensaje      TEXT
estado       TEXT (pendiente, aceptada, rechazada)
fecha_creacion TIMESTAMP
actualizado  TIMESTAMP
```

### Tabla: `favoritos`
```sql
id           INTEGER PRIMARY KEY
usuario_id   TEXT (FK → usuarios.id)
nft_id       INTEGER (FK → nfts.id)
fecha_creacion TIMESTAMP
UNIQUE(usuario_id, nft_id)
```

### Tabla: `notificaciones`
```sql
id           INTEGER PRIMARY KEY
usuario_id   TEXT (FK → usuarios.id)
titulo       TEXT
mensaje      TEXT
tipo         TEXT (welcome, oferta, favorito, transaccion)
leida        INTEGER (0=no leída, 1=leída)
relacion_id  INTEGER (ID del objeto relacionado)
fecha        TIMESTAMP
```

### Tabla: `configuracion`
```sql
id           INTEGER PRIMARY KEY
usuario_id   TEXT UNIQUE (FK → usuarios.id)
tema         TEXT (dark, light, auto)
idioma       TEXT (es, en, pt)
moneda       TEXT (ETH, USD, MXN, EUR)
notificaciones INTEGER (0 o 1)
mostrar_iva  INTEGER (0 o 1)
fecha_creacion TIMESTAMP
actualizado  TIMESTAMP
```

---

## 💻 Uso en Python

### Importar y crear instancia

```python
from base import DatabaseNFT

db = DatabaseNFT('losprofetas.db')
```

### Crear usuario

```python
db.crear_usuario(
    id='user-001',
    username='artista',
    email='artista@mail.com',
    password_hash='hash_aqui',
    nombre='Mi Nombre'
)
```

### Crear NFT

```python
nft_id = db.crear_nft(
    titulo='Mi Obra Digital',
    artista_id='user-001',
    precio=1.5,
    categoria='art',
    descripcion='Una obra maestra',
    tags=['digital', 'generativo', 'arte'],
    color_inicio='#ff9a9e',
    color_fin='#fecfef',
    regalias=5
)
```

### Obtener NFTs

```python
# Todos los NFTs
todos = db.obtener_todos_nfts()

# Filtrar por categoría
artes = db.obtener_todos_nfts(filtro_categoria='art')

# Ordenar por precio ascendente
ordenado = db.obtener_todos_nfts(ordenar_por='precio ASC')

# NFTs de un artista
obras = db.obtener_nfts_por_artista('user-001')
```

### Agregar/Remover Favoritos

```python
# Agregar a favoritos
db.agregar_favorito('user-001', nft_id=5)

# Remover de favoritos
db.remover_favorito('user-001', nft_id=5)

# Verificar si es favorito
es_fav = db.es_favorito('user-001', nft_id=5)

# Obtener todos los favoritos
favoritos = db.obtener_favoritos('user-001')
```

### Comentarios

```python
# Crear comentario
comentario_id = db.crear_comentario(
    nft_id=5,
    usuario_id='user-001',
    contenido='¡Obra maestra!'
)

# Obtener comentarios
comentarios = db.obtener_comentarios(nft_id=5)

# Eliminar comentario
db.eliminar_comentario(comentario_id=10)
```

### Transacciones

```python
# Registrar compra
tx_id = db.crear_transaccion(
    nft_id=5,
    vendedor_id='artista-001',
    comprador_id='usuario-001',
    cantidad=1.5,
    tipo='compra'
)

# Historial de un NFT
historial = db.obtener_historial_transacciones(nft_id=5)

# Transacciones de un usuario
mis_transacciones = db.obtener_transacciones_usuario('usuario-001')
```

### Ofertas

```python
# Hacer oferta
oferta_id = db.crear_oferta(
    nft_id=5,
    usuario_id='usuario-001',
    monto=1.2,
    mensaje='Me interesa'
)

# Obtener ofertas
ofertas = db.obtener_ofertas_nft(nft_id=5)

# Actualizar estado
db.actualizar_oferta(oferta_id=10, estado='aceptada')
```

### Notificaciones

```python
# Crear notificación
db.crear_notificacion(
    usuario_id='user-001',
    titulo='Nueva oferta',
    mensaje='Alguien ofreció por tu obra',
    tipo='oferta',
    relacion_id=42
)

# Obtener notificaciones
notificaciones = db.obtener_notificaciones('user-001')

# Solo no leídas
no_leidas = db.obtener_notificaciones('user-001', no_leidas=True)

# Marcar como leída
db.marcar_notificacion_leida(notificacion_id=10)

# Marcar todas como leídas
db.marcar_todas_leidas('user-001')

# Contar no leídas
cantidad = db.contar_no_leidas('user-001')
```

### Configuración

```python
# Obtener configuración
config = db.obtener_configuracion('user-001')

# Actualizar configuración
db.actualizar_configuracion(
    usuario_id='user-001',
    tema='light',
    moneda='USD',
    notificaciones=1
)
```

### Estadísticas

```python
# Del mercado
stats = db.obtener_estadisticas_mercado()
# {
#   'total_nfts': 50,
#   'total_usuarios': 20,
#   'total_transacciones': 100,
#   'volumen_total': 150.5
# }

# De usuario
stats_user = db.obtener_estadisticas_usuario('user-001')
# {
#   'obras': 5,
#   'favoritos': 12,
#   'notificaciones': 3,
#   'compras': 8
# }
```

### Exportar datos

```python
datos = db.exportar_datos_usuario('user-001')
# Retorna:
# {
#   'usuario': {...},
#   'nfts_creados': [...],
#   'favoritos': [...],
#   'transacciones': [...],
#   'configuracion': {...},
#   'fecha_exportacion': '2024-...'
# }
```

---

## 🌐 Endpoints REST (API)

### Usuarios

```
GET    /api/usuarios/<usuario_id>              # Obtener usuario
POST   /api/usuarios                           # Crear usuario
PUT    /api/usuarios/<usuario_id>              # Actualizar usuario
```

### NFTs

```
GET    /api/nfts                               # Listar todos (con filtros)
GET    /api/nfts/<nft_id>                      # Obtener NFT
POST   /api/nfts                               # Crear NFT
PUT    /api/nfts/<nft_id>                      # Actualizar NFT
DELETE /api/nfts/<nft_id>                      # Eliminar NFT
GET    /api/artistas/<artista_id>/nfts         # NFTs de artista
```

### Comentarios

```
GET    /api/nfts/<nft_id>/comentarios          # Obtener comentarios
POST   /api/nfts/<nft_id>/comentarios          # Crear comentario
DELETE /api/comentarios/<comentario_id>        # Eliminar comentario
```

### Transacciones

```
POST   /api/transacciones                      # Registrar transacción
GET    /api/nfts/<nft_id>/historial            # Historial de NFT
GET    /api/usuarios/<usuario_id>/transacciones# Transacciones del usuario
```

### Ofertas

```
POST   /api/nfts/<nft_id>/ofertas               # Crear oferta
GET    /api/nfts/<nft_id>/ofertas               # Obtener ofertas
PUT    /api/ofertas/<oferta_id>/<estado>        # Actualizar estado
```

### Favoritos

```
GET    /api/usuarios/<usuario_id>/favoritos            # Listar favoritos
POST   /api/usuarios/<usuario_id>/favoritos/<nft_id>   # Agregar
DELETE /api/usuarios/<usuario_id>/favoritos/<nft_id>   # Remover
GET    /api/usuarios/<usuario_id>/es-favorito/<nft_id> # Verificar
```

### Notificaciones

```
GET    /api/usuarios/<usuario_id>/notificaciones              # Listar
GET    /api/usuarios/<usuario_id>/notificaciones/no-leidas    # Contar no leídas
PUT    /api/notificaciones/<notificacion_id>/leer             # Marcar leída
PUT    /api/usuarios/<usuario_id>/notificaciones/marcar-todas # Marcar todas
```

### Configuración

```
GET    /api/usuarios/<usuario_id>/configuracion     # Obtener
PUT    /api/usuarios/<usuario_id>/configuracion     # Actualizar
```

### Estadísticas

```
GET    /api/estadisticas/mercado                    # Stats del mercado
GET    /api/estadisticas/usuarios/<usuario_id>      # Stats del usuario
GET    /api/usuarios/<usuario_id>/exportar           # Exportar datos
```

### Sistema

```
GET    /api/health                               # Health check
```

---

## 🧪 Ejemplos cURL

### Crear NFT

```bash
curl -X POST http://localhost:5000/api/nfts \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Mi Obra",
    "artista_id": "sys-arivera",
    "precio": 1.5,
    "categoria": "art",
    "descripcion": "Una obra digital",
    "tags": ["digital", "arte"],
    "color_inicio": "#ff9a9e",
    "color_fin": "#fecfef",
    "regalias": 5
  }'
```

### Obtener todos los NFTs

```bash
curl http://localhost:5000/api/nfts?categoria=art&sort=precio%20DESC&limite=10
```

### Agregar a favoritos

```bash
curl -X POST \
  http://localhost:5000/api/usuarios/sys-user-demo/favoritos/5 \
  -H "Content-Type: application/json"
```

### Crear comentario

```bash
curl -X POST http://localhost:5000/api/nfts/5/comentarios \
  -H "Content-Type: application/json" \
  -d '{
    "usuario_id": "sys-user-demo",
    "contenido": "¡Me encanta!"
  }'
```

---

## 🔐 Seguridad

⚠️ **IMPORTANTE**: Este es un sistema de demostración. En producción:

- Implementar autenticación JWT
- Validar inputs en todos los endpoints
- Usar bcrypt para contraseñas
- HTTPS obligatorio
- Rate limiting
- Sanitización de datos
- CORS restringido

---

## 🐛 Troubleshooting

### Error: "sqlite3.OperationalError: database is locked"

Asegúrate de cerrar la conexión anterior o ajusta el timeout:

```python
db = DatabaseNFT('losprofetas.db')
```

### Import Error: "No module named 'flask'"

Instala las dependencias:

```bash
pip install -r requirements.txt
```

### La base de datos está corrupta

Elimina `losprofetas.db` y vuelve a ejecutar `seed.py`:

```bash
rm losprofetas.db  # o del losprofetas.db en Windows
python seed.py
```

---

## 📊 Estadísticas Iniciales (después de seed.py)

- 👥 Usuarios: 6
- 🎨 NFTs: 8
- 💬 Comentarios: 3
- 💳 Transacciones: 1
- 🤝 Ofertas: 1
- 🔔 Notificaciones: 3

---

## 📞 Soporte

Para preguntas sobre la estructura de la BD, consulta los docstrings en `base.py`.

¡Happy coding! 🚀
