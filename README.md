# Los profetas — Interfaz NFT

Mercado de NFTs estático con autenticación, publicación de obras, comentarios, ofertas, favoritos, perfil editable, configuración y persistencia local. Diseño basado en la versión original (paleta violeta/cyan, Inter, gradientes vibrantes en cards) con pulido de detalles.

## Cómo correrlo

Abrir `index.html` en un navegador moderno. No requiere servidor — toda la persistencia se hace con `localStorage`.

## Funcionalidades

**Diseño** (basado en el original):
- Paleta violeta `#7c3aed` + cyan `#06b6d4` con gradientes vibrantes en las cards.
- Tipografía Inter + JetBrains Mono para precios y datos técnicos.
- Tema oscuro (default) y claro, con toggle en el topbar y selector en Configuración.
- Animaciones suaves de entrada (hero staggered, cards lift on hover).

**Cuentas:**
- Login y registro con tabs en un único modal.
- Términos y Condiciones obligatorios, con modal completo de lectura.
- "Continuar con Wallet" (simulado) crea cuenta automática.

**Perfil:**
- Avatar editable (sube imagen, persiste como base64).
- Nombre, bio, email editables.
- Stats: obras, favoritos, notificaciones.

**NFTs:**
- Crear con título, descripción, categoría, precio, tags, % regalías y T&C.
- Imagen subida (drag & drop) o gradiente generado.
- Vista de detalle con 3 pestañas: Detalles, Historial de transacciones, Comentarios.
- Botones: Comprar, Intercambiar, Hacer oferta, Contactar artista, Favorito, Compartir, Editar (si es tuyo).
- Mis NFTs: editar / eliminar / ver.

**Filtros y búsqueda:**
- Por título, artista o tags.
- Categoría (Arte, Música, Coleccionables, Fotografía).
- Ordenar (recientes, precio ↑/↓, populares).
- Tags rápidos: Todo, ★ Favoritos, < 1 ETH, 🔥 Tendencia, ✨ Nuevos.

**Configuración:**
- Tema (oscuro/claro/auto).
- Idioma (es/en/pt).
- Moneda (ETH/USD/MXN/EUR) — recalcula precios en vivo.
- Switches: notificaciones por email, mostrar IVA estimado.
- Exportar mis datos en JSON.
- Cerrar sesión / Eliminar cuenta.

**Otros:**
- Notificaciones con badge de no leídas y dropdown.
- Ofertas registradas en el historial.
- Confirmaciones modales para acciones destructivas.

## Estructura

```
.
├── index.html   # Markup + modales
├── style.css    # Estilos (paleta original)
├── app.js       # Lógica completa
└── README.md
```

## Ideas para seguir

- Backend real con Supabase / Firebase para feed compartido.
- Web3 real con `ethers.js` + contrato ERC-721 en testnet (Sepolia).
- Subastas con timer.
- Páginas de artista con feed de actividad.
- Sistema de seguidores.
- Verificación de artistas (badge ✓).
- Gráfico de precio histórico (Chart.js).
- Galería 3D con three.js.
- PWA (manifest + service worker).
- i18n real con archivos `i18n/{es,en}.json`.
- Tests con Vitest o Playwright.
- Royalties on-chain con splits a colaboradores.

---

© 2026 · Los profetas
