#!/bin/bash
set -xe

#USERS_URL="http://localhost:5001/users"
USERS_URL="http://localhost:8080/api/users"

#PRODUCT_URL="http://localhost:5002/products"
PRODUCT_URL="http://localhost:8080/api/products"

#ORDERS_URL="http://localhost:5003/orders"
ORDERS_URL="http://localhost:8080/api/orders"

# Crear usuario
curl -X POST $USERS_URL \
  -H "Content-Type: application/json" \
  -d '{"id":"u1","name":"Mario"}'

# Crear producto
curl -X POST $PRODUCT_URL \
  -H "Content-Type: application/json" \
  -d '{"id":"p1","name":"Laptop","price":1200}'

# Crear orden (order-service llama a los otros 2)
curl -X POST $ORDERS_URL \
  -H "Content-Type: application/json" \
  -d '{"id":"o1","user_id":"u1","product_id":"p1"}'

# Ver orden
curl http://localhost:5003/orders/o1

