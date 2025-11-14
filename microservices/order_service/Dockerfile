FROM golang:1.23-alpine AS builder

WORKDIR /app

COPY go.mod ./
RUN go mod tidy

COPY . .
RUN go build -o order_service main.go

FROM alpine:3.20

WORKDIR /app

COPY --from=builder /app/order_service .

EXPOSE 5003

CMD ["./order_service"]

