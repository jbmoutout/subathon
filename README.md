# zawathon — combien pour tenir ?

A small live dashboard for the **Zawa zawathon** (a subathon where the stream keeps going as long as
subs / Tipeee tips add time). It reads the public counter API and answers, in one glance:

- the **current guaranteed end** of the stream (if all donations stopped now), and
- via a timeline slider, **when any past end-date got locked in**, and **how many subs / 5 € tips** are
  needed to push the stream to any future date.

Conversion (1 sub = +1 min 30, 1 Tipeee 5 € = +2 min) is **derived live** from `/api/events` — it
auto-adapts if the rule changes — with the announced values as fallback.

## Data source

[`zawathon.ascentcloud.art`](https://zawathon.ascentcloud.art) — `/api/data` and `/api/events`.
The API sends no CORS headers, so the site proxies `/api/*` through its own origin
(`vercel.json` rewrites in production, `_redirects` for Netlify/Cloudflare, `serve.py` locally).

## Run locally

```bash
python3 serve.py        # → http://localhost:8000/
```

`serve.py` serves `index.html` and proxies `/api/*` to the upstream so the browser sees one origin.
The whole app is a single static file: [`index.html`](index.html).
