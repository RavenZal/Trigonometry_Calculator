from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
import logging
from socketserver import ThreadingMixIn
from urllib.parse import urlparse

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 使用线程混合类支持并发处理
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """支持多线程的HTTP服务器"""
    pass

class CalculationHandler(BaseHTTPRequestHandler):
    # Go中间层服务配置
    GO_SERVICE_URL = "http://go-middleware:8081/calculate"  # 根据实际Go服务地址修改
    REQUEST_TIMEOUT = 3  # 请求超时时间(秒)
    
    def _set_response(self, status_code=200, content_type='application/json'):
        """设置HTTP响应头"""
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()
    
    def _validate_request(self, data):
        """验证请求数据"""
        # 检查必需字段
        required_fields = ['angle', 'unit', 'function']
        if not all(key in data for key in required_fields):
            missing = [field for field in required_fields if field not in data]
            return False, {"error": f"Missing required fields: {', '.join(missing)}"}
        
        # 检查角度是否为数字
        try:
            angle = float(data['angle'])
        except (ValueError, TypeError):
            return False, {"error": "Angle must be a number"}
        
        # 检查单位是否合法
        if data['unit'] not in ['degree', 'radian']:
            return False, {"error": "Invalid unit. Must be 'degree' or 'radian'"}
        
        # 检查三角函数类型是否合法
        valid_functions = ['sin', 'cos', 'tan']
        if data['function'] not in valid_functions:
            return False, {"error": f"Invalid function. Must be one of {', '.join(valid_functions)}"}
        
        return True, None
    
    def _forward_to_go_service(self, data):
        """将请求转发给Go中间层服务"""
        try:
            response = requests.post(
                self.GO_SERVICE_URL,
                json=data,
                timeout=self.REQUEST_TIMEOUT
            )
            response.raise_for_status()  # 检查HTTP错误状态
            return response.json()
        except requests.exceptions.Timeout:
            logger.error("Request to Go service timed out")
            return {"error": "Go service timeout"}
        except requests.exceptions.ConnectionError:
            logger.error("Failed to connect to Go service")
            return {"error": "Cannot connect to Go service"}
        except requests.exceptions.RequestException as e:
            logger.error(f"Go service request failed: {str(e)}")
            return {"error": f"Go service error: {str(e)}"}
        except json.JSONDecodeError:
            logger.error("Invalid JSON response from Go service")
            return {"error": "Invalid response from Go service"}
    
    def do_POST(self):
        """处理POST请求"""
        # 只处理/calculate路径
        if self.path != '/calculate':
            self._set_response(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode())
            return
            
        # 检查请求体长度
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            self._set_response(400)
            self.wfile.write(json.dumps({"error": "Empty request body"}).encode())
            return
            
        try:
            # 解析JSON请求体
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
        except json.JSONDecodeError:
            self._set_response(400)
            self.wfile.write(json.dumps({"error": "Invalid JSON format"}).encode())
            return
            
        # 验证请求数据
        is_valid, error_response = self._validate_request(data)
        if not is_valid:
            self._set_response(400)
            self.wfile.write(json.dumps(error_response).encode())
            return
            
        # 转发请求到Go服务
        go_response = self._forward_to_go_service(data)
        
        # 处理Go服务的响应
        if 'error' in go_response:
            self._set_response(500)
            self.wfile.write(json.dumps({"error": go_response['error']}).encode())
        else:
            self._set_response(200)
            self.wfile.write(json.dumps({"result": go_response.get('result')}).encode())

def run_server(port=8080):
    """启动HTTP服务器"""
    server_address = ('', port)
    httpd = ThreadedHTTPServer(server_address, CalculationHandler)
    logger.info(f'Starting proxy server on port {port}...')
    logger.info(f'Forwarding requests to: {CalculationHandler.GO_SERVICE_URL}')
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
    finally:
        httpd.server_close()
        logger.info('Proxy server stopped')

if __name__ == '__main__':
    run_server()
