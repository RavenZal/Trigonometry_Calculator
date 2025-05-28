
---

### **接口定义与协议说明**

#### **1. Python客户端 ↔ Go中间层**
| 项目 | 配置 |
|------|------|
| **协议** | HTTP |
| **端口** | 8080 (Go中间层监听) |
| **接口路径** | `POST /calculate` |
| **请求格式** | JSON |
```json
{
  "angle": 45.0,
  "unit": "degree",  // "degree"或"radian"
  "function": "sin"  // "sin", "cos", "tan"
}
```
| **响应格式** | JSON |
```json
// 成功
{ "result": 0.7071 }

// 失败
{ "error": "Invalid function" }
```

---

#### **2. Go中间层 ↔ Matlab计算服务器**
| 项目 | 配置 |
|------|------|
| **协议** | TCP/IP |
| **端口** | 12345 (Matlab监听) |
| **连接方式** | Go作为TCP客户端，Matlab作为TCP服务器 |
| **请求格式** | 纯文本，逗号分隔 |
```
sin,45.000000,degree
```
| **响应格式** | 纯文本数值 |
```
0.70710678
```

---

### **TCP/IP端口配置表**
| 组件 | 角色 | 协议 | 端口 | 方向 | 说明 |
|------|------|------|------|------|------|
| **Go中间层** | HTTP服务器 | HTTP | 8080 | 入站 | 接收来自Python客户端的请求 |
| **Go中间层** | TCP客户端 | TCP | 12345 | 出站 | 向Matlab服务器发送请求 |
| **Matlab服务器** | TCP服务器 | TCP | 12345 | 入站 | 接收来自Go中间层的计算请求 |

---

### **关键配置说明**
1. **Python客户端**
   - 目标地址：`http://localhost:8080/calculate`
   - 无端口监听（仅作为HTTP客户端）
   ```
   ```

2. **Go中间层**
   - 监听端口：8080 (HTTP)
   - 连接端口：12345 (TCP)
   - 配置示例：
   ```go
   http.ListenAndServe(":8080", nil)  // HTTP监听
   net.Dial("tcp", "localhost:12345") // TCP连接
   ```

3. **Matlab服务器**
   - 监听端口：12345 (TCP)
   - 配置代码：
   ```matlab
   t = tcpip('0.0.0.0', 12345, 'NetworkRole', 'server');
   fopen(t);  // 启动TCP监听
   ```

---

### **防火墙与网络要求**
1. **必需开放端口**：
   - 8080 (Go HTTP服务)
   - 12345 (Matlab TCP服务)

2. **本地测试配置**：
   ```mermaid
   graph LR
   A[Python客户端] -->|HTTP:8080| B[Go中间层]
   B -->|TCP:12345| C[Matlab服务器]
   ```

3. **跨机器部署**：
   - 修改连接地址：
     - Python客户端：`http://<go-server-ip>:8080/calculate`
     - Go中间层：`net.Dial("tcp", "<matlab-server-ip>:12345")`
   - 确保网络策略允许跨机器通信

---

### **协议细节说明**
1. **TCP通信流程**：
   ```mermaid
   sequenceDiagram
   Go中间层->>Matlab服务器: TCP连接建立 (SYN)
   Matlab服务器-->>Go中间层: SYN-ACK
   Go中间层->>Matlab服务器: 请求数据 (sin,45.000000,degree)
   Matlab服务器-->>Go中间层: 响应数据 (0.70710678)
   Go中间层->>Matlab服务器: FIN断开连接
   ```

2. **数据格式要求**：
   - 字段顺序：`函数名,角度值,单位`
   - 数值精度：8位小数
   - 单位限制：仅接受`degree`或`radian`

3. **错误处理**：
   - HTTP错误码：400(参数错误), 500(服务器错误)
   - TCP错误：连接失败返回HTTP 503
   - Matlab计算错误：返回"inf"或"nan"字符串

---

### **配置验证步骤**
1. 验证端口可用性：
   ```bash
   # 检查8080端口
   netstat -tuln | grep 8080
   
   # 检查12345端口
   netstat -tuln | grep 12345
   ```

2. 测试TCP连接：
   ```bash
   telnet localhost 12345
   ```

3. 测试HTTP接口：
   ```bash
   curl -X POST http://localhost:8080/calculate \
   -H "Content-Type: application/json" \
   -d '{"angle":45, "unit":"degree", "function":"sin"}'
   ```
