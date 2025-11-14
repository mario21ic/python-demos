from flask import Flask, request, jsonify
import os
import redis
import json

app = Flask(__name__)

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
r = redis.from_url(REDIS_URL)


@app.get("/health")
def health():
    return {"status": "ok", "service": "user-service"}, 200


@app.post("/users")
def create_user():
    data = request.get_json() or {}
    user_id = str(data.get("id", "")).strip()
    name = data.get("name", "").strip()

    if not user_id or not name:
        return {"error": "fields 'id' and 'name' are required"}, 400

    key = f"user:{user_id}"
    r.set(key, json.dumps({"id": user_id, "name": name}))

    return {"message": "user created", "id": user_id, "name": name}, 201


@app.get("/users/<user_id>")
def get_user(user_id):
    key = f"user:{user_id}"
    raw = r.get(key)
    if not raw:
        return {"error": "user not found"}, 404
    user = json.loads(raw)
    return jsonify(user), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

