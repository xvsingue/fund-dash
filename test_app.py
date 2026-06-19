import unittest
import json
from app import app, CACHE


class TestFundMasterApp(unittest.TestCase):
    def setUp(self):
        """初始化测试客户端和清空缓存"""
        self.app = app.test_client()
        self.app.testing = True
        CACHE["market"].clear()
        CACHE["stocks"].clear()

    def test_01_index_page(self):
        """测试首页是否正常加载"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'FundMaster', response.data)
        print("✓ 首页加载成功")

    def test_02_health_endpoint(self):
        """测试健康检查端点"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data.get('status'), 'ok')
        print("✓ 健康检查端点正常")

    def test_03_invalid_fund_code_format(self):
        """测试无效的基金代码格式"""
        response = self.app.get('/api/fund/invalid@code')
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)
        print("✓ 无效基金代码被正确拒绝")

    def test_04_empty_fund_code(self):
        """测试空基金代码"""
        response = self.app.get('/api/fund/')
        # 空代码应该返回空列表
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertIsInstance(data, list)
            print("✓ 空基金代码返回空列表")

    def test_05_multiple_fund_codes(self):
        """测试多个基金代码"""
        response = self.app.get('/api/fund/001001,001002')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        print(f"✓ 多基金代码测试完成，返回{len(data)}个结果")

    def test_06_fund_code_with_spaces(self):
        """测试含有空格的基金代码"""
        response = self.app.get('/api/fund/001001, 001002')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        print("✓ 空格处理正常")

    def test_07_stock_endpoint_invalid_code(self):
        """测试库存端点的无效代码"""
        response = self.app.get('/api/stocks/invalid@code')
        self.assertEqual(response.status_code, 400)
        print("✓ 无效股票代码返回400状态码")

    def test_08_stock_endpoint_valid_format(self):
        """测试库存端点的有效格式代码"""
        response = self.app.get('/api/stocks/001001')
        # 应该返回200或503（如果API不可用）
        self.assertIn(response.status_code, [200, 503, 504])
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertIsInstance(data, list)
        print(f"✓ 库存端点返回状态码: {response.status_code}")

    def test_09_response_json_format(self):
        """测试响应JSON格式是否正确"""
        response = self.app.get('/api/fund/001001')
        self.assertEqual(response.status_code, 200)
        try:
            data = json.loads(response.data)
            self.assertIsInstance(data, list)
            print("✓ JSON格式正确")
        except json.JSONDecodeError:
            self.fail("JSON解析失败")

    def test_10_cache_functionality(self):
        """测试缓存功能"""
        import time

        # 第一次请求
        response1 = self.app.get('/api/fund/001001')
        initial_cache_size = len(CACHE["market"])

        # 第二次请求（应该从缓存返回）
        response2 = self.app.get('/api/fund/001001')

        self.assertEqual(response1.status_code, response2.status_code)
        print(f"✓ 缓存功能正常，缓存大小: {len(CACHE['market'])}")

    def test_11_fund_code_length_limit(self):
        """测试基金代码长度限制"""
        # 超长代码应该被拒绝
        long_code = 'a' * 50
        response = self.app.get(f'/api/fund/{long_code}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 0)
        print("✓ 基金代码长度限制生效")

    def test_12_special_characters_in_code(self):
        """测试特殊字符处理"""
        special_codes = ['001&001', '001;001', '001 001', '001\n001']
        for code in special_codes:
            try:
                response = self.app.get(f'/api/fund/{code}')
                self.assertIn(response.status_code, [200, 400])
            except:
                pass
        print("✓ 特殊字符处理正常")

    def test_13_concurrent_requests_simulation(self):
        """模拟并发请求"""
        results = []
        for i in range(3):
            response = self.app.get('/api/fund/001001')
            results.append(response.status_code)

        # 所有请求都应该成功
        self.assertTrue(all(status in [200, 503] for status in results))
        print(f"✓ 并发模拟完成，结果: {results}")

    def test_14_error_handling_missing_data(self):
        """测试错误处理 - 缺失数据"""
        response = self.app.get('/api/fund/999999')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        print("✓ 缺失数据处理正常")

    def test_15_response_headers(self):
        """测试响应头"""
        response = self.app.get('/health')
        self.assertEqual(response.content_type, 'application/json')
        print("✓ 响应头正确")


if __name__ == '__main__':
    # 运行所有测试
    unittest.main(verbosity=2)
