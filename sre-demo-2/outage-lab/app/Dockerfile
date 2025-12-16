FROM golang:1.22-alpine AS build
WORKDIR /app
COPY go.mod .
COPY main.go .
RUN go build -o outage-app

FROM alpine:3.19
COPY --from=build /app/outage-app /outage-app
EXPOSE 8080
ENTRYPOINT ["/outage-app"]
