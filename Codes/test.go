package main

import (
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

func Sin(degrees float64) (float64, error) {
	radians := degrees * math.Pi / 180
	return math.Sin(radians), nil
}

func Tan(degrees float64) (float64, error) {
//todo: while input type is Tan
}

func ArcSin(x float64) (float64, error) {
//todo: while input type is ArcSin
}

func Arctan(x float64) (float64, error) {
//todo: while input type is ArcTan
}

func main() {
	if len(os.Args) < 3 {
		fmt.Println("使用方法: trigcalc <操作> <数值>")
		fmt.Println("支持的操作: sin, tan, arcsin, arctan")
		return
	}

	operation := strings.ToLower(os.Args[1])
	input := os.Args[2]

	value, err := strconv.ParseFloat(input, 64)
	if err != nil {
		fmt.Printf("无效的数值输入：%s\n", input)
		return
	}

	var result float64
	var calcErr error

	switch operation {
	case "sin":
		result, calcErr = Sin(value)
	case "tan":
		result, calcErr = Tan(value)
	case "arcsin":
		result, calcErr = ArcSin(value)
	case "arctan":
		result, calcErr = Arctan(value)
	default:
		fmt.Printf("不支持的操作：%s\n", operation)
		return
	}

	if calcErr != nil {
		fmt.Printf("错误：%v\n", calcErr)
	} else {
		fmt.Printf("结果：%.4f\n", result)
	}
}
