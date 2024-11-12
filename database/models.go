package database

import (
	"time"

	"gorm.io/gorm"
)

// Should update UserName -> Name
type User struct {
	// gorm.Model
	Username string `gorm:"primaryKey"`
	Phone    string
	Hash     string
	Active   bool
}

type Registration struct {
	gorm.Model
	Phone    *string
	Username string
	State    uint
}

// Should update Prompt -> Text
type Prompt struct {
	gorm.Model
	Prompt string
	Date   time.Time
}

// Should update Prompt -> PromptId
type Pic struct {
	gorm.Model
	Url      string
	Prompt   int
	Username string
}
