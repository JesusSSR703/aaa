"""
Los profetas — Dashboard Avanzado
Panel de control visual con ML, análisis y estadísticas
Integrado con api.py
"""

from flask import Flask, render_template_string, jsonify, request
from base import DatabaseNFT
import json
from datetime import datetime

app = Flask(__name__)
db = DatabaseNFT('losprofetas.db')

# ==================== TEMPLATE HTML ====================

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Los profetas - Dashboard Avanzado</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.0.0/dist/chart.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/axios@1.4.0/dist/axios.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #e0e0e0;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        header {
            background: rgba(124, 58, 237, 0.15);
            border: 1px solid rgba(124, 58, 237, 0.3);
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
        }
        
        header h1 {
            font-size: 32px;
            background: linear-gradient(135deg, #7c3aed, #06b6d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 5px;
        }
        
        header p {
            color: #a0a0a0;
            font-size: 14px;
        }
        
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        
        .tab-btn {
            padding: 12px 24px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(124, 58, 237, 0.3);
            color: #e0e0e0;
            cursor: pointer;
            border-radius: 8px;
            transition: all 0.3s;
            font-weight: 500;
        }
        
        .tab-btn:hover {
            background: rgba(124, 58, 237, 0.2);
            border-color: rgba(124, 58, 237, 0.6);
        }
        
        .tab-btn.active {
            background: linear-gradient(135deg, #7c3aed, #06b6d4);
            border-color: transparent;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
            animation: fadeIn 0.3s;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(124, 58, 237, 0.2);
            padding: 20px;
            border-radius: 12px;
            backdrop-filter: blur(10px);
            transition: all 0.3s;
        }
        
        .card:hover {
            border-color: rgba(124, 58, 237, 0.5);
            background: rgba(255, 255, 255, 0.08);
        }
        
        .card-title {
            font-size: 14px;
            color: #a0a0a0;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }
        
        .card-value {
            font-size: 32px;
            font-weight: 700;
            background: linear-gradient(135deg, #7c3aed, #06b6d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .chart-container {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(124, 58, 237, 0.2);
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
            position: relative;
            height: 400px;
        }
        
        .list {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(124, 58, 237, 0.2);
            border-radius: 12px;
            overflow: hidden;
        }
        
        .list-item {
            padding: 15px 20px;
            border-bottom: 1px solid rgba(124, 58, 237, 0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .list-item:last-child {
            border-bottom: none;
        }
        
        .list-item-title {
            font-weight: 500;
        }
        
        .list-item-value {
            color: #7c3aed;
            font-weight: 600;
        }
        
        .badge {
            display: inline-block;
            padding: 4px 12px;
            background: rgba(124, 58, 237, 0.3);
            border: 1px solid rgba(124, 58, 237, 0.6);
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
        }
        
        .badge.up {
            background: rgba(34, 197, 94, 0.3);
            border-color: rgba(34, 197, 94, 0.6);
            color: #86efac;
        }
        
        .badge.down {
            background: rgba(239, 68, 68, 0.3);
            border-color: rgba(239, 68, 68, 0.6);
            color: #fca5a5;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #7c3aed;
        }
        
        .spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 2px solid rgba(124, 58, 237, 0.3);
            border-top-color: #7c3aed;
            border-radius: 50%;
            animation: spin 0.6s linear infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .error {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.5);
            color: #fca5a5;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        
        .success {
            background: rgba(34, 197, 94, 0.1);
            border: 1px solid rgba(34, 197, 94, 0.5);
            color: #86efac;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        
        .row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        input, select {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(124, 58, 237, 0.3);
            color: #e0e0e0;
            padding: 10px 15px;
            border-radius: 8px;
            margin-bottom: 10px;
            width: 100%;
        }
        
        button.btn {
            background: linear-gradient(135deg, #7c3aed, #06b6d4);
            border: none;
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        button.btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(124, 58, 237, 0.3);
        }
        
        footer {
            text-align: center;
            padding: 20px;
            color: #606060;
            font-size: 12px;
            margin-top: 40px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Los profetas — Dashboard Avanzado</h1>
            <p>Panel de control con ML, análisis de datos e inteligencia artificial</p>
        </header>
        
        <div class="tabs">
            <button class="tab-btn active" onclick="switchTab('estadisticas')">📈 Estadísticas</button>
            <button class="tab-btn" onclick="switchTab('ml')">🤖 Machine Learning</button>
            <button class="tab-btn" onclick="switchTab('ia')">✨ Inteligencia Artificial</button>
            <button class="tab-btn" onclick="switchTab('analisis')">🔍 Análisis Avanzado</button>
            <button class="tab-btn" onclick="switchTab('predicciones')">🔮 Predicciones</button>
        </div>
        
        <!-- TAB 1: ESTADÍSTICAS -->
        <div id="estadisticas" class="tab-content active">
            <h2 style="margin-bottom: 20px; color: #7c3aed;">📊 Estadísticas del Mercado</h2>
            
            <div class="grid">
                <div class="card">
                    <div class="card-title">Total NFTs</div>
                    <div class="card-value" id="total-nfts">—</div>
                </div>
                <div class="card">
                    <div class="card-title">Usuarios Activos</div>
                    <div class="card-value" id="total-usuarios">—</div>
                </div>
                <div class="card">
                    <div class="card-title">Transacciones</div>
                    <div class="card-value" id="total-transacciones">—</div>
                </div>
                <div class="card">
                    <div class="card-title">Volumen (ETH)</div>
                    <div class="card-value" id="volumen-total">—</div>
                </div>
            </div>
            
            <div class="row">
                <div class="chart-container">
                    <canvas id="categoriesChart"></canvas>
                </div>
                <div class="chart-container">
                    <canvas id="pricesChart"></canvas>
                </div>
            </div>
        </div>
        
        <!-- TAB 2: MACHINE LEARNING -->
        <div id="ml" class="tab-content">
            <h2 style="margin-bottom: 20px; color: #7c3aed;">🤖 Machine Learning & Análisis</h2>
            
            <div class="row">
                <div>
                    <h3 style="margin-bottom: 15px;">Recomendaciones Personalizadas</h3>
                    <input type="text" id="usuario-recomendaciones" placeholder="ID del usuario (ej: sys-user-demo)">
                    <button class="btn" onclick="loadRecomendaciones()">Generar Recomendaciones</button>
                    <div id="recomendaciones-list" style="margin-top: 20px;"></div>
                </div>
                <div>
                    <h3 style="margin-bottom: 15px;">Detectar Anomalías</h3>
                    <button class="btn" onclick="loadAnomalias()">Analizar Anomalías</button>
                    <div id="anomalias-list" style="margin-top: 20px;"></div>
                </div>
            </div>
        </div>
        
        <!-- TAB 3: INTELIGENCIA ARTIFICIAL -->
        <div id="ia" class="tab-content">
            <h2 style="margin-bottom: 20px; color: #7c3aed;">✨ Inteligencia Artificial</h2>
            
            <div class="row">
                <div>
                    <h3 style="margin-bottom: 15px;">Búsqueda Inteligente</h3>
                    <input type="text" id="busqueda-query" placeholder="Buscar NFT (ej: lunar, arte, música)...">
                    <button class="btn" onclick="loadBusquedaInteligente()">Buscar</button>
                    <div id="busqueda-results" style="margin-top: 20px;"></div>
                </div>
                <div>
                    <h3 style="margin-bottom: 15px;">Análisis de Usuario</h3>
                    <input type="text" id="usuario-analisis" placeholder="ID del usuario">
                    <button class="btn" onclick="loadAnalisisUsuario()">Analizar Perfil</button>
                    <div id="analisis-usuario" style="margin-top: 20px;"></div>
                </div>
            </div>
        </div>
        
        <!-- TAB 4: ANÁLISIS AVANZADO -->
        <div id="analisis" class="tab-content">
            <h2 style="margin-bottom: 20px; color: #7c3aed;">🔍 Análisis Avanzado</h2>
            
            <button class="btn" onclick="loadTendencias()" style="margin-bottom: 20px;">Analizar Tendencias</button>
            <button class="btn" onclick="loadInsights()" style="margin-bottom: 20px;">Generar Insights</button>
            
            <div id="tendencias" style="margin-bottom: 40px;"></div>
            <div id="insights"></div>
        </div>
        
        <!-- TAB 5: PREDICCIONES -->
        <div id="predicciones" class="tab-content">
            <h2 style="margin-bottom: 20px; color: #7c3aed;">🔮 Predicciones con ML</h2>
            
            <input type="number" id="nft-prediccion" placeholder="ID del NFT (ej: 1)">
            <button class="btn" onclick="loadPrediccion()" style="margin-bottom: 20px;">Predecir Precio</button>
            
            <div id="prediccion-result"></div>
            
            <h3 style="margin: 40px 0 20px; color: #7c3aed;">NFTs Similares</h3>
            <input type="number" id="nft-similares" placeholder="ID del NFT">
            <button class="btn" onclick="loadSimilares()" style="margin-bottom: 20px;">Encontrar Similares</button>
            
            <div id="similares-result"></div>
        </div>
    </div>
    
    <footer>
        Los profetas © 2024 - Dashboard de Análisis Avanzado con ML e IA
    </footer>
    
    <script>
        const API_URL = 'http://localhost:5001';
        
        function switchTab(tab) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById(tab).classList.add('active');
            event.target.classList.add('active');
        }
        
        function showLoading(elementId) {
            document.getElementById(elementId).innerHTML = '<div class="loading"><div class="spinner"></div> Cargando...</div>';
        }
        
        function showError(elementId, message) {
            document.getElementById(elementId).innerHTML = `<div class="error">❌ ${message}</div>`;
        }
        
        // Estadísticas
        async function loadEstadisticas() {
            try {
                const response = await axios.get(`${API_URL}/api/estadisticas/mercado`);
                const data = response.data;
                
                document.getElementById('total-nfts').textContent = data.total_nfts;
                document.getElementById('total-usuarios').textContent = data.total_usuarios;
                document.getElementById('total-transacciones').textContent = data.total_transacciones;
                document.getElementById('volumen-total').textContent = data.volumen_total + ' ETH';
                
                // Gráficos
                await loadCharts();
            } catch (error) {
                console.error(error);
            }
        }
        
        async function loadCharts() {
            try {
                const response = await axios.get(`${API_URL}/api/dashboard/tendencias`);
                const data = response.data;
                
                // Gráfico de categorías
                const cats = data.categorias_trending || [];
                const ctx1 = document.getElementById('categoriesChart');
                new Chart(ctx1, {
                    type: 'doughnut',
                    data: {
                        labels: cats.map(c => c.nombre),
                        datasets: [{
                            data: cats.map(c => c.count),
                            backgroundColor: ['#7c3aed', '#06b6d4', '#f97316', '#ec4899', '#8b5cf6']
                        }]
                    },
                    options: { responsive: true, maintainAspectRatio: false }
                });
                
                // Gráfico de precios
                const stats = data.estadisticas_por_categoria || {};
                const ctx2 = document.getElementById('pricesChart');
                new Chart(ctx2, {
                    type: 'bar',
                    data: {
                        labels: Object.keys(stats),
                        datasets: [{
                            label: 'Precio Promedio',
                            data: Object.values(stats).map(s => s.precio_promedio),
                            backgroundColor: '#7c3aed'
                        }]
                    },
                    options: { responsive: true, maintainAspectRatio: false }
                });
            } catch (error) {
                console.error(error);
            }
        }
        
        // Recomendaciones
        async function loadRecomendaciones() {
            const usuarioId = document.getElementById('usuario-recomendaciones').value;
            if (!usuarioId) {
                showError('recomendaciones-list', 'Ingresa un ID de usuario');
                return;
            }
            
            showLoading('recomendaciones-list');
            try {
                const response = await axios.get(`${API_URL}/api/dashboard/recomendaciones/${usuarioId}`);
                const recomendaciones = response.data;
                
                let html = '<div class="list">';
                recomendaciones.slice(0, 5).forEach(nft => {
                    html += `<div class="list-item">
                        <div>
                            <div class="list-item-title">${nft.titulo}</div>
                            <small style="color: #606060;">${nft.categoria} • Score: ${nft.score_recomendacion}</small>
                        </div>
                        <div class="list-item-value">${nft.precio} ETH</div>
                    </div>`;
                });
                html += '</div>';
                
                document.getElementById('recomendaciones-list').innerHTML = html;
            } catch (error) {
                showError('recomendaciones-list', 'Error al cargar recomendaciones');
            }
        }
        
        // Anomalías
        async function loadAnomalias() {
            showLoading('anomalias-list');
            try {
                const response = await axios.get(`${API_URL}/api/dashboard/anomalias`);
                const anomalias = response.data;
                
                if (!anomalias.length) {
                    document.getElementById('anomalias-list').innerHTML = '<div class="success">✓ No se detectaron anomalías</div>';
                    return;
                }
                
                let html = '<div class="list">';
                anomalias.forEach(anom => {
                    html += `<div class="list-item">
                        <div>
                            <div class="list-item-title">${anom.titulo}</div>
                            <small style="color: #606060;">Precio: ${anom.precio} ETH (Esperado: ${anom.precio_esperado})</small>
                        </div>
                        <span class="badge ${anom.severidad === 'alta' ? 'down' : 'up'}">${anom.severidad.toUpperCase()}</span>
                    </div>`;
                });
                html += '</div>';
                
                document.getElementById('anomalias-list').innerHTML = html;
            } catch (error) {
                showError('anomalias-list', 'Error al detectar anomalías');
            }
        }
        
        // Búsqueda Inteligente
        async function loadBusquedaInteligente() {
            const query = document.getElementById('busqueda-query').value;
            if (!query) {
                showError('busqueda-results', 'Ingresa un término de búsqueda');
                return;
            }
            
            showLoading('busqueda-results');
            try {
                const response = await axios.post(`${API_URL}/api/dashboard/busqueda`, { query });
                const resultados = response.data;
                
                let html = '<div class="list">';
                resultados.slice(0, 5).forEach(nft => {
                    html += `<div class="list-item">
                        <div>
                            <div class="list-item-title">${nft.titulo}</div>
                            <small style="color: #606060;">Por: ${nft.artista_id} • Score: ${nft.score_busqueda}</small>
                        </div>
                        <div class="list-item-value">${nft.precio} ETH</div>
                    </div>`;
                });
                html += '</div>';
                
                document.getElementById('busqueda-results').innerHTML = html;
            } catch (error) {
                showError('busqueda-results', 'Error en la búsqueda');
            }
        }
        
        // Análisis de Usuario
        async function loadAnalisisUsuario() {
            const usuarioId = document.getElementById('usuario-analisis').value;
            if (!usuarioId) {
                showError('analisis-usuario', 'Ingresa un ID de usuario');
                return;
            }
            
            showLoading('analisis-usuario');
            try {
                const response = await axios.get(`${API_URL}/api/dashboard/analisis-usuario/${usuarioId}`);
                const analisis = response.data;
                
                let html = `
                    <div class="card">
                        <div style="margin-bottom: 15px;">
                            <div class="card-title">${analisis.usuario}</div>
                            <div style="font-size: 18px; color: #7c3aed;">${analisis.tipo_usuario}</div>
                        </div>
                        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px;">
                            <div>
                                <small style="color: #606060;">Engagement Score</small>
                                <div style="font-size: 24px; color: #7c3aed; font-weight: 700;">${analisis.engagement_score}%</div>
                            </div>
                            <div>
                                <small style="color: #606060;">Balance Neto</small>
                                <div style="font-size: 24px; color: #7c3aed; font-weight: 700;">${analisis.balance_neto} ETH</div>
                            </div>
                            <div>
                                <small style="color: #606060;">Obras</small>
                                <div style="font-size: 20px; color: #06b6d4;">${analisis.estadisticas.obras}</div>
                            </div>
                            <div>
                                <small style="color: #606060;">Compras</small>
                                <div style="font-size: 20px; color: #06b6d4;">${analisis.estadisticas.compras}</div>
                            </div>
                        </div>
                    </div>
                `;
                
                document.getElementById('analisis-usuario').innerHTML = html;
            } catch (error) {
                showError('analisis-usuario', 'Error al analizar usuario');
            }
        }
        
        // Tendencias
        async function loadTendencias() {
            showLoading('tendencias');
            try {
                const response = await axios.get(`${API_URL}/api/dashboard/tendencias`);
                const tendencias = response.data;
                
                let html = '<h3 style="color: #7c3aed; margin-bottom: 15px;">Categorías Trending</h3>';
                html += '<div class="list">';
                (tendencias.categorias_trending || []).forEach(cat => {
                    html += `<div class="list-item">
                        <span>${cat.nombre}</span>
                        <span class="list-item-value">${cat.count} NFTs</span>
                    </div>`;
                });
                html += '</div>';
                
                document.getElementById('tendencias').innerHTML = html;
            } catch (error) {
                showError('tendencias', 'Error al cargar tendencias');
            }
        }
        
        // Insights
        async function loadInsights() {
            showLoading('insights');
            try {
                const response = await axios.get(`${API_URL}/api/dashboard/insights`);
                const insights = response.data;
                
                let html = `
                    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px;">
                        <div class="card">
                            <div class="card-title">NFTs Más Populares</div>
                            ${(insights.nfts_trending || []).map(n => `<div style="padding: 8px 0;">❤️ ${n.titulo} (${n.likes} likes)</div>`).join('')}
                        </div>
                        <div class="card">
                            <div class="card-title">NFTs Premium</div>
                            ${(insights.nfts_premium || []).map(n => `<div style="padding: 8px 0;">💎 ${n.titulo} (${n.precio} ETH)</div>`).join('')}
                        </div>
                    </div>
                `;
                
                document.getElementById('insights').innerHTML = html;
            } catch (error) {
                showError('insights', 'Error al generar insights');
            }
        }
        
        // Predicciones
        async function loadPrediccion() {
            const nftId = document.getElementById('nft-prediccion').value;
            if (!nftId) {
                showError('prediccion-result', 'Ingresa un ID de NFT');
                return;
            }
            
            showLoading('prediccion-result');
            try {
                const response = await axios.get(`${API_URL}/api/dashboard/prediccion/${nftId}`);
                const pred = response.data;
                
                const cambio = pred.cambio_esperado;
                const badge = cambio > 0 ? 'up' : 'down';
                
                let html = `
                    <div class="card">
                        <h3>${pred.titulo}</h3>
                        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-top: 15px;">
                            <div>
                                <small style="color: #606060;">Precio Actual</small>
                                <div style="font-size: 20px; color: #7c3aed;">${pred.precio_actual} ETH</div>
                            </div>
                            <div>
                                <small style="color: #606060;">Predicción</small>
                                <div style="font-size: 20px; color: #06b6d4;">${pred.precio_predicho} ETH</div>
                            </div>
                            <div>
                                <small style="color: #606060;">Cambio Esperado</small>
                                <div style="font-size: 20px;"><span class="badge ${badge}">${cambio > 0 ? '↑' : '↓'} ${Math.abs(cambio)} ETH</span></div>
                            </div>
                            <div>
                                <small style="color: #606060;">Confianza</small>
                                <div style="font-size: 20px; color: #7c3aed;">${(pred.confianza * 100).toFixed(0)}%</div>
                            </div>
                        </div>
                        <div style="margin-top: 15px; padding: 12px; background: rgba(124, 58, 237, 0.1); border-radius: 8px;">
                            <strong>Tendencia:</strong> ${pred.tendencia} <br>
                            <strong>Recomendación:</strong> <span class="badge ${pred.recomendacion === 'COMPRAR' ? 'up' : 'down'}">${pred.recomendacion}</span>
                        </div>
                    </div>
                `;
                
                document.getElementById('prediccion-result').innerHTML = html;
            } catch (error) {
                showError('prediccion-result', 'Error al predecir precio');
            }
        }
        
        // Similares
        async function loadSimilares() {
            const nftId = document.getElementById('nft-similares').value;
            if (!nftId) {
                showError('similares-result', 'Ingresa un ID de NFT');
                return;
            }
            
            showLoading('similares-result');
            try {
                const response = await axios.get(`${API_URL}/api/dashboard/similares/${nftId}`);
                const similares = response.data;
                
                let html = '<div class="list">';
                similares.forEach(nft => {
                    html += `<div class="list-item">
                        <div>
                            <div class="list-item-title">${nft.titulo}</div>
                            <small style="color: #606060;">${nft.categoria} • Similitud: ${nft.score_similitud}</small>
                        </div>
                        <div class="list-item-value">${nft.precio} ETH</div>
                    </div>`;
                });
                html += '</div>';
                
                document.getElementById('similares-result').innerHTML = html;
            } catch (error) {
                showError('similares-result', 'Error al buscar similares');
            }
        }
        
        // Cargar estadísticas al iniciar
        window.onload = () => {
            loadEstadisticas();
        };
    </script>
</body>
</html>
"""

# ==================== RUTAS DASHBOARD ====================

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/dashboard/tendencias')
def api_tendencias():
    return jsonify(db.analizar_tendencias_mercado())

@app.route('/api/dashboard/anomalias')
def api_anomalias():
    return jsonify(db.detectar_anomalias())

@app.route('/api/dashboard/insights')
def api_insights():
    return jsonify(db.generar_insights())

@app.route('/api/dashboard/recomendaciones/<usuario_id>')
def api_recomendaciones(usuario_id):
    return jsonify(db.obtener_recomendaciones(usuario_id))

@app.route('/api/dashboard/analisis-usuario/<usuario_id>')
def api_analisis_usuario(usuario_id):
    return jsonify(db.analisis_usuario_detallado(usuario_id))

@app.route('/api/dashboard/prediccion/<int:nft_id>')
def api_prediccion(nft_id):
    return jsonify(db.predecir_precio_nft(nft_id))

@app.route('/api/dashboard/similares/<int:nft_id>')
def api_similares(nft_id):
    return jsonify(db.obtener_similares(nft_id))

@app.route('/api/dashboard/busqueda', methods=['POST'])
def api_busqueda():
    query = request.json.get('query', '')
    return jsonify(db.busqueda_inteligente(query))

# ==================== EJECUTAR ====================

if __name__ == '__main__':
    print("\n🎨 Dashboard Visual disponible en: http://localhost:5001\n")
    print("Características:")
    print("✓ Estadísticas en tiempo real")
    print("✓ Gráficos interactivos")
    print("✓ Machine Learning (recomendaciones, predicciones)")
    print("✓ Inteligencia Artificial (búsqueda, análisis)")
    print("✓ Detección de anomalías")
    print("✓ Tendencias de mercado\n")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
