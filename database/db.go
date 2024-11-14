package database

import (
	"snapshot/config"

	"github.com/charmbracelet/log"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

const (
	inMemoryDbName = "file::memory:?cache=shared"
)

var db *gorm.DB = nil

func GetDb() *gorm.DB {
	if db == nil {
		return Open("snapshot.db")
	}

	return db
}

func Open(name string) *gorm.DB {
	if config.IsInMemoryDb {
		name = inMemoryDbName
	}
	log.Info("Opening", "db_name", name)
	db, err := gorm.Open(sqlite.Open(name), &gorm.Config{})
	if err != nil {
		log.Fatal("Unable to open database", "name", name, "err", err)
	}
	return db
}
