package main

import (
	"os"
	"ructf-radio-sploit/auth"
)

func main() {
	secret := os.Args[1]
	user := os.Args[2]

	err := auth.InitAuth(secret)
	if err != nil {
		panic(err)
	}
	payload := map[string]string{"user": user}
	token := auth.Encode(&payload)
	println(token)
}
