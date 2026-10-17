const selector = document.querySelector('#training-user');
const content = document.querySelector('#content');

for (let value = 0; value <= 99; value += 1) {
  const code = String(value).padStart(2, '0');
  const option = document.createElement('option');
  option.value = code;
  option.textContent = `${code} — ${code === '00' ? 'Formateur' : 'Participant'}`;
  option.selected = code === '07';
  selector.appendChild(option);
}

const escapeHtml = (value) => String(value ?? '—')
  .replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;')
  .replaceAll('"', '&quot;').replaceAll("'", '&#039;');

const labels = {
  training_user: 'Training user', sales_order_type: 'Sales Order Type',
  sales_organization: 'Sales Organization', distribution_channel: 'Distribution Channel',
  organization_division: 'Organization Division', sold_to_party: 'Sold-To Party',
  customer_reference: 'Customer Reference', material: 'Material', quantity: 'Quantity', unit: 'Unit'
};

function rows(data, compare = null) {
  return Object.entries(data).map(([key, value]) => {
    const changed = compare && compare[key] !== value ? ' changed' : '';
    return `<div class="data-row${changed}"><span>${escapeHtml(labels[key] || key)}</span><code>${escapeHtml(value)}</code></div>`;
  }).join('');
}

function workflowBranch(data, branch, title, summary) {
  const nodes = data.nodes.filter(node => node.branch === branch);
  return `<div class="workflow-branch">
    <div class="branch-label"><strong>${escapeHtml(title)}</strong><p>${escapeHtml(summary)}</p></div>
    <div class="flow">${nodes.map(node => `<div class="flow-node"><span>${escapeHtml(node.object_type)}</span><strong>${escapeHtml(node.label)}</strong><code>${escapeHtml(node.object_id)}</code></div>`).join('')}</div>
  </div>`;
}

function render(data) {
  document.querySelector('#resolved-user').textContent = data.training_context.training_user;
  document.querySelector('#course').textContent = `${data.source.course_code} · Chapitre ${data.source.chapter}`;
  document.querySelector('#exercise-title').textContent = data.source.exercise_title;
  const source = [
    ['Book', data.source.book], ['Scénario', data.source.scenario_id],
    ['Exercice', `${data.source.exercise} · page ${data.source.exercise_page}`],
    ['Solution', `page ${data.source.solution_page}`], ['Canonical Object ID', data.source.canonical_object_id]
  ];
  document.querySelector('#source-grid').innerHTML = source.map(([key, value]) => `<div><dt>${escapeHtml(key)}</dt><dd>${escapeHtml(value)}</dd></div>`).join('');
  document.querySelector('#original-data').innerHTML = rows(data.original_book_data);
  document.querySelector('#runtime-data').innerHTML = rows(data.runtime_data, data.original_book_data);
  document.querySelector('#workflow').innerHTML =
    workflowBranch(data.workflow, 'CASH_SALE', 'Vente au comptant', data.workflow.cash_sale_summary) +
    workflowBranch(data.workflow, 'PRO_FORMA', 'Pro forma', data.workflow.pro_forma_summary);

  const mapping = data.sap_mapping;
  document.querySelector('#interface-badge').innerHTML = `${escapeHtml(mapping.service)}<br>${escapeHtml(mapping.entity_set)}`;
  document.querySelector('#mapping-rows').innerHTML = mapping.rows.map(row => `<tr>
    <td><code>${escapeHtml(row.canonical_field)}</code></td><td>${escapeHtml(row.canonical_value)}</td>
    <td>${row.sap_fields.map(field => `<code>${escapeHtml(field)}</code>`).join('<br>')}</td><td><span class="pill">${escapeHtml(row.disposition)}</span></td>
  </tr>`).join('');
  document.querySelector('#payload-preview').textContent = JSON.stringify(mapping.offline_payload_preview, null, 2);

  document.querySelector('#prechecks').innerHTML = data.prechecks.map(check => {
    const stateClass = check.status === 'PASS' ? 'pass' : check.status === 'BLOCKED' ? 'blocked' : '';
    return `<article class="check"><div class="check-top"><h3>${escapeHtml(check.name)}</h3><span class="status ${stateClass}">${escapeHtml(check.status)}</span></div>
      <dl><dt>Valeur</dt><dd><code>${escapeHtml(check.resolved_values.join(', '))}</code></dd><dt>Service</dt><dd>${escapeHtml(check.service || 'Non confirmé')}</dd><dt>EntitySet</dt><dd>${escapeHtml(check.entity_set || 'Non confirmé')}</dd><dt>Méthode</dt><dd>${escapeHtml(check.method)} uniquement</dd><dt>Filtre</dt><dd><code>${escapeHtml(check.proposed_filter || 'Non confirmé')}</code></dd></dl>
      <p class="reason">${escapeHtml(check.reason)}</p></article>`;
  }).join('');

  const final = data.final_result;
  document.querySelector('#result-section').classList.toggle('ready', final.status === 'READY');
  document.querySelector('#final-status').textContent = final.status;
  document.querySelector('#final-copy').textContent = final.status === 'READY'
    ? 'Résolution, mapping et contrôles read-only validés.'
    : `Mapping local ${final.local_mapping_status}; validation SAP read-only encore requise.`;
  document.querySelector('#blocking-reasons').innerHTML = final.blocking_reasons.map(reason => `<li><strong>${escapeHtml(reason.code)}</strong><br>${escapeHtml(reason.detail)}</li>`).join('');
}

async function loadScenario() {
  content.classList.add('loading');
  try {
    const response = await fetch(`/api/golden-book?training_user=${encodeURIComponent(selector.value)}`, {method: 'GET'});
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Scénario indisponible');
    render(data);
  } catch (error) {
    content.innerHTML = `<div class="error">${escapeHtml(error.message)}</div>`;
  } finally {
    content.classList.remove('loading');
  }
}

selector.addEventListener('change', loadScenario);
loadScenario();
