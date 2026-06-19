💁声明:改项目大部分由ai完成,部分功能还有待完善和更新,后续会持续更新、改进代!!!

💎 FundMaster Pro - 全资产穿透监控助手
<img width="664" height="579" alt="image" src="https://github.com/user-attachments/assets/2b5e9273-6484-4052-a72f-8b16a0f2f6b6" />



这是一个专为基金投资者设计的实时估值监控与穿透分析工具。通过简单的基金代码输入，即可实现对持仓盈亏的毫秒级追踪，并能一键“看透”基金背后的重仓股票分布。

✨ 核心功能
📈 实时行情追踪：接入新浪财经/天天基金实时接口，实时计算当日估值涨跌。

💰 盈亏自动对账：只需录入持仓份额与成本，系统自动计算“今日预估盈亏”与“累计持仓盈亏”。

🔍 深度穿透分析：一键解析所有持仓基金的季度重仓股，通过加权算法生成合并后的前十大持仓饼图。

📱 响应式设计：完美适配手机、平板与电脑浏览器，支持“添加到主屏幕”作为 Web App 使用。

🔒 隐私保护：所有持仓数据均存储在用户本地浏览器的 localStorage 中，不经过任何数据库，确保资产隐私安全。

🚀 快速开始
1. 线上访问
直接访问已部署的网址即可使用： 👉 http://fund-dash-web.vercel.app/

2. 本地运行
如果你想在本地进行二次开发：

Bash
# 克隆仓库
git clone https://github.com/xvsingue/fund-dash.git

# 安装依赖
pip install -r requirements.txt

# 运行项目
python app.py
访问 http://127.0.0.1:5000 即可预览。

🛠 技术架构
后端 (Backend): Python / Flask (Serverless 架构部署于 Vercel)

前端 (Frontend): 原生 JavaScript (ES6+) / HTML5 / CSS3 (Flex & Grid)

图表 (Visuals): ECharts (趋势折线图) / Chart.js (穿透占比饼图)

数据源 (Data Source): 天天基金网 / 新浪财经 API

⚠️ 注意事项
数据延迟：行情数据源自第三方接口，盘中估值仅供参考，实际净值请以官方公布为准。

访问受限：由于穿透分析需要频繁请求数据，若遇到“拦截”提示，请稍候 1-2 分钟重试，这是由于 IP 频率控制导致的。

浏览器兼容：建议使用 Chrome, Safari 或 Edge 浏览器以获得最佳视觉效果。
