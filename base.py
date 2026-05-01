"""
Los profetas — Base de Datos + ML/AI
Sistema de persistencia para mercado NFT con Machine Learning e Inteligencia Artificial
SQLite3 + Análisis de datos + Recomendaciones + Predicciones
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
import hashlib
from collections import Counter
import statistics
import math

# Machine Learning (si está disponible, si no, usamos lógica simple)
try:
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    from sklearn.linear_model import LinearRegression
    import numpy as np
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    print("⚠️  scikit-learn no instalado. ML simplificado disponible.")

class DatabaseNFT:
    """Gestor de base de datos para el mercado NFT"""
    
    def __init__(self, db_path: str = 'losprofetas.db'):
        """Inicializa conexión a la base de datos"""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._crear_tablas()
    
    def _crear_tablas(self):
        """Crea todas las tablas necesarias"""
        
        # Tabla de usuarios
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                avatar_b64 TEXT,
                nombre TEXT,
                bio TEXT,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                activo INTEGER DEFAULT 1
            )
        ''')
        # Tabla de NFTs
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS nfts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descripcion TEXT,
                artista_id TEXT NOT NULL,
                precio REAL NOT NULL,
                categoria TEXT NOT NULL,
                color_inicio TEXT,
                color_fin TEXT,
                imagen_url TEXT,
                imagen_b64 TEXT,
                tags TEXT,
                regalias REAL DEFAULT 5,
                likes INTEGER DEFAULT 0,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(artista_id) REFERENCES usuarios(id) ON DELETE CASCADE
            )
        ''')
        
        # Tabla de comentarios
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS comentarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nft_id INTEGER NOT NULL,
                usuario_id TEXT NOT NULL,
                contenido TEXT NOT NULL,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                likes INTEGER DEFAULT 0,
                FOREIGN KEY(nft_id) REFERENCES nfts(id) ON DELETE CASCADE,
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            )
        ''')
        
        # Tabla de transacciones
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transacciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nft_id INTEGER NOT NULL,
                vendedor_id TEXT NOT NULL,
                comprador_id TEXT NOT NULL,
                cantidad REAL NOT NULL,
                tipo TEXT NOT NULL,
                estado TEXT DEFAULT 'completada',
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(nft_id) REFERENCES nfts(id) ON DELETE CASCADE,
                FOREIGN KEY(vendedor_id) REFERENCES usuarios(id),
                FOREIGN KEY(comprador_id) REFERENCES usuarios(id)
            )
        ''')
        
        # Tabla de ofertas
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ofertas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nft_id INTEGER NOT NULL,
                usuario_id TEXT NOT NULL,
                monto REAL NOT NULL,
                mensaje TEXT,
                estado TEXT DEFAULT 'pendiente',
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(nft_id) REFERENCES nfts(id) ON DELETE CASCADE,
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            )
        ''')
        
        # Tabla de favoritos
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS favoritos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id TEXT NOT NULL,
                nft_id INTEGER NOT NULL,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(usuario_id, nft_id),
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                FOREIGN KEY(nft_id) REFERENCES nfts(id) ON DELETE CASCADE
            )
        ''')
        
        # Tabla de notificaciones
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS notificaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id TEXT NOT NULL,
                titulo TEXT NOT NULL,
                mensaje TEXT NOT NULL,
                tipo TEXT NOT NULL,
                leida INTEGER DEFAULT 0,
                relacion_id INTEGER,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            )
        ''')
        
        # Tabla de configuración
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS configuracion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id TEXT UNIQUE NOT NULL,
                tema TEXT DEFAULT 'dark',
                idioma TEXT DEFAULT 'es',
                moneda TEXT DEFAULT 'ETH',
                notificaciones INTEGER DEFAULT 1,
                mostrar_iva INTEGER DEFAULT 0,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            )
        ''')
        
        self.conn.commit()
    
    # ==================== USUARIOS ====================
    
    def crear_usuario(self, id: str, username: str, email: str, password_hash: str, 
                     nombre: str = None) -> bool:
        """Crea un nuevo usuario"""
        try:
            self.cursor.execute('''
                INSERT INTO usuarios (id, username, email, password_hash, nombre)
                VALUES (?, ?, ?, ?, ?)
            ''', (id, username, email, password_hash, nombre))
            self.conn.commit()
            # Crear configuración por defecto
            self.cursor.execute('''
                INSERT INTO configuracion (usuario_id) VALUES (?)
            ''', (id,))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def obtener_usuario(self, usuario_id: str) -> Optional[Dict]:
        """Obtiene datos de un usuario"""
        self.cursor.execute('SELECT * FROM usuarios WHERE id = ?', (usuario_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def obtener_usuario_por_email(self, email: str) -> Optional[Dict]:
        """Obtiene usuario por email"""
        self.cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def actualizar_usuario(self, usuario_id: str, **kwargs) -> bool:
        """Actualiza datos del usuario"""
        campos = ', '.join([f"{k} = ?" for k in kwargs.keys()])
        valores = list(kwargs.values()) + [usuario_id]
        try:
            self.cursor.execute(f'''
                UPDATE usuarios SET {campos}, actualizado = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', valores)
            self.conn.commit()
            return True
        except:
            return False
    
    # ==================== NFTs ====================
    
    def crear_nft(self, titulo: str, artista_id: str, precio: float, 
                 categoria: str, descripcion: str = None, tags: List[str] = None,
                 color_inicio: str = None, color_fin: str = None,
                 imagen_url: str = None, imagen_b64: str = None,
                 regalias: float = 5) -> Optional[int]:
        """Crea un nuevo NFT"""
        try:
            tags_json = json.dumps(tags or [])
            self.cursor.execute('''
                INSERT INTO nfts 
                (titulo, descripcion, artista_id, precio, categoria, color_inicio, 
                 color_fin, imagen_url, imagen_b64, tags, regalias)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (titulo, descripcion, artista_id, precio, categoria, color_inicio,
                  color_fin, imagen_url, imagen_b64, tags_json, regalias))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Error creando NFT: {e}")
            return None
    
    def obtener_nft(self, nft_id: int) -> Optional[Dict]:
        """Obtiene datos de un NFT"""
        self.cursor.execute('SELECT * FROM nfts WHERE id = ?', (nft_id,))
        row = self.cursor.fetchone()
        if row:
            nft = dict(row)
            nft['tags'] = json.loads(nft['tags'] or '[]')
            return nft
        return None
    
    def obtener_todos_nfts(self, filtro_categoria: str = None, 
                          ordenar_por: str = 'fecha_creacion DESC',
                          limite: int = 50) -> List[Dict]:
        """Obtiene todos los NFTs con filtros opcionales"""
        query = 'SELECT * FROM nfts WHERE 1=1'
        params = []
        
        if filtro_categoria and filtro_categoria != 'all':
            query += ' AND categoria = ?'
            params.append(filtro_categoria)
        
        query += f' ORDER BY {ordenar_por} LIMIT ?'
        params.append(limite)
        
        self.cursor.execute(query, params)
        nfts = []
        for row in self.cursor.fetchall():
            nft = dict(row)
            nft['tags'] = json.loads(nft['tags'] or '[]')
            nfts.append(nft)
        return nfts
    
    def obtener_nfts_por_artista(self, artista_id: str) -> List[Dict]:
        """Obtiene todos los NFTs de un artista"""
        self.cursor.execute('''
            SELECT * FROM nfts WHERE artista_id = ? ORDER BY fecha_creacion DESC
        ''', (artista_id,))
        nfts = []
        for row in self.cursor.fetchall():
            nft = dict(row)
            nft['tags'] = json.loads(nft['tags'] or '[]')
            nfts.append(nft)
        return nfts
    
    def actualizar_nft(self, nft_id: int, **kwargs) -> bool:
        """Actualiza datos de un NFT"""
        campos = ', '.join([f"{k} = ?" for k in kwargs.keys()])
        valores = list(kwargs.values()) + [nft_id]
        try:
            self.cursor.execute(f'''
                UPDATE nfts SET {campos}, actualizado = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', valores)
            self.conn.commit()
            return True
        except:
            return False
    
    def eliminar_nft(self, nft_id: int) -> bool:
        """Elimina un NFT"""
        try:
            self.cursor.execute('DELETE FROM nfts WHERE id = ?', (nft_id,))
            self.conn.commit()
            return True
        except:
            return False
    
    # ==================== COMENTARIOS ====================
    
    def crear_comentario(self, nft_id: int, usuario_id: str, contenido: str) -> Optional[int]:
        """Crea un comentario en un NFT"""
        try:
            self.cursor.execute('''
                INSERT INTO comentarios (nft_id, usuario_id, contenido)
                VALUES (?, ?, ?)
            ''', (nft_id, usuario_id, contenido))
            self.conn.commit()
            return self.cursor.lastrowid
        except:
            return None
    
    def obtener_comentarios(self, nft_id: int) -> List[Dict]:
        """Obtiene comentarios de un NFT"""
        self.cursor.execute('''
            SELECT * FROM comentarios WHERE nft_id = ? ORDER BY fecha_creacion DESC
        ''', (nft_id,))
        return [dict(row) for row in self.cursor.fetchall()]
    
    def eliminar_comentario(self, comentario_id: int) -> bool:
        """Elimina un comentario"""
        try:
            self.cursor.execute('DELETE FROM comentarios WHERE id = ?', (comentario_id,))
            self.conn.commit()
            return True
        except:
            return False
    
    # ==================== TRANSACCIONES ====================
    
    def crear_transaccion(self, nft_id: int, vendedor_id: str, comprador_id: str,
                         cantidad: float, tipo: str = 'compra') -> Optional[int]:
        """Registra una transacción"""
        try:
            self.cursor.execute('''
                INSERT INTO transacciones (nft_id, vendedor_id, comprador_id, cantidad, tipo)
                VALUES (?, ?, ?, ?, ?)
            ''', (nft_id, vendedor_id, comprador_id, cantidad, tipo))
            self.conn.commit()
            return self.cursor.lastrowid
        except:
            return None
    
    def obtener_historial_transacciones(self, nft_id: int) -> List[Dict]:
        """Obtiene historial de transacciones de un NFT"""
        self.cursor.execute('''
            SELECT * FROM transacciones WHERE nft_id = ? ORDER BY fecha DESC
        ''', (nft_id,))
        return [dict(row) for row in self.cursor.fetchall()]
    
    def obtener_transacciones_usuario(self, usuario_id: str) -> List[Dict]:
        """Obtiene transacciones de un usuario (compras y ventas)"""
        self.cursor.execute('''
            SELECT * FROM transacciones 
            WHERE vendedor_id = ? OR comprador_id = ? 
            ORDER BY fecha DESC
        ''', (usuario_id, usuario_id))
        return [dict(row) for row in self.cursor.fetchall()]
    
    # ==================== OFERTAS ====================
    
    def crear_oferta(self, nft_id: int, usuario_id: str, monto: float, 
                    mensaje: str = None) -> Optional[int]:
        """Crea una oferta para un NFT"""
        try:
            self.cursor.execute('''
                INSERT INTO ofertas (nft_id, usuario_id, monto, mensaje)
                VALUES (?, ?, ?, ?)
            ''', (nft_id, usuario_id, monto, mensaje))
            self.conn.commit()
            return self.cursor.lastrowid
        except:
            return None
    
    def obtener_ofertas_nft(self, nft_id: int) -> List[Dict]:
        """Obtiene ofertas para un NFT"""
        self.cursor.execute('''
            SELECT * FROM ofertas WHERE nft_id = ? AND estado = 'pendiente'
            ORDER BY monto DESC
        ''', (nft_id,))
        return [dict(row) for row in self.cursor.fetchall()]
    
    def actualizar_oferta(self, oferta_id: int, estado: str) -> bool:
        """Actualiza el estado de una oferta"""
        try:
            self.cursor.execute('''
                UPDATE ofertas SET estado = ?, actualizado = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (estado, oferta_id))
            self.conn.commit()
            return True
        except:
            return False
    
    # ==================== FAVORITOS ====================
    
    def agregar_favorito(self, usuario_id: str, nft_id: int) -> bool:
        """Agrega un NFT a favoritos"""
        try:
            self.cursor.execute('''
                INSERT INTO favoritos (usuario_id, nft_id)
                VALUES (?, ?)
            ''', (usuario_id, nft_id))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def remover_favorito(self, usuario_id: str, nft_id: int) -> bool:
        """Remueve un NFT de favoritos"""
        try:
            self.cursor.execute('''
                DELETE FROM favoritos WHERE usuario_id = ? AND nft_id = ?
            ''', (usuario_id, nft_id))
            self.conn.commit()
            return True
        except:
            return False
    
    def obtener_favoritos(self, usuario_id: str) -> List[Dict]:
        """Obtiene NFTs favoritos del usuario"""
        self.cursor.execute('''
            SELECT n.* FROM nfts n
            JOIN favoritos f ON n.id = f.nft_id
            WHERE f.usuario_id = ?
            ORDER BY f.fecha_creacion DESC
        ''', (usuario_id,))
        nfts = []
        for row in self.cursor.fetchall():
            nft = dict(row)
            nft['tags'] = json.loads(nft['tags'] or '[]')
            nfts.append(nft)
        return nfts
    
    def es_favorito(self, usuario_id: str, nft_id: int) -> bool:
        """Verifica si un NFT es favorito"""
        self.cursor.execute('''
            SELECT 1 FROM favoritos WHERE usuario_id = ? AND nft_id = ?
        ''', (usuario_id, nft_id))
        return self.cursor.fetchone() is not None
    
    # ==================== NOTIFICACIONES ====================
    
    def crear_notificacion(self, usuario_id: str, titulo: str, mensaje: str,
                          tipo: str, relacion_id: int = None) -> Optional[int]:
        """Crea una notificación"""
        try:
            self.cursor.execute('''
                INSERT INTO notificaciones (usuario_id, titulo, mensaje, tipo, relacion_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (usuario_id, titulo, mensaje, tipo, relacion_id))
            self.conn.commit()
            return self.cursor.lastrowid
        except:
            return None
    
    def obtener_notificaciones(self, usuario_id: str, no_leidas: bool = False) -> List[Dict]:
        """Obtiene notificaciones del usuario"""
        query = 'SELECT * FROM notificaciones WHERE usuario_id = ?'
        params = [usuario_id]
        
        if no_leidas:
            query += ' AND leida = 0'
        
        query += ' ORDER BY fecha DESC LIMIT 50'
        
        self.cursor.execute(query, params)
        return [dict(row) for row in self.cursor.fetchall()]
    
    def marcar_notificacion_leida(self, notificacion_id: int) -> bool:
        """Marca notificación como leída"""
        try:
            self.cursor.execute('''
                UPDATE notificaciones SET leida = 1 WHERE id = ?
            ''', (notificacion_id,))
            self.conn.commit()
            return True
        except:
            return False
    
    def marcar_todas_leidas(self, usuario_id: str) -> bool:
        """Marca todas las notificaciones como leídas"""
        try:
            self.cursor.execute('''
                UPDATE notificaciones SET leida = 1 WHERE usuario_id = ?
            ''', (usuario_id,))
            self.conn.commit()
            return True
        except:
            return False
    
    def contar_no_leidas(self, usuario_id: str) -> int:
        """Cuenta notificaciones no leídas"""
        self.cursor.execute('''
            SELECT COUNT(*) as total FROM notificaciones 
            WHERE usuario_id = ? AND leida = 0
        ''', (usuario_id,))
        return self.cursor.fetchone()['total']
    
    # ==================== CONFIGURACIÓN ====================
    
    def obtener_configuracion(self, usuario_id: str) -> Optional[Dict]:
        """Obtiene configuración del usuario"""
        self.cursor.execute('''
            SELECT * FROM configuracion WHERE usuario_id = ?
        ''', (usuario_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def actualizar_configuracion(self, usuario_id: str, **kwargs) -> bool:
        """Actualiza configuración del usuario"""
        campos = ', '.join([f"{k} = ?" for k in kwargs.keys()])
        valores = list(kwargs.values()) + [usuario_id]
        try:
            self.cursor.execute(f'''
                UPDATE configuracion SET {campos}, actualizado = CURRENT_TIMESTAMP
                WHERE usuario_id = ?
            ''', valores)
            self.conn.commit()
            return True
        except:
            return False
    
    # ==================== ESTADÍSTICAS ====================
    
    def obtener_estadisticas_usuario(self, usuario_id: str) -> Dict:
        """Obtiene estadísticas del usuario"""
        nfts = self.cursor.execute(
            'SELECT COUNT(*) FROM nfts WHERE artista_id = ?', (usuario_id,)
        ).fetchone()[0]
        
        favoritos = self.cursor.execute(
            'SELECT COUNT(*) FROM favoritos WHERE usuario_id = ?', (usuario_id,)
        ).fetchone()[0]
        
        notificaciones = self.cursor.execute(
            'SELECT COUNT(*) FROM notificaciones WHERE usuario_id = ?', (usuario_id,)
        ).fetchone()[0]
        
        compras = self.cursor.execute(
            'SELECT COUNT(*) FROM transacciones WHERE comprador_id = ?', (usuario_id,)
        ).fetchone()[0]
        
        return {
            'obras': nfts,
            'favoritos': favoritos,
            'notificaciones': notificaciones,
            'compras': compras
        }
    
    def obtener_estadisticas_mercado(self) -> Dict:
        """Obtiene estadísticas del mercado"""
        total_nfts = self.cursor.execute(
            'SELECT COUNT(*) FROM nfts'
        ).fetchone()[0]
        
        total_usuarios = self.cursor.execute(
            'SELECT COUNT(*) FROM usuarios'
        ).fetchone()[0]
        
        total_transacciones = self.cursor.execute(
            'SELECT COUNT(*) FROM transacciones'
        ).fetchone()[0]
        
        volumen_total = self.cursor.execute(
            'SELECT SUM(cantidad) FROM transacciones'
        ).fetchone()[0] or 0
        
        return {
            'total_nfts': total_nfts,
            'total_usuarios': total_usuarios,
            'total_transacciones': total_transacciones,
            'volumen_total': volumen_total
        }
    
    # ==================== UTILIDADES ====================
    
    def cerrar(self):
        """Cierra la conexión a la base de datos"""
        self.conn.close()
    
    def limpiar_datos(self):
        """Limpia todos los datos (usa con cuidado)"""
        try:
            self.cursor.execute('DELETE FROM notificaciones')
            self.cursor.execute('DELETE FROM favoritos')
            self.cursor.execute('DELETE FROM ofertas')
            self.cursor.execute('DELETE FROM transacciones')
            self.cursor.execute('DELETE FROM comentarios')
            self.cursor.execute('DELETE FROM nfts')
            self.cursor.execute('DELETE FROM configuracion')
            self.cursor.execute('DELETE FROM usuarios')
            self.conn.commit()
            return True
        except:
            return False
    
    def exportar_datos_usuario(self, usuario_id: str) -> Dict:
        """Exporta todos los datos de un usuario"""
        usuario = self.obtener_usuario(usuario_id)
        nfts = self.obtener_nfts_por_artista(usuario_id)
        favoritos = self.obtener_favoritos(usuario_id)
        transacciones = self.obtener_transacciones_usuario(usuario_id)
        configuracion = self.obtener_configuracion(usuario_id)
        
        return {
            'usuario': usuario,
            'nfts_creados': nfts,
            'favoritos': favoritos,
            'transacciones': transacciones,
            'configuracion': configuracion,
            'fecha_exportacion': datetime.now().isoformat()
        }
    
    # ==================== MACHINE LEARNING ====================
    
    def obtener_recomendaciones(self, usuario_id: str, limite: int = 10) -> List[Dict]:
        """
        IA: Genera recomendaciones personalizadas basadas en:
        - Categorías favoritas del usuario
        - NFTs que ha comprado/comentado
        - Artistas similares
        - Tendencias del mercado
        """
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            return []
        
        # Obtener historial del usuario
        favoritos = self.obtener_favoritos(usuario_id)
        transacciones = self.obtener_transacciones_usuario(usuario_id)
        todos_nfts = self.obtener_todos_nfts(limite=1000)
        
        if not todos_nfts:
            return []
        
        # Categorías que le gustan
        categorias_favoritas = Counter()
        tags_favoritos = Counter()
        artistas_seguidos = Counter()
        
        for nft in favoritos:
            categorias_favoritas[nft.get('categoria')] += 2
            for tag in nft.get('tags', []):
                tags_favoritos[tag] += 1
        
        for tx in transacciones:
            nft = self.obtener_nft(tx['nft_id'])
            if nft:
                categorias_favoritas[nft['categoria']] += 3
                artistas_seguidos[nft['artista_id']] += 2
        
        # Puntuación de recomendación para cada NFT
        recomendaciones = []
        ya_visto = {nft['id'] for nft in favoritos + [self.obtener_nft(tx['nft_id']) for tx in transacciones if self.obtener_nft(tx['nft_id'])]}
        
        for nft in todos_nfts:
            if nft['id'] in ya_visto:
                continue
            
            score = 0
            # Bonus por categoría
            score += categorias_favoritas.get(nft['categoria'], 0) * 2
            # Bonus por tags
            for tag in nft.get('tags', []):
                score += tags_favoritos.get(tag, 0) * 1.5
            # Bonus por popularidad (likes)
            score += nft.get('likes', 0) * 0.5
            # Bonus por precio similar a compras anteriores
            for tx in transacciones:
                tx_nft = self.obtener_nft(tx['nft_id'])
                if tx_nft:
                    precio_diff = abs(nft['precio'] - tx_nft['precio'])
                    score += max(0, 5 - precio_diff) * 0.3
            
            if score > 0:
                recomendaciones.append({**nft, 'score_recomendacion': round(score, 2)})
        
        # Ordenar por score y retornar
        recomendaciones.sort(key=lambda x: x['score_recomendacion'], reverse=True)
        return recomendaciones[:limite]
    
    def analizar_tendencias_mercado(self) -> Dict:
        """
        IA: Analiza tendencias del mercado NFT
        Retorna: categorías trending, precios, volumen, etc.
        """
        nfts = self.obtener_todos_nfts(limite=1000)
        transacciones = self.cursor.execute('SELECT * FROM transacciones').fetchall()
        
        if not nfts:
            return {'error': 'No hay datos'}
        
        # Análisis por categoría
        categorias = Counter()
        precios_por_categoria = {}
        likes_por_categoria = Counter()
        
        for nft in nfts:
            cat = nft['categoria']
            categorias[cat] += 1
            likes_por_categoria[cat] += nft.get('likes', 0)
            
            if cat not in precios_por_categoria:
                precios_por_categoria[cat] = []
            precios_por_categoria[cat].append(nft['precio'])
        
        # Estadísticas por categoría
        categoria_stats = {}
        for cat, precios in precios_por_categoria.items():
            categoria_stats[cat] = {
                'cantidad': len(precios),
                'precio_promedio': round(statistics.mean(precios), 3),
                'precio_min': round(min(precios), 3),
                'precio_max': round(max(precios), 3),
                'likes_totales': likes_por_categoria[cat],
                'volatilidad': round(statistics.stdev(precios), 3) if len(precios) > 1 else 0
            }
        
        # Volumen y tendencias
        volumen_total = sum(t['cantidad'] for t in transacciones)
        
        # Categorías trending (más populares)
        trending = sorted(categorias.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'categorias_trending': [{'nombre': cat, 'count': count} for cat, count in trending],
            'estadisticas_por_categoria': categoria_stats,
            'volumen_total': round(volumen_total, 3),
            'total_nfts': len(nfts),
            'numero_transacciones': len(list(transacciones))
        }
    
    def predecir_precio_nft(self, nft_id: int) -> Dict:
        """
        ML: Predice el precio futuro de un NFT basándose en:
        - Precios históricos
        - Categoría
        - Tendencias de mercado
        - Características similares
        """
        nft = self.obtener_nft(nft_id)
        if not nft:
            return {'error': 'NFT no encontrado'}
        
        # Obtener historial de transacciones del NFT
        historial = self.obtener_historial_transacciones(nft_id)
        
        if not historial:
            # Si no hay historial, usar promedio de categoría
            nfts_categoria = self.obtener_todos_nfts(
                filtro_categoria=nft['categoria'], limite=100
            )
            if nfts_categoria:
                precios = [n['precio'] for n in nfts_categoria]
                precio_promedio = statistics.mean(precios)
                tendencia = 'estable'
                confianza = 0.5
            else:
                precio_promedio = nft['precio']
                tendencia = 'desconocida'
                confianza = 0.1
        else:
            # Análisis de tendencia histórica
            precios = [t['cantidad'] for t in historial]
            
            if len(precios) == 1:
                precio_promedio = precios[0]
                tendencia = 'estable'
                confianza = 0.6
            else:
                # Análisis simple de tendencia
                if HAS_SKLEARN and len(precios) > 2:
                    try:
                        X = np.array([[i] for i in range(len(precios))])
                        y = np.array(precios)
                        model = LinearRegression()
                        model.fit(X, y)
                        prediccion = float(model.predict([[len(precios)]])[0])
                        slope = model.coef_[0]
                        
                        if slope > 0.05:
                            tendencia = 'alcista'
                        elif slope < -0.05:
                            tendencia = 'bajista'
                        else:
                            tendencia = 'estable'
                        
                        precio_promedio = round(prediccion, 3)
                        confianza = min(0.95, 0.6 + len(precios) * 0.05)
                    except:
                        precio_promedio = statistics.mean(precios)
                        tendencia = 'estable'
                        confianza = 0.7
                else:
                    precio_promedio = statistics.mean(precios)
                    diff = precios[-1] - precios[0] if len(precios) > 1 else 0
                    if diff > 0.1:
                        tendencia = 'alcista'
                    elif diff < -0.1:
                        tendencia = 'bajista'
                    else:
                        tendencia = 'estable'
                    confianza = 0.7
        
        # Factores adicionales
        likes_factor = 1 + (nft.get('likes', 0) * 0.01)
        regalias_factor = 1 + (nft.get('regalias', 5) / 100)
        
        precio_predicho = round(precio_promedio * likes_factor * regalias_factor, 3)
        
        return {
            'nft_id': nft_id,
            'titulo': nft['titulo'],
            'precio_actual': nft['precio'],
            'precio_predicho': precio_predicho,
            'cambio_esperado': round(precio_predicho - nft['precio'], 3),
            'tendencia': tendencia,
            'confianza': round(confianza, 2),
            'recomendacion': 'COMPRAR' if precio_predicho > nft['precio'] * 1.1 else 'VENDER' if precio_predicho < nft['precio'] * 0.9 else 'ESPERAR'
        }
    
    def detectar_anomalias(self) -> List[Dict]:
        """
        IA: Detecta anomalías en el mercado:
        - NFTs con precios sospechosos
        - Usuarios con comportamiento extraño
        - Transacciones inusuales
        """
        anomalias = []
        nfts = self.obtener_todos_nfts(limite=500)
        
        if not nfts:
            return anomalias
        
        # Análisis de precios por categoría
        precios_por_cat = {}
        for nft in nfts:
            cat = nft['categoria']
            if cat not in precios_por_cat:
                precios_por_cat[cat] = []
            precios_por_cat[cat].append(nft['precio'])
        
        # Detectar outliers de precio
        for nft in nfts:
            cat = nft['categoria']
            precios = precios_por_cat[cat]
            
            if len(precios) > 3:
                media = statistics.mean(precios)
                std = statistics.stdev(precios)
                z_score = abs((nft['precio'] - media) / std) if std > 0 else 0
                
                if z_score > 2.5:  # Más de 2.5 desviaciones estándar
                    anomalias.append({
                        'tipo': 'precio_anomalo',
                        'nft_id': nft['id'],
                        'titulo': nft['titulo'],
                        'precio': nft['precio'],
                        'precio_esperado': round(media, 3),
                        'z_score': round(z_score, 2),
                        'severidad': 'alta' if z_score > 3.5 else 'media'
                    })
        
        return anomalias
    
    def obtener_similares(self, nft_id: int, limite: int = 5) -> List[Dict]:
        """
        IA: Encuentra NFTs similares basándose en:
        - Categoría
        - Tags
        - Rango de precio
        - Artista
        """
        nft = self.obtener_nft(nft_id)
        if not nft:
            return []
        
        todos = self.obtener_todos_nfts(limite=500)
        similares = []
        
        for otro in todos:
            if otro['id'] == nft_id:
                continue
            
            score = 0
            
            # Misma categoría: +3
            if otro['categoria'] == nft['categoria']:
                score += 3
            
            # Tags compartidos
            tags_propios = set(nft.get('tags', []))
            tags_otro = set(otro.get('tags', []))
            tags_comunes = len(tags_propios & tags_otro)
            score += tags_comunes * 2
            
            # Precio similar (±30%)
            if abs(otro['precio'] - nft['precio']) / nft['precio'] < 0.3:
                score += 2
            
            # Mismo artista
            if otro['artista_id'] == nft['artista_id']:
                score += 2
            
            if score > 0:
                similares.append({**otro, 'score_similitud': score})
        
        similares.sort(key=lambda x: x['score_similitud'], reverse=True)
        return similares[:limite]
    
    def analisis_usuario_detallado(self, usuario_id: str) -> Dict:
        """
        IA: Análisis completo del perfil de usuario
        Incluye: actividad, preferencias, patrón de compra, valor
        """
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            return {'error': 'Usuario no encontrado'}
        
        stats = self.obtener_estadisticas_usuario(usuario_id)
        favoritos = self.obtener_favoritos(usuario_id)
        transacciones = self.obtener_transacciones_usuario(usuario_id)
        nfts_creados = self.obtener_nfts_por_artista(usuario_id)
        
        # Análisis de preferencias
        categorias = Counter()
        tags = Counter()
        gasto_total = 0
        ingreso_total = 0
        
        for fav in favoritos:
            categorias[fav.get('categoria')] += 1
            for tag in fav.get('tags', []):
                tags[tag] += 1
        
        for tx in transacciones:
            if tx['comprador_id'] == usuario_id:
                gasto_total += tx['cantidad']
            if tx['vendedor_id'] == usuario_id:
                ingreso_total += tx['cantidad']
        
        # Clasificación de usuario
        if ingreso_total > 5 and stats['obras'] > 3:
            tipo_usuario = 'Artista Activo'
        elif gasto_total > 5 and stats['compras'] > 5:
            tipo_usuario = 'Coleccionista'
        elif stats['favoritos'] > 10:
            tipo_usuario = 'Explorador'
        else:
            tipo_usuario = 'Nuevo Usuario'
        
        # Score de engagement
        engagement_score = min(100, (
            stats['obras'] * 10 +
            stats['compras'] * 8 +
            stats['favoritos'] * 2 +
            len([c for c in self.obtener_comentarios(0) if c.get('usuario_id') == usuario_id]) * 5
        ))
        
        return {
            'usuario': usuario['username'],
            'tipo_usuario': tipo_usuario,
            'engagement_score': round(engagement_score, 1),
            'estadisticas': stats,
            'categorias_favoritas': dict(categorias.most_common(5)),
            'tags_favoritos': dict(tags.most_common(5)),
            'gasto_total': round(gasto_total, 3),
            'ingreso_total': round(ingreso_total, 3),
            'balance_neto': round(ingreso_total - gasto_total, 3),
            'valor_portfolio': round(sum(nft['precio'] for nft in nfts_creados), 3),
            'fecha_registro': usuario['fecha_registro'],
            'ultima_actividad': usuario['actualizado']
        }
    
    def busqueda_inteligente(self, query: str, filtros: Dict = None) -> List[Dict]:
        """
        IA: Búsqueda semántica inteligente
        Busca en títulos, descripciones, tags, artistas
        Retorna resultados relevantes ordenados
        """
        query = query.lower()
        todos_nfts = self.obtener_todos_nfts(limite=500)
        resultados = []
        
        for nft in todos_nfts:
            score = 0
            
            # Búsqueda en título (mayor peso)
            if query in nft['titulo'].lower():
                score += 10
            if query == nft['titulo'].lower():
                score += 50
            
            # Búsqueda en descripción
            if query in (nft.get('descripcion', '') or '').lower():
                score += 5
            
            # Búsqueda en tags
            for tag in nft.get('tags', []):
                if query in tag.lower():
                    score += 3
                if query == tag.lower():
                    score += 10
            
            # Búsqueda en artista
            artista = self.obtener_usuario(nft['artista_id'])
            if artista:
                if query in artista['nombre'].lower():
                    score += 8
                if query in artista['username'].lower():
                    score += 6
            
            # Aplicar filtros si existen
            if filtros:
                if filtros.get('categoria') and nft['categoria'] != filtros['categoria']:
                    continue
                if filtros.get('precio_min') and nft['precio'] < filtros['precio_min']:
                    continue
                if filtros.get('precio_max') and nft['precio'] > filtros['precio_max']:
                    continue
            
            if score > 0:
                resultados.append({**nft, 'score_busqueda': score})
        
        resultados.sort(key=lambda x: x['score_busqueda'], reverse=True)
        return resultados
    
    def generar_insights(self) -> Dict:
        """
        IA: Genera insights automáticos del mercado
        Información valiosa para decisiones
        """
        stats_mercado = self.obtener_estadisticas_mercado()
        tendencias = self.analizar_tendencias_mercado()
        anomalias = self.detectar_anomalias()
        
        nfts = self.obtener_todos_nfts(limite=500)
        usuarios = self.cursor.execute('SELECT COUNT(*) FROM usuarios').fetchone()[0]
        
        # NFTs más populares
        nfts_top = sorted(nfts, key=lambda x: x.get('likes', 0), reverse=True)[:5]
        
        # NFTs más caros
        nfts_premium = sorted(nfts, key=lambda x: x['precio'], reverse=True)[:5]
        
        # NFTs más baratos
        nfts_budget = sorted(nfts, key=lambda x: x['precio'])[:5]
        
        # Categoría más valiosa
        cat_stats = tendencias.get('estadisticas_por_categoria', {})
        cat_mas_valiosa = max(cat_stats.items(), 
                              key=lambda x: x[1].get('precio_promedio', 0))[0] if cat_stats else 'N/A'
        
        return {
            'resumen': {
                'total_nfts': stats_mercado['total_nfts'],
                'total_usuarios': usuarios,
                'transacciones': stats_mercado['total_transacciones'],
                'volumen_mercado': stats_mercado['volumen_total']
            },
            'nfts_trending': [{'titulo': n['titulo'], 'likes': n.get('likes', 0)} for n in nfts_top],
            'nfts_premium': [{'titulo': n['titulo'], 'precio': n['precio']} for n in nfts_premium],
            'nfts_budget': [{'titulo': n['titulo'], 'precio': n['precio']} for n in nfts_budget],
            'categoria_mas_valiosa': cat_mas_valiosa,
            'anomalias_detectadas': len(anomalias),
            'fecha_analisis': datetime.now().isoformat()
        }


# ==================== EJEMPLO DE USO ====================
if __name__ == '__main__':
    # Inicializar BD
    db = DatabaseNFT('losprofetas.db')
    
    print("✓ Base de datos inicializada correctamente")
    print("✓ Capacidades de ML y análisis disponibles")
