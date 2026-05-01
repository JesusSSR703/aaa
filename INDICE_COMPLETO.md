# 📑 Índice Completo de Archivos

## 🎯 Archivos de Entrada (Comienza aquí)

### 1. **INICIAR_TODO.py** ⭐ RECOMENDADO
- **Qué hace**: Script maestro que automatiza TODO
- **Ejecución**: `python INICIAR_TODO.py`
- **Resultado**: API + Dashboard corriendo en 30 segundos
- **Para**: Usuarios que quieren empezar YA

### 2. **LEEME_PRIMERO.md** ⭐ LECTURA OBLIGATORIA
- **Qué es**: Guía de inicio rápido de 5 minutos
- **Contenido**: URLs, características, ejemplos básicos
- **Lectura**: 5 minutos
- **Para**: Entender qué está disponible

### 3. **validacion.py**
- **Qué hace**: Verifica que todo esté correcto
- **Ejecución**: `python validacion.py`
- **Resultado**: Reporte de estado del sistema
- **Para**: Diagnosticar problemas

---

## 🏛️ Archivos Core (Motor del Sistema)

### **base.py** ⭐ NÚCLEO PRINCIPAL
- **Responsabilidad**: Motor de BD + ML + IA
- **Tamaño**: ~800 líneas
- **Proporciona**: Clase `DatabaseNFT`
- **Funciones principales**:
  - ✅ 30+ métodos CRUD
  - ✅ 5 funciones ML (recomendaciones, predicción, anomalías, similares, tendencias)
  - ✅ 3 funciones IA (búsqueda inteligente, análisis usuario, insights)
- **Dependencias**: sqlite3, numpy, sklearn (opcional)
- **Uso**: `from base import DatabaseNFT`

### **api.py** ⭐ REST API
- **Responsabilidad**: Exponer base.py como API REST
- **Puerto**: 5000 (configurable)
- **Proporciona**: 50+ endpoints
- **Categorías**:
  - Usuarios: 5 endpoints
  - NFTs: 8 endpoints
  - Comentarios: 3 endpoints
  - Transacciones: 4 endpoints
  - Ofertas: 4 endpoints
  - Favoritos: 4 endpoints
  - Notificaciones: 4 endpoints
  - Configuración: 2 endpoints
  - ML: 5 endpoints
  - IA: 3 endpoints
- **Ejemplo**: `GET http://localhost:5000/api/nfts`

### **dashboard.py** ⭐ DASHBOARD VISUAL
- **Responsabilidad**: Interfaz web visual
- **Puerto**: 5001 (configurable)
- **Proporciona**: HTML/CSS/JS interactivo
- **Características**:
  - 5 tabs funcionales
  - Gráficos con Chart.js
  - Estadísticas en tiempo real
  - Controles interactivos
- **Acceso**: `http://localhost:5001`

---

## 🔧 Archivos de Setup

### **seed.py**
- **Qué hace**: Carga datos iniciales en la BD
- **Ejecución**: `python seed.py`
- **Carga**: 6 usuarios, 8 NFTs, transacciones, comentarios
- **Cuándo usarlo**: Después de instalar dependencias
- **Efecto**: Crea `losprofetas.db` con datos

### **setup.py**
- **Qué hace**: Setup manual paso a paso
- **Ejecución**: `python setup.py`
- **Alternativa a**: INICIAR_TODO.py (más control)
- **Para**: Usuarios avanzados

### **requirements.txt**
- **Qué contiene**: Lista de dependencias Python
- **Instalación**: `pip install -r requirements.txt`
- **Paquetes**:
  - flask==2.3.0
  - flask-cors==4.0.0
  - scikit-learn==1.3.2
  - numpy==1.24.3
  - pandas==2.0.3
  - matplotlib==3.7.2
  - scipy==1.11.2

### **losprofetas.db**
- **Qué es**: Base de datos SQLite3
- **Creación**: Automática al ejecutar seed.py
- **Tamaño**: ~200 KB (con datos iniciales)
- **Contenido**: 8 tablas, relaciones, constraints

---

## 📚 Documentación Técnica

### **COMPLETO_v2.0.md** ⭐ DOCUMENTACIÓN PRINCIPAL
- **Tamaño**: 300+ líneas
- **Contenido**:
  - Arquitectura del sistema
  - Schema completo de BD
  - Todos los endpoints (50+)
  - Métodos ML/IA con explicaciones
  - Ejemplos de código
  - Configuración avanzada
  - Troubleshooting
- **Lectura**: 30-60 minutos
- **Para**: Implementadores y desarrolladores

### **DATABASE.md**
- **Contenido**: 
  - Schema SQL de todas las tablas
  - Documentación de métodos
  - Ejemplos Python
  - Ejemplos cURL
  - Troubleshooting
- **Lectura**: 20 minutos
- **Para**: Trabajo con BD

### **INTEGRACION.md**
- **Contenido**:
  - Cómo integrar con app.js
  - Ejemplos JavaScript completos
  - Manejo de respuestas
  - Manejo de errores
  - Flujos de usuario
- **Lectura**: 15 minutos
- **Para**: Desarrolladores frontend

### **REFERENCIA_RAPIDA.py**
- **Qué es**: Cheat sheet visual (ejecutable)
- **Ejecución**: `python REFERENCIA_RAPIDA.py`
- **Contenido**: ASCII art con todos los métodos
- **Para**: Consulta rápida

### **RESUMEN_FINAL.py**
- **Qué es**: Resumen visual del proyecto completo
- **Ejecución**: `python RESUMEN_FINAL.py`
- **Contenido**: Overview de todo lo que recibiste
- **Para**: Visión general

---

## 🌐 Archivos Web (App Principal)

### **index.html**
- **Qué es**: Página principal del marketplace
- **Propósito**: Landing page + interfaz usuario
- **Características**: Responsive, moderno
- **Integración**: Con app.js

### **app.js**
- **Qué es**: Lógica JavaScript de la app
- **Responsabilidades**: Interactividad, comunicación API
- **Integración**: Llamar a endpoints de api.py
- **Ejemplos**: Ver INTEGRACION.md

### **style.css**
- **Qué es**: Estilos CSS
- **Estilo**: Moderno, gradientes, glassmorphism
- **Responsivo**: Mobile-first

---

## 🔗 Archivos Adicionales

### **servidor_integrado.py**
- **Qué es**: Alternativa a ejecutar api.py + dashboard.py por separado
- **Ejecución**: `python servidor_integrado.py`
- **Ventaja**: Un solo comando para ambos servidores
- **Puerto**: 5000 (ambos servicios en uno)

### **README.md**
- **Qué es**: Archivo original del proyecto
- **Contenido**: Descripción general
- **Estado**: Versión v1 (ver COMPLETO_v2.0.md para v2)

---

## 📊 Estructura de Base de Datos

### Tablas Creadas

```
usuarios              → Perfiles de usuarios
├─ id (PK)
├─ username (UNIQUE)
├─ email (UNIQUE)
├─ avatar_b64
├─ bio
├─ fecha_creacion

nfts                  → Obras NFT
├─ id (PK)
├─ titulo
├─ precio
├─ categoria
├─ artista_id (FK → usuarios)
├─ descripcion
├─ likes
├─ fecha_creacion

comentarios           → Interacciones
├─ id (PK)
├─ nft_id (FK → nfts)
├─ usuario_id (FK → usuarios)
├─ texto
├─ fecha

transacciones         → Compras/Ventas
├─ id (PK)
├─ vendedor_id (FK → usuarios)
├─ comprador_id (FK → usuarios)
├─ nft_id (FK → nfts)
├─ monto
├─ cantidad
├─ fecha

ofertas               → Pujas
├─ id (PK)
├─ nft_id (FK → nfts)
├─ usuario_id (FK → usuarios)
├─ monto
├─ estado
├─ fecha

favoritos             → Marcadores
├─ id (PK)
├─ usuario_id (FK → usuarios)
├─ nft_id (FK → nfts)

notificaciones        → Alertas
├─ id (PK)
├─ usuario_id (FK → usuarios)
├─ titulo
├─ mensaje
├─ leida
├─ fecha

configuracion         → Preferencias
├─ id (PK)
├─ usuario_id (FK → usuarios, UNIQUE)
├─ tema
├─ idioma
├─ notificaciones_activas
```

---

## 🚀 Flujos de Uso

### Flujo 1: Principiante
1. Lee: LEEME_PRIMERO.md
2. Ejecuta: `python INICIAR_TODO.py`
3. Abre: http://localhost:5001
4. Explora: Dashboard con 5 tabs
5. Resultado: Sistema corriendo

### Flujo 2: Desarrollador
1. Lee: COMPLETO_v2.0.md
2. Instala: `pip install -r requirements.txt`
3. Carga datos: `python seed.py`
4. Inicia API: `python api.py`
5. Integra: Ver ejemplos en INTEGRACION.md
6. Usa: Endpoints en app.js

### Flujo 3: Administrador
1. Valida: `python validacion.py`
2. Verifica: BD con seed.py
3. Monitorea: Dashboard en 5001
4. Analiza: Tab "Análisis" y "Predicciones"
5. Mantiene: Ejecuta según sea necesario

---

## 📋 Checklist de Uso

- [ ] Leer LEEME_PRIMERO.md
- [ ] Ejecutar python INICIAR_TODO.py
- [ ] Abrir http://localhost:5001
- [ ] Explorar todos los tabs
- [ ] Leer COMPLETO_v2.0.md
- [ ] Ejecutar python validacion.py
- [ ] Revisar ejemplos en INTEGRACION.md
- [ ] Integrar con app.js
- [ ] Hacer backup de losprofetas.db
- [ ] Customizar según necesidades

---

## 📱 Acceso a Servicios

| Servicio | URL | Archivo |
|----------|-----|---------|
| Dashboard | http://localhost:5001 | dashboard.py |
| API | http://localhost:5000 | api.py |
| Health Check | http://localhost:5000/api/health | api.py |
| NFTs | http://localhost:5000/api/nfts | api.py |
| Recomendaciones | http://localhost:5000/api/ml/recomendaciones/sys-user-demo | api.py |

---

## 🎓 Lecturas Recomendadas

### Nivel 1: Usuario (5-10 min)
- [ ] LEEME_PRIMERO.md

### Nivel 2: Desarrollador (30 min)
- [ ] LEEME_PRIMERO.md
- [ ] INTEGRACION.md
- [ ] DATABASE.md

### Nivel 3: Full Stack (60+ min)
- [ ] LEEME_PRIMERO.md
- [ ] COMPLETO_v2.0.md
- [ ] DATABASE.md
- [ ] INTEGRACION.md
- [ ] Revisar código de base.py

### Nivel 4: Experto (120+ min)
- [ ] Todo lo anterior
- [ ] Estudiar código completo
- [ ] Modify requirements.txt
- [ ] Expandir con PostgreSQL
- [ ] Deploy a producción

---

## ✅ Validación Rápida

```bash
# 1. Verificar archivos
python validacion.py

# 2. Cargar datos
python seed.py

# 3. Iniciar API
python api.py

# 4. En otra terminal, iniciar Dashboard
python dashboard.py

# 5. Abrir navegador
# http://localhost:5001

# Esperas a ver el dashboard con 5 tabs
# ¡ÉXITO! 🎉
```

---

## 📞 Ayuda Rápida

```
¿Qué archivo?          ¿Para?
────────────────────────────────────────
LEEME_PRIMERO.md       Empezar rápido
COMPLETO_v2.0.md       Entender todo
DATABASE.md            Trabajar con BD
INTEGRACION.md         Integrar con JS
base.py                Lógica de BD
api.py                 REST endpoints
dashboard.py           Interface visual
```

---

**¡Todos los archivos están listos para usar! 🚀**
