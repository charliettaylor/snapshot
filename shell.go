package main

import (
	"fmt"

	"snapshot/msg"
)

func ShellInput() {
	shellClient := msg.NewShellClient()

	var input string

	for input != "q" {
		fmt.Scan(&input)
		shellClient.ReceiveText("9517518340", input)
	}
}
