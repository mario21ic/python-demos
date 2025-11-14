package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"

	"github.com/go-chi/chi/v5"
	"github.com/redis/go-redis/v9"
)

type Order struct {
	ID        string `json:"id"`
	UserID    string `json:"user_id"`
	ProductID string `json:"product_id"`
	Status    string `json:"status"`
}

var (
	rdb               *redis.Client
	ctx               = context.Background()
	userServiceURL    string
	productServiceURL string
)

func main() {
	redisURL := os.Getenv("REDIS_URL")
	if redisURL == "" {
		redisURL = "redis://redis:6379/0"
	}

	opt, err := redis.ParseURL(redisURL)
	if err != nil {
		log.Fatalf("error parsing redis url: %v", err)
	}
	rdb = redis.NewClient(opt)

	userServiceURL = os.Getenv("USER_SERVICE_URL")
	if userServiceURL == "" {
		userServiceURL = "http://user-service:5001"
	}
	productServiceURL = os.Getenv("PRODUCT_SERVICE_URL")
	if productServiceURL == "" {
		productServiceURL = "http://product-service:5002"
	}

	r := chi.NewRouter()
	r.Get("/health", healthHandler)
	r.Post("/orders", createOrderHandler)
	r.Get("/orders/{id}", getOrderHandler)

	addr := ":5003"
	log.Printf("order-service running on %s", addr)
	if err := http.ListenAndServe(addr, r); err != nil {
		log.Fatal(err)
	}
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	writeJSON(w, http.StatusOK, map[string]string{
		"status":  "ok",
		"service": "order-service",
	})
}

func createOrderHandler(w http.ResponseWriter, r *http.Request) {
	var o Order
	if err := json.NewDecoder(r.Body).Decode(&o); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid json"})
		return
	}
	if o.ID == "" || o.UserID == "" || o.ProductID == "" {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "fields 'id', 'user_id' and 'product_id' are required"})
		return
	}

	// 1. Validar usuario
	if !checkExists(fmt.Sprintf("%s/users/%s", userServiceURL, o.UserID)) {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "user does not exist"})
		return
	}

	// 2. Validar producto
	if !checkExists(fmt.Sprintf("%s/products/%s", productServiceURL, o.ProductID)) {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "product does not exist"})
		return
	}

	// 3. Guardar orden en Redis
	o.Status = "CREATED"
	key := "order:" + o.ID
	data, err := json.Marshal(o)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": "internal error"})
		return
	}

	if err := rdb.Set(ctx, key, data, 0).Err(); err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": "redis error"})
		return
	}

	writeJSON(w, http.StatusCreated, o)
}

func getOrderHandler(w http.ResponseWriter, r *http.Request) {
	id := chi.URLParam(r, "id")
	key := "order:" + id

	raw, err := rdb.Get(ctx, key).Bytes()
	if err == redis.Nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "order not found"})
		return
	} else if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": "redis error"})
		return
	}

	var o Order
	if err := json.Unmarshal(raw, &o); err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": "decode error"})
		return
	}

	writeJSON(w, http.StatusOK, o)
}

func checkExists(url string) bool {
	resp, err := http.Get(url)
	if err != nil {
		log.Printf("error calling %s: %v", url, err)
		return false
	}
	defer resp.Body.Close()
	_, _ = io.ReadAll(resp.Body)
	return resp.StatusCode == http.StatusOK
}

func writeJSON(w http.ResponseWriter, status int, v any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(v)
}

