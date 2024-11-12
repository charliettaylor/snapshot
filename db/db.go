package db

import (
	"database/sql"

	"github.com/charmbracelet/log"
	_ "github.com/mattn/go-sqlite3"
)

const (
	driver = "sqlite3"
)

type DatabaseController struct {
	db *sql.DB
}

func Open(name string) *DatabaseController {
	log.Info("Opening", "db_name", name)
	db, err := sql.Open(driver, name)
	if err != nil {
		log.Fatal("Unable to open database", "driver", driver, "name", name, "err", err)
	}
	return &DatabaseController{
		db,
	}
}

func (c *DatabaseController) Close() {
	c.db.Close()
}
