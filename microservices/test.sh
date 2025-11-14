#!/bin/bash
set -xe


# Crear usuario
curl -X POST http://localhost:5001/users \
  -H "Content-Type: application/json" \
  -d '{"id":"u1","name":"Mario"}'

# Crear producto
curl -X POST http://localhost:5002/products \
  -H "Content-Type: application/json" \
  -d '{"id":"p1","name":"Laptop","price":1200}'

# Crear orden (order-service llama a los otros 2)
curl -X POST http://localhost:5003/orders \
  -H "Content-Type: application/json" \
  -d '{"id":"o1","user_id":"u1","product_id":"p1"}'

# Ver orden
curl http://localhost:5003/orders/o1

