"""
Los profetas — Integración Frontend
Ejemplos de cómo conectar la aplicación JavaScript con la API Python
"""

# ==================== NOTAS DE INTEGRACIÓN ====================

# 1. CONFIGURACIÓN BASE EN app.js
# Cambiar el almacenamiento local por llamadas a la API:

JAVASCRIPT_CONFIG = """
// En app.js, al inicio:

const API_BASE_URL = 'http://localhost:5000/api';
const CURRENT_USER_ID = 'sys-user-demo'; // Del localStorage o del servidor

// Reemplazar Store.get() y Store.set() con llamadas API:
const ApiStore = {
  async get(endpoint) {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`);
      if (!response.ok) throw new Error(response.status);
      return await response.json();
    } catch (e) {
      console.error('Error fetching:', e);
      return null;
    }
  },
  
  async set(endpoint, data, method = 'POST') {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      if (!response.ok) throw new Error(response.status);
      return await response.json();
    } catch (e) {
      console.error('Error posting:', e);
      return null;
    }
  }
};
"""

# ==================== CASOS DE USO ====================

CARGAR_NFTS = """
// 1. CARGAR TODOS LOS NFTs
async function cargarNFTs() {
  const nfts = await ApiStore.get('/nfts?categoria=all&sort=fecha_creacion DESC&limite=50');
  state.nfts = nfts;
  renderNFTs();
}

// 2. CARGAR NFT ESPECÍFICO
async function cargarNFT(nftId) {
  const nft = await ApiStore.get(`/nfts/${nftId}`);
  mostrarDetalleNFT(nft);
}

// 3. BUSCAR Y FILTRAR
async function buscarNFTs(filtro) {
  const categoria = filtro.categoria || 'all';
  const q = filtro.busqueda ? `&q=${filtro.busqueda}` : '';
  const sort = filtro.sort || 'fecha_creacion DESC';
  
  const nfts = await ApiStore.get(
    `/nfts?categoria=${categoria}&sort=${sort}${q}&limite=50`
  );
  renderNFTs(nfts);
}
"""

CREAR_NFT = """
// CREAR NFT
async function crearNFT(datos) {
  const nftData = {
    titulo: datos.titulo,
    artista_id: CURRENT_USER_ID,
    precio: parseFloat(datos.precio),
    categoria: datos.categoria,
    descripcion: datos.descripcion,
    tags: datos.tags.split(',').map(t => t.trim()),
    color_inicio: datos.colorInicio,
    color_fin: datos.colorFin,
    imagen_b64: datos.imagenBase64,
    regalias: parseFloat(datos.regalias || 5)
  };
  
  const resultado = await ApiStore.set('/nfts', nftData);
  if (resultado.id) {
    showToast('NFT creado exitosamente');
    return resultado.id;
  } else {
    showToast('Error al crear NFT');
    return null;
  }
}

// Usar desde el formulario:
$('#uploadForm').onsubmit = async (e) => {
  e.preventDefault();
  const id = await crearNFT({
    titulo: $('#titulo').value,
    descripcion: $('#descripcion').value,
    categoria: $('#categoria').value,
    precio: $('#precio').value,
    tags: $('#tags').value,
    colorInicio: $('#colorStart').value,
    colorFin: $('#colorEnd').value,
    imagenBase64: state.uploadImage,
    regalias: $('#regalias').value
  });
  if (id) closeModal('uploadModal');
};
"""

COMENTARIOS = """
// COMENTARIOS
async function obtenerComentarios(nftId) {
  const comentarios = await ApiStore.get(`/nfts/${nftId}/comentarios`);
  mostrarComentarios(comentarios);
}

async function agregarComentario(nftId, contenido) {
  const resultado = await ApiStore.set(
    `/nfts/${nftId}/comentarios`,
    {
      usuario_id: CURRENT_USER_ID,
      contenido: contenido
    }
  );
  
  if (resultado.id) {
    showToast('Comentario agregado');
    // Recargar comentarios
    obtenerComentarios(nftId);
  }
}
"""

FAVORITOS = """
// FAVORITOS
async function toggleFavorito(nftId) {
  const es_fav = await ApiStore.get(
    `/usuarios/${CURRENT_USER_ID}/es-favorito/${nftId}`
  );
  
  if (es_fav.es_favorito) {
    // Remover
    await ApiStore.set(
      `/usuarios/${CURRENT_USER_ID}/favoritos/${nftId}`,
      {},
      'DELETE'
    );
    showToast('Removido de favoritos');
  } else {
    // Agregar
    await ApiStore.set(
      `/usuarios/${CURRENT_USER_ID}/favoritos/${nftId}`,
      {}
    );
    showToast('Agregado a favoritos');
  }
  
  // Actualizar UI
  actualizarBotonesFavorito(nftId);
}

async function cargarFavoritos() {
  const favoritos = await ApiStore.get(
    `/usuarios/${CURRENT_USER_ID}/favoritos`
  );
  state.favorites = favoritos.map(f => f.id);
  renderNFTs(favoritos);
}
"""

TRANSACCIONES = """
// COMPRAR NFT / HACER OFERTA
async function comprarNFT(nftId, precioETH) {
  if (!confirm(`¿Confirmar compra por ${precioETH} ETH?`)) return;
  
  const tx = await ApiStore.set('/transacciones', {
    nft_id: nftId,
    vendedor_id: getNFT(nftId).artista_id,
    comprador_id: CURRENT_USER_ID,
    cantidad: precioETH,
    tipo: 'compra'
  });
  
  if (tx.id) {
    showToast('¡Compra registrada! Transacción ID: ' + tx.id);
    // Actualizar balance
    actualizarBalance();
  }
}

async function hacerOferta(nftId, montoETH, mensaje) {
  const oferta = await ApiStore.set(
    `/nfts/${nftId}/ofertas`,
    {
      usuario_id: CURRENT_USER_ID,
      monto: montoETH,
      mensaje: mensaje
    }
  );
  
  if (oferta.id) {
    showToast('Oferta enviada');
    closeModal('ofertaModal');
  }
}

// Ver historial de transacciones
async function verHistorial(nftId) {
  const historial = await ApiStore.get(`/nfts/${nftId}/historial`);
  mostrarHistorial(historial);
}
"""

NOTIFICACIONES = """
// NOTIFICACIONES
async function cargarNotificaciones() {
  const notifs = await ApiStore.get(`/usuarios/${CURRENT_USER_ID}/notificaciones`);
  state.notifications = notifs;
  actualizarBadgeNotificaciones();
}

async function cargarNoLeidas() {
  const data = await ApiStore.get(
    `/usuarios/${CURRENT_USER_ID}/notificaciones/no-leidas`
  );
  mostrarBadge(data.no_leidas);
}

async function marcarComoLeida(notifId) {
  await ApiStore.set(
    `/notificaciones/${notifId}/leer`,
    {},
    'PUT'
  );
  cargarNotificaciones();
}

async function marcarTodas() {
  await ApiStore.set(
    `/usuarios/${CURRENT_USER_ID}/notificaciones/marcar-todas`,
    {},
    'PUT'
  );
  showToast('Todas marcadas como leídas');
  cargarNotificaciones();
}
"""

CONFIGURACION = """
// CONFIGURACIÓN DE USUARIO
async function obtenerConfiguracion() {
  const config = await ApiStore.get(
    `/usuarios/${CURRENT_USER_ID}/configuracion`
  );
  state.settings = config;
  aplicarConfiguracion(config);
}

async function guardarConfiguracion(nuevosTemas) {
  await ApiStore.set(
    `/usuarios/${CURRENT_USER_ID}/configuracion`,
    nuevosTemas,
    'PUT'
  );
  showToast('Configuración guardada');
  obtenerConfiguracion();
}

// En el formulario de configuración:
$('#settingsForm').onsubmit = async (e) => {
  e.preventDefault();
  
  await guardarConfiguracion({
    tema: $('#tema').value,
    idioma: $('#idioma').value,
    moneda: $('#moneda').value,
    notificaciones: $('#notif').checked ? 1 : 0,
    mostrar_iva: $('#iva').checked ? 1 : 0
  });
};
"""

PERFIL = """
// PERFIL DE USUARIO
async function cargarPerfil(usuarioId) {
  const usuario = await ApiStore.get(`/usuarios/${usuarioId}`);
  const stats = await ApiStore.get(`/estadisticas/usuarios/${usuarioId}`);
  
  mostrarPerfil(usuario, stats);
}

async function actualizarPerfil(datos) {
  const resultado = await ApiStore.set(
    `/usuarios/${CURRENT_USER_ID}`,
    datos,
    'PUT'
  );
  
  if (resultado) {
    showToast('Perfil actualizado');
    cargarPerfil(CURRENT_USER_ID);
  }
}

// Actualizar avatar
async function cambiarAvatar(imagenBase64) {
  await actualizarPerfil({
    avatar_b64: imagenBase64
  });
}
"""

FLUJO_INICIO = """
// ==================== FLUJO AL INICIAR LA APP ====================

async function inicializarApp() {
  console.log('🚀 Inicializando Los profetas...');
  
  // 1. Cargar usuario actual
  const usuario = await ApiStore.get(`/usuarios/${CURRENT_USER_ID}`);
  if (!usuario) {
    console.error('Usuario no encontrado');
    mostrarLogin();
    return;
  }
  state.user = usuario;
  
  // 2. Cargar configuración
  await obtenerConfiguracion();
  
  // 3. Cargar NFTs principales
  await cargarNFTs();
  
  // 4. Cargar notificaciones
  await cargarNotificaciones();
  
  // 5. Cargar favoritos
  await cargarFavoritos();
  
  // 6. Renderizar UI
  renderUI();
  
  // 7. Actualizar stats
  const stats = await ApiStore.get(`/estadisticas/mercado`);
  mostrarEstadisticas(stats);
  
  console.log('✅ App inicializada');
}

// Llamar al cargar:
window.addEventListener('DOMContentLoaded', inicializarApp);
"""

# ==================== MANEJO DE ERRORES ====================

ERROR_HANDLING = """
// Envolver todas las llamadas API con manejo de errores:

async function llamarAPI(endpoint, opciones = {}) {
  try {
    const method = opciones.method || 'GET';
    const headers = {
      'Content-Type': 'application/json',
      ...opciones.headers
    };
    
    const config = {
      method,
      headers,
      ...opciones
    };
    
    if (opciones.body) {
      config.body = JSON.stringify(opciones.body);
    }
    
    const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
    
    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('API Call Failed:', error);
    showToast(`Error: ${error.message}`);
    return null;
  }
}
"""

print(__doc__)
print("\n" + "="*60)
print("EJEMPLOS DE INTEGRACIÓN")
print("="*60)

print("\n📌 1. CONFIGURACIÓN BASE")
print(JAVASCRIPT_CONFIG)

print("\n📌 2. CARGAR NFTs")
print(CARGAR_NFTS)

print("\n📌 3. CREAR NFT")
print(CREAR_NFT)

print("\n📌 4. COMENTARIOS")
print(COMENTARIOS)

print("\n📌 5. FAVORITOS")
print(FAVORITOS)

print("\n📌 6. TRANSACCIONES Y COMPRAS")
print(TRANSACCIONES)

print("\n📌 7. NOTIFICACIONES")
print(NOTIFICACIONES)

print("\n📌 8. CONFIGURACIÓN")
print(CONFIGURACION)

print("\n📌 9. PERFIL")
print(PERFIL)

print("\n📌 10. FLUJO DE INICIALIZACIÓN")
print(FLUJO_INICIO)

print("\n📌 11. MANEJO DE ERRORES")
print(ERROR_HANDLING)

print("\n" + "="*60)
print("✅ FIN DE EJEMPLOS")
print("="*60)
print("""
Para más detalles, consulta:
- DATABASE.md: Documentación completa
- base.py: Métodos disponibles
- api.py: Endpoints REST
""")
