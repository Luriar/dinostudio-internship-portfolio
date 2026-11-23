import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class PortfolioDocumentationTests(unittest.TestCase):
    def test_six_repository_links(self):
        text=(ROOT/"README.md").read_text(encoding="utf-8")
        names=[
            "dm-workflow-optimization-demo",
            "seller-discovery-asf-demo",
            "seller-history-collector-demo",
            "mysql-campaign-operations-demo",
            "threads-workflow-automation-demo",
            "vling-youtube-pipeline-demo",
        ]
        for name in names:
            with self.subTest(name=name):
                self.assertIn("https://github.com/Luriar/"+name,text)

    def test_disclaimers(self):
        text=(ROOT/"README.md").read_text(encoding="utf-8")
        self.assertIn("2024년 7월 1일",text)
        self.assertIn("2024년 10월",text)
        self.assertIn("원본",text)
        self.assertTrue((ROOT/"docs"/"DEMO_GUIDE.md").is_file())

if __name__=="__main__":
    unittest.main()
