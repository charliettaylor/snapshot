package msg

import (
	"net/http"

	"github.com/charmbracelet/log"
	"gorm.io/gorm"
)

type TestClient struct {
	db *gorm.DB
}

func NewTestClient(db *gorm.DB) *TestClient {
	return &TestClient{
		db,
	}
}

func (c *TestClient) SendMessage(to string, text string) {
	log.Info("TestClient SendMessage", "to", to, "text", text)
}

func (c *TestClient) ReceiveText(from string, text string) {
	log.Info("TestClient HandleImage", "from", from, "mediaUrl", text)
}

func (c *TestClient) ReceiveImage(from string, contentType string, mediaUrl string) {
	log.Info("TestClient HandleImage", "from", from, "mediaUrl", mediaUrl)
}

func (c *TestClient) Validate(*http.Request) bool {
	return true
}
