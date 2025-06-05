package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net"
	"net/http"
	"strings"
)

type CalculationRequest struct {
	Angle    float64 `json:"angle"`
	Unit     string  `json:"unit"`
	Function string  `json:"function"`
}

type CalculationResponse struct {
	Result float64 `json:"result,omitempty"`
	Error  string  `json:"error,omitempty"`
}

func main() {
	http.HandleFunc("/calculate", handleCalculate)
	log.Println("Go中间层启动，监听 :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

func handleCalculate(w http.ResponseWriter, r *http.Request) {
	//todo:请求格式有误
	//todo:参数有误
	//todo:服务器连接失败
	//todo:请求发送失败
	//todo：结果读取失败
	//todo：无效的计算结果
}

func sendSuccess(w http.ResponseWriter, result float64) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(CalculationResponse{Result: result})
}

func sendError(w http.ResponseWriter, msg string, statusCode int) {
        w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(statusCode)
	json.NewEncoder(w).Encode(CalculationResponse{Error: msg})
}
