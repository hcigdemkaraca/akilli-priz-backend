# Akıllı Priz Backend (Render.com)

Flask backend that acts as a bridge between iOS app and ESP32 device.

## Features

- ✅ RESTful API
- ✅ CORS enabled for iOS app
- ✅ Command routing (iOS → ESP32)
- ✅ Telemetry routing (ESP32 → iOS)
- ✅ Ready for Render.com deployment

## API Endpoints

### Health Check
```
GET /health
```

### Command
```
POST /command   # iOS sends command
GET /command    # ESP32 reads command
```

### Telemetry
```
POST /telemetry  # ESP32 sends data
GET /telemetry   # iOS reads data
```

### Status
```
GET /status  # Full system status
```

## Local Development

```bash
pip install -r requirements.txt
python app.py
```

Server runs at `http://localhost:5000`

## Deploy to Render.com

1. Push to GitHub
2. Create new Web Service on Render.com
3. Connect GitHub repository
4. Deploy (automatic)

See `RENDER_SETUP.md` for detailed instructions.

## Environment Variables

- `PORT`: Server port (default: 5000)

## Tech Stack

- Flask 3.0.0
- Flask-CORS 4.0.0
- Gunicorn 21.2.0
- Python 3.11+

