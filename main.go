package main

import (
	"net/http"

	"snapshot/api"
	"snapshot/config"
	"snapshot/database"
	"snapshot/msg"

	"github.com/charmbracelet/log"
)

const (
	ServiceName = "Snapshot"
	port        = ":8080"
)

func main() {

	// log.SetReportCaller(true)
	log.Infof("Starting %s", ServiceName)

	// Load .env environment variables
	err := config.Load()
	if err != nil {
		log.Fatal(err)
	}

	database.Open(config.DbName)

	smsClient := msg.NewSmsClient()

	api.RegisterEndpoints(smsClient)

	if config.IsShell {
		log.Info("Running in shell mode")
		ShellInput()
	}

	log.Info("Listening on", "port", port)
	log.Fatal(http.ListenAndServe(port, nil))
}
