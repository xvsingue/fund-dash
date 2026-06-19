from flask import Flask, render_template, jsonify, request
import requests
import re
import logging
import time
import random
import os
from functools import wraps
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

app = Flask(__name__)

# 日志配置
log_level = os.getenv('LOG_LEVEL', 'INFO')
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger(__name__)

# 缓存配置
CACHE = {"market": {}, "stocks": {}}
CACHE_EXPIRE_MARKET = 300  # 5分钟
CACHE_EXPIRE_STOCK = 3600  # 1小时

# 预编译正则表达式
FUND_DATA_PATTERN = re.compile(r'"(.*)"')
STOCK_NAME_PATTERN = re.compile(r'<a href="http://quote.*?">(.*?)</a>')
STOCK_RATE_PATTERN = re.compile(r'<td class="alignRight">(\d+\.\d+)%</td>')

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]

# 创建带重试机制的会话
def create_session_with_retries(retries=3, backoff_factor=0.5):
    session = requests.Session()
    retry_strategy = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

REQUESTS_SESSION = create_session_with_retries()


def get_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Referer": "http://fund.eastmoney.com/",
        "Accept": "*/*"
    }


def validate_fund_code(code):
    """严格验证基金代码：必须是6位纯数字"""
    return bool(code and isinstance(code, str) and code.isdigit() and len(code) == 6)


def is_cache_valid(cache_dict, code, expire_seconds):
    """检查缓存是否有效"""
    if code not in cache_dict:
        return False
    try:
        cached_item = cache_dict[code]
        if not isinstance(cached_item, dict) or "time" not in cached_item:
            return False
        cache_time = cached_item.get("time", 0)
        return time.time() - cache_time < expire_seconds
    except (KeyError, TypeError):
        return False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/fund/<codes>')
def get_fund_market(codes):
    """获取基金市场数据"""
    try:
        results = []
        for code in codes.split(','):
            code = code.strip()
            if not code:
                continue

            if not validate_fund_code(code):
                logger.warning(f"Invalid fund code: {code}")
                continue

            # 检查缓存
            if is_cache_valid(CACHE["market"], code, CACHE_EXPIRE_MARKET):
                results.append(CACHE["market"][code]["data"])
                continue

            # 获取新数据
            try:
                time.sleep(0.1)
                url = f"http://hq.sinajs.cn/list=f_{code}"

                resp = REQUESTS_SESSION.get(url, headers={"Referer": "http://finance.sina.com.cn"}, timeout=5)
                resp.raise_for_status()
                content = resp.content.decode('gbk')

                match = FUND_DATA_PATTERN.search(content)
                if match and match.group(1):
                    p = match.group(1).split(',')
                    data = {
                        "code": code,
                        "name": (p[0] or "未知")[:50],
                        "gsz": p[1] or "0",
                        "jz": p[3] or "0",
                        "gszzl": p[5] or "0.00"
                    }
                    CACHE["market"][code] = {"data": data, "time": time.time()}
                    results.append(data)
                else:
                    cached = CACHE["market"].get(code, {}).get("data")
                    if cached:
                        results.append(cached)
                        logger.warning(f"No data found for {code}, using cache")
            except requests.RequestException as e:
                logger.error(f"API error for code {code}: {str(e)}")
                cached = CACHE["market"].get(code, {}).get("data")
                if cached:
                    results.append(cached)

        return jsonify(results), 200
    except Exception as e:
        logger.error(f"Unexpected error in get_fund_market: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/api/stocks/<code>')
def get_heavy_stocks(code):
    """获取基金重持股票"""
    try:
        if not validate_fund_code(code):
            logger.warning(f"Invalid fund code: {code}")
            return jsonify({"error": "Invalid fund code"}), 400

        # 检查缓存
        if is_cache_valid(CACHE["stocks"], code, CACHE_EXPIRE_STOCK):
            return jsonify(CACHE["stocks"][code]["data"]), 200

        time.sleep(random.uniform(0.5, 1.2))
        url = f"http://fundf10.eastmoney.com/cczc_{code}.html"

        resp = REQUESTS_SESSION.get(url, headers=get_headers(), timeout=5)
        resp.raise_for_status()
        resp.encoding = 'utf-8'
        html = resp.text

        # 提取股票名称和比例
        names = STOCK_NAME_PATTERN.findall(html)
        rates = STOCK_RATE_PATTERN.findall(html)

        # 配对数据：确保名称和比例一一对应
        data = []
        max_items = min(10, len(names), len(rates))
        for i in range(max_items):
            try:
                rate_val = float(rates[i])
                data.append({
                    "name": names[i][:50],  # 限制长度防止注入
                    "rate": f"{rate_val:.2f}"
                })
            except (ValueError, IndexError):
                continue

        if data:
            CACHE["stocks"][code] = {"data": data, "time": time.time()}
            return jsonify(data), 200

        return jsonify(data), 200
    except requests.RequestException as e:
        logger.error(f"API timeout/error for stocks {code}: {str(e)}")
        return jsonify({"error": "API not available", "data": []}), 503
    except Exception as e:
        logger.error(f"Unexpected error in get_heavy_stocks: {str(e)}")
        return jsonify({"error": "Internal server error", "data": []}), 500


@app.route('/api/cache/clear', methods=['POST'])
def clear_cache():
    """清空缓存（用于测试和维护）"""
    try:
        CACHE["market"].clear()
        CACHE["stocks"].clear()
        logger.info("Cache cleared")
        return jsonify({"status": "ok", "message": "Cache cleared"}), 200
    except Exception as e:
        logger.error(f"Error clearing cache: {str(e)}")
        return jsonify({"error": "Failed to clear cache"}), 500


@app.route('/health')
def health():
    """健康检查端点"""
    return jsonify({"status": "ok"}), 200


@app.errorhandler(404)
def not_found(error):
    """404 错误处理"""
    logger.warning(f"404 error: {request.path}")
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """500 错误处理"""
    logger.error(f"500 error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    app.run(debug=False, port=5000)