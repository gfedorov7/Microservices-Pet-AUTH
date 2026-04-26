package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"github.com/joho/godotenv"
	"github.com/segmentio/kafka-go"
	"io"
	"net/http"
	"os"
)

const BatchSize int = 3

type Event struct {
	UserID          int    `json:"user_id"`
	AnonymousUserId string `json:"anonymous_user_id"`
	Type            string `json:"type"`
	Timestamp       string `json:"timestamp"`
	UserAgent       string `json:"user_agent"`
	IP              string `json:"ip"`
}

func InsertToClickHouse(batch []Event, connectionString string) {
	var buf bytes.Buffer

	for _, e := range batch {
		line, _ := json.Marshal(e)
		buf.Write(line)
		buf.WriteByte('\n')
	}

	resp, err := http.Post(
		connectionString+"?query=INSERT%20INTO%20auth.user_events%20FORMAT%20JSONEachRow",
		"application/json",
		&buf,
	)
	if err != nil {
		fmt.Println("insert error:", err)
		return
	}
	defer resp.Body.Close()

	bodyBytes, _ := io.ReadAll(resp.Body)
	fmt.Println("STATUS:", resp.Status)
	fmt.Println("BODY:", string(bodyBytes))
}

func main() {
	err := godotenv.Load(".env")
	if err != nil {
		fmt.Println("No .env file found")
		return
	}

	connectionString := os.Getenv("CLICKHOUSE_CONNECTION")

	reader := kafka.NewReader(kafka.ReaderConfig{
		Brokers: []string{"kafka:9092"},
		Topic:   "auth",
	})
	defer reader.Close()

	fmt.Println("Start consuming...")
	var batch []Event
	for {
		msg, err := reader.ReadMessage(context.Background())
		if err != nil {
			fmt.Println(err)
			return
		}

		var e Event
		err = json.Unmarshal(msg.Value, &e)
		if err != nil {
			fmt.Println(err)
			return
		}

		batch = append(batch, e)
		fmt.Println(e)
		fmt.Println(len(batch))

		if len(batch) >= BatchSize {
			go InsertToClickHouse(batch, connectionString)
			batch = batch[:0]
		}
	}
}
