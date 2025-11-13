from flask import Flask, jsonify
import redis
import time
from redis.exceptions import RedisError, ConnectionError, TimeoutError

app = Flask(__name__)

# Conexión a Redis (en Docker: host="redis")
r = redis.Redis(host="redis", port=6379, db=0)


class CircuitOpenError(Exception):
    """Se lanza cuando el circuito está abierto y no se permiten llamadas."""
    pass


class CircuitBreaker:
    def __init__(self, failure_threshold=3, recovery_timeout=10):
        """
        failure_threshold: número de errores consecutivos antes de abrir el circuito.
        recovery_timeout: tiempo en segundos que el circuito permanece abierto antes de probar de nuevo (half-open).
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout

        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.failure_count = 0
        self.last_failure_time = None

    def _can_attempt(self):
        if self.state == "CLOSED":
            return True

        now = time.time()

        if self.state == "OPEN":
            # Ver si ya pasó el tiempo de recuperación
            if self.last_failure_time is not None and \
               (now - self.last_failure_time) >= self.recovery_timeout:
                # Pasamos a HALF_OPEN y probamos una vez
                self.state = "HALF_OPEN"
                return True
            else:
                # Sigue abierto, no se permite llamar
                return False

        if self.state == "HALF_OPEN":
            # Solo se permite una llamada de prueba, la manejamos en call()
            return True

        return False

    def call(self, func, *args, **kwargs):
        if not self._can_attempt():
            raise CircuitOpenError("Circuito abierto, no se permiten llamadas")

        try:
            result = func(*args, **kwargs)
        except Exception as e:
            # Falló la llamada
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"

            raise e
        else:
            # Llamada exitosa
            if self.state in ("OPEN", "HALF_OPEN"):
                # Reseteamos el estado
                self.state = "CLOSED"
            self.failure_count = 0
            self.last_failure_time = None
            return result


# Instancia global del CircuitBreaker para Redis
redis_circuit_breaker = CircuitBreaker(
    failure_threshold=3,   # 3 fallos seguidos abren el circuito
    recovery_timeout=10    # 10 segundos antes de probar de nuevo
)


@app.route("/contador", methods=["GET"])
def contador():
    """Contador normal sin circuit breaker."""
    visitas = r.incr("visitas")
    return jsonify({"contador": visitas})


@app.route("/contador_cb", methods=["GET"])
def contador_cb():
    """
    Contador que usa circuit breaker para acceder a Redis.
    Si Redis falla varias veces seguidas, se abre el circuito y se responde rápido.
    """

    def redis_operation():
        # Esta función es la que protege el circuit breaker
        return r.incr("visitas_cb")

    try:
        valor = redis_circuit_breaker.call(redis_operation)
        return jsonify({
            "contador_cb": valor,
            "circuit_state": redis_circuit_breaker.state
        })
    except CircuitOpenError:
        # Circuito abierto: fallamos rápido
        return jsonify({
            "error": "Circuito abierto: Redis no disponible temporalmente",
            "circuit_state": redis_circuit_breaker.state
        }), 503
    except (ConnectionError, TimeoutError, RedisError) as e:
        # Error real al conectar a Redis (y el circuit breaker llevará la cuenta)
        return jsonify({
            "error": "Error al conectarse a Redis",
            "detail": str(e),
            "circuit_state": redis_circuit_breaker.state
        }), 500


@app.route("/")
def home():
    return "API Flask + Redis con Circuit Breaker"


if __name__ == "__main__":
    # host 0.0.0.0 para que sea accesible desde fuera del contenedor
    app.run(host="0.0.0.0", port=5001)

