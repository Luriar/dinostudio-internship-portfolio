"""Run the independent 2026 synthetic demos together; no company data or live services."""
from pathlib import Path
import argparse
import csv
import json
import os
import subprocess
import sys
import tempfile

def invoke(repo, *args):
    env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
    result = subprocess.run([sys.executable, *map(str, args)], cwd=repo, env=env,
                            capture_output=True, text=True, encoding="utf-8", check=True, timeout=60)
    return json.loads(result.stdout)

def require(condition, message):
    if not condition:
        raise AssertionError(message)

def run(root):
    asf = root / "seller-discovery-asf-demo"
    hc = root / "seller-history-collector-demo"
    vling = root / "vling-youtube-pipeline-demo"
    with tempfile.TemporaryDirectory(prefix="portfolio-demo-") as tmp:
        tmp = Path(tmp)
        candidates = tmp / "candidates.csv"
        args = ("run_pipeline.py", "--db", tmp / "asf.sqlite", "--export", candidates)
        first = invoke(asf, *args)
        second = invoke(asf, *args)
        with candidates.open(encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
        codes = {row["code"] for row in rows}
        require(bool(codes) and len(rows) == len(codes), "ASF candidate export must be unique")
        require(first["synthetic_only"] and second["synthetic_only"], "Expected synthetic data")
        require(first["summary"] == second["summary"], "ASF repeat changed classification")
        source = json.loads((hc / "fixtures" / "observations.json").read_text(encoding="utf-8"))
        selected = [item for item in source if item["code"] in codes]
        require(bool(selected), "No matching synthetic activity observations")
        fixture = tmp / "selected.json"
        fixture.write_text(json.dumps(selected), encoding="utf-8")
        history = tmp / "history.csv"
        args = ("run_history.py", "--input", fixture, "--db", tmp / "history.sqlite",
                "--export", history)
        h1 = invoke(hc, *args)
        h2 = invoke(hc, *args)
        with history.open(encoding="utf-8-sig", newline="") as f:
            records = list(csv.DictReader(f))
        require(h1["synthetic_only"] and h2["synthetic_only"], "Expected synthetic history")
        require({r["code"] for r in records} == {o["code"] for o in selected},
                "History must match exported candidates")
        require(len(records) == len({(r["code"], r["observed_on"]) for r in records}),
                "Duplicate historical snapshot")
        require(h1["sample_trend"] == h2["sample_trend"], "Repeat import changed trend")
        db = tmp / "warehouse.sqlite"
        v1 = invoke(vling, "seed.py", "--db", db)
        v2 = invoke(vling, "seed.py", "--db", db)
        require(v1["synthetic_only"] and v2["synthetic_only"], "Expected synthetic warehouse")
        check = """
import json, sys
from app import create_app
from pipeline import connect, load_fixture
from contextlib import closing
from pathlib import Path
db = sys.argv[1]
client = create_app(db).test_client()
channels = client.get('/api/channels').get_json()
videos = client.get('/api/videos').get_json()
assert channels and videos
code = channels[0]['id']
assert client.post('/note/channel/' + code, data={'note':'synthetic review'}).status_code == 302
with closing(connect(db)) as conn:
    load_fixture(conn, Path('fixtures/sample.json'))
updated = client.get('/api/channels').get_json()
assert len(updated) == len(channels)
assert next(x for x in updated if x['id'] == code)['analyst_note'] == 'synthetic review'
assert client.get('/').status_code == 200
assert client.get('/videos').status_code == 200
assert client.get('/api/summary').status_code == 200
print(json.dumps({'channels':len(updated),'videos':len(videos),'note_preserved':True,
                  'page_checks':3,'synthetic_only':True}))
"""
        web = invoke(vling, "-c", check, db)
        dm = invoke(root / "dm-workflow-optimization-demo", "workflow.py")
        dbops = invoke(root / "mysql-campaign-operations-demo", "operations.py")
        threads = invoke(root / "threads-workflow-automation-demo", "review_queue.py")
        return {
            "synthetic_only": True,
            "asf_to_hc": {"candidate_codes": len(codes), "matched_observations": len(selected),
                          "unique_history_rows": len(records), "repeat_import_stable": True},
            "vling": web,
            "standalone_demos": {
                "dm": {"json_output": isinstance(dm, dict)},
                "db_operations": {"json_output": isinstance(dbops, dict)},
                "threads": {"json_output": isinstance(threads, dict)}
            }
        }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repos-root", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.repos_root.resolve()), ensure_ascii=False, indent=2))
