# 🎨 LOS PROFETAS — MERCADO DE NFTs COMPLETO

**Solución profesional de hackathon con BD, Machine Learning e Inteligencia Artificial**

> **Versión 2.0** — Sistema integrado con Dashboard visual, análisis avanzado y predicciones ML

---

## 📋 Resumen Rápido

Una plataforma de NFTs **100% funcional** con:

✅ **Base de Datos robusta** — SQLite3 con 8 tablas normalizadas  
✅ **Machine Learning** — Recomendaciones, predicción de precios, detección de anomalías  
✅ **Inteligencia Artificial** — Búsqueda inteligente, análisis de usuarios, insights automáticos  
✅ **Dashboard Visual** — Gráficos interactivos, estadísticas en tiempo real  
✅ **API REST** — 50+ endpoints documentados  
✅ **Datos de Prueba** — 6 usuarios, 8 NFTs listos para explorar  

---

## 🚀 ¿Cómo Empezar?

### Opción 1: Setup Automático (Recomendado)

```bash
python INICIAR_TODO.py
```

Esto hace todo automáticamente:
- Instala dependencias
- Crea la base de datos
- Inicia API y Dashboard
- Abre en tu navegador

### Opción 2: Manual

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Crear BD con datos de prueba
python seed.py

# 3. Iniciar API (puerto 5000)
python api.py

# 4. En otra terminal, iniciar Dashboard (puerto 5001)
python dashboard.py
```

---

## 🌐 ¿Dónde Ver Todo?

Una vez iniciado, abre tu navegador:

| URL | Qué Ver |
|-----|---------|
| http://localhost:5001 | **Dashboard** (TODO visual) |
| http://localhost:5000/api/health | **API Status** |
| http://localhost:5000/api/nfts | **Todos los NFTs** |
| http://localhost:5000/api/ml/recomendaciones/sys-user-demo | **Recomendaciones ML** |

---

## 🎯 Funcionalidades Principales

### 1. Machine Learning

```python
# Recomendaciones personalizadas
GET /api/ml/recomendaciones/{usuario_id}

# Predicción de precios
GET /api/ml/prediccion/{nft_id}

# Detectar anomalías
GET /api/ml/anomalias

# Encontrar similares
GET /api/ml/similares/{nft_id}
```

### 2. Inteligencia Artificial

```python
# Búsqueda semántica
POST /api/ai/busqueda { "query": "lunar" }

# Análisis de usuario
GET /api/ai/analisis-usuario/{usuario_id}

# Insights del mercado
GET /api/ai/insights
```

### 3. Dashboard Interactivo

- 📊 **Estadísticas**: Total NFTs, usuarios, transacciones, volumen
- 📈 **Gráficos**: Categorías (doughnut), Precios (bar)
- 🤖 **ML**: Recomendaciones, anomalías
- ✨ **IA**: Búsqueda, análisis de perfil
- 🔍 **Análisis**: Tendencias, insights
- 🔮 **Predicciones**: Precios futuros, similares

### 4. Base de Datos Completa

```python
from base import DatabaseNFT

db = DatabaseNFT('losprofetas.db')

# Crear NFT
nft_id = db.crear_nft(
    titulo='Mi Obra',
    artista_id='user-1',
    precio=1.5,
    categoria='art'
)

# Agregar a favoritos
db.agregar_favorito('user-2', nft_id)

# Obtener recomendaciones
recomendaciones = db.obtener_recomendaciones('user-2')

# Predecir precio
prediccion = db.predecir_precio_nft(nft_id)

db.cerrar()
```

---

## 📊 Datos Iniciales (Seed)

Después de ejecutar `seed.py`:

### Usuarios
```
sys-arivera        Artista
sys-lsantos        Artista  
sys-mortega        Artista
sys-kdiaz          Artista
sys-nperez         Artista
sys-user-demo      ← Usa este para pruebas
```

### NFTs
```
1. Profecía Lunar        0.85 ETH   (Arte)
2. Ecos del Mañana       1.2 ETH    (Música)
3. Guardiana 07          0.45 ETH   (Coleccionable)
4. Vidente Urbano        2.1 ETH    (Arte)
5. Ritmo Ancestral       0.33 ETH   (Música)
6. Sello Profético       0.12 ETH   (Coleccionable)
7. Nexo Digital          1.75 ETH   (Arte)
8. Ondas Cósmicas        1.5 ETH    (Música)
```

---

## 📁 Estructura de Archivos

```
├── base.py                 ← Motor BD + ML + IA (¡LO IMPORTANTE!)
├── api.py                  ← API REST (50+ endpoints)
├── dashboard.py            ← Dashboard web visual
├── seed.py                 ← Carga datos de prueba
├── setup.py                ← Setup automático
├── INICIAR_TODO.py         ← Script maestro (recomendado)
│
├── COMPLETO_v2.0.md        ← Guía COMPLETA (léela)
├── DATABASE.md             ← Docs técnicas
├── INTEGRACION.md          ← Cómo integrar con app.js
├── RESUMEN.md              ← Resumen visual
│
├── losprofetas.db          ← BD SQLite (se crea automáticamente)
└── requirements.txt        ← Dependencias Python
```

---

## 💡 Ejemplos de Uso

### JavaScript (en tu app.js)

```javascript
// Obtener recomendaciones
const recs = await fetch('http://localhost:5000/api/ml/recomendaciones/sys-user-demo')
  .then(r => r.json());
console.log(recs); // Array de NFTs recomendados

// Buscar inteligentemente
const resultados = await fetch('http://localhost:5000/api/ai/busqueda', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: 'lunar' })
}).then(r => r.json());

// Predecir precio de un NFT
const prediccion = await fetch('http://localhost:5000/api/ml/prediccion/1')
  .then(r => r.json());
console.log(`Predicción: ${prediccion.precio_predicho} ETH`);
```

### Python

```python
from base import DatabaseNFT

db = DatabaseNFT()

# Recomendaciones
recs = db.obtener_recomendaciones('sys-user-demo')
for nft in recs[:3]:
    print(f"⭐ {nft['titulo']} - {nft['precio']} ETH")

# Análisis de tendencias
tendencias = db.analizar_tendencias_mercado()
print(f"Categorías trending: {tendencias['categorias_trending']}")

# Anomalías
anomalias = db.detectar_anomalias()
print(f"Anomalías detectadas: {len(anomalias)}")

db.cerrar()
```

### cURL

```bash
# Listar todos los NFTs
curl http://localhost:5000/api/nfts

# Recomendaciones
curl http://localhost:5000/api/ml/recomendaciones/sys-user-demo

# Tendencias
curl http://localhost:5000/api/ml/tendencias

# Predicción
curl http://localhost:5000/api/ml/prediccion/1

# Anomalías
curl http://localhost:5000/api/ml/anomalias
```

---

## 🎓 Documentación Disponible

| Archivo | Contenido |
|---------|----------|
| **COMPLETO_v2.0.md** | 📖 **Guía completa** del sistema (¡LÉELA!) |
| DATABASE.md | Estructura de BD y métodos |
| INTEGRACION.md | Cómo integrar con app.js |
| RESUMEN.md | Resumen visual del proyecto |
| base.py | Docstrings de todos los métodos |
| api.py | Endpoints REST documentados |
| dashboard.py | HTML/CSS/JS del dashboard |

---

## 🔑 Características Destacadas

### Machine Learning

🤖 **Recomendador**
- Analiza preferencias del usuario
- Calcula scoring de relevancia
- Retorna top-10 personalizados

🤖 **Predictor de Precios**
- Regresión lineal con sklearn
- Análisis de tendencias
- Confianza 10-95%

🤖 **Detector de Anomalías**
- Z-score estadístico
- Precios sospechosos
- Comportamiento inusual

### Inteligencia Artificial

✨ **Búsqueda Inteligente**
- Búsqueda semántica
- Filtros avanzados
- Ordenamiento por relevancia

✨ **Análisis de Usuario**
- Clasificación (Artista, Coleccionista, etc)
- Engagement score
- Patrones de compra

✨ **Insights Automáticos**
- NFTs trending
- Categoría más valiosa
- Anomalías detectadas

---

## ⚙️ Configuración

### Cambiar Puertos

En `api.py`:
```python
app.run(port=5000)  # Cambiar a 8000, 3000, etc.
```

En `dashboard.py`:
```python
app.run(port=5001)  # Cambiar a 8001, 3001, etc.
```

### Ajustar BD

En `base.py`:
```python
db = DatabaseNFT('otro_archivo.db')  # Usar otra BD
```

---

## ❓ Preguntas Frecuentes

**¿La BD está segura?**
Es SQLite3 con constraints. Para producción, migrar a PostgreSQL.

**¿Puedo cambiar el puerto?**
Sí, en `api.py` y `dashboard.py` al final.

**¿Cómo integro con mi app.js?**
Ver `INTEGRACION.md` con ejemplos completos.

**¿Qué pasa si elimino losprofetas.db?**
Ejecuta `python seed.py` de nuevo.

**¿Puedo usar sin sklearn?**
Sí, funciona con lógica simplificada.

---

## 📞 Soporte Rápido

| Problema | Solución |
|----------|----------|
| ImportError: flask | `pip install -r requirements.txt` |
| Port already in use | Cambiar puerto en api.py/dashboard.py |
| BD corrupta | `rm losprofetas.db && python seed.py` |
| Gráficos no aparecen | Espera a que cargue, abre consola (F12) |

---

## ✅ Validación

Después de iniciar, verifica que:

- ✓ http://localhost:5001 abre sin errores
- ✓ Dashboard muestra estadísticas
- ✓ Tab "ML" genera recomendaciones
- ✓ Tab "IA" busca inteligentemente
- ✓ Tab "Predicciones" muestra precios futuros
- ✓ http://localhost:5000/api/health responde

---

## 🎯 Próximos Pasos

1. **Explorar Dashboard** → http://localhost:5001
2. **Leer COMPLETO_v2.0.md** → Documentación completa
3. **Probar APIs** → cURL o Postman
4. **Integrar con app.js** → Ver INTEGRACION.md
5. **Expandir BD** → Agregar más usuarios/NFTs

---

## 🚀 Deploy en Producción

Para subir a un servidor:

```bash
# 1. Instalar en servidor
pip install -r requirements.txt

# 2. Usar gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api:app

# 3. Con Nginx reverse proxy
# (Consulta documentación)

# 4. Migrar a PostgreSQL
# (Ver DATABASE.md)
```

---

## 📊 Estadísticas de la Solución

| Métrica | Valor |
|---------|-------|
| Líneas de código | ~2500 |
| Métodos de BD | 30+ |
| Endpoints API | 50+ |
| Capacidades ML | 5 |
| Capacidades IA | 3 |
| Tablas de BD | 8 |
| Datos iniciales | 6 usuarios, 8 NFTs |

---

## 📄 Licencia

Proyecto creado para **hackathon**. Uso libre para desarrollo.

---

**¡LISTO PARA USAR! 🚀**

Ejecuta `python INICIAR_TODO.py` y comienza.

Para dudas técnicas, consulta `COMPLETO_v2.0.md`.
