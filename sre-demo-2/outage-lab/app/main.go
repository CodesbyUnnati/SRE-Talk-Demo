package main

import (
	"encoding/json"
	"log"
	"math/rand"
	"net/http"
	"os"
	"sync/atomic"
	"time"
)

var regexValidation atomic.Bool
var badSecurityRule atomic.Bool

func loadConfig() {
	data, err := os.ReadFile("/config/config.json")
	if err != nil {
		log.Println("Config read error:", err)
		return
	}

	var cfg map[string]bool
	json.Unmarshal(data, &cfg)

	regexValidation.Store(cfg["regex_validation"])
	badSecurityRule.Store(cfg["bad_security_rule"])

	log.Println("Config reloaded:", cfg)
}

func handler(w http.ResponseWriter, r *http.Request) {

	// CrowdStrike-style: global failure
	if badSecurityRule.Load() {
		http.Error(w, "Blocked by security rule", 500)
		return
	}

	// Cloudflare-style: partial failure
	if regexValidation.Load() && rand.Intn(100) < 30 {
		http.Error(w, "Regex validation failed", 502)
		return
	}

	// AWS-style: dependency latency
	time.Sleep(time.Duration(rand.Intn(400)) * time.Millisecond)

	w.Write([]byte("OK\n"))
}

func main() {
	rand.Seed(time.Now().UnixNano())

	go func() {
		for {
			loadConfig()
			time.Sleep(5 * time.Second)
		}
	}()

	http.HandleFunc("/", handler)
	log.Println("Service running on :8080")
	http.ListenAndServe(":8080", nil)
}
