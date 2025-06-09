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
	var req CalculationRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		sendError(w, "无效的请求格式", http.StatusBadRequest)
		return
	}

	if req.Function == "" || (req.Unit != "degree" && req.Unit != "radian") {
		sendError(w, "参数不合法", http.StatusBadRequest)
		return
	}

	matlabRequest := fmt.Sprintf("%s,%.8f,%s", strings.ToLower(req.Function), req.Angle, req.Unit)

	conn, err := net.Dial("tcp", "localhost:12345")
	if err != nil {
		sendError(w, "无法连接到Matlab服务器", http.StatusInternalServerError)
		return
	}
	defer conn.Close()

	if _, err = fmt.Fprintln(conn, matlabRequest); err != nil {
		sendError(w, "请求发送失败", http.StatusInternalServerError)
		return
	}

	resultBytes, err := io.ReadAll(conn)
	if err != nil {
		sendError(w, "结果读取失败", http.StatusInternalServerError)
		return
	}

	var result float64
	if _, err = fmt.Sscanf(string(resultBytes), "%f", &result); err != nil {
		sendError(w, "无效的计算结果", http.StatusInternalServerError)
		return
	}

	sendSuccess(w, result)
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
