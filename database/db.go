package database

import (
	"github.com/charmbracelet/log"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

var db *gorm.DB

func GetDb() *gorm.DB {
	if db == nil {
		log.Fatal("Database is opened.")
	}
	return db
}

func Open(name string) *gorm.DB {
	log.Info("Opening", "db_name", name)
	db, err := gorm.Open(sqlite.Open(name), &gorm.Config{
		QueryFields: true,
	})
	if err != nil {
		log.Fatal("Unable to open database", "name", name, "err", err)
	}
	return db
}
