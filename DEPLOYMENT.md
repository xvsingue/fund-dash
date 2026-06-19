# FundMaster Pro - 部署和最佳实践指南

## 快速开始

### 开发环境

```bash
# 1. 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行应用
python app.py
```

访问 http://localhost:5000

## 生产部署

### 使用 Gunicorn + Nginx

```bash
# 安装生产级依赖
pip install gunicorn

# 运行应用（多进程）
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 环境配置

1. 复制 `.env.example` 为 `.env`
2. 根据需要修改配置值
3. 加载环境变量（生产环境使用密钥管理服务）

## 监控和日志

所有异常错误会自动记录到标准输出。建议配置：
- 日志收集工具（ELK, Splunk）
- 错误跟踪服务（Sentry）
- APM 工具（New Relic, DataDog）

## 性能最优化

### 后端
- ✅ 内存缓存机制（可升级为 Redis）
- ✅ 请求超时设置（5秒）
- ✅ 自适应延迟（防止频繁爬虫）

### 前端
- ✅ 本地存储缓存（localStorage）
- ✅ 异步 fetch 请求
- ✅ 表格虚拟化（当数据过多）

### 建议升级

1. **Redis 缓存** - 用于多实例部署
```python
import redis
redis_client = redis.Redis(host='localhost', port=6379)
```

2. **数据库** - SQLAlchemy + PostgreSQL
```python
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
```

3. **消息队列** - Celery + RabbitMQ
用于处理长运行的爬虫任务

## 安全建议

- ✅ 输入验证已实现
- ✅ XSS 防护已实现（模板自动转义）
- 🔄 添加 CORS 配置
- 🔄 实施 Rate Limiting
- 🔄 启用 HTTPS

## 测试

添加测试文件 `test_app.py`：

```python
import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_health(self):
        response = self.app.get('/health')
        self.assertEqual(response.json['status'], 'ok')

if __name__ == '__main__':
    unittest.main()
```

运行测试：
```bash
python -m unittest test_app.py
```

## 故障排查

### 问题：基金数据总是显示 "查询中..."
- 检查网络连接
- 查看应用日志：`grep "ERROR" <logfile>`
- 检查外部 API 是否可访问

### 问题：缓存不更新
- 检查缓存过期时间配置
- 清除浏览器 localStorage：`localStorage.clear()`
- 检查服务器时间同步

### 问题：性能缓慢
- 增加缓存时间（在准确性允许的范围内）
- 使用 Redis 替代内存缓存
- 添加 CDN 用于静态资源

## 数据隐私

本应用仅在本地存储用户数据（localStorage），不向服务器发送个人信息。
所有外部 API 调用仅用于获取公开市场数据。
