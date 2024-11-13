package msg

import (
	"net/http"

	"github.com/charmbracelet/log"
)

type ShellClient struct{}

func NewShellClient() *ShellClient {
	return &ShellClient{}
}

func (c *ShellClient) SendMessage(to string, text string) {
	log.Info("SendMessage", "to", to, "text", text)
}

func (c *ShellClient) ReceiveText(from string, text string) {
	log.Info("ReceiveText", "from", from, "mediaUrl", text)
}

func (c *ShellClient) ReceiveImage(from string, contentType string, mediaUrl string) {
	log.Info("ReceiveImage", "from", from, "mediaUrl", mediaUrl)
}

func (c *ShellClient) Validate(req *http.Request) bool {
	header := req.Header.Get("X-Shell-Signature")
	if header == "" {
		return false
	}
	return true
}
