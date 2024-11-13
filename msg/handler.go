package msg

import (
	"snapshot/config"
	"snapshot/database"
	"strings"

	"github.com/charmbracelet/log"
)

func HandleText(from string, text string) {
	log.Info("HandleText", "from", from, "text", text)

	if strings.Contains(text, config.AdminPass) {
		handleAdminMessage(from, text)
		return
	}

	var reg database.Registration
	database.GetDb().Where(database.Registration{Phone: &from}).FirstOrCreate(&reg)
}

func HandleImage(from string, contentType string, mediaUrl string) {
	log.Info("HandleImage", "from", from, "url", mediaUrl)
}

func handleAdminMessage(from string, text string) {
	log.Info("HandleAdminMessage", "from", from, "text", text)
}
