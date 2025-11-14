const express = require("express");
const { createClient } = require("redis");

const app = express();
app.use(express.json());

const REDIS_URL = process.env.REDIS_URL || "redis://redis:6379/0";
const redisClient = createClient({ url: REDIS_URL });

redisClient.on("error", (err) => {
  console.error("Redis error:", err);
});

(async () => {
  await redisClient.connect();
})();

app.get("/api/products/health", (req, res) => {
  res.json({ status: "ok", service: "product-service" });
});

app.post("/api/products", async (req, res) => {
  const { id, name, price } = req.body;

  if (!id || !name) {
    return res
      .status(400)
      .json({ error: "fields 'id' and 'name' are required" });
  }

  const key = `product:${id}`;
  const product = { id, name, price: price || 0 };

  await redisClient.set(key, JSON.stringify(product));

  res.status(201).json({ message: "product created", product });
});

app.get("/api/products/:id", async (req, res) => {
  const productId = req.params.id;
  const key = `product:${productId}`;

  const raw = await redisClient.get(key);
  if (!raw) {
    return res.status(404).json({ error: "product not found" });
  }

  const product = JSON.parse(raw);
  res.json(product);
});

const PORT = process.env.PORT || 5002;
app.listen(PORT, () => {
  console.log(`product-service running on port ${PORT}`);
});

