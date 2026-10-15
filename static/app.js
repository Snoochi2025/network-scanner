const form = document.getElementById("scan-form");
const button = document.getElementById("scan-button");
const status = document.getElementById("status");
const results = document.getElementById("results");
const resultsBody = document.getElementById("results-body");

function setStatus(message, modifier) {
  status.textContent = message;
  status.className = modifier ? `status status--${modifier}` : "status";
}

function setBusy(busy) {
  button.disabled = busy;
  button.textContent = busy ? "Scanning…" : "Scan";
}

function renderResults(data) {
  const summary = `Scanned ${data.scanned} port${data.scanned === 1 ? "" : "s"} on ${data.target} (${data.ip}) in ${data.duration_ms} ms.`;

  if (data.total_open === 0) {
    setStatus(`No open ports were found. ${summary}`, "empty");
    return;
  }

  setStatus(`Total open ports found: ${data.total_open}. ${summary}`, "ok");

  for (const entry of data.open_ports) {
    const row = document.createElement("tr");

    const port = document.createElement("td");
    port.className = "port";
    port.textContent = entry.port;

    const service = document.createElement("td");
    service.textContent = entry.service;

    row.append(port, service);
    resultsBody.append(row);
  }

  results.hidden = false;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const params = new URLSearchParams({
    target: document.getElementById("target").value.trim(),
    start: document.getElementById("start").value,
    end: document.getElementById("end").value,
  });

  setBusy(true);
  setStatus("Scanning…", "busy");
  resultsBody.replaceChildren();
  results.hidden = true;

  try {
    const response = await fetch(`/api/scan?${params}`);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "The scan failed.");
    }

    renderResults(data);
  } catch (error) {
    setStatus(error.message, "error");
  } finally {
    setBusy(false);
  }
});
