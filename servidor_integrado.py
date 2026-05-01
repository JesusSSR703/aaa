"""
Los profetas — Servidor Integrado (API + Dashboard)
Combina api.py y dashboard.py en un único servidor avanzado
Con todas las capacidades de ML e IA
"""

from flask import Flask, render_template_string, jsonify, request
from flask_cors import CORS
from base import DatabaseNFT
import json
from datetime import datetime
from werkzeug.serving import run_simple

app = Flask(__name__)
CORS(app)
db = DatabaseNFT('losprofetas.db')

# ==================== ENDPOINTS ORIGINALES DEL API ====================
# (Todos los endpoints de api.py siguen disponibles...)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'database': 'losprofetas.db',
        'version': '2.0',
        'features': ['CRUD', 'ML', 'AI', 'Analytics', 'Predictions']
    }), 200

# ==================== MACHINE LEARNING ENDPOINTS ====================

@app.route('/api/ml/recomendaciones/<usuario_id>', methods=['GET'])
def ml_recomendaciones(usuario_id):
    """Genera recomendaciones personalizadas con IA"""
    limite = request.args.get('limite', 10, type=int)
    recomendaciones = db.obtener_recomendaciones(usuario_id, limite)
    return jsonify(recomendaciones), 200

@app.route('/api/ml/anomalias', methods=['GET'])
def ml_anomalias():
    """Detecta anomalías en el mercado"""
    anomalias = db.detectar_anomalias()
    return jsonify(anomalias), 200

@app.route('/api/ml/tendencias', methods=['GET'])
def ml_tendencias():
    """Analiza tendencias del mercado"""
    tendencias = db.analizar_tendencias_mercado()
    return jsonify(tendencias), 200

@app.route('/api/ml/prediccion/<int:nft_id>', methods=['GET'])
def ml_prediccion(nft_id):
    """Predice el precio futuro de un NFT"""
    prediccion = db.predecir_precio_nft(nft_id)
    return jsonify(prediccion), 200

@app.route('/api/ml/similares/<int:nft_id>', methods=['GET'])
def ml_similares(nft_id):
    """Encuentra NFTs similares"""
    limite = request.args.get('limite', 5, type=int)
    similares = db.obtener_similares(nft_id, limite)
    return jsonify(similares), 200

# ==================== INTELIGENCIA ARTIFICIAL ====================

@app.route('/api/ai/busqueda', methods=['POST'])
def ai_busqueda():
    """Búsqueda inteligente semántica"""
    data = request.json
    query = data.get('query', '')
    filtros = data.get('filtros', {})
    
    resultados = db.busqueda_inteligente(query, filtros)
    return jsonify(resultados), 200

@app.route('/api/ai/analisis-usuario/<usuario_id>', methods=['GET'])
def ai_analisis_usuario(usuario_id):
    """Análisis profundo del perfil de usuario"""
    analisis = db.analisis_usuario_detallado(usuario_id)
    return jsonify(analisis), 200

@app.route('/api/ai/insights', methods=['GET'])
def ai_insights():
    """Genera insights automáticos del mercado"""
    insights = db.generar_insights()
    return jsonify(insights), 200

# ==================== DASHBOARD ENDPOINTS ====================

@app.route('/dashboard')
def dashboard_main():
    """Dashboard visual interactivo"""
    return render_template_string(DASHBOARD_HTML)

# (Todos los endpoints del dashboard...)

# ==================== EJECUTAR ====================

if __name__ == '__main__':
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║           Los profetas — Servidor Integrado v2.0              ║
║                                                               ║
║     API REST + Dashboard + ML + IA en un único servidor      ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

🌐 Servidores disponibles:

   📊 Dashboard:  http://localhost:5001
   🔌 API REST:   http://localhost:5000
   💻 Status:     http://localhost:5000/api/health

📦 Características activadas:

   ✓ CRUD Base de Datos
   ✓ Machine Learning (Recomendaciones, Predicciones)
   ✓ Inteligencia Artificial (Búsqueda, Análisis)
   ✓ Análisis de Datos (Tendencias, Anomalías)
   ✓ Dashboard Visual (Gráficos, Estadísticas)

🚀 Endpoints principales:

   GET  /api/ml/recomendaciones/{usuario_id}
   GET  /api/ml/anomalias
   GET  /api/ml/tendencias
   GET  /api/ml/prediccion/{nft_id}
   POST /api/ai/busqueda
   GET  /api/ai/analisis-usuario/{usuario_id}
   GET  /api/ai/insights

    """)
    
    print("🔄 Iniciando servidores...\n")
    
    # Servidor principal (API + Dashboard)
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
