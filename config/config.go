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

	// Environment variables in .env
	envKey               = "environment"
	twilioAccountSidKey  = "twilio_account_sid"
	twilioAuthTokenKey   = "twilio_auth_token"
	twilioPhoneNumberKey = "twilio_phone_number"
	dbNameKey            = "db_name"
	hashSecretKey        = "hash_secret"
	adminPassKey         = "admin_pass"
	betaCodeKey          = "beta_code"
	betaAllowlistKey     = "beta_allowlist"

	// Other environment variables
	debugKey      = "DEBUG"
	shellKey      = "SHELL"
	inMemoryDbKey = "IN_MEMORY_DB"

	// format strings
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

var IsDebug bool
var IsInMemoryDb bool
var IsShell bool

func Load() error {
	log.Info("Loading environment variables from .env")

	err := godotenv.Load()
	if err != nil {
		log.Fatal(err)
	}

	IsDebug = os.Getenv(debugKey) == "1"
	if IsDebug {
		log.SetLevel(log.DebugLevel)
	}
	log.Debug("", debugKey, IsDebug)

	IsShell = os.Getenv(shellKey) == "1"
	log.Debug("", shellKey, IsShell)

	IsInMemoryDb = os.Getenv(inMemoryDbKey) == "1"
	log.Debug("", inMemoryDbKey, IsInMemoryDb)

	environ := strings.ToUpper(os.Getenv(envKey))
	if environ == string(PROD) {
		Env = PROD
	} else if environ == string(BETA) {
		Env = BETA
	} else if environ == string(DEV) {
		Env = DEV
	} else {
		return errors.New(fmt.Sprintf(missingInvalidErr, envKey))
	}
	log.Debug("", envKey, Env)

	Twilio = TwilioConfig{
		os.Getenv(twilioAccountSidKey),
		os.Getenv(twilioAuthTokenKey),
		os.Getenv(twilioPhoneNumberKey),
	}

	DbName = os.Getenv(dbNameKey)
	if len(DbName) < 4 || DbName[len(DbName)-3:] != ".db" {
		return errors.New(fmt.Sprintf(missingInvalidErr, dbNameKey) + "Format: `<name>.db`")
	}
	log.Debug("", dbNameKey, DbName)

	HashSecret = os.Getenv(hashSecretKey)
	if HashSecret == "" {
		return errors.New(fmt.Sprintf(missingErr, hashSecretKey))
	}
	log.Debug("", hashSecretKey, "set")

	AdminPass = os.Getenv(adminPassKey)
	if len(AdminPass) < 5 {
		return errors.New(fmt.Sprintf(missingInvalidErr, adminPassKey) + "Minimum length: 5")
	}
	log.Debug("", adminPassKey, "set")

	BetaCode = os.Getenv(betaCodeKey)
	if len(BetaCode) < 5 {
		return errors.New(fmt.Sprintf(missingInvalidErr, betaCodeKey) + "Minimum length: 5")
	}
	log.Debug("", betaCodeKey, BetaCode)

	BetaAllowlist = strings.Split(os.Getenv(betaAllowlistKey), ",")
	log.Debug("", betaAllowlistKey, BetaAllowlist)

	log.Info("Successfully loaded environment variables")
	return nil
}
