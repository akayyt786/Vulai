import unittest
from apps.tools.output_parsers import katana_parser, dalfox_parser, gobuster_parser, arjun_parser, sslyze_parser

class TestParsers(unittest.TestCase):

    def test_katana_parser(self):
        raw = "http://example.com/about\nhttp://example.com/contact\nhttp://example.com/about"
        result = katana_parser.parse(raw)
        self.assertEqual(result["count"], 2)
        self.assertEqual(result["findings"][0]["severity"], "info")
        self.assertEqual(result["findings"][0]["location"], "http://example.com/about")

    def test_dalfox_parser(self):
        raw = "[V][GET] http://example.com/xss.php?q=123 ... proof: <script>alert(1)</script>\n[POC][POST] http://example.com/login ... proof: \"><svg onload=alert(1)>"
        result = dalfox_parser.parse(raw)
        self.assertEqual(result["count"], 2)
        self.assertEqual(result["findings"][0]["severity"], "high")
        self.assertEqual(result["findings"][1]["severity"], "medium")
        self.assertEqual(result["findings"][0]["title"], "Verified XSS (GET)")

    def test_gobuster_parser(self):
        raw = "/admin (Status: 200) [Size: 1024]\n/index.html (Status: 200) [Size: 512]\n/config.php (Status: 200) [Size: 128]"
        result = gobuster_parser.parse(raw)
        self.assertEqual(result["count"], 3)
        self.assertEqual(result["findings"][0]["severity"], "high") # admin keyword
        self.assertEqual(result["findings"][2]["severity"], "high") # config keyword
        self.assertEqual(result["findings"][1]["severity"], "medium") # 200 OK

    def test_arjun_parser_regex(self):
        raw = "Heuristic scan found 2 parameters: id, token"
        result = arjun_parser.parse(raw)
        self.assertEqual(result["count"], 2)
        self.assertEqual(result["findings"][0]["title"], "Discovered Parameter: id")

    def test_sslyze_parser(self):
        raw = "Heartbleed: VULNERABLE\nSSL 2.0: Accepted\nTLS 1.1: Accepted\nHostname validation: FAILED"
        result = sslyze_parser.parse(raw)
        # findings: Heartbleed, SSL 2.0, TLS 1.1, Hostname Mismatch
        self.assertEqual(result["count"], 4)
        self.assertEqual(result["findings"][0]["severity"], "critical")
        self.assertEqual(result["findings"][1]["severity"], "medium")
        self.assertEqual(result["findings"][2]["severity"], "low")
        self.assertEqual(result["findings"][3]["severity"], "low")

if __name__ == '__main__':
    unittest.main()
