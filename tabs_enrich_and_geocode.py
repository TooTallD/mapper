import pandas as pd, requests, os, time, argparse
from bs4 import BeautifulSoup
from urllib.parse import urljoin

parser = argparse.ArgumentParser()
parser.add_argument("--geocode", default="false")
parser.add_argument("--limit", type=int, default=25)
parser.add_argument("--sleep", type=float, default=1.0)
args = parser.parse_args()

inp = "data/master_projects_with_addresses.csv"
outdir = "output"
os.makedirs(outdir, exist_ok=True)
df = pd.read_csv(inp)

if "Location Address" not in df.columns:
    df["Location Address"] = ""

headers = {"User-Agent": "Mozilla/5.0"}
base_url = "https://www.tdlr.texas.gov/TABS/Projects/"

def fetch_address(pid):
    url = urljoin(base_url, pid)
    try:
        r = requests.get(url, headers=headers, timeout=30)
        if r.status_code != 200:
            return ""
        fname = os.path.join(outdir, f"debug_{pid}.html")
        with open(fname, "w", encoding="utf-8") as f: f.write(r.text)
        soup = BeautifulSoup(r.text, "html.parser")
        txt = soup.get_text(" ", strip=True)
        for label in ["Location Address", "Project Address", "Project Location"]:
            if label in txt:
                idx = txt.index(label)
                snippet = txt[idx: idx+300]
                parts = snippet.split(":")
                if len(parts) > 1:
                    addr = parts[1].split("  ")[0].strip()
                    return addr
    except Exception as e:
        return ""
    return ""

limit = args.limit if args.limit>0 else len(df)
for i,(idx,row) in enumerate(df.iterrows()):
    if i>=limit: break
    if not row.get("Location Address") or str(row["Location Address"]).strip()=="":
        pid = str(row.get("Project Id","")).strip()
        if pid:
            addr = fetch_address(pid)
            df.at[idx,"Location Address"] = addr
            print(f"[ADDR] {pid} -> {addr}")
        time.sleep(args.sleep)

df.to_csv(os.path.join(outdir,"projects_enriched.csv"), index=False)
