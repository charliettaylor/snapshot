package config

import (
	"errors"
	"fmt"
	"os"
	"strings"

	"github.com/charmbracelet/log"
	"github.com/joho/godotenv"
)

type Environment string

const (
	PROD Environment = "PROD"
	BETA Environment = "BETA"
	DEV  Environment = "DEV"

	envName               = "environment"
	twilioAccountSidName  = "twilio_account_sid"
	twilioAuthTokenName   = "twilio_auth_token"
	twilioPhoneNumberName = "twilio_phone_number"
	dbFileName            = "db_name"
	hashSecretName        = "hash_secret"
	adminPassName         = "admin_pass"
	betaCodeName          = "beta_code"
	betaAllowlistName     = "beta_allowlist"

	missingErr        = "Missing environment variable: `%s`. "
	missingInvalidErr = "Missing or invalid environment variable: `%s`. "
)

type TwilioConfig struct {
	AccountSid  string
	AuthToken   string
	PhoneNumber string
}

var Env Environment
var Twilio TwilioConfig
var DbName string
var HashSecret string
var AdminPass string
var BetaCode string
var BetaAllowlist []string

func Load() error {
	log.Info("Loading environment variables from .env")

	err := godotenv.Load()
	if err != nil {
		log.Fatal(err)
	}

	environ := strings.ToUpper(os.Getenv(envName))
	if environ == string(PROD) {
		Env = PROD
	} else if environ == string(BETA) {
		Env = BETA
	} else if environ == string(DEV) {
		Env = DEV
	} else {
		return errors.New(fmt.Sprintf(missingInvalidErr, envName))
	}

	Twilio = TwilioConfig{
		os.Getenv(twilioAccountSidName),
		os.Getenv(twilioAuthTokenName),
		os.Getenv(twilioPhoneNumberName),
	}

	DbName = os.Getenv(dbFileName)
	if len(DbName) < 4 || DbName[len(DbName)-3:] != ".db" {
		return errors.New(fmt.Sprintf(missingInvalidErr, dbFileName) + "Format: `<name>.db`")
	}

	HashSecret = os.Getenv(hashSecretName)
	if HashSecret == "" {
		return errors.New(fmt.Sprintf(missingErr, hashSecretName))
	}

	AdminPass = os.Getenv(adminPassName)
	if len(AdminPass) < 5 {
		return errors.New(fmt.Sprintf(missingInvalidErr, adminPassName) + "Minimum length: 5")
	}

	BetaCode = os.Getenv(betaCodeName)
	if len(BetaCode) < 5 {
		return errors.New(fmt.Sprintf(missingInvalidErr, betaCodeName) + "Minimum length: 5")
	}

	BetaAllowlist = strings.Split(os.Getenv(betaAllowlistName), ",")

	log.Info("Successfully loaded environment variables")
	return nil
}
