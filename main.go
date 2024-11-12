package main

import (
	"net/http"
	"os"
	"strings"

	"snapshot/db"
	"snapshot/sms"

	"github.com/charmbracelet/log"
	"github.com/joho/godotenv"
)

const (
	port = ":8080"
)

func main() {

	log.Info("Starting Snapshot service")

	// Load .env environment variables
	err := godotenv.Load()
	if err != nil {
		log.Fatal(err)
	}

	dbName := os.Getenv("db_name")
	db := db.Open(dbName)
	defer db.Close()

	smsClient := sms.NewClient()

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, "./static/index.html")
	})

	http.HandleFunc("/sms", func(w http.ResponseWriter, r *http.Request) {

		err := r.ParseForm()
		if err != nil {
			http.Error(w, "Unable to parse request parameters", 400)
		}

		if !smsClient.Validate(r) {
			http.Error(w, "Failed to validate Twilio signature", 400)
		}

		from := r.Form.Get("From")
		body := r.Form.Get("Body")
		contentType := r.Form.Get("MediaContentType0")
		mediaUrl := r.Form.Get("MediaUrl0")
		if strings.Contains(contentType, "image") && mediaUrl != "" {
			smsClient.HandleImage(from, contentType, mediaUrl)
		} else {
			smsClient.HandleMessage(from, body)
		}
	})

	log.Info("Listening on", "port", port)
	log.Fatal(http.ListenAndServe(port, nil))
}
