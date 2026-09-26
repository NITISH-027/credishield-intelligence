const API_BASE = '/api';

export async function searchBuyers(query, cin = null, gstin = null) {
  const res = await fetch(`${API_BASE}/buyers/search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, cin, gstin })
  });
  if (!res.ok) throw new Error(`Search failed: ${res.statusText}`);
  return res.json();
}

export async function getBuyersList(isDemo = null) {
  const url = isDemo !== null ? `${API_BASE}/buyers?is_demo=${isDemo}` : `${API_BASE}/buyers`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Fetch failed: ${res.statusText}`);
  return res.json();
}

export async function getBuyerDetail(buyerId) {
  const res = await fetch(`${API_BASE}/buyers/${buyerId}`);
  if (!res.ok) throw new Error(`Fetch failed: ${res.statusText}`);
  return res.json();
}

export async function getBuyerGraph(buyerId) {
  const res = await fetch(`${API_BASE}/buyers/${buyerId}/graph`);
  if (!res.ok) throw new Error(`Fetch failed: ${res.statusText}`);
  return res.json();
}

export async function getBuyerPaymentHistory(buyerId) {
  const res = await fetch(`${API_BASE}/buyers/${buyerId}/payment-history`);
  if (!res.ok) throw new Error(`Fetch failed: ${res.statusText}`);
  return res.json();
}

export async function getBuyerDisputes(buyerId) {
  const res = await fetch(`${API_BASE}/buyers/${buyerId}/disputes`);
  if (!res.ok) throw new Error(`Fetch failed: ${res.statusText}`);
  return res.json();
}

export async function getBuyerFilings(buyerId) {
  const res = await fetch(`${API_BASE}/buyers/${buyerId}/filings`);
  if (!res.ok) throw new Error(`Fetch failed: ${res.statusText}`);
  return res.json();
}

export async function getBuyerInsolvency(buyerId) {
  const res = await fetch(`${API_BASE}/buyers/${buyerId}/insolvency`);
  if (!res.ok) throw new Error(`Fetch failed: ${res.statusText}`);
  return res.json();
}

export async function getBuyerTimeline(buyerId) {
  const res = await fetch(`${API_BASE}/buyers/${buyerId}/timeline`);
  if (!res.ok) throw new Error(`Fetch failed: ${res.statusText}`);
  return res.json();
}

export async function getBuyerRecommendation(buyerId) {
  const res = await fetch(`${API_BASE}/buyers/${buyerId}/recommendation`);
  if (!res.ok) throw new Error(`Fetch failed: ${res.statusText}`);
  return res.json();
}

export async function getBuyerEvidence(buyerId) {
  const res = await fetch(`${API_BASE}/buyers/${buyerId}/evidence`);
  if (!res.ok) throw new Error(`Fetch failed: ${res.statusText}`);
  return res.json();
}

export async function getDemoArchetypes() {
  const res = await fetch(`${API_BASE}/demo/buyers`);
  if (!res.ok) throw new Error(`Fetch failed: ${res.statusText}`);
  return res.json();
}

export async function resetDemoData() {
  const res = await fetch(`${API_BASE}/demo/reset`, { method: 'POST' });
  if (!res.ok) throw new Error(`Reset failed: ${res.statusText}`);
  return res.json();
}
