/* =========================================================
   Los profetas — app.js
   Mercado NFT (demo) con persistencia local
   ========================================================= */

(() => {
  'use strict';

  /* ======================== Storage ======================== */
  const KEY = (k) => `losprofetas:${k}`;
  const Store = {
    get(k, def = null){
      try{ const v = localStorage.getItem(KEY(k)); return v == null ? def : JSON.parse(v); }
      catch(e){ return def; }
    },
    set(k, v){ try{ localStorage.setItem(KEY(k), JSON.stringify(v)); }catch(e){} },
    del(k){ try{ localStorage.removeItem(KEY(k)); }catch(e){} },
    clearAll(){ Object.keys(localStorage).filter(k => k.startsWith('losprofetas:')).forEach(k => localStorage.removeItem(k)); }
  };

  /* ======================== Estado ======================== */
  const state = {
    user: Store.get('user', null),
    session: Store.get('session', false),
    nfts: Store.get('nfts', null),
    comments: Store.get('comments', {}),
    favorites: Store.get('favorites', []),
    notifications: Store.get('notifications', []),
    transactions: Store.get('transactions', {}),
    settings: Store.get('settings', { theme: 'dark', currency: 'ETH', lang: 'es', notif: true, iva: false }),
    walletConnected: Store.get('wallet', false),
    filters: { category: 'all', q: '', sort: 'recent', tag: 'all' },
    uploadImage: null
  };

  /* ======================== Datos seed ======================== */
  const SEED = [
    {id:1,title:'Profecía Lunar',artist:'A. Rivera',artistId:'sys-arivera',price:0.85,category:'art',colorStart:'#ff9a9e',colorEnd:'#fecfef',description:'Visión nocturna sobre el ocaso del segundo siglo digital. Generativa, edición de 1.',tags:['lunar','generativo','místico'],createdAt:Date.now()-86400000*12,likes:42,royalty:5},
    {id:2,title:'Ecos del Mañana',artist:'L. Santos',artistId:'sys-lsantos',price:1.2,category:'music',colorStart:'#a18cd1',colorEnd:'#fbc2eb',description:'Composición algorítmica inspirada en frecuencias solares. Loop infinito.',tags:['ambient','solar','loop'],createdAt:Date.now()-86400000*8,likes:78,royalty:7.5},
    {id:3,title:'Guardiana 07',artist:'M. Ortega',artistId:'sys-mortega',price:0.45,category:'collectible',colorStart:'#89f7fe',colorEnd:'#66a6ff',description:'Séptima de una serie de 12 guardianas. Acceso a comunidad privada.',tags:['serie','guardianes','utility'],createdAt:Date.now()-86400000*30,likes:23,royalty:5},
    {id:4,title:'Vidente Urbano',artist:'K. Díaz',artistId:'sys-kdiaz',price:2.1,category:'art',colorStart:'#f6d365',colorEnd:'#fda085',description:'Retrato fotográfico digital con técnicas de glitch art.',tags:['retrato','urbano','glitch'],createdAt:Date.now()-86400000*3,likes:156,royalty:8},
    {id:5,title:'Ritmo Ancestral',artist:'N. Pérez',artistId:'sys-nperez',price:0.33,category:'music',colorStart:'#f093fb',colorEnd:'#f5576c',description:'Sample de tambores prehispánicos cruzados con synths analógicos.',tags:['ancestral','beats','fusión'],createdAt:Date.now()-86400000*45,likes:94,royalty:5},
    {id:6,title:'Sello Profético',artist:'Colectivo',artistId:'sys-colectivo',price:0.12,category:'collectible',colorStart:'#5ee7df',colorEnd:'#b490ca',description:'Acceso simbólico al Colectivo. Tira limitada de 1000.',tags:['acceso','sigilo','colectivo'],createdAt:Date.now()-86400000*60,likes:312,royalty:2.5}
  ];
  if(!state.nfts){ state.nfts = SEED; Store.set('nfts', state.nfts); }

  /* ======================== Helpers ======================== */
  const $ = (s, r=document) => r.querySelector(s);
  const $$ = (s, r=document) => Array.from(r.querySelectorAll(s));
  const uid = () => 'id-' + Math.random().toString(36).slice(2,10) + Date.now().toString(36);
  const escapeHtml = (s) => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const fmtTime = (ts) => {
    const diff = (Date.now() - ts) / 1000;
    if(diff < 60) return 'hace un momento';
    if(diff < 3600) return `hace ${Math.floor(diff/60)} min`;
    if(diff < 86400) return `hace ${Math.floor(diff/3600)} h`;
    if(diff < 86400*7) return `hace ${Math.floor(diff/86400)} d`;
    return new Date(ts).toLocaleDateString('es-MX', { day: 'numeric', month: 'short', year: 'numeric' });
  };

  const RATES = { ETH: 1, USD: 3000, MXN: 51000, EUR: 2750 };
  const fmtPrice = (eth) => {
    const cur = state.settings.currency;
    if(cur === 'ETH') return `${eth.toFixed(eth < 1 ? 3 : 2)} ETH`;
    const v = eth * RATES[cur];
    const sym = { USD: '$', MXN: '$', EUR: '€' }[cur];
    return `${sym}${v.toLocaleString('es-MX', { maximumFractionDigits: 0 })} ${cur}`;
  };
  const fmtPriceAlt = (eth) => {
    const cur = state.settings.currency;
    if(cur === 'ETH') return `≈ $${(eth * RATES.USD).toLocaleString('es-MX', { maximumFractionDigits: 0 })} USD`;
    return `${eth.toFixed(3)} ETH`;
  };

  /* ======================== Toast ======================== */
  let toastT;
  const toast = $('#toast');
  function showToast(msg, ms=2200){
    toast.textContent = msg;
    toast.classList.remove('hidden');
    clearTimeout(toastT);
    toastT = setTimeout(() => toast.classList.add('hidden'), ms);
  }

  /* ======================== Confirm ======================== */
  function confirmDialog(title, message){
    return new Promise(resolve => {
      $('#confirmTitle').textContent = title;
      $('#confirmMsg').textContent = message;
      const m = $('#confirmModal');
      m.classList.remove('hidden');
      const ok = $('#confirmOk'), cancel = $('#confirmCancel');
      const close = (val) => { m.classList.add('hidden'); ok.onclick = cancel.onclick = null; resolve(val); };
      ok.onclick = () => close(true);
      cancel.onclick = () => close(false);
    });
  }

  /* ======================== Modales ======================== */
  function openModal(id){ $('#'+id).classList.remove('hidden'); document.body.style.overflow = 'hidden'; }
  function closeModal(id){ $('#'+id).classList.add('hidden'); document.body.style.overflow = ''; }

  document.addEventListener('click', (e) => {
    if(e.target.classList.contains('modal')) closeModal(e.target.id);
    const closeBtn = e.target.closest('[data-close]');
    if(closeBtn) closeModal(closeBtn.dataset.close);
  });
  document.addEventListener('keydown', (e) => {
    if(e.key === 'Escape') $$('.modal:not(.hidden)').forEach(m => closeModal(m.id));
  });

  /* ======================== Tema ======================== */
  function applyTheme(theme){
    let t = theme;
    if(theme === 'auto') t = matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', t);
    $$('.seg-btn[data-theme-set]').forEach(b => b.classList.toggle('active', b.dataset.themeSet === theme));
  }
  applyTheme(state.settings.theme);

  $('#themeToggle').addEventListener('click', () => {
    const next = (document.documentElement.getAttribute('data-theme') === 'dark') ? 'light' : 'dark';
    state.settings.theme = next;
    Store.set('settings', state.settings);
    applyTheme(next);
    showToast(`Tema: ${next === 'dark' ? 'oscuro' : 'claro'}`);
  });

  /* ======================== Wallet ======================== */
  const connectBtn = $('#connectBtn');
  function refreshWalletBtn(){
    if(state.walletConnected){
      connectBtn.textContent = 'Wallet: 0xAB…12';
    } else {
      connectBtn.textContent = 'Conectar Wallet';
    }
  }
  connectBtn.addEventListener('click', () => {
    state.walletConnected = !state.walletConnected;
    Store.set('wallet', state.walletConnected);
    showToast(state.walletConnected ? 'Wallet conectada (simulada)' : 'Wallet desconectada');
    refreshWalletBtn();
  });

  /* ======================== Auth UI ======================== */
  function defaultAvatar(name='?'){
    const initials = name.split(' ').map(s => s[0]).slice(0,2).join('').toUpperCase();
    const hue = Math.abs([...name].reduce((a,c) => a + c.charCodeAt(0), 0)) % 360;
    const svg = `<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 80 80'><defs><linearGradient id='g' x1='0' x2='1' y1='0' y2='1'><stop offset='0' stop-color='hsl(${hue},70%,55%)'/><stop offset='1' stop-color='hsl(${(hue+50)%360},70%,45%)'/></linearGradient></defs><rect width='80' height='80' fill='url(%23g)'/><text x='50%' y='54%' text-anchor='middle' dominant-baseline='middle' font-family='Inter,sans-serif' font-size='32' font-weight='700' fill='white'>${initials}</text></svg>`;
    return 'data:image/svg+xml;utf8,' + encodeURIComponent(svg).replace(/'/g, '%27');
  }

  function refreshAuthUI(){
    const profileBtn = $('#profileBtn');
    if(state.session && state.user){
      profileBtn.hidden = false;
      $('#topAvatar').src = state.user.avatar || defaultAvatar(state.user.name);
    } else {
      profileBtn.hidden = true;
    }
  }

  $$('#authModal .tab').forEach(t => {
    t.addEventListener('click', () => {
      $$('#authModal .tab').forEach(b => b.classList.toggle('active', b === t));
      $$('[data-tabpane]').forEach(p => p.classList.toggle('hidden', p.dataset.tabpane !== t.dataset.tab));
    });
  });

  $('#loginForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    const email = fd.get('email');
    let user = Store.get('users', {})[email];
    if(!user){
      user = { id: uid(), email, name: email.split('@')[0], avatar: null, bio: '', createdAt: Date.now() };
      const users = Store.get('users', {}); users[email] = user; Store.set('users', users);
    }
    state.user = user; state.session = true;
    Store.set('user', user); Store.set('session', true);
    closeModal('authModal');
    refreshAuthUI();
    showToast(`Bienvenido, ${user.name}`);
    e.target.reset();
  });

  $('#registerForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    if(!fd.get('tos')){ showToast('Debes aceptar los términos'); return; }
    const user = {
      id: uid(),
      email: fd.get('email'),
      name: fd.get('name'),
      avatar: null, bio: '',
      newsletter: !!fd.get('newsletter'),
      createdAt: Date.now()
    };
    const users = Store.get('users', {}); users[user.email] = user; Store.set('users', users);
    state.user = user; state.session = true;
    Store.set('user', user); Store.set('session', true);
    closeModal('authModal');
    refreshAuthUI();
    addNotification('¡Bienvenido! Completa tu perfil para empezar.');
    showToast(`Cuenta creada · Bienvenido ${user.name}`);
    e.target.reset();
  });

  function requireAuth(action='realizar esta acción'){
    if(!state.session){
      showToast(`Inicia sesión para ${action}`);
      openModal('authModal');
      return false;
    }
    return true;
  }

  /* ======================== Acciones globales [data-action] ======================== */
  document.addEventListener('click', (e) => {
    const a = e.target.closest('[data-action]');
    if(!a) return;
    e.preventDefault();
    const action = a.dataset.action;
    if(action === 'open-upload'){ if(requireAuth('crear un NFT')) openUpload(); }
    else if(action === 'open-mine'){ if(requireAuth('ver tus NFTs')) renderMine(); }
    else if(action === 'open-favs'){ state.filters.tag = 'favorites'; $$('.tag').forEach(b => b.classList.toggle('active', b.dataset.tag === 'favorites')); render(); window.scrollTo({ top: $('#gallery').offsetTop - 100, behavior: 'smooth' }); }
    else if(action === 'open-tos'){ openModal('tosModal'); }
    else if(action === 'connect-wallet-auth'){
      state.walletConnected = true; Store.set('wallet', true);
      const wAddr = '0x' + Math.random().toString(16).slice(2,10).toUpperCase();
      const user = { id: uid(), email: `${wAddr}@wallet`, name: `Wallet ${wAddr.slice(0,6)}`, avatar: null, bio: '', createdAt: Date.now() };
      const users = Store.get('users', {}); users[user.email] = user; Store.set('users', users);
      state.user = user; state.session = true;
      Store.set('user', user); Store.set('session', true);
      closeModal('authModal');
      refreshAuthUI(); refreshWalletBtn();
      showToast('Conectado con wallet');
    }
  });

  /* ======================== Profile ======================== */
  $('#profileBtn').addEventListener('click', renderProfile);

  function renderProfile(){
    if(!state.user) return;
    const u = state.user;
    const myNfts = state.nfts.filter(n => n.artistId === u.id);
    $('#profileContent').innerHTML = `
      <div class="profile-banner">
        <div class="profile-avatar-wrap">
          <img id="profileAvatarImg" src="${u.avatar || defaultAvatar(u.name)}" alt="">
          <label title="Cambiar foto">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M9 2L7.17 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2h-3.17L15 2H9zm3 15c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z"/></svg>
            <input type="file" accept="image/*" hidden id="avatarInput">
          </label>
        </div>
      </div>
      <div class="profile-meta">
        <div>
          <h2 class="profile-name">${escapeHtml(u.name)}</h2>
          <div class="profile-handle">@${escapeHtml((u.email||'').split('@')[0])} · ${u.id.slice(-6).toUpperCase()}</div>
          <p class="profile-bio">${escapeHtml(u.bio || 'Aún no has añadido una biografía. Edita tu perfil para presentarte.')}</p>
          <div class="profile-stats">
            <div class="ps"><strong>${myNfts.length}</strong>Obras</div>
            <div class="ps"><strong>${state.favorites.length}</strong>Favoritos</div>
            <div class="ps"><strong>${state.notifications.length}</strong>Notificaciones</div>
          </div>
        </div>
        <button class="btn ghost" id="editProfileBtn">Editar perfil</button>
      </div>

      <form class="profile-edit-form hidden" id="profileEditForm">
        <label class="field"><span>Nombre</span><input type="text" name="name" value="${escapeHtml(u.name)}" required></label>
        <label class="field"><span>Bio</span><textarea name="bio" rows="3" maxlength="200" placeholder="Cuéntanos quién eres…">${escapeHtml(u.bio || '')}</textarea></label>
        <label class="field"><span>Email</span><input type="email" name="email" value="${escapeHtml(u.email||'')}" required></label>
        <div class="form-row right">
          <button type="button" class="btn ghost" id="cancelEditProfile">Cancelar</button>
          <button type="submit" class="btn primary">Guardar</button>
        </div>
      </form>
    `;
    openModal('profileModal');

    $('#avatarInput').addEventListener('change', (e) => {
      const file = e.target.files[0]; if(!file) return;
      if(file.size > 2*1024*1024){ showToast('Imagen muy grande (máx 2 MB)'); return; }
      const reader = new FileReader();
      reader.onload = () => {
        state.user.avatar = reader.result;
        const users = Store.get('users', {}); users[state.user.email] = state.user; Store.set('users', users);
        Store.set('user', state.user);
        $('#profileAvatarImg').src = reader.result;
        $('#topAvatar').src = reader.result;
        showToast('Foto actualizada');
      };
      reader.readAsDataURL(file);
    });

    $('#editProfileBtn').addEventListener('click', () => {
      $('#profileEditForm').classList.remove('hidden');
      $('#editProfileBtn').classList.add('hidden');
    });
    $('#cancelEditProfile').addEventListener('click', () => {
      $('#profileEditForm').classList.add('hidden');
      $('#editProfileBtn').classList.remove('hidden');
    });
    $('#profileEditForm').addEventListener('submit', (e) => {
      e.preventDefault();
      const fd = new FormData(e.target);
      Object.assign(state.user, { name: fd.get('name'), bio: fd.get('bio'), email: fd.get('email') });
      const users = Store.get('users', {}); users[state.user.email] = state.user; Store.set('users', users);
      Store.set('user', state.user);
      showToast('Perfil actualizado');
      renderProfile();
    });
  }

  /* ======================== Subir NFT ======================== */
  function openUpload(){
    $('#uploadForm').reset();
    $('#uploadPreview').hidden = true;
    $('#uploadPreview').src = '';
    $('#dropzoneInner').style.display = '';
    state.uploadImage = null;
    openModal('uploadModal');
  }

  const dropzone = document.querySelector('.dropzone');
  const uploadFile = $('#uploadFile');
  const uploadPreview = $('#uploadPreview');
  const dropzoneInner = $('#dropzoneInner');

  function handleFile(file){
    if(!file) return;
    if(!file.type.startsWith('image/')){ showToast('Solo imágenes'); return; }
    if(file.size > 4*1024*1024){ showToast('Imagen muy grande (máx 4 MB)'); return; }
    const reader = new FileReader();
    reader.onload = () => {
      state.uploadImage = reader.result;
      uploadPreview.src = reader.result;
      uploadPreview.hidden = false;
      dropzoneInner.style.display = 'none';
    };
    reader.readAsDataURL(file);
  }
  uploadFile.addEventListener('change', e => handleFile(e.target.files[0]));
  ['dragenter','dragover'].forEach(ev => dropzone.addEventListener(ev, e => { e.preventDefault(); dropzone.classList.add('dragover'); }));
  ['dragleave','drop'].forEach(ev => dropzone.addEventListener(ev, e => { e.preventDefault(); dropzone.classList.remove('dragover'); }));
  dropzone.addEventListener('drop', e => handleFile(e.dataTransfer.files[0]));

  $('#useGradient').addEventListener('click', () => {
    state.uploadImage = null;
    uploadPreview.hidden = true;
    dropzoneInner.style.display = '';
    showToast('Se generará un gradiente único');
  });

  $('#uploadForm').addEventListener('submit', (e) => {
    e.preventDefault();
    if(!requireAuth('publicar')) return;
    const fd = new FormData(e.target);
    if(!fd.get('tos')){ showToast('Debes aceptar los términos'); return; }
    const hue = Math.floor(Math.random() * 360);
    const nft = {
      id: uid(),
      title: fd.get('title'),
      description: fd.get('description') || '',
      artist: state.user.name,
      artistId: state.user.id,
      category: fd.get('category'),
      price: parseFloat(fd.get('price')),
      tags: (fd.get('tags') || '').split(',').map(s => s.trim()).filter(Boolean),
      royalty: parseFloat(fd.get('royalty') || 5),
      image: state.uploadImage,
      colorStart: `hsl(${hue},70%,60%)`,
      colorEnd: `hsl(${(hue+60)%360},70%,55%)`,
      createdAt: Date.now(),
      likes: 0
    };
    state.nfts.unshift(nft);
    Store.set('nfts', state.nfts);
    addNotification(`Publicaste "${nft.title}"`);
    closeModal('uploadModal');
    showToast('NFT publicado');
    state.uploadImage = null;
    render();
  });

  /* ======================== Mis NFTs ======================== */
  function renderMine(){
    const mine = state.nfts.filter(n => n.artistId === state.user.id);
    const list = $('#mineList');
    if(mine.length === 0){
      list.innerHTML = `<div class="empty-state"><div class="empty-icon">∅</div><h3>Aún no tienes obras</h3><p>Crea tu primera obra desde "Crear" en el menú.</p></div>`;
    } else {
      list.innerHTML = mine.map(n => `
        <div class="mine-card">
          <div class="art" style="${artBg(n)}">${n.image ? `<img src="${n.image}" alt="">` : ''}</div>
          <div class="ttl">${escapeHtml(n.title)}</div>
          <div class="pr">${fmtPrice(n.price)}</div>
          <div class="mine-actions">
            <button class="small-btn trade" data-edit="${n.id}">Editar</button>
            <button class="small-btn buy" data-view="${n.id}">Ver</button>
          </div>
        </div>
      `).join('');
      list.querySelectorAll('[data-edit]').forEach(b => b.addEventListener('click', () => openEdit(b.dataset.edit)));
      list.querySelectorAll('[data-view]').forEach(b => b.addEventListener('click', () => { closeModal('mineModal'); openDetail(b.dataset.view); }));
    }
    openModal('mineModal');
  }

  /* ======================== Editar NFT ======================== */
  function openEdit(id){
    const nft = state.nfts.find(n => n.id == id);
    if(!nft) return;
    const f = $('#editForm');
    f.id.value = nft.id;
    f.title.value = nft.title;
    f.description.value = nft.description || '';
    f.category.value = nft.category;
    f.price.value = nft.price;
    openModal('editModal');

    f.onsubmit = (e) => {
      e.preventDefault();
      const fd = new FormData(f);
      Object.assign(nft, {
        title: fd.get('title'),
        description: fd.get('description'),
        category: fd.get('category'),
        price: parseFloat(fd.get('price'))
      });
      Store.set('nfts', state.nfts);
      closeModal('editModal');
      showToast('Cambios guardados');
      render();
      if(!$('#mineModal').classList.contains('hidden')) renderMine();
    };
    $('#deleteNftBtn').onclick = async () => {
      const ok = await confirmDialog('Eliminar NFT', '¿Eliminar esta obra? Esta acción no se puede deshacer.');
      if(!ok) return;
      state.nfts = state.nfts.filter(n => n.id != id);
      Store.set('nfts', state.nfts);
      closeModal('editModal');
      showToast('NFT eliminado');
      render();
      if(!$('#mineModal').classList.contains('hidden')) renderMine();
    };
  }

  /* ======================== Detalle NFT ======================== */
  function artBg(nft){
    return `background: linear-gradient(135deg, ${nft.colorStart}, ${nft.colorEnd})`;
  }

  function openDetail(id){
    const nft = state.nfts.find(n => n.id == id);
    if(!nft) return;
    const isFav = state.favorites.includes(nft.id);
    const isMine = state.user && nft.artistId === state.user.id;
    const comments = state.comments[nft.id] || [];
    const txs = state.transactions[nft.id] || [{ type: 'mint', price: nft.price, by: nft.artist, time: nft.createdAt }];

    $('#modalContent').innerHTML = `
      <div class="nft-detail">
        <div class="detail-art" style="${artBg(nft)}">${nft.image ? `<img src="${nft.image}" alt="${escapeHtml(nft.title)}">` : ''}</div>
        <div class="detail-info">
          <div style="display:inline-block;padding:4px 10px;background:var(--glass);border:1px solid var(--border);border-radius:999px;font-size:11px;text-transform:capitalize;color:var(--text-soft);margin-bottom:8px">${nft.category}</div>
          <h2>${escapeHtml(nft.title)}</h2>
          <div class="by">por <strong>${escapeHtml(nft.artist)}</strong> · ${fmtTime(nft.createdAt)}</div>
          <p class="description">${escapeHtml(nft.description || 'Sin descripción.')}</p>

          ${nft.tags && nft.tags.length ? `<div class="tag-chips">${nft.tags.map(t => `<span class="chip">#${escapeHtml(t)}</span>`).join('')}</div>` : ''}

          <div class="price-block">
            <div>
              <div class="price-lbl">Precio actual</div>
              <div class="price-val">${fmtPrice(nft.price)}</div>
            </div>
            <div class="price-alt">${fmtPriceAlt(nft.price)}</div>
          </div>

          <div class="detail-actions">
            <button class="btn primary" data-buy="${nft.id}">Comprar ahora</button>
            <button class="btn ghost" data-trade="${nft.id}">Intercambiar</button>
            <button class="btn ghost" data-offer="${nft.id}">Hacer oferta</button>
            <button class="btn ghost" data-contact="${nft.id}">Contactar artista</button>
          </div>

          <div class="form-row" style="gap:8px;flex-wrap:wrap">
            <button class="btn ghost" data-fav="${nft.id}">${isFav ? '★ Favorito' : '☆ Favorito'}</button>
            <button class="btn ghost" data-share="${nft.id}">⤴ Compartir</button>
            ${isMine ? `<button class="btn ghost" data-edit-nft="${nft.id}">✎ Editar</button>` : ''}
          </div>
        </div>
      </div>

      <div class="detail-tabs">
        <button class="dt-tab active" data-pane="d-detail">Detalles</button>
        <button class="dt-tab" data-pane="d-history">Historial</button>
        <button class="dt-tab" data-pane="d-comments">Comentarios <span class="muted">(${comments.length})</span></button>
      </div>

      <div class="dt-pane" id="d-detail">
        <div class="detail-grid">
          <div><div class="muted small">Categoría</div><strong style="text-transform:capitalize">${escapeHtml(nft.category)}</strong></div>
          <div><div class="muted small">Likes</div><strong>${(nft.likes||0).toLocaleString()}</strong></div>
          <div><div class="muted small">Regalías al creador</div><strong>${nft.royalty || 5}%</strong></div>
          <div><div class="muted small">Token ID</div><strong style="font-family:'JetBrains Mono',monospace;font-size:13px">#${String(nft.id).slice(-8).toUpperCase()}</strong></div>
        </div>
      </div>

      <div class="dt-pane hidden" id="d-history">
        ${txs.map(t => `
          <div class="history-row">
            <div class="ev-icon">${t.type === 'mint' ? '✦' : t.type === 'sale' ? '◆' : '◇'}</div>
            <div><strong>${t.type === 'mint' ? 'Acuñación' : t.type === 'sale' ? 'Venta' : 'Oferta'}</strong><div class="muted small">por ${escapeHtml(t.by)}</div></div>
            <div class="ev-price">${fmtPrice(t.price)}</div>
            <div class="ev-time">${fmtTime(t.time)}</div>
          </div>
        `).join('')}
      </div>

      <div class="dt-pane hidden" id="d-comments">
        ${state.session ? `
          <form class="comment-form" id="commentForm">
            <img class="cm-avatar" src="${state.user.avatar || defaultAvatar(state.user.name)}" alt="">
            <textarea name="text" placeholder="Escribe un comentario…" required></textarea>
            <button type="submit" class="btn primary">Enviar</button>
          </form>
        ` : `<p class="muted small">Inicia sesión para comentar.</p>`}
        <div class="comment-list">
          ${comments.length === 0 ? '<p class="muted small">Aún no hay comentarios. Sé el primero en comentar.</p>' :
            comments.slice().reverse().map(c => `
              <div class="comment">
                <img class="cm-avatar" src="${c.avatar || defaultAvatar(c.name)}" alt="">
                <div class="comment-body">
                  <div class="comment-head"><strong>${escapeHtml(c.name)}</strong><span class="cm-time">${fmtTime(c.time)}</span></div>
                  <div class="comment-text">${escapeHtml(c.text)}</div>
                </div>
              </div>`).join('')}
        </div>
      </div>
    `;
    openModal('modal');

    // Tabs
    $$('.dt-tab').forEach(t => t.addEventListener('click', () => {
      $$('.dt-tab').forEach(b => b.classList.toggle('active', b === t));
      $$('.dt-pane').forEach(p => p.classList.toggle('hidden', p.id !== t.dataset.pane));
    }));

    $('#modalContent').querySelector('[data-buy]').addEventListener('click', () => buyNft(nft));
    $('#modalContent').querySelector('[data-trade]').addEventListener('click', () => actionTrade(nft));
    $('#modalContent').querySelector('[data-offer]').addEventListener('click', () => actionOffer(nft));
    $('#modalContent').querySelector('[data-contact]').addEventListener('click', () => actionContact(nft));
    $('#modalContent').querySelector('[data-fav]').addEventListener('click', () => { toggleFav(nft.id); openDetail(nft.id); });
    $('#modalContent').querySelector('[data-share]').addEventListener('click', () => shareNft(nft));
    const editBtn = $('#modalContent').querySelector('[data-edit-nft]');
    if(editBtn) editBtn.addEventListener('click', () => { closeModal('modal'); openEdit(nft.id); });

    const cf = $('#commentForm');
    if(cf){
      cf.addEventListener('submit', (e) => {
        e.preventDefault();
        const text = (new FormData(cf).get('text') || '').trim();
        if(!text) return;
        const arr = state.comments[nft.id] || [];
        arr.push({ id: uid(), text, name: state.user.name, avatar: state.user.avatar, time: Date.now() });
        state.comments[nft.id] = arr;
        Store.set('comments', state.comments);
        showToast('Comentario publicado');
        openDetail(nft.id);
      });
    }
  }

  function buyNft(nft){
    if(!requireAuth('comprar')) return;
    if(!state.walletConnected){ showToast('Conecta tu wallet primero'); return; }
    if(state.user && nft.artistId === state.user.id){ showToast('No puedes comprar tu propia obra'); return; }
    const arr = state.transactions[nft.id] || [{ type:'mint', price: nft.price, by: nft.artist, time: nft.createdAt }];
    arr.push({ type:'sale', price: nft.price, by: state.user.name, time: Date.now() });
    state.transactions[nft.id] = arr; Store.set('transactions', state.transactions);
    addNotification(`Compraste "${nft.title}" por ${fmtPrice(nft.price)}`);
    closeModal('modal');
    showToast('Compra simulada completada');
  }
  function actionTrade(nft){
    if(!requireAuth('intercambiar')) return;
    addNotification(`Solicitud de intercambio enviada para "${nft.title}"`);
    closeModal('modal');
    showToast('Solicitud de intercambio enviada');
  }
  function actionOffer(nft){
    if(!requireAuth('ofertar')) return;
    const offer = prompt(`¿Cuánto ofreces por "${nft.title}"? (en ETH)\nPrecio actual: ${fmtPrice(nft.price)}`, (nft.price * 0.85).toFixed(3));
    if(!offer) return;
    const v = parseFloat(offer);
    if(isNaN(v) || v <= 0){ showToast('Cantidad inválida'); return; }
    const arr = state.transactions[nft.id] || [];
    arr.push({ type:'offer', price: v, by: state.user.name, time: Date.now() });
    state.transactions[nft.id] = arr; Store.set('transactions', state.transactions);
    addNotification(`Oferta de ${v} ETH enviada para "${nft.title}"`);
    showToast('Oferta enviada');
  }
  function actionContact(nft){
    if(!requireAuth('contactar')) return;
    showToast(`Mensaje enviado a ${nft.artist}`);
    addNotification(`Enviaste mensaje a ${nft.artist} sobre "${nft.title}"`);
  }
  function toggleFav(id){
    if(!requireAuth('agregar a favoritos')) return;
    const nid = isNaN(id) ? id : Number(id);
    const idx = state.favorites.findIndex(x => x == id);
    if(idx >= 0) state.favorites.splice(idx,1); else state.favorites.push(nid);
    Store.set('favorites', state.favorites);
    render();
  }
  function shareNft(nft){
    const text = `Mira "${nft.title}" por ${nft.artist} en Los profetas`;
    if(navigator.share){
      navigator.share({ title: nft.title, text, url: location.href }).catch(()=>{});
    } else if(navigator.clipboard){
      navigator.clipboard.writeText(`${text} — ${location.href}`);
      showToast('Enlace copiado al portapapeles');
    } else {
      showToast('Compartir no soportado en este navegador');
    }
  }

  /* ======================== Galería + filtros ======================== */
  const gallery = $('#gallery');
  const emptyState = $('#emptyState');

  function applyFilters(items){
    let r = items.slice();
    const f = state.filters;
    if(f.category !== 'all') r = r.filter(n => n.category === f.category);
    if(f.q){
      const q = f.q.toLowerCase();
      r = r.filter(n =>
        n.title.toLowerCase().includes(q) ||
        n.artist.toLowerCase().includes(q) ||
        (n.tags||[]).some(t => t.toLowerCase().includes(q))
      );
    }
    if(f.tag === 'favorites') r = r.filter(n => state.favorites.some(id => id == n.id));
    else if(f.tag === 'under1') r = r.filter(n => n.price < 1);
    else if(f.tag === 'trending') r = r.slice().sort((a,b) => (b.likes||0) - (a.likes||0)).slice(0, 6);
    else if(f.tag === 'new') r = r.slice().sort((a,b) => (b.createdAt||0) - (a.createdAt||0)).slice(0, 6);

    switch(f.sort){
      case 'price-asc': r.sort((a,b) => a.price - b.price); break;
      case 'price-desc': r.sort((a,b) => b.price - a.price); break;
      case 'popular': r.sort((a,b) => (b.likes||0) - (a.likes||0)); break;
      default: r.sort((a,b) => (b.createdAt||0) - (a.createdAt||0));
    }
    return r;
  }

  function render(){
    const items = applyFilters(state.nfts);
    $('#statAssets').textContent = state.nfts.length.toLocaleString();
    $('#resultCount').textContent = `${items.length} obra${items.length !== 1 ? 's' : ''}`;
    if(items.length === 0){
      gallery.innerHTML = '';
      emptyState.classList.remove('hidden');
      return;
    }
    emptyState.classList.add('hidden');

    gallery.innerHTML = items.map((nft, i) => {
      const isFav = state.favorites.some(id => id == nft.id);
      const heart = isFav
        ? '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 21s-7-4.35-9.5-9.5C.5 7 4 4 7 4c2 0 3.5 1 5 3 1.5-2 3-3 5-3 3 0 6.5 3 4.5 7.5C19 16.65 12 21 12 21z"/></svg>'
        : '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 21s-7-4.35-9.5-9.5C.5 7 4 4 7 4c2 0 3.5 1 5 3 1.5-2 3-3 5-3 3 0 6.5 3 4.5 7.5C19 16.65 12 21 12 21z"/></svg>';
      return `
        <article class="card" data-id="${nft.id}" style="animation-delay:${Math.min(i, 8) * 50}ms">
          <div class="art" style="${artBg(nft)}">
            ${nft.image ? `<img src="${nft.image}" alt="${escapeHtml(nft.title)}">` : ''}
            <div class="art-badge">${nft.category}</div>
            <button class="fav-btn ${isFav ? 'active' : ''}" data-fav="${nft.id}" aria-label="Favorito">${heart}</button>
          </div>
          <div class="meta">
            <div>
              <div class="nft-title">${escapeHtml(nft.title)}</div>
              <div class="nft-artist">${escapeHtml(nft.artist)}</div>
            </div>
            <div style="text-align:right">
              <div class="price">${fmtPrice(nft.price)}</div>
              <div class="nft-cat">${(nft.likes||0)} ★</div>
            </div>
          </div>
          <div class="actions">
            <button class="small-btn trade" data-trade="${nft.id}">Intercambiar</button>
            <button class="small-btn buy" data-buy="${nft.id}">Comprar</button>
          </div>
        </article>
      `;
    }).join('');

    gallery.querySelectorAll('.card').forEach(c => {
      c.addEventListener('click', (e) => {
        if(e.target.closest('button')) return;
        openDetail(c.dataset.id);
      });
    });
    gallery.querySelectorAll('[data-fav]').forEach(b => b.addEventListener('click', (e) => { e.stopPropagation(); toggleFav(b.dataset.fav); }));
    gallery.querySelectorAll('[data-trade]').forEach(b => b.addEventListener('click', (e) => { e.stopPropagation(); openDetail(b.dataset.trade); }));
    gallery.querySelectorAll('[data-buy]').forEach(b => b.addEventListener('click', (e) => { e.stopPropagation(); openDetail(b.dataset.buy); }));
  }

  $('#filter').addEventListener('change', e => { state.filters.category = e.target.value; render(); });
  $('#sort').addEventListener('change', e => { state.filters.sort = e.target.value; render(); });
  $('#search').addEventListener('input', e => { state.filters.q = e.target.value.trim(); render(); });
  $$('.tag').forEach(t => t.addEventListener('click', () => {
    $$('.tag').forEach(b => b.classList.toggle('active', b === t));
    state.filters.tag = t.dataset.tag;
    render();
  }));

  /* ======================== Notificaciones ======================== */
  function addNotification(text){
    state.notifications.unshift({ id: uid(), text, time: Date.now(), read: false });
    if(state.notifications.length > 30) state.notifications.length = 30;
    Store.set('notifications', state.notifications);
    refreshNotifBadge();
  }
  function refreshNotifBadge(){
    const unread = state.notifications.filter(n => !n.read).length;
    const b = $('#notifBadge');
    if(unread > 0){ b.textContent = unread; b.hidden = false; } else { b.hidden = true; }
  }
  $('#notifBtn').addEventListener('click', (e) => {
    e.stopPropagation();
    const dd = $('#notifDropdown');
    if(dd.hidden){
      dd.hidden = false;
      $('#notifList').innerHTML = state.notifications.length === 0
        ? '<div style="padding:24px;text-align:center;color:var(--muted)">Sin notificaciones</div>'
        : state.notifications.map(n => `
          <div class="notif-item ${n.read ? '' : 'unread'}">
            <div><div class="nf-text">${escapeHtml(n.text)}</div><div class="nf-time">${fmtTime(n.time)}</div></div>
          </div>`).join('');
    } else {
      dd.hidden = true;
    }
  });
  $('#markAllRead').addEventListener('click', () => {
    state.notifications.forEach(n => n.read = true);
    Store.set('notifications', state.notifications);
    refreshNotifBadge();
    $('#notifDropdown').hidden = true;
  });
  document.addEventListener('click', (e) => {
    if(!e.target.closest('#notifDropdown') && !e.target.closest('#notifBtn')){
      $('#notifDropdown').hidden = true;
    }
  });

  /* ======================== Configuración ======================== */
  $('#settingsBtn').addEventListener('click', () => {
    $('#setLang').value = state.settings.lang;
    $('#setCurrency').value = state.settings.currency;
    $('#setNotif').checked = !!state.settings.notif;
    $('#setIva').checked = !!state.settings.iva;
    $$('.seg-btn[data-theme-set]').forEach(b => b.classList.toggle('active', b.dataset.themeSet === state.settings.theme));
    openModal('settingsModal');
  });

  $$('.seg-btn[data-theme-set]').forEach(b => b.addEventListener('click', () => {
    state.settings.theme = b.dataset.themeSet;
    Store.set('settings', state.settings);
    applyTheme(state.settings.theme);
  }));
  $('#setLang').addEventListener('change', e => { state.settings.lang = e.target.value; Store.set('settings', state.settings); showToast('Idioma actualizado (demo)'); });
  $('#setCurrency').addEventListener('change', e => { state.settings.currency = e.target.value; Store.set('settings', state.settings); render(); showToast(`Moneda: ${e.target.value}`); });
  $('#setNotif').addEventListener('change', e => { state.settings.notif = e.target.checked; Store.set('settings', state.settings); });
  $('#setIva').addEventListener('change', e => { state.settings.iva = e.target.checked; Store.set('settings', state.settings); render(); });

  $('#exportData').addEventListener('click', () => {
    const data = {
      user: state.user,
      myNfts: state.nfts.filter(n => n.artistId === state.user?.id),
      favorites: state.favorites,
      comments: state.comments,
      notifications: state.notifications,
      settings: state.settings
    };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `losprofetas-export-${Date.now()}.json`;
    a.click();
    showToast('Datos exportados');
  });

  $('#logoutBtn').addEventListener('click', async () => {
    const ok = await confirmDialog('Cerrar sesión', '¿Quieres cerrar tu sesión actual?');
    if(!ok) return;
    state.user = null; state.session = false;
    Store.del('user'); Store.set('session', false);
    closeModal('settingsModal');
    refreshAuthUI();
    showToast('Sesión cerrada');
  });

  $('#deleteAccount').addEventListener('click', async () => {
    const ok = await confirmDialog('Eliminar cuenta', 'Se borrarán todos tus datos locales. ¿Continuar?');
    if(!ok) return;
    Store.clearAll();
    location.reload();
  });

  /* ======================== Cerrar modal con botón × del detalle ======================== */
  $('#closeModal').addEventListener('click', () => closeModal('modal'));

  /* ======================== Init ======================== */
  refreshAuthUI();
  refreshWalletBtn();
  refreshNotifBadge();
  render();

  if(state.notifications.length === 0){
    addNotification('Bienvenido a Los profetas — explora la colección.');
  }

})();
