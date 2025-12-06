# Akıllı Priz - Render.com Backend
# Flask web server - ESP32 ve iOS uygulaması arasında köprü

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)  # iOS uygulaması için CORS etkinleştir

# Global durum değişkenleri
current_state = {
    "state": "OFF",
    "timestamp": datetime.now().isoformat()
}

telemetry_data = {
    "current": 0.0,
    "voltage": 220.0,
    "power": 0.0,
    "energy": 0.0,
    "temperature": 25.0,
    "timestamp": datetime.now().isoformat(),
    "state": "OFF"
}

# MARK: - Health Check
@app.route('/health', methods=['GET'])
def health():
    """Sunucu sağlık kontrolü"""
    return jsonify({"status": "OK", "timestamp": datetime.now().isoformat()}), 200

# MARK: - Command Endpoints (iOS App kullanır)
@app.route('/command', methods=['GET', 'POST'])
def command():
    """
    iOS App POST ile komut gönderir
    ESP32 GET ile komut alır
    """
    global current_state
    
    if request.method == 'POST':
        # iOS App'den gelen komut
        data = request.get_json()
        new_state = data.get('state', 'OFF')
        
        if new_state in ['ON', 'OFF']:
            current_state = {
                "state": new_state,
                "timestamp": datetime.now().isoformat()
            }
            print(f"📱 iOS → Command: {new_state}")
            return jsonify(current_state), 200
        else:
            return jsonify({"error": "Invalid state"}), 400
    
    elif request.method == 'GET':
        # ESP32'den gelen istek - mevcut komutu döndür
        print(f"🤖 ESP32 ← Command: {current_state['state']}")
        return jsonify(current_state), 200

# MARK: - Telemetry Endpoints
@app.route('/telemetry', methods=['GET', 'POST'])
def telemetry():
    """
    ESP32 POST ile telemetri gönderir
    iOS App GET ile telemetri alır
    """
    global telemetry_data
    
    if request.method == 'POST':
        # ESP32'den gelen telemetri verisi
        data = request.get_json()
        
        telemetry_data = {
            "current": data.get('current', 0.0),
            "voltage": data.get('voltage', 220.0),
            "power": data.get('power', 0.0),
            "energy": data.get('energy', 0.0),
            "temperature": data.get('temperature', 25.0),
            "timestamp": datetime.now().isoformat(),
            "state": data.get('state', 'OFF')
        }
        
        print(f"🤖 ESP32 → Telemetry: {telemetry_data['power']}W, {telemetry_data['state']}")
        return jsonify({"success": True}), 200
    
    elif request.method == 'GET':
        # iOS App'den gelen istek - telemetri verisini döndür
        print(f"📱 iOS ← Telemetry: {telemetry_data['power']}W")
        return jsonify(telemetry_data), 200

# MARK: - Status Endpoint (İsteğe bağlı)
@app.route('/status', methods=['GET'])
def status():
    """Genel durum bilgisi"""
    return jsonify({
        "command": current_state,
        "telemetry": telemetry_data,
        "server_time": datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

