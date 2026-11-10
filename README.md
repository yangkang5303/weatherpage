# 🌍 Global Weather Forecast

A real-time global weather dashboard with an interactive map, 7-day forecasts, and city management — available in Chinese and English.

![Static Site](https://img.shields.io/badge/static-site-blue) ![License](https://img.shields.io/badge/license-MIT-green)

---

## Features

- **Interactive map** — Leaflet.js map with live weather markers; switch between World, China, USA, UK, France, Germany, and Thailand views
- **Real-time weather** — Powered by the free [Open-Meteo API](https://open-meteo.com/) (no API key required)
- **7-day forecast** — Daily high/low temperatures and precipitation probability bars
- **Current conditions** — Temperature, feels-like, humidity, wind speed & direction, UV index
- **Local time** — Shows the current local time for each city in the World view
- **°C / °F toggle** — Switch temperature units with a single button
- **Dark mode** — One-click light/dark theme switch
- **EN / 中文** — Full bilingual UI (English and Chinese)
- **Favorites** — Save and manage your own city list (saved in your browser, private to each visitor)
- **City search** — Search any city worldwide via geocoding

## Screenshots


 <img width="1429" height="755" alt="image" src="https://github.com/user-attachments/assets/85555449-fada-40b0-869b-9aa258b8dd44" />
 <img width="790" height="498" alt="image" src="https://github.com/user-attachments/assets/adc6ceaa-5698-42e3-a386-20acd6934448" />
 

## Getting Started

This is a pure static site (no backend). Favorites are stored in each visitor's browser (`localStorage`).

### Local

```bash
git clone https://github.com/yangkang5303/weatherpage.git
cd weatherpage/public
python3 -m http.server 8080
```

Open **http://localhost:8080**

### Deploy to Cloudflare

```bash
npx wrangler deploy
```

Or connect the repo in the Cloudflare dashboard (Workers & Pages) with deploy command `npx wrangler deploy`. Security headers (CSP etc.) are defined in `public/_headers`.

## Project Structure

```
weatherpage/
├── public/
│   ├── index.html      # Single-page app (Leaflet, vanilla JS)
│   └── _headers        # Cloudflare security headers
├── wrangler.jsonc      # Cloudflare config
└── LICENSE
```

## External Services

| Service | Purpose |
|---|---|
| [Open-Meteo](https://open-meteo.com/) | Weather & geocoding (free, no key) |
| [OpenStreetMap](https://www.openstreetmap.org/) | Map tiles |
| [Leaflet.js](https://leafletjs.com/) | Interactive map |

## Security

- No backend, no database, no user data on the server
- Favorites live only in the visitor's own browser
- XSS protection via HTML escaping on all user/API-derived content
- Security headers (CSP, X-Frame-Options, etc.) via `public/_headers`

## License

MIT
