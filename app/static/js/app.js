import * as THREE from 'https://unpkg.com/three@0.164.1/build/three.module.js';

const state = {
  role: null,
  userId: 1,
  category: null,
  design: null,
  material: 'Wool Blend',
  color: '#1e3a8a',
  skinTone: 'fair',
  measurements: null,
  models: [],
};

const views = ['login-view', 'public-view', 'measurement-view', 'models-view', 'order-view', 'garment-view'];
const show = (id) => views.forEach((v) => document.getElementById(v).classList.toggle('hidden', v !== id));

const loginButtons = document.querySelectorAll('.role-btn');
const categoriesEl = document.getElementById('categories');
const collectionEl = document.getElementById('collection-list');
const recommendationsEl = document.getElementById('recommendations');
const modelGrid = document.getElementById('model-grid');

loginButtons.forEach((btn) => {
  btn.addEventListener('click', async () => {
    state.role = btn.dataset.role;
    if (state.role === 'public') {
      show('public-view');
      await loadCatalog();
    } else {
      show('garment-view');
    }
  });
});

async function loadCatalog() {
  const catalog = await fetch('/api/catalog').then((r) => r.json());
  categoriesEl.innerHTML = Object.keys(catalog)
    .map((c) => `<button class="cat-btn" data-cat="${c}">${c.toUpperCase()}</button>`)
    .join('');

  document.querySelectorAll('.cat-btn').forEach((b) => {
    b.addEventListener('click', () => {
      state.category = b.dataset.cat;
      document.getElementById('collection-step').classList.remove('hidden');
      collectionEl.innerHTML = catalog[state.category]
        .map((name) => `<button class="design-btn" data-design="${name}">${name}</button>`)
        .join('');

      document.querySelectorAll('.design-btn').forEach((d) => {
        d.addEventListener('click', () => {
          state.design = d.dataset.design;
          document.getElementById('design-step').classList.remove('hidden');
        });
      });
    });
  });
}

document.getElementById('recommend-colors').addEventListener('click', async () => {
  state.skinTone = document.getElementById('skin-tone').value;
  state.material = document.getElementById('material').value || 'Wool Blend';
  state.color = document.getElementById('dress-color').value;
  const data = await fetch(`/api/skin-tone/${state.skinTone}/recommendations`).then((r) => r.json());
  recommendationsEl.innerHTML = data.recommended_colors.map((c) => `<span style="background:${c};color:#fff">${c}</span>`).join('');
});

document.getElementById('to-measurements').addEventListener('click', () => show('measurement-view'));

document.getElementById('generate-models').addEventListener('click', async () => {
  const fd = new FormData(document.getElementById('measurement-form'));
  state.measurements = Object.fromEntries(fd.entries());
  for (const k in state.measurements) state.measurements[k] = Number(state.measurements[k]);

  const payload = {
    user_id: state.userId,
    category: state.category,
    design: state.design,
    material: state.material,
    color: state.color,
    skin_tone: state.skinTone,
    measurements: state.measurements,
  };

  const data = await fetch('/api/models/generate', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload),
  }).then((r) => r.json());

  state.models = data.models;
  renderModels();
  renderHumanoid(data.models[0]?.body_scale || 1);
  show('models-view');
});

function renderModels() {
  modelGrid.innerHTML = state.models.map((m) => `
    <div class="model-card">
      <strong>${m.label}</strong>
      <div>Scale: ${m.body_scale}</div>
      <div>Material: ${m.material}</div>
      <div class="btns">
        <button data-order="${m.model_id}">Order</button>
        <button data-customize="${m.model_id}">Customize</button>
      </div>
    </div>
  `).join('');

  modelGrid.querySelectorAll('[data-order]').forEach((b) => b.addEventListener('click', () => show('order-view')));
  modelGrid.querySelectorAll('[data-customize]').forEach((b) => b.addEventListener('click', () => {
    document.getElementById('custom-prompt').value = `Refine ${b.dataset.customize} with embossed textures and alternate collar.`;
  }));
}

document.getElementById('create-custom').addEventListener('click', async () => {
  const prompt = document.getElementById('custom-prompt').value;
  if (!prompt) return;
  const payload = {
    user_id: state.userId,
    category: state.category,
    design: `${state.design} (Custom)`,
    material: state.material,
    color: state.color,
    skin_tone: state.skinTone,
    measurements: state.measurements,
    prompt,
  };
  const data = await fetch('/api/models/generate', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload),
  }).then((r) => r.json());
  state.models.push(data.models[0]);
  renderModels();
});

document.getElementById('submit-order').addEventListener('click', async () => {
  const fd = new FormData(document.getElementById('order-form'));
  const orderPayload = {
    user_id: state.userId,
    dress_category: state.category,
    dress_design: state.design,
    material: state.material,
    color: state.color,
    measurements: state.measurements,
    shipping_address: `${fd.get('address')}, ${fd.get('location')}`,
    extra_details: fd.get('extra') || '',
  };
  const result = await fetch('/api/orders', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(orderPayload),
  }).then((r) => r.json());
  document.getElementById('order-result').textContent = JSON.stringify(result, null, 2);
});

document.getElementById('ar-btn').addEventListener('click', () => {
  alert('WebXR AR preview can be activated on compatible mobile browsers with camera permission.');
});

function renderHumanoid(scale = 1) {
  const canvas = document.getElementById('viewer');
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
  renderer.setSize(canvas.clientWidth, canvas.clientHeight, false);

  const scene = new THREE.Scene();
  scene.background = new THREE.Color('#cbd5e1');
  const camera = new THREE.PerspectiveCamera(45, canvas.clientWidth / canvas.clientHeight, 0.1, 1000);
  camera.position.set(0, 1.4, 3.2);

  const light = new THREE.DirectionalLight(0xffffff, 1);
  light.position.set(2, 4, 3);
  scene.add(light);
  scene.add(new THREE.AmbientLight(0xffffff, .8));

  const mat = new THREE.MeshStandardMaterial({ color: state.color });
  const skin = new THREE.MeshStandardMaterial({ color: '#b8b8b8' });
  const group = new THREE.Group();

  const torso = new THREE.Mesh(new THREE.BoxGeometry(0.75, 1, 0.35), mat);
  torso.position.y = 1.1;
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.22, 24, 24), skin);
  head.position.y = 1.82;
  const leftLeg = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 0.95, 16), mat);
  leftLeg.position.set(-0.2, 0.35, 0);
  const rightLeg = leftLeg.clone();
  rightLeg.position.x = 0.2;
  const leftArm = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, 0.82, 16), mat);
  leftArm.position.set(-0.52, 1.18, 0);
  leftArm.rotation.z = 0.25;
  const rightArm = leftArm.clone();
  rightArm.position.x = 0.52;
  rightArm.rotation.z = -0.25;

  group.add(torso, head, leftLeg, rightLeg, leftArm, rightArm);
  group.scale.setScalar(scale);
  scene.add(group);

  const animate = () => {
    group.rotation.y += 0.01;
    renderer.render(scene, camera);
    requestAnimationFrame(animate);
  };
  animate();
}

document.getElementById('load-dashboard').addEventListener('click', async () => {
  const data = await fetch('/api/garment/dashboard').then((r) => r.json());
  drawBarChart(data.status_counts);
  const tbody = document.querySelector('#payment-table tbody');
  tbody.innerHTML = data.payments.map((p) => `
    <tr><td>${p.order_id}</td><td>${p.amount}</td><td>${p.mode}</td><td>${p.account_ref}</td><td>${p.paid_at}</td></tr>
  `).join('');
  const orders = await fetch('/api/garment/orders').then((r) => r.json());
  document.getElementById('garment-orders').innerHTML = orders.map((o) => `<div class="model-card">#${o.id} ${o.design}<br>${o.status}</div>`).join('');
});

function drawBarChart(statusCounts) {
  const canvas = document.getElementById('dashboard-chart');
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const keys = Object.keys(statusCounts);
  const values = Object.values(statusCounts);
  const maxVal = Math.max(1, ...values);
  const w = canvas.width / keys.length;

  keys.forEach((k, i) => {
    const h = (values[i] / maxVal) * (canvas.height - 80);
    const x = i * w + 20;
    const y = canvas.height - h - 40;
    ctx.fillStyle = '#2563eb';
    ctx.fillRect(x, y, w - 40, h);
    ctx.fillStyle = '#0f172a';
    ctx.fillText(k, x, canvas.height - 20);
    ctx.fillText(String(values[i]), x + 8, y - 8);
  });
}

document.getElementById('export-csv').addEventListener('click', async () => {
  const data = await fetch('/api/garment/dashboard').then((r) => r.json());
  const rows = [['status', 'count'], ...Object.entries(data.status_counts)];
  const csv = rows.map((r) => r.join(',')).join('\n');
  const blob = new Blob([csv], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'dashboard_status.csv';
  a.click();
  URL.revokeObjectURL(url);
});
