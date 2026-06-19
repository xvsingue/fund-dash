#!/bin/bash
# FundMaster 项目运行脚本

echo "=========================================="
echo "FundMaster 项目运行"
echo "=========================================="

# 检查虚拟环境
if [ ! -d ".venv" ]; then
    echo "✓ 创建虚拟环境..."
    python3 -m venv .venv
fi

# 激活虚拟环境
echo "✓ 激活虚拟环境..."
source .venv/bin/activate

# 安装依赖
echo "✓ 安装依赖包..."
pip install -r requirements.txt > /dev/null 2>&1

# 运行应用
echo ""
echo "=========================================="
echo "✅ FundMaster 应用启动成功！"
echo "=========================================="
echo ""
echo "📍 访问地址: http://localhost:5000"
echo "🛑 停止应用: 按 Ctrl+C"
echo ""
echo "=========================================="
echo ""

python app.py
