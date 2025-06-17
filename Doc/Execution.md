## **运行流程**
### **步骤1：启动Matlab计算服务器**
1. 在Matlab中运行 `startServer()` 函数。
2. 确保Matlab监听TCP端口 `12345`，控制台显示 `Matlab Server Started.`。

### **步骤2：启动Go中间层**
1. 保存Go代码为 `main.go`。
2. 在终端中执行以下命令：
   ```bash
   go run main.go
   ```
3. 确保中间层监听HTTP端口 `8080`，日志显示 `Go中间层启动，监听 :8080`。

### **步骤3：运行Python客户端**
1. 执行Python客户端代码：
   ```bash
   python client.py
   ```
2. 按照提示输入参数，例如：
   ```text
   Enter angle: 45
   Degree or Radian? degree
   Function (sin/cos/tan): sin
   ```
3. 客户端将返回计算结果：
   ```text
   Result: 0.70710678
   ```
## **验证示例**
| 输入参数               | 预期输出       |
|------------------------|----------------|
| `angle=45, unit=degree, function=sin` | `Result: 0.70710678` |
| `angle=π/4, unit=radian, function=cos` | `Result: 0.70710678` |
| `angle=0, unit=degree, function=tan` | `Result: 0.0` |
