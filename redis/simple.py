from flask import Flask, jsonify
import redis

app = Flask(__name__)

# Conexión a Redis (puede ser Redis local o remoto)
# Si usas Docker: host="redis"
r = redis.Redis(host="redis", port=6379, db=0)

@app.route("/contador", methods=["GET"])
def contador():
    # incrementa el valor de la clave "visitas"
    visitas = r.incr("visitas")
    return jsonify({"contador": visitas})

@app.route("/")
def home():
    return "API Flask + Redis funcionando"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

