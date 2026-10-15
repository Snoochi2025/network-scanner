# Working in this repo (Base44 sandbox)

## Running it

```bash
docker compose -f docker-compose.base44.yml up -d --build
```

One service, `web`, on host port 3000. It uses the plain `python:3.12-slim` image
with the repo bind-mounted at `/app` — there is no Dockerfile and no build step,
because the project only uses the Python standard library.

## Things that are not obvious

- **No dependencies at all.** No `requirements.txt`, no lockfile, nothing to
  install. If you ever add a third-party package, add a manifest *and* an install
  step to the compose startup command.
- **The scanner logic is shared.** `scanner.py` holds `scan_ports()` and the
  service-name table. Both `network_scanner.py` (the original CLI) and
  `web_app.py` (the page) call it, so a change to the scanning behaviour belongs
  in `scanner.py` and applies to both.
- **Editing.** `static/*.html|css|js` are read from disk on each request and sent
  with `Cache-Control: no-store`, so page edits appear on a browser reload with no
  restart. Changes to a `.py` file need `docker compose -f docker-compose.base44.yml restart web`
  (a plain `http.server` process has no auto-reload).
- **The healthcheck uses `urllib`,** not `curl`/`wget`, because those are not in
  the `python:3.12-slim` image.
- **Scan results are container-local.** The server runs inside the container, so
  scanning `127.0.0.1` scans the container's own loopback and reports 0 open ports.
  That is expected here, not a bug.
- **No web framework and no Host/Origin allowlist.** `web_app.py` is a plain
  `ThreadingHTTPServer` bound to `0.0.0.0:3000`, so there is nothing to configure
  for the preview proxy.

## Verifying

```bash
curl -s http://localhost:3000/            # the page renders
curl -s 'http://localhost:3000/api/scan?target=127.0.0.1&start=1&end=100'
curl -s 'http://localhost:3000/api/scan?target=localhost&start=1&end=5'
docker compose -f docker-compose.base44.yml ps        # web should be healthy
```

The command line version still works unchanged:

```bash
docker compose -f docker-compose.base44.yml exec web python network_scanner.py
```
