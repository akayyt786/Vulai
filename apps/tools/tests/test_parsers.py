import unittest
import json
from apps.tools.output_parsers import (
    katana_parser, dalfox_parser, gobuster_parser, arjun_parser, sslyze_parser,
    nmap_parser, nikto_parser, nuclei_parser, sqlmap_parser, ffuf_parser,
    semgrep_parser, trufflehog_parser, gitleaks_parser, subfinder_parser, trivy_parser
)

class TestParsers(unittest.TestCase):

    def test_katana_parser(self):
        raw = "http://example.com/about\nhttp://example.com/contact\nhttp://example.com/about"
        result = katana_parser.parse(raw)
        self.assertEqual(result["count"], 2)
        self.assertEqual(result["findings"][0]["severity"], "info")

    def test_dalfox_parser(self):
        raw = "[V][GET] http://example.com/xss.php?q=123 ... proof: <script>alert(1)</script>\n[POC][POST] http://example.com/login ... proof: \"><svg onload=alert(1)>"
        result = dalfox_parser.parse(raw)
        self.assertEqual(result["count"], 2)
        self.assertEqual(result["findings"][0]["severity"], "high")

    def test_gobuster_parser(self):
        raw = "/admin (Status: 200) [Size: 1024]\n/index.html (Status: 200) [Size: 512]\n/config.php (Status: 200) [Size: 128]"
        result = gobuster_parser.parse(raw)
        self.assertEqual(result["count"], 3)
        self.assertEqual(result["findings"][0]["severity"], "high")

    def test_arjun_parser_regex(self):
        raw = "Heuristic scan found 2 parameters: id, token"
        result = arjun_parser.parse(raw)
        self.assertEqual(result["count"], 2)
        self.assertEqual(result["findings"][0]["title"], "Discovered Parameter: id")

    def test_sslyze_parser(self):
        raw = "Heartbleed: VULNERABLE\nSSL 2.0: Accepted\nTLS 1.1: Accepted\nHostname validation: FAILED"
        result = sslyze_parser.parse(raw)
        self.assertEqual(result["count"], 4)
        self.assertEqual(result["findings"][0]["severity"], "critical")

    def test_nmap_parser(self):
        raw = "80/tcp open http Apache httpd 2.4.41\n443/tcp open ssl/http Apache httpd 2.4.41"
        result = nmap_parser.parse(raw)
        self.assertEqual(result["count"], 2)
        self.assertEqual(result["findings"][0]["title"], "Open Port Discovered: 80/tcp")
        self.assertEqual(result["findings"][0]["severity"], "info")

    def test_nikto_parser(self):
        raw = "+ OSVDB-3092: /admin/: This might be interesting...\n+ /test.php: Vulnerable to RCE"
        result = nikto_parser.parse(raw)
        self.assertEqual(result["count"], 2)
        self.assertEqual(result["findings"][0]["severity"], "medium")
        self.assertEqual(result["findings"][1]["severity"], "high")

    def test_nuclei_parser(self):
        raw_json_line = json.dumps({
            "template-id": "exposed-config",
            "info": {"severity": "medium", "description": "Exposed config file"},
            "matched-at": "http://example.com/config.php"
        })
        result = nuclei_parser.parse(raw_json_line)
        self.assertEqual(result["count"], 1)
        self.assertEqual(result["findings"][0]["severity"], "medium")
        self.assertEqual(result["findings"][0]["location"], "http://example.com/config.php")

    def test_sqlmap_parser(self):
        raw = "GET parameter 'id' is vulnerable. Type: Boolean-based blind. Title: MySQL >= 5.0.12"
        result = sqlmap_parser.parse(raw)
        self.assertEqual(result["count"], 1)
        self.assertEqual(result["findings"][0]["severity"], "high")

    def test_ffuf_parser(self):
        raw_json = json.dumps({"results": [{"url": "http://example.com/.env", "status": 200, "length": 123, "words": 10}]})
        result = ffuf_parser.parse(raw_json)
        self.assertEqual(result["count"], 1)
        self.assertEqual(result["findings"][0]["severity"], "high")

    def test_semgrep_parser(self):
        raw_json = json.dumps({"results": [{"check_id": "rules.sqli", "path": "app.py", "start": {"line": 10}, "extra": {"message": "SQLi found", "severity": "ERROR", "lines": "db.execute(query)"}}]})
        result = semgrep_parser.parse(raw_json)
        self.assertEqual(result["count"], 1)
        self.assertEqual(result["findings"][0]["severity"], "high")

    def test_trufflehog_parser(self):
        raw_json = json.dumps({"DetectorName": "AWSKey", "SourceMetadata": {"Data": {"Git": {"file": "config.js", "line": 5}}}, "Raw": "AKIA..."})
        result = trufflehog_parser.parse(raw_json)
        self.assertEqual(result["count"], 1)
        self.assertEqual(result["findings"][0]["severity"], "high")

    def test_gitleaks_parser(self):
        raw_json = json.dumps([{"Description": "AWS secret", "RuleID": "aws-key", "File": "env.local", "StartLine": 10, "Match": "AKIA..."}])
        result = gitleaks_parser.parse(raw_json)
        self.assertEqual(result["count"], 1)
        self.assertEqual(result["findings"][0]["severity"], "high")

    def test_subfinder_parser(self):
        raw = "dev.example.com\nprod.example.com\ndev.example.com"
        result = subfinder_parser.parse(raw)
        self.assertEqual(result["count"], 2) # Deduplicated
        self.assertEqual(result["findings"][0]["severity"], "info")

    def test_trivy_parser(self):
        raw_json = json.dumps({"Results": [{"Target": "package.json", "Vulnerabilities": [{"VulnerabilityID": "CVE-2023-1234", "PkgName": "express", "Severity": "HIGH", "Title": "XSS in express"}]}]})
        result = trivy_parser.parse(raw_json)
        self.assertEqual(result["count"], 1)
        self.assertEqual(result["findings"][0]["severity"], "high")

if __name__ == '__main__':
    unittest.main()
