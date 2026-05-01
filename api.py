"""
Los profetas — API REST
Servidor Flask para exponer la base de datos como API JSON
"""

from flask import Flask, request, jsonify
from base import DatabaseNFT
import json
from datetime import datetime

app = Flask(__name__)
db = DatabaseNFT('losprofetas.db')

# ==================== CONFIGURACIÓN ====================

@app.before_request
def configurar_cors():
    """Configura CORS para desarrollo"""
    pass

@app.after_request
def agregar_cors_headers(response):
    """Agrega headers CORS"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

# ==================== USUARIOS ====================

@app.route('/api/usuarios/<usuario_id>', methods=['GET'])
def obtener_usuario(usuario_id):
    """Obtiene datos de un usuario"""
    usuario = db.obtener_usuario(usuario_id)
    if usuario:
        return jsonify(usuario), 200
    return jsonify({'error': 'Usuario no encontrado'}), 404

@app.route('/api/usuarios', methods=['POST'])
def crear_usuario():
    """Crea un nuevo usuario"""
    datos = request.json
    if not datos or not all(k in datos for k in ['id', 'username', 'email', 'password_hash']):
        return jsonify({'error': 'Datos incompletos'}), 400
    
    if db.crear_usuario(
        id=datos['id'],
        username=datos['username'],
        email=datos['email'],
        password_hash=datos['password_hash'],
        nombre=datos.get('nombre')
    ):
        return jsonify({'message': 'Usuario creado', 'id': datos['id']}), 201
    return jsonify({'error': 'Error al crear usuario'}), 400

@app.route('/api/usuarios/<usuario_id>', methods=['PUT'])
def actualizar_usuario(usuario_id):
    """Actualiza datos del usuario"""
    datos = request.json
    if db.actualizar_usuario(usuario_id, **datos):
        return jsonify({'message': 'Usuario actualizado'}), 200
    return jsonify({'error': 'Error al actualizar'}), 400

# ==================== NFTs ====================

@app.route('/api/nfts', methods=['GET'])
def obtener_nfts():
    """Obtiene todos los NFTs con filtros opcionales"""
    categoria = request.args.get('categoria')
    ordenar = request.args.get('sort', 'fecha_creacion DESC')
    limite = int(request.args.get('limite', 50))
    
    nfts = db.obtener_todos_nfts(
        filtro_categoria=categoria,
        ordenar_por=ordenar,
        limite=limite
    )
    return jsonify(nfts), 200

@app.route('/api/nfts/<int:nft_id>', methods=['GET'])
def obtener_nft(nft_id):
    """Obtiene un NFT específico"""
    nft = db.obtener_nft(nft_id)
    if nft:
        # Incluir comentarios y transacciones
        nft['comentarios'] = db.obtener_comentarios(nft_id)
        nft['historial'] = db.obtener_historial_transacciones(nft_id)
        nft['ofertas'] = db.obtener_ofertas_nft(nft_id)
        return jsonify(nft), 200
    return jsonify({'error': 'NFT no encontrado'}), 404

@app.route('/api/nfts', methods=['POST'])
def crear_nft():
    """Crea un nuevo NFT"""
    datos = request.json
    if not all(k in datos for k in ['titulo', 'artista_id', 'precio', 'categoria']):
        return jsonify({'error': 'Datos incompletos'}), 400
    
    nft_id = db.crear_nft(
        titulo=datos['titulo'],
        artista_id=datos['artista_id'],
        precio=datos['precio'],
        categoria=datos['categoria'],
        descripcion=datos.get('descripcion'),
        tags=datos.get('tags', []),
        color_inicio=datos.get('color_inicio'),
        color_fin=datos.get('color_fin'),
        imagen_url=datos.get('imagen_url'),
        imagen_b64=datos.get('imagen_b64'),
        regalias=datos.get('regalias', 5)
    )
    
    if nft_id:
        return jsonify({'message': 'NFT creado', 'id': nft_id}), 201
    return jsonify({'error': 'Error al crear NFT'}), 400

@app.route('/api/nfts/<int:nft_id>', methods=['PUT'])
def actualizar_nft(nft_id):
    """Actualiza un NFT"""
    datos = request.json
    if db.actualizar_nft(nft_id, **datos):
        return jsonify({'message': 'NFT actualizado'}), 200
    return jsonify({'error': 'Error al actualizar'}), 400

@app.route('/api/nfts/<int:nft_id>', methods=['DELETE'])
def eliminar_nft(nft_id):
    """Elimina un NFT"""
    if db.eliminar_nft(nft_id):
        return jsonify({'message': 'NFT eliminado'}), 200
    return jsonify({'error': 'Error al eliminar'}), 400

@app.route('/api/artistas/<artista_id>/nfts', methods=['GET'])
def obtener_nfts_artista(artista_id):
    """Obtiene todos los NFTs de un artista"""
    nfts = db.obtener_nfts_por_artista(artista_id)
    return jsonify(nfts), 200

# ==================== COMENTARIOS ====================

@app.route('/api/nfts/<int:nft_id>/comentarios', methods=['GET'])
def obtener_comentarios(nft_id):
    """Obtiene comentarios de un NFT"""
    comentarios = db.obtener_comentarios(nft_id)
    return jsonify(comentarios), 200

@app.route('/api/nfts/<int:nft_id>/comentarios', methods=['POST'])
def crear_comentario(nft_id):
    """Crea un comentario"""
    datos = request.json
    if not datos or not all(k in datos for k in ['usuario_id', 'contenido']):
        return jsonify({'error': 'Datos incompletos'}), 400
    
    comentario_id = db.crear_comentario(
        nft_id=nft_id,
        usuario_id=datos['usuario_id'],
        contenido=datos['contenido']
    )
    
    if comentario_id:
        return jsonify({'message': 'Comentario creado', 'id': comentario_id}), 201
    return jsonify({'error': 'Error al crear comentario'}), 400

@app.route('/api/comentarios/<int:comentario_id>', methods=['DELETE'])
def eliminar_comentario(comentario_id):
    """Elimina un comentario"""
    if db.eliminar_comentario(comentario_id):
        return jsonify({'message': 'Comentario eliminado'}), 200
    return jsonify({'error': 'Error al eliminar'}), 400

# ==================== TRANSACCIONES ====================

@app.route('/api/transacciones', methods=['POST'])
def crear_transaccion():
    """Registra una transacción"""
    datos = request.json
    if not all(k in datos for k in ['nft_id', 'vendedor_id', 'comprador_id', 'cantidad']):
        return jsonify({'error': 'Datos incompletos'}), 400
    
    tx_id = db.crear_transaccion(
        nft_id=datos['nft_id'],
        vendedor_id=datos['vendedor_id'],
        comprador_id=datos['comprador_id'],
        cantidad=datos['cantidad'],
        tipo=datos.get('tipo', 'compra')
    )
    
    if tx_id:
        return jsonify({'message': 'Transacción registrada', 'id': tx_id}), 201
    return jsonify({'error': 'Error al registrar'}), 400

@app.route('/api/nfts/<int:nft_id>/historial', methods=['GET'])
def obtener_historial(nft_id):
    """Obtiene historial de transacciones de un NFT"""
    historial = db.obtener_historial_transacciones(nft_id)
    return jsonify(historial), 200

@app.route('/api/usuarios/<usuario_id>/transacciones', methods=['GET'])
def obtener_transacciones_usuario(usuario_id):
    """Obtiene transacciones de un usuario"""
    transacciones = db.obtener_transacciones_usuario(usuario_id)
    return jsonify(transacciones), 200

# ==================== OFERTAS ====================

@app.route('/api/nfts/<int:nft_id>/ofertas', methods=['POST'])
def crear_oferta(nft_id):
    """Crea una oferta para un NFT"""
    datos = request.json
    if not datos or not all(k in datos for k in ['usuario_id', 'monto']):
        return jsonify({'error': 'Datos incompletos'}), 400
    
    oferta_id = db.crear_oferta(
        nft_id=nft_id,
        usuario_id=datos['usuario_id'],
        monto=datos['monto'],
        mensaje=datos.get('mensaje')
    )
    
    if oferta_id:
        return jsonify({'message': 'Oferta creada', 'id': oferta_id}), 201
    return jsonify({'error': 'Error al crear oferta'}), 400

@app.route('/api/nfts/<int:nft_id>/ofertas', methods=['GET'])
def obtener_ofertas(nft_id):
    """Obtiene ofertas pendientes para un NFT"""
    ofertas = db.obtener_ofertas_nft(nft_id)
    return jsonify(ofertas), 200

@app.route('/api/ofertas/<int:oferta_id>/<estado>', methods=['PUT'])
def actualizar_oferta(oferta_id, estado):
    """Actualiza el estado de una oferta"""
    if db.actualizar_oferta(oferta_id, estado):
        return jsonify({'message': f'Oferta {estado}'}), 200
    return jsonify({'error': 'Error al actualizar'}), 400

# ==================== FAVORITOS ====================

@app.route('/api/usuarios/<usuario_id>/favoritos', methods=['GET'])
def obtener_favoritos(usuario_id):
    """Obtiene favoritos del usuario"""
    favoritos = db.obtener_favoritos(usuario_id)
    return jsonify(favoritos), 200

@app.route('/api/usuarios/<usuario_id>/favoritos/<int:nft_id>', methods=['POST'])
def agregar_favorito(usuario_id, nft_id):
    """Agrega un NFT a favoritos"""
    if db.agregar_favorito(usuario_id, nft_id):
        return jsonify({'message': 'Agregado a favoritos'}), 201
    return jsonify({'error': 'Ya está en favoritos'}), 400

@app.route('/api/usuarios/<usuario_id>/favoritos/<int:nft_id>', methods=['DELETE'])
def remover_favorito(usuario_id, nft_id):
    """Remueve un NFT de favoritos"""
    if db.remover_favorito(usuario_id, nft_id):
        return jsonify({'message': 'Removido de favoritos'}), 200
    return jsonify({'error': 'Error al remover'}), 400

@app.route('/api/usuarios/<usuario_id>/es-favorito/<int:nft_id>', methods=['GET'])
def es_favorito(usuario_id, nft_id):
    """Verifica si un NFT es favorito"""
    es_fav = db.es_favorito(usuario_id, nft_id)
    return jsonify({'es_favorito': es_fav}), 200

# ==================== NOTIFICACIONES ====================

@app.route('/api/usuarios/<usuario_id>/notificaciones', methods=['GET'])
def obtener_notificaciones(usuario_id):
    """Obtiene notificaciones del usuario"""
    no_leidas = request.args.get('no_leidas', 'false').lower() == 'true'
    notificaciones = db.obtener_notificaciones(usuario_id, no_leidas=no_leidas)
    return jsonify(notificaciones), 200

@app.route('/api/usuarios/<usuario_id>/notificaciones/no-leidas', methods=['GET'])
def contar_no_leidas(usuario_id):
    """Cuenta notificaciones no leídas"""
    count = db.contar_no_leidas(usuario_id)
    return jsonify({'no_leidas': count}), 200

@app.route('/api/notificaciones/<int:notificacion_id>/leer', methods=['PUT'])
def marcar_leida(notificacion_id):
    """Marca notificación como leída"""
    if db.marcar_notificacion_leida(notificacion_id):
        return jsonify({'message': 'Marcado como leído'}), 200
    return jsonify({'error': 'Error'}), 400

@app.route('/api/usuarios/<usuario_id>/notificaciones/marcar-todas', methods=['PUT'])
def marcar_todas_leidas(usuario_id):
    """Marca todas las notificaciones como leídas"""
    if db.marcar_todas_leidas(usuario_id):
        return jsonify({'message': 'Todas marcadas como leídas'}), 200
    return jsonify({'error': 'Error'}), 400

# ==================== CONFIGURACIÓN ====================

@app.route('/api/usuarios/<usuario_id>/configuracion', methods=['GET'])
def obtener_configuracion(usuario_id):
    """Obtiene configuración del usuario"""
    config = db.obtener_configuracion(usuario_id)
    if config:
        return jsonify(config), 200
    return jsonify({'error': 'Configuración no encontrada'}), 404

@app.route('/api/usuarios/<usuario_id>/configuracion', methods=['PUT'])
def actualizar_configuracion(usuario_id):
    """Actualiza configuración"""
    datos = request.json
    if db.actualizar_configuracion(usuario_id, **datos):
        return jsonify({'message': 'Configuración actualizada'}), 200
    return jsonify({'error': 'Error al actualizar'}), 400

# ==================== ESTADÍSTICAS ====================

@app.route('/api/estadisticas/mercado', methods=['GET'])
def obtener_stats_mercado():
    """Obtiene estadísticas del mercado"""
    stats = db.obtener_estadisticas_mercado()
    return jsonify(stats), 200

@app.route('/api/estadisticas/usuarios/<usuario_id>', methods=['GET'])
def obtener_stats_usuario(usuario_id):
    """Obtiene estadísticas del usuario"""
    stats = db.obtener_estadisticas_usuario(usuario_id)
    return jsonify(stats), 200

@app.route('/api/usuarios/<usuario_id>/exportar', methods=['GET'])
def exportar_datos(usuario_id):
    """Exporta todos los datos del usuario"""
    datos = db.exportar_datos_usuario(usuario_id)
    if datos['usuario']:
        return jsonify(datos), 200
    return jsonify({'error': 'Usuario no encontrado'}), 404

# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verificar que el servidor está funcionando"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'database': 'losprofetas.db'
    }), 200

# ==================== ERRORES ====================

@app.errorhandler(404)
def no_encontrado(error):
    return jsonify({'error': 'Endpoint no encontrado'}), 404

@app.errorhandler(500)
def error_servidor(error):
    return jsonify({'error': 'Error interno del servidor'}), 500

# ==================== EJECUTAR ====================

if __name__ == '__main__':
    print("\n🚀 Iniciando API Los profetas en http://localhost:5000\n")
    print("Documentación de endpoints disponible en el código")
    print("Base de datos: losprofetas.db\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
