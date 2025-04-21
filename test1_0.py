import unittest
from unittest.mock import patch, MagicMock
from urllib.parse import urlparse
import tldextract
from web1_0 import (
    normalize_url, is_valid_url, crawl,
    visited, broken_links, internal_links,
    external_links, file_links, subdomains, max_pages
)
import requests


class TestCrawlerFunctions(unittest.TestCase):
    """测试基础功能函数"""

    def test_normalize_url(self):
        self.assertEqual(normalize_url("google.com"), "https://google.com")
        self.assertEqual(normalize_url("http://github.com"), "http://github.com")
        self.assertEqual(normalize_url("docs.github.com"), "https://docs.github.com")

    def test_is_valid_url(self):
        self.assertTrue(is_valid_url("https://google.com/search"))
        self.assertTrue(is_valid_url("http://github.com/about"))
        self.assertFalse(is_valid_url("ftp://google.com"))
        self.assertFalse(is_valid_url("javascript:void(0)"))


class BaseCrawlerTest(unittest.TestCase):
    """测试基类，包含共用方法"""

    def setUp(self):
        # 重置全局状态
        visited.clear()
        broken_links.clear()
        internal_links.clear()
        external_links.clear()
        file_links.clear()
        subdomains.clear()

    def create_mock_response(self, html, status=200):
        mock = MagicMock()
        mock.status_code = status
        mock.text = html
        return mock


class TestGoogleCrawl(BaseCrawlerTest):
    """测试Google网站爬取"""

    @patch('requests.get')
    def test_google_crawl(self, mock_get):
        """测试Google首页爬取"""
        mock_get.return_value = self.create_mock_response(
            """
            <html>
                <a href="/search?q=python">Python搜索</a>
                <a href="https://maps.google.com">地图</a>
                <a href="https://www.youtube.com">外部链接</a>
                <a href="/privacy.pdf">隐私政策</a>
            </html>
            """
        )

        crawl("https://www.google.com", "google.com")

        self.assertIn("https://www.google.com", visited)
        self.assertIn("https://www.google.com/search?q=python", internal_links)
        self.assertIn("https://maps.google.com", internal_links)
        self.assertIn("https://www.youtube.com", external_links)
        self.assertIn("https://www.google.com/privacy.pdf", file_links)
        self.assertIn("maps.google.com", subdomains)


class TestGitHubCrawl(BaseCrawlerTest):
    """测试GitHub网站爬取"""

    @patch('requests.get')
    def test_github_crawl(self, mock_get):
        """测试GitHub首页爬取"""
        mock_get.return_value = self.create_mock_response(
            """
            <html>
                <a href="/features">功能</a>
                <a href="https://docs.github.com">文档</a>
                <a href="/blog">博客</a>
                <a href="https://twitter.com/github">Twitter</a>
                <a href="/terms.pdf">用户协议</a>
            </html>
            """
        )

        crawl("https://github.com", "github.com")

        self.assertIn("https://github.com/features", internal_links)
        self.assertIn("https://docs.github.com", internal_links)
        self.assertIn("https://twitter.com/github", external_links)
        self.assertIn("https://github.com/terms.pdf", file_links)
        self.assertIn("docs.github.com", subdomains)


if __name__ == '__main__':
    unittest.main(verbosity=2)