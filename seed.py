"""
Los profetas — Datos de Prueba (Seed)
Carga datos iniciales en la base de datos para pruebas
"""

from base import DatabaseNFT
import uuid
import hashlib

def hash_password(password: str) -> str:
    """Genera hash para contraseña"""
    return hashlib.sha256(password.encode()).hexdigest()

def cargar_datos_prueba():
    """Carga datos iniciales de prueba"""
    db = DatabaseNFT('losprofetas.db')
    
    print("\n🚀 Iniciando carga de datos de prueba...\n")
    
    # ========== Crear usuarios ==========
    usuarios_datos = [
        {
            'id': 'sys-arivera',
            'username': 'arivera',
            'email': 'arivera@losprofetas.com',
            'password': 'password123',
            'nombre': 'Alejandro Rivera'
        },
        {
            'id': 'sys-lsantos',
            'username': 'lsantos',
            'email': 'lsantos@losprofetas.com',
            'password': 'password123',
            'nombre': 'Laura Santos'
        },
        {
            'id': 'sys-mortega',
            'username': 'mortega',
            'email': 'mortega@losprofetas.com',
            'password': 'password123',
            'nombre': 'María Ortega'
        },
        {
            'id': 'sys-kdiaz',
            'username': 'kdiaz',
            'email': 'kdiaz@losprofetas.com',
            'password': 'password123',
            'nombre': 'Karina Díaz'
        },
        {
            'id': 'sys-nperez',
            'username': 'nperez',
            'email': 'nperez@losprofetas.com',
            'password': 'password123',
            'nombre': 'Nicolás Pérez'
        },
        {
            'id': 'sys-user-demo',
            'username': 'usuario_demo',
            'email': 'demo@losprofetas.com',
            'password': 'demo123',
            'nombre': 'Usuario Demostración'
        }
    ]
    
    usuarios_creados = []
    for u in usuarios_datos:
        if db.crear_usuario(
            id=u['id'],
            username=u['username'],
            email=u['email'],
            password_hash=hash_password(u['password']),
            nombre=u['nombre']
        ):
            print(f"✓ Usuario creado: {u['nombre']} ({u['username']})")
            usuarios_creados.append(u['id'])
        else:
            print(f"⚠ Usuario ya existe: {u['username']}")
            usuarios_creados.append(u['id'])
    
    # ========== Crear NFTs ==========
    nfts_datos = [
        {
            'titulo': 'Profecía Lunar',
            'artista_id': 'sys-arivera',
            'precio': 0.85,
            'categoria': 'art',
            'color_inicio': '#ff9a9e',
            'color_fin': '#fecfef',
            'descripcion': 'Visión nocturna sobre el ocaso del segundo siglo digital. Generativa, edición de 1.',
            'tags': ['lunar', 'generativo', 'místico'],
            'regalias': 5
        },
        {
            'titulo': 'Ecos del Mañana',
            'artista_id': 'sys-lsantos',
            'precio': 1.2,
            'categoria': 'music',
            'color_inicio': '#a18cd1',
            'color_fin': '#fbc2eb',
            'descripcion': 'Composición algorítmica inspirada en frecuencias solares. Loop infinito.',
            'tags': ['ambient', 'solar', 'loop'],
            'regalias': 7.5
        },
        {
            'titulo': 'Guardiana 07',
            'artista_id': 'sys-mortega',
            'precio': 0.45,
            'categoria': 'collectible',
            'color_inicio': '#89f7fe',
            'color_fin': '#66a6ff',
            'descripcion': 'Séptima de una serie de 12 guardianas. Acceso a comunidad privada.',
            'tags': ['serie', 'guardianes', 'utility'],
            'regalias': 5
        },
        {
            'titulo': 'Vidente Urbano',
            'artista_id': 'sys-kdiaz',
            'precio': 2.1,
            'categoria': 'art',
            'color_inicio': '#f6d365',
            'color_fin': '#fda085',
            'descripcion': 'Retrato fotográfico digital con técnicas de glitch art.',
            'tags': ['retrato', 'urbano', 'glitch'],
            'regalias': 8
        },
        {
            'titulo': 'Ritmo Ancestral',
            'artista_id': 'sys-nperez',
            'precio': 0.33,
            'categoria': 'music',
            'color_inicio': '#f093fb',
            'color_fin': '#f5576c',
            'descripcion': 'Sample de tambores prehispánicos cruzados con synths analógicos.',
            'tags': ['ancestral', 'beats', 'fusión'],
            'regalias': 5
        },
        {
            'titulo': 'Sello Profético',
            'artista_id': 'sys-arivera',
            'precio': 0.12,
            'categoria': 'collectible',
            'color_inicio': '#5ee7df',
            'color_fin': '#b490ca',
            'descripcion': 'Acceso simbólico al Colectivo. Tira limitada de 1000.',
            'tags': ['acceso', 'sigilo', 'colectivo'],
            'regalias': 2.5
        },
        {
            'titulo': 'Nexo Digital',
            'artista_id': 'sys-lsantos',
            'precio': 1.75,
            'categoria': 'art',
            'color_inicio': '#fa709a',
            'color_fin': '#fee140',
            'descripcion': 'Instalación interactiva que explora la conectividad humana.',
            'tags': ['digital', 'interactivo', 'nexo'],
            'regalias': 6
        },
        {
            'titulo': 'Ondas Cósmicas',
            'artista_id': 'sys-mortega',
            'precio': 1.5,
            'categoria': 'music',
            'color_inicio': '#30cfd0',
            'color_fin': '#330867',
            'descripcion': 'Sinfonía generativa basada en radiación cósmica de fondo.',
            'tags': ['cosmos', 'generativo', 'experimental'],
            'regalias': 7
        }
    ]
    
    nfts_creados = []
    for nft in nfts_datos:
        nft_id = db.crear_nft(
            titulo=nft['titulo'],
            artista_id=nft['artista_id'],
            precio=nft['precio'],
            categoria=nft['categoria'],
            color_inicio=nft['color_inicio'],
            color_fin=nft['color_fin'],
            descripcion=nft['descripcion'],
            tags=nft['tags'],
            regalias=nft['regalias']
        )
        if nft_id:
            print(f"✓ NFT creado: {nft['titulo']} (ID: {nft_id})")
            nfts_creados.append(nft_id)
    
    # ========== Agregar favoritos ==========
    print("\n📌 Agregando favoritos...\n")
    if nfts_creados:
        db.agregar_favorito('sys-user-demo', nfts_creados[0])
        print(f"✓ Favorito agregado: NFT {nfts_creados[0]}")
        
        if len(nfts_creados) > 1:
            db.agregar_favorito('sys-user-demo', nfts_creados[1])
            print(f"✓ Favorito agregado: NFT {nfts_creados[1]}")
    
    # ========== Crear comentarios ==========
    print("\n💬 Agregando comentarios...\n")
    comentarios_datos = [
        {'nft_id': 1, 'usuario_id': 'sys-user-demo', 'contenido': '¡Obra maestra! 🌙'},
        {'nft_id': 2, 'usuario_id': 'sys-user-demo', 'contenido': 'La mejor composición que he escuchado'},
        {'nft_id': 1, 'usuario_id': 'sys-kdiaz', 'contenido': 'Inspirador trabajo'},
    ]
    
    for com in comentarios_datos:
        comentario_id = db.crear_comentario(
            nft_id=com['nft_id'],
            usuario_id=com['usuario_id'],
            contenido=com['contenido']
        )
        if comentario_id:
            print(f"✓ Comentario agregado en NFT {com['nft_id']}")
    
    # ========== Crear transacciones ==========
    print("\n💳 Creando transacciones...\n")
    if len(nfts_creados) > 0:
        tx_id = db.crear_transaccion(
            nft_id=nfts_creados[0],
            vendedor_id='sys-arivera',
            comprador_id='sys-user-demo',
            cantidad=0.85,
            tipo='compra'
        )
        if tx_id:
            print(f"✓ Transacción registrada: ID {tx_id}")
    
    # ========== Crear ofertas ==========
    print("\n🤝 Creando ofertas...\n")
    if len(nfts_creados) > 1:
        oferta_id = db.crear_oferta(
            nft_id=nfts_creados[1],
            usuario_id='sys-user-demo',
            monto=1.0,
            mensaje='Interesado en adquirir esta obra'
        )
        if oferta_id:
            print(f"✓ Oferta creada: ID {oferta_id}")
    
    # ========== Crear notificaciones ==========
    print("\n🔔 Creando notificaciones...\n")
    notificaciones = [
        {
            'usuario_id': 'sys-user-demo',
            'titulo': 'Bienvenido a Los profetas',
            'mensaje': 'Tu cuenta ha sido creada exitosamente',
            'tipo': 'welcome'
        },
        {
            'usuario_id': 'sys-user-demo',
            'titulo': 'Nueva oferta recibida',
            'mensaje': 'Alguien está interesado en tu obra',
            'tipo': 'oferta'
        },
        {
            'usuario_id': 'sys-user-demo',
            'titulo': 'Tu favorito está en venta',
            'mensaje': 'Un NFT que marcaste como favorito está disponible',
            'tipo': 'favorito'
        }
    ]
    
    for notif in notificaciones:
        notif_id = db.crear_notificacion(
            usuario_id=notif['usuario_id'],
            titulo=notif['titulo'],
            mensaje=notif['mensaje'],
            tipo=notif['tipo']
        )
        if notif_id:
            print(f"✓ Notificación creada: {notif['titulo']}")
    
    # ========== Estadísticas ==========
    print("\n\n📊 ESTADÍSTICAS DEL MERCADO\n")
    stats_mercado = db.obtener_estadisticas_mercado()
    print(f"Total de NFTs: {stats_mercado['total_nfts']}")
    print(f"Total de usuarios: {stats_mercado['total_usuarios']}")
    print(f"Total de transacciones: {stats_mercado['total_transacciones']}")
    print(f"Volumen total: {stats_mercado['volumen_total']:.2f} ETH")
    
    print("\n📊 ESTADÍSTICAS DEL USUARIO DEMO\n")
    stats_usuario = db.obtener_estadisticas_usuario('sys-user-demo')
    print(f"Obras creadas: {stats_usuario['obras']}")
    print(f"Favoritos: {stats_usuario['favoritos']}")
    print(f"Notificaciones: {stats_usuario['notificaciones']}")
    print(f"Compras realizadas: {stats_usuario['compras']}")
    
    print("\n✅ ¡Base de datos cargada exitosamente!\n")
    
    db.cerrar()

if __name__ == '__main__':
    cargar_datos_prueba()
