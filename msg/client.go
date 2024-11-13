package msg

import (
	"net/http"
)

type MsgClient interface {
	Validate(*http.Request) bool
	SendMessage(string, string)
	ReceiveText(string, string)
	ReceiveImage(string, string, string)
}
