// Settlement notifier. Internal tooling.
//
// Findings map to socket-basics' DEFAULT go_enabled_rules:
//
//	go-hardcoded-credentials
//	go-sql-format-string
//	go-bind-all-interfaces
//	go-ssh-insecure-ignore-host-key
package main

import (
	"database/sql"
	"fmt"
	"log"
	"net"

	"golang.org/x/crypto/ssh"
)

// go-hardcoded-credentials
const (
	notifierDBPassword = "n0tif1er-svc-2024"
	sftpPassword       = "contoso-sftp-batch"
)

// go-sql-format-string
func settlementsByBatch(db *sql.DB, batchID string) (*sql.Rows, error) {
	q := fmt.Sprintf("SELECT id, merchant_id FROM settlements WHERE batch_id = '%s'", batchID)
	return db.Query(q)
}

// go-ssh-insecure-ignore-host-key
func sftpClient(host string) (*ssh.Client, error) {
	cfg := &ssh.ClientConfig{
		User:            "batch",
		Auth:            []ssh.AuthMethod{ssh.Password(sftpPassword)},
		HostKeyCallback: ssh.InsecureIgnoreHostKey(),
	}
	return ssh.Dial("tcp", host+":22", cfg)
}

// go-bind-all-interfaces
func serveAdmin() {
	ln, err := net.Listen("tcp", "0.0.0.0:9090")
	if err != nil {
		log.Fatal(err)
	}
	defer ln.Close()
	log.Println("admin listener on 0.0.0.0:9090")
}

func main() {
	log.Println("notifier starting, db pw len", len(notifierDBPassword))
	serveAdmin()
}
