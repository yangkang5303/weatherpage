# 🌍 Global Weather Forecast

A real-time global weather dashboard with an interactive map, 7-day forecasts, and city management — available in Chinese and English.

![Python](https://img.shields.io/badge/Python-3.11-blue) ![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey) ![License](https://img.shields.io/badge/license-MIT-green)

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
- **Favorites** — Save and manage your own city list (persisted server-side)
- **City search** — Search any city worldwide via geocoding

## Screenshots


 <img width="1429" height="755" alt="image" src="https://github.com/user-attachments/assets/85555449-fada-40b0-869b-9aa258b8dd44" />
 <img width="790" height="498" alt="image" src="https://github.com/user-attachments/assets/adc6ceaa-5698-42e3-a386-20acd6934448" />
 

## Getting Started

### Local (Python)

```bash
git clone https://github.com/yangkang5303/weatherpage.git
cd weatherpage
pip install flask
python server.py
```

Open **http://localhost:8080**

### Docker

```bash
docker compose up -d
```

Open **http://localhost:8080**

The `weather_data.json` file is volume-mounted so your favorites persist across container restarts.

## Project Structure

```
weatherpage/
├── index.html          # Single-page frontend (Leaflet, vanilla JS)
├── server.py           # Flask backend (favorites API)
├── weather_data.json   # Persisted favorites list
├── Dockerfile
└── docker-compose.yml
```

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Serve the app |
| `GET` | `/api/data` | Get all data |
| `GET` | `/api/favorites` | List favorite cities |
| `POST` | `/api/favorites` | Add a city `{name, country, lat, lon}` |
| `DELETE` | `/api/favorites/<name>` | Remove a city |

## External Services

| Service | Purpose |
|---|---|
| [Open-Meteo](https://open-meteo.com/) | Weather & geocoding (free, no key) |
| [OpenStreetMap](https://www.openstreetmap.org/) | Map tiles |
| [Leaflet.js](https://leafletjs.com/) | Interactive map |

## Security

- Input validation on all API endpoints (type, length, lat/lon range checks)
- XSS protection via HTML escaping on all user/API-derived content
- Security headers: CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy
- Favorites capped at 50 entries
- Production server runs with `debug=False`

## License

MIT
