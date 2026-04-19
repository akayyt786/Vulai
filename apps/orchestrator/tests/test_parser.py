from django.test import SimpleTestCase
from apps.orchestrator.parser import parse_llm_response

class ParserTest(SimpleTestCase):
    def test_parse_valid_json(self):
        raw = '{"action": "run_tool", "tool": "nmap"}'
        parsed = parse_llm_response(raw)
        self.assertEqual(parsed["action"], "run_tool")

    def test_parse_markdown_fenced_json(self):
        raw = '```json\n{"action": "done", "reasoning": "all clear"}\n```'
        parsed = parse_llm_response(raw)
        self.assertEqual(parsed["action"], "done")

    def test_parse_invalid_json_returns_pivot(self):
        raw = 'Not JSON at all'
        parsed = parse_llm_response(raw)
        self.assertEqual(parsed["action"], "pivot")
