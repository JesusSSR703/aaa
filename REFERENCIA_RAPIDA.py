#!/usr/bin/env python3
"""
Los profetas — Quick Reference
Cheat sheet de la base de datos
"""

print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                    LOS PROFETAS — QUICK REFERENCE                        ║
║                         Mercado NFT - Base de Datos                      ║
╚═══════════════════════════════════════════════════════════════════════════╝

┌───────────────────────────────────────────────────────────────────────────┐
│ 1. SETUP INICIAL                                                          │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Opción A (Automático):          $ python setup.py                       │
│  Opción B (Manual):              $ pip install -r requirements.txt       │
│                                  $ python seed.py                        │
│                                  $ python api.py                         │
│                                                                           │
│  API disponible en:               http://localhost:5000                  │
│  Health check:                    http://localhost:5000/api/health       │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│ 2. OBJETOS PRINCIPALES                                                    │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  USUARIO                           NFT                                   │
│  ├─ id: 'sys-arivera'             ├─ id: 1                              │
│  ├─ username: 'arivera'           ├─ titulo: 'Profecía Lunar'           │
│  ├─ email: 'a@mail.com'           ├─ precio: 0.85                       │
│  ├─ nombre: 'Alejandro Rivera'    ├─ categoria: 'art'                   │
│  └─ avatar_b64: 'base64...'       ├─ artista_id: 'sys-arivera' (FK)    │
│                                    ├─ tags: ['lunar', 'generativo']     │
│  TRANSACCIÓN                       └─ regalias: 5%                       │
│  ├─ id: 1                                                               │
│  ├─ nft_id: 1                      COMENTARIO                           │
│  ├─ vendedor: 'sys-arivera'        ├─ id: 1                             │
│  ├─ comprador: 'sys-user-demo'     ├─ nft_id: 1 (FK)                    │
│  ├─ cantidad: 0.85 ETH             ├─ usuario_id: 'sys-user-demo' (FK) │
│  └─ tipo: 'compra'                 ├─ contenido: '¡Obra maestra!'      │
│                                    └─ fecha: 2024-01-15...              │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│ 3. MÉTODOS PYTHON - USUARIOS                                             │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  db.crear_usuario(id, username, email, password_hash, nombre)           │
│  db.obtener_usuario(usuario_id)                                         │
│  db.obtener_usuario_por_email(email)                                    │
│  db.actualizar_usuario(usuario_id, nombre=..., bio=...)                 │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│ 4. MÉTODOS PYTHON - NFTs                                                 │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  nft_id = db.crear_nft(titulo, artista_id, precio, categoria,          │
│                        descripcion, tags, regalias=5)                   │
│  db.obtener_nft(nft_id)                                                 │
│  db.obtener_todos_nfts(filtro_categoria, ordenar_por, limite)          │
│  db.obtener_nfts_por_artista(artista_id)                               │
│  db.actualizar_nft(nft_id, precio=..., titulo=...)                      │
│  db.eliminar_nft(nft_id)                                                │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│ 5. MÉTODOS PYTHON - FAVORITOS                                            │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  db.agregar_favorito(usuario_id, nft_id)                                │
│  db.remover_favorito(usuario_id, nft_id)                                │
│  db.obtener_favoritos(usuario_id)    # → Lista de NFTs                 │
│  db.es_favorito(usuario_id, nft_id)  # → True/False                    │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│ 6. MÉTODOS PYTHON - COMENTARIOS Y TRANSACCIONES                          │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  COMENTARIOS                       TRANSACCIONES                        │
│  ├─ crear_comentario(nft_id,       ├─ crear_transaccion(                │
│  │   usuario_id, contenido)       │   nft_id, vendedor_id,            │
│  ├─ obtener_comentarios(nft_id)    │   comprador_id, cantidad)         │
│  └─ eliminar_comentario(com_id)    ├─ obtener_historial(nft_id)       │
│                                    └─ obtener_transacciones_usuario()  │
│                                                                           │
│  OFERTAS                           NOTIFICACIONES                       │
│  ├─ crear_oferta(nft_id,           ├─ crear_notificacion(usuario_id,  │
│  │   usuario_id, monto)            │   titulo, mensaje, tipo)          │
│  ├─ obtener_ofertas_nft(nft_id)    ├─ obtener_notificaciones(user_id) │
│  └─ actualizar_oferta(id, estado)  ├─ marcar_notificacion_leida(id)   │
│                                    └─ contar_no_leidas(user_id)        │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│ 7. ENDPOINTS REST - LECTURA (GET)                                        │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  /api/nfts                              Todos los NFTs                  │
│  /api/nfts?categoria=art&limite=10      Con filtros                     │
│  /api/nfts/5                            NFT específico (con details)    │
│  /api/usuarios/sys-user-demo            Perfil del usuario              │
│  /api/usuarios/sys-user-demo/favoritos  Favoritos                       │
│  /api/nfts/5/comentarios                Comentarios de NFT              │
│  /api/nfts/5/historial                  Historial de transacciones     │
│  /api/usuarios/sys-user-demo/nfts       NFTs del usuario               │
│  /api/estadisticas/mercado              Stats del mercado               │
│  /api/estadisticas/usuarios/sys-id      Stats del usuario               │
│  /api/health                            Health check                    │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│ 8. ENDPOINTS REST - ESCRITURA (POST/PUT/DELETE)                          │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  POST   /api/nfts                       Crear NFT                       │
│  PUT    /api/nfts/5                     Editar NFT                      │
│  DELETE /api/nfts/5                     Eliminar NFT                    │
│  POST   /api/nfts/5/comentarios         Agregar comentario              │
│  DELETE /api/comentarios/10             Eliminar comentario             │
│  POST   /api/transacciones              Registrar compra                │
│  POST   /api/nfts/5/ofertas             Hacer oferta                    │
│  PUT    /api/ofertas/8/aceptada         Aceptar/rechazar oferta        │
│  POST   /api/usuarios/id/favoritos/5    Agregar a favoritos             │
│  DELETE /api/usuarios/id/favoritos/5    Remover de favoritos            │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│ 9. EJEMPLO DE FLUJO COMPLETO                                             │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  1. Artista crea NFT:                                                   │
│     POST /api/nfts → {titulo, precio, categoria, ...}                   │
│                                                                           │
│  2. Usuario ve NFT:                                                      │
│     GET /api/nfts/5 → {nft, comentarios, historial}                    │
│                                                                           │
│  3. Usuario hace oferta:                                                │
│     POST /api/nfts/5/ofertas → {usuario_id, monto}                      │
│                                                                           │
│  4. Usuario comenta:                                                    │
│     POST /api/nfts/5/comentarios → {usuario_id, contenido}              │
│                                                                           │
│  5. Usuario agrega a favoritos:                                         │
│     POST /api/usuarios/user-1/favoritos/5                               │
│                                                                           │
│  6. Usuario compra:                                                     │
│     POST /api/transacciones → {nft_id, vendedor, comprador, cantidad}   │
│                                                                           │
│  7. Sistema notifica:                                                   │
│     Automáticamente se crea notificación en la BD                        │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│ 10. DATOS INICIALES (SEED)                                               │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  USUARIOS:                     NFTs:                                     │
│  • sys-arivera                 • Profecía Lunar (0.85 ETH)              │
│  • sys-lsantos                 • Ecos del Mañana (1.2 ETH)              │
│  • sys-mortega                 • Guardiana 07 (0.45 ETH)                │
│  • sys-kdiaz                   • Vidente Urbano (2.1 ETH)               │
│  • sys-nperez                  • Ritmo Ancestral (0.33 ETH)             │
│  • sys-user-demo ← USAR ESTE   • Sello Profético (0.12 ETH)            │
│                                • Nexo Digital (1.75 ETH)                │
│                                • Ondas Cósmicas (1.5 ETH)               │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│ 11. ARCHIVOS DE REFERENCIA                                               │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  base.py          → Código fuente, todos los métodos con docstrings     │
│  api.py           → Endpoints REST, ejemplos en comentarios             │
│  DATABASE.md      → Documentación técnica completa                      │
│  INTEGRACION.md   → Cómo integrar con app.js                            │
│  RESUMEN.md       → Resumen visual del proyecto                         │
│  requirements.txt → pip install -r requirements.txt                     │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│ 12. COMANDOS ÚTILES                                                       │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  python setup.py                 # Setup automático completo            │
│  python seed.py                  # Recargar datos de prueba             │
│  python api.py                   # Iniciar servidor                     │
│                                                                           │
│  # En Python:                                                            │
│  from base import DatabaseNFT                                           │
│  db = DatabaseNFT()                                                     │
│  nft = db.obtener_nft(1)                                                │
│  print(nft)                                                             │
│                                                                           │
│  # cURL:                                                                 │
│  curl http://localhost:5000/api/nfts                                    │
│  curl http://localhost:5000/api/nfts/1                                  │
│  curl http://localhost:5000/api/health                                  │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

╔═══════════════════════════════════════════════════════════════════════════╗
║ ✅ BASE DE DATOS LISTA PARA EL HACKATHON                                  ║
║                                                                           ║
║ Contacto: Ver DATABASE.md, INTEGRACION.md, RESUMEN.md para más info     ║
╚═══════════════════════════════════════════════════════════════════════════╝
""")
