package api

import (
	"net/http"
	"slices"
	"strings"

	"snapshot/config"
	"snapshot/msg"
)

const (
	formFrom            = "From"
	formBody            = "Body"
	formContentType     = "MediaContentType0"
	formMediaUrl        = "MediaUrl0"
	acceptedContentType = "image"
)

func RegisterEndpoints(msgClient msg.MsgClient) {
	betaQueue := map[string]bool{}

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, "./static/index.html")
	})

	http.HandleFunc("/sms", func(w http.ResponseWriter, r *http.Request) {

		err := r.ParseForm()
		if err != nil {
			http.Error(w, "Unable to parse request parameters", 400)
		}

		if !msgClient.Validate(r) {
			http.Error(w, "Failed to validate request signature", 400)
		}

		from := r.Form.Get(formFrom)
		body := r.Form.Get(formBody)
		contentType := r.Form.Get(formContentType)
		mediaUrl := r.Form.Get(formMediaUrl)
		if strings.Contains(contentType, acceptedContentType) && mediaUrl != "" {
			msgClient.ReceiveImage(from, contentType, mediaUrl)
			return
		}

		if body == config.BetaCode {
			betaQueue[from] = true
			return
		}

		if strings.Contains(body, config.BetaCode) {
			body = body[len(config.BetaCode)+1:]
			betaQueue[from] = true
		}

		if betaQueue[from] {
			if !slices.Contains(config.BetaAllowlist, from) {
				http.Error(w, "Not allowlisted for Beta env", 401)
			}
			if config.Env == config.PROD {
				http.Error(w, "Beta code detected", 501)
				delete(betaQueue, from)
				return
			}
		}

		msgClient.ReceiveText(from, body)
	})
}
