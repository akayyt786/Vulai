import unittest
from apps.orchestrator.pivot_engine import determine_pivot

class TestPivotEngine(unittest.TestCase):

    def test_url_pivot_layer_sorting(self):
        context = {
            "input_type": "url",
            "surfaces_covered": ["dns", "ports"],
            "current_layer": 1
        }
        # Next should be 'web_tech' in Layer 1
        pivot = determine_pivot(context, {})
        self.assertEqual(pivot["next_surface"], "web_tech")
        self.assertEqual(pivot["next_layer"], 1)

    def test_url_pivot_next_layer(self):
        # Cover all of Layer 1
        context = {
            "input_type": "url",
            "surfaces_covered": ["dns", "ports", "web_tech", "ssl", "headers", "certs"],
            "current_layer": 1
        }
        # Next should be 'directories' in Layer 2
        pivot = determine_pivot(context, {})
        self.assertEqual(pivot["next_surface"], "directories")
        self.assertEqual(pivot["next_layer"], 2)

    def test_pivot_done(self):
        # Mock full coverage (just a few for brevity in test logic)
        context = {
            "input_type": "url",
            "surfaces_covered": [
                "dns", "ports", "web_tech", "ssl", "headers", "certs",
                "directories", "api_endpoints", "subdomains", "parameters", "js_analysis", "robots", "crawl",
                "vuln_scan", "sqli", "xss", "ssti", "ssrf", "xxe", "open_redirect", "cors", "clickjacking", "csrf", "traversal", "file_inclusion", "cmd_injection",
                "brute_force", "default_creds", "jwt_analysis", "oauth", "pw_reset", "session_fixation", "cookie_flags",
                "waf", "cdn", "cloud_metadata", "admin_panel", "backup_exposure", "source_disclosure", "error_pages",
                "chain_analysis", "targeted_payloads"
            ],
            "current_layer": 6
        }
        pivot = determine_pivot(context, {})
        self.assertEqual(pivot["strategy"], "done")

if __name__ == '__main__':
    unittest.main()
