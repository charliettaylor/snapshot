package sms

import (
	"encoding/json"
	"net/http"
	"os"
	"snapshot/database"
	"strings"

	"github.com/charmbracelet/log"
	"github.com/twilio/twilio-go"
	twilioClient "github.com/twilio/twilio-go/client"
	twilioApi "github.com/twilio/twilio-go/rest/api/v2010"
	"gorm.io/gorm"
)

type Client struct {
	twilioClient     *twilio.RestClient
	Account          Account
	requestValidator twilioClient.RequestValidator
	db               *gorm.DB
}

type Account struct {
	AccountSid  string
	AuthToken   string
	PhoneNumber string
}

func NewClient(db *gorm.DB) *Client {
	accountSid := os.Getenv("twilio_account_sid")
	authToken := os.Getenv("twilio_auth_token")
	phoneNumber := os.Getenv("twilio_phone_number")

	account := Account{
		accountSid, authToken, phoneNumber,
	}

	client := twilio.NewRestClientWithParams(twilio.ClientParams{
		Username: accountSid,
		Password: authToken,
	})

	return &Client{
		client,
		account,
		twilioClient.NewRequestValidator(authToken),
		db,
	}
}

func (c *Client) SendMessage(to string, text string) {
	log.Info("SendMessage")

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

func (c *Client) Validate(req *http.Request) bool {
	header := req.Header.Get("X-Twilio-Signature")

	params := make(map[string]string)
	for key, values := range req.Form {
		if len(values) > 0 {
			params[key] = values[0]
		}
	}
	return c.requestValidator.Validate(req.URL.String(), params, header)
}

func (c *Client) HandleMessage(from string, text string) {
	log.Info("HandleMessage", "from", from, "text", text)

	adminPass := os.Getenv("admin_pass")
	if strings.Contains(text, adminPass) {
		c.handleAdminMessage(from, text)
		return
	}

	var reg database.Registration
	c.db.Where(database.Registration{Phone: &from}).FirstOrCreate(&reg)
}

func (c *Client) HandleImage(from string, contentType string, mediaUrl string) {
	log.Info("HandleImage", "from", from, "mediaUrl", mediaUrl)
}

func (c *Client) handleAdminMessage(from string, text string) {
	log.Info("HandleAdminMessage", "from", from, "text", text)
}
