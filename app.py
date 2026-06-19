from flask import Flask, render_template, jsonify, request
import requests
import re
import logging
import time
import random
from functools import wraps
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
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


def get_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Referer": "http://fund.eastmoney.com/",
        "Accept": "*/*"
    }


def validate_fund_code(code):
    return code and isinstance(code, str) and len(code) <= 10 and code.isalnum()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/fund/<codes>')
def get_fund_market(codes):
    try:
        results = []
        for code in codes.split(','):
            code = code.strip()
            if not validate_fund_code(code):
                logger.warning(f"Invalid fund code: {code}")
                continue

            now = time.time()
            if code in CACHE["market"] and (now - CACHE["market"][code].get("time", 0) < CACHE_EXPIRE_MARKET):
                results.append(CACHE["market"][code]["data"])
                continue

            try:
                time.sleep(0.1)
                url = f"http://hq.sinajs.cn/list=f_{code}"
                resp = requests.get(url, headers={"Referer": "http://finance.sina.com.cn"}, timeout=5)
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
                    CACHE["market"][code] = {"data": data, "time": now}
                    results.append(data)
                else:
                    cached = CACHE["market"].get(code, {}).get("data")
                    if cached:
                        results.append(cached)
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
    try:
        if not validate_fund_code(code):
            logger.warning(f"Invalid fund code: {code}")
            return jsonify([]), 400

        now = time.time()
        if code in CACHE["stocks"] and (now - CACHE["stocks"][code].get("time", 0) < CACHE_EXPIRE_STOCK):
            return jsonify(CACHE["stocks"][code]["data"]), 200

        time.sleep(random.uniform(0.5, 1.2))
        url = f"http://fundf10.eastmoney.com/cczc_{code}.html"
        resp = requests.get(url, headers=get_headers(), timeout=5)
        resp.encoding = 'utf-8'
        html = resp.text

        names = STOCK_NAME_PATTERN.findall(html)
        rates = STOCK_RATE_PATTERN.findall(html)

        data = [{"name": names[i], "rate": rates[i]} for i in range(min(10, len(names), len(rates)))]
        if data:
            CACHE["stocks"][code] = {"data": data, "time": now}
            return jsonify(data), 200

        return jsonify([]), 200
    except requests.RequestException as e:
        logger.error(f"API error for stocks {code}: {str(e)}")
        return jsonify([]), 503
    except Exception as e:
        logger.error(f"Unexpected error in get_heavy_stocks: {str(e)}")
        return jsonify([]), 500


@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)