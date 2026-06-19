# FundMaster 快速开始指南

## 📦 系统要求

- Python 3.7+
- Flask 3.0+
- 现代浏览器

## 🚀 快速启动

### 1. 环境设置

```bash
# 克隆项目（如果需要）
cd FundMaster

# 创建虚拟环境
python3 -m venv .venv

# 激活虚拟环境
source .venv/bin/activate  # macOS/Linux
# 或
.venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 启动应用

```bash
# 开发模式
python app.py

# 生产模式（使用 gunicorn）
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 3. 访问应用

打开浏览器访问: **http://localhost:5000**

---

## 🧪 运行测试

### 后端测试
```bash
# 运行所有单元测试
python -m unittest test_app -v

# 运行特定测试
python -m unittest test_app.TestFundMasterApp.test_01_index_page
```

### 集成测试
```bash
# 启动应用后运行集成测试
python integration_test.py
```

---

## 📋 核心功能

### 1. 查询基金行情
```
GET /api/fund/<codes>
```
- 查询一个或多个基金的最新行情
- 参数: 基金代码 (6位数字，逗号分隔)
- 示例: `/api/fund/001001,110022`

### 2. 查询基金重持股
```
GET /api/stocks/<code>
```
- 查询基金的前10只重持股票
- 参数: 基金代码 (6位数字)
- 示例: `/api/stocks/001001`

### 3. 健康检查
```
GET /health
```
- 检查服务状态
- 返回: `{"status": "ok"}`

### 4. 清除缓存
```
POST /api/cache/clear
```
- 手动清除所有缓存
- 返回: `{"status": "ok", "message": "Cache cleared"}`

---

## ⚙️ 配置

### 环境变量

创建 `.env` 文件（参考 `.env.example`）：

```bash
# 日志级别 (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO

# Flask 调试模式
FLASK_DEBUG=False

# 缓存过期时间 (秒)
CACHE_EXPIRE_MARKET=300      # 市场数据: 5分钟
CACHE_EXPIRE_STOCK=3600       # 库存数据: 1小时

# API 超时
FUND_API_TIMEOUT=5
STOCK_API_TIMEOUT=5

# 网络重试
REQUEST_RETRIES=3
BACKOFF_FACTOR=0.5
```

---

## 📊 使用示例

### 前端使用

1. **添加基金**
   - 点击 "➕ 添加" 按钮
   - 输入基金代码 (6位数字)
   - 输入持仓份额
   - 输入买入成本（可选）
   - 保存

2. **刷新行情**
   - 点击 "🔄 刷新" 按钮
   - 查看实时行情和盈亏

3. **查看深度穿透**
   - 点击 "🔍 开启深度穿透"
   - 查看持仓股票权重

4. **删除基金**
   - 点击表格右侧的 "×" 按钮
   - 确认删除

### API 调用

```bash
# 查询基金行情
curl http://localhost:5000/api/fund/001001,110022

# 查询基金持股
curl http://localhost:5000/api/stocks/001001

# 清除缓存
curl -X POST http://localhost:5000/api/cache/clear

# 健康检查
curl http://localhost:5000/health
```

---

## 🐛 常见问题

### Q: 基金数据显示 "查询中..."

**A**: 这是正常的，说明数据正在加载。请：
1. 检查网络连接
2. 等待 2-3 秒
3. 点击 "🔄 刷新" 重试

### Q: 深度穿透显示空数据

**A**: 可能原因：
1. 基金库存 API 暂时不可用
2. 基金代码无效
3. 请尝试其他基金或等待 1 分钟后重试

### Q: 缓存如何工作？

**A**: 
- 基金行情: 5 分钟缓存
- 基金持股: 1 小时缓存
- 使用 POST /api/cache/clear 手动清除

### Q: 如何部署到生产环境？

**A**: 参考 `DEPLOYMENT.md` 文件获取详细说明

---

## 📈 性能优化建议

### 生产环境

```bash
# 使用 Gunicorn + Nginx

# 1. 启动 Gunicorn
gunicorn -w 8 -b 127.0.0.1:5000 app:app

# 2. 配置 Nginx 反向代理
# 见 nginx.conf
```

### Redis 缓存

```python
# 将内存缓存升级为 Redis
import redis
redis_client = redis.Redis(host='localhost', port=6379)
```

### 监控

```bash
# 监控应用性能
pip install newrelic
newrelic-admin run-program python app.py
```

---

## 📚 更多资源

| 文件 | 说明 |
|------|------|
| `OPTIMIZATION.md` | 代码优化说明 |
| `ISSUES_REPORT.md` | 问题分析报告 |
| `TEST_REPORT.md` | 测试报告 |
| `RUNTIME_REPORT.md` | 运行报告 |
| `DEPLOYMENT.md` | 部署指南 |

---

## 🎓 技术栈

**后端**
- Flask 3.0.0
- Python 3.13
- Requests 2.31.0
- Gunicorn 24.1.1

**前端**
- HTML5
- Vanilla JavaScript
- Chart.js
- ECharts

**部署**
- Vercel (可选)
- Docker (推荐)

---

## 🤝 支持

遇到问题？

1. 查看 `TEST_REPORT.md` 和 `RUNTIME_REPORT.md`
2. 检查 `ISSUES_REPORT.md` 中的常见问题
3. 查看应用日志: `tail -f app.log`
4. 运行测试: `python -m unittest test_app -v`

---

## ✅ 检查清单

启动前确认：

- [ ] Python 版本 >= 3.7
- [ ] 依赖已安装 (`pip install -r requirements.txt`)
- [ ] 虚拟环境已激活
- [ ] 网络连接正常
- [ ] 端口 5000 未被占用

---

**祝你使用愉快！** 🎉
