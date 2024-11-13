package msg

import (
	"encoding/json"
	"net/http"

	"github.com/charmbracelet/log"
	"github.com/twilio/twilio-go"
	twilioClient "github.com/twilio/twilio-go/client"
	twilioApi "github.com/twilio/twilio-go/rest/api/v2010"

	"snapshot/config"
)

type SmsClient struct {
	twilioClient     *twilio.RestClient
	Account          Account
	requestValidator twilioClient.RequestValidator
}

type Account struct {
	AccountSid  string
	AuthToken   string
	PhoneNumber string
}

func NewSmsClient() *SmsClient {

	account := Account{
		config.Twilio.AccountSid,
		config.Twilio.AuthToken,
		config.Twilio.PhoneNumber,
	}

	client := twilio.NewRestClientWithParams(twilio.ClientParams{
		Username: account.AccountSid,
		Password: account.AuthToken,
	})

	return &SmsClient{
		client,
		account,
		twilioClient.NewRequestValidator(account.AuthToken),
	}
}

func (c *SmsClient) SendMessage(to string, text string) {
	log.Info("SmsClient SendMessage", "to", to, "text", text)

	params := &twilioApi.CreateMessageParams{}
	params.SetTo(to)
	params.SetFrom(c.Account.PhoneNumber)
	params.SetBody(text)

	resp, err := c.twilioClient.Api.CreateMessage(params)
	if err != nil {
		log.Error("Error sending SMS message: " + err.Error())
	} else {
		response, _ := json.MarshalIndent(*resp, "", "  ")
		log.Debug(string(response))
	}
}

func (c *SmsClient) Validate(req *http.Request) bool {
	header := req.Header.Get("X-Twilio-Signature")

	params := make(map[string]string)
	for key, values := range req.Form {
		if len(values) > 0 {
			params[key] = values[0]
		}
	}
	return c.requestValidator.Validate(req.URL.String(), params, header)
}

func (c *SmsClient) ReceiveText(from string, text string) {
	log.Info("HandleMessage", "from", from, "text", text)
	HandleText(from, text)
}

func (c *SmsClient) ReceiveImage(from string, contentType string, mediaUrl string) {
	log.Info("HandleImage", "from", from, "mediaUrl", mediaUrl)
}
