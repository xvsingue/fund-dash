# 🚀 FundMaster 项目完整运行指南

## 📌 快速开始（3 步）

### 第 1 步：激活虚拟环境
```bash
cd /Users/apple/D/mac2014/py_code/FundMaster
source .venv/bin/activate
```

### 第 2 步：安装依赖（如果需要）
```bash
pip install -r requirements.txt
```

### 第 3 步：启动应用
```bash
python app.py
```

✅ 应用已启动！打开浏览器访问 **http://localhost:5000**

---

## 📖 详细步骤

### 步骤 1：进入项目目录

```bash
cd /Users/apple/D/mac2014/py_code/FundMaster
```

### 步骤 2：激活虚拟环境

**macOS / Linux:**
```bash
source .venv/bin/activate
```

**Windows:**
```bash
.venv\Scripts\activate
```

激活后，你会看到命令行前缀显示 `(.venv)`

### 步骤 3：验证依赖已安装

```bash
pip list | grep Flask
```

如果看到 `Flask 3.0.0`，说明依赖已安装。

### 步骤 4：启动应用

```bash
python app.py
```

你会看到类似的输出：
```
 * Serving Flask app 'app'
 * Debug mode: off
 * Running on http://127.0.0.1:5000
```

### 步骤 5：打开浏览器

在浏览器中访问：**http://localhost:5000**

你应该看到 FundMaster 首页 💎

---

## 🎯 使用应用

### 1. 添加基金

1. 点击右上角 "➕ 添加" 按钮
2. 输入基金代码（6位数字，如 `001001`）
3. 输入持仓份额（如 `100`）
4. 输入买入成本（可选，如 `1.20`）
5. 点击 "保存"

### 2. 查看行情

1. 点击 "🔄 刷新" 按钮获取最新行情
2. 查看基金估值和盈亏情况

### 3. 深度穿透分析

1. 点击 "🔍 开启深度穿透" 按钮
2. 等待加载（2-3 秒）
3. 查看持仓股票权重分布

---

## 🧪 运行测试

### 方式 1：运行所有单元测试

```bash
python -m unittest test_app -v
```

预期结果：
```
✓ 15 个测试全部通过
✓ 耗时约 2.5 秒
```

### 方式 2：运行特定测试

```bash
# 测试首页
python -m unittest test_app.TestFundMasterApp.test_01_index_page -v

# 测试基金查询
python -m unittest test_app.TestFundMasterApp.test_05_multiple_fund_codes -v
```

---

## 🔧 API 端点测试

### 在另一个终端中测试 API

```bash
# 健康检查
curl http://localhost:5000/health

# 查询单个基金
curl http://localhost:5000/api/fund/001001

# 查询多个基金
curl http://localhost:5000/api/fund/001001,110022,519674

# 查询基金持股
curl http://localhost:5000/api/stocks/001001

# 清除缓存
curl -X POST http://localhost:5000/api/cache/clear
```

---

## 📊 命令参考

| 命令 | 说明 |
|------|------|
| `source .venv/bin/activate` | 激活虚拟环境 |
| `python app.py` | 启动应用 |
| `python -m unittest test_app -v` | 运行测试 |
| `Ctrl+C` | 停止应用 |
| `deactivate` | 退出虚拟环境 |

---

## ⚠️ 常见问题

### Q: 启动时出现 "ModuleNotFoundError: No module named 'flask'"

**A:** 虚拟环境未激活或依赖未安装
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Q: 端口 5000 已被占用

**A:** 修改启动命令（改为其他端口，如 5001）
```bash
python -c "from app import app; app.run(port=5001)"
```

### Q: 无法访问 http://localhost:5000

**A:** 检查应用是否正在运行
- 查看终端是否显示 "Running on"
- 确保没有按 Ctrl+C
- 检查防火墙设置

### Q: 基金数据显示 "查询中..."

**A:** 这是正常的，正在从外部 API 获取数据
- 等待 2-3 秒
- 点击 "🔄 刷新" 按钮重试
- 检查网络连接

### Q: 如何查看日志？

**A:** 终端会显示所有日志信息
```
INFO:app:Invalid fund code: invalid@code
ERROR:app:API error for code 001001: ...
```

---

## 🌐 功能演示

### 基金代码示例

| 代码 | 名称 | 类型 |
|------|------|------|
| 001001 | 华夏债券A | 债券基金 |
| 110022 | 易方达消费 | 股票基金 |
| 005918 | 建信养老 | 目标日期 |
| 519674 | 银河创新 | 股票基金 |
| 163402 | 兴全趋势 | 混合基金 |

### 测试流程

1. ✅ 启动应用
2. ✅ 添加基金 `001001`
3. ✅ 点击 "刷新" 查看行情
4. ✅ 点击 "深度穿透" 查看持股

---

## 📚 相关文档

启动后，可以查看以下文档了解更多：

| 文档 | 内容 |
|------|------|
| `QUICKSTART.md` | 快速开始指南 |
| `PROJECT_SUMMARY.md` | 项目完成总结 |
| `TEST_REPORT.md` | 详细测试报告 |
| `RUNTIME_REPORT.md` | 运行性能报告 |
| `OPTIMIZATION.md` | 代码优化说明 |
| `DEPLOYMENT.md` | 生产部署指南 |

---

## 🔌 停止应用

在启动应用的终端中按：
```
Ctrl + C
```

然后退出虚拟环境（可选）：
```bash
deactivate
```

---

## 🎓 生产环境运行

### 方式 1：使用 Gunicorn（推荐）

```bash
# 安装 Gunicorn（可选，已在 requirements.txt 中）
pip install gunicorn

# 启动应用（4 个 worker 进程）
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 方式 2：使用 Docker

```bash
# 构建 Docker 镜像
docker build -t fundmaster .

# 运行容器
docker run -p 5000:5000 fundmaster
```

### 方式 3：部署到云服务

参考 `DEPLOYMENT.md` 获取详细说明

---

## ✅ 检查清单

启动前确认：

- [ ] 进入项目目录
- [ ] 虚拟环境已激活（看到 `(.venv)` 前缀）
- [ ] 依赖已安装（`pip list | grep Flask`）
- [ ] 网络连接正常
- [ ] 端口 5000 未被占用

启动后验证：

- [ ] 应用输出 "Running on http://127.0.0.1:5000"
- [ ] 浏览器能访问 http://localhost:5000
- [ ] 能看到 FundMaster 首页
- [ ] "🔄 刷新" 按钮可以获取数据

---

## 📞 获取帮助

1. **查看文档**
   - `QUICKSTART.md` - 快速帮助
   - `PROJECT_SUMMARY.md` - 项目概览

2. **运行测试**
   ```bash
   python -m unittest test_app -v
   ```

3. **查看日志**
   - 查看终端输出
   - 错误信息会显示原因

4. **检查 API**
   ```bash
   curl http://localhost:5000/health
   ```

---

## 🎉 祝你使用愉快！

现在你已经了解了如何运行 FundMaster 项目。

**立即开始**：
```bash
cd /Users/apple/D/mac2014/py_code/FundMaster
source .venv/bin/activate
python app.py
```

然后在浏览器中访问 **http://localhost:5000** 🚀
