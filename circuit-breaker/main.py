import requests
from pybreaker import CircuitBreaker, CircuitBreakerError

# Definir una función que llama a una API externa
def call_external_api():
    response = requests.get('http://whoogle.discovery.mair')
    return response.status_code

# Configurar un circuit breaker con una capacidad de falla de 3 y un tiempo de inactividad de 30 segundos
breaker = CircuitBreaker(fail_max=3, reset_timeout=30)

# Envolver la función de llamada a la API en el circuit breaker
@breaker
def api_call():
    try:
        status_code = call_external_api()
        if status_code == 200:
            return "API call successful"
        else:
            raise Exception("API call failed")
    except:
        raise CircuitBreakerError("API call failed too many times")

# Ejecutar la llamada a la API
try:
    result = api_call()
    print(result)
except CircuitBreakerError:
    print("API call failed too many times. Circuit breaker is open.")

