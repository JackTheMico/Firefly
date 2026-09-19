#!/usr/bin/env python3
import os
import json
import subprocess
import time
import urllib.request
import tempfile

IMGBED_HOST = "https://jackwyimgbed.dlwxxxdlw.workers.dev"
UPLOAD_URL = f"{IMGBED_HOST}/upload"
API_TOKEN = "imgbed_5361b57bfe0e54dddeb2e60c5e28950118b637363bc37ddafd12ed795d70374f"
MAP_FILE = "imgbed-upload-map.json"

# Load existing map if any
if os.path.exists(MAP_FILE):
    with open(MAP_FILE, "r", encoding="utf-8") as f:
        upload_map = json.load(f)
else:
    upload_map = {}

def upload_file_to_imgbed(file_path):
    cmd = [
        "curl", "-s", "--connect-timeout", "15", "--max-time", "60",
        "-X", "POST", UPLOAD_URL,
        "-H", f"Authorization: Bearer {API_TOKEN}",
        "-F", f"file=@{file_path}"
    ]
    
    for attempt in range(3):
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            try:
                data = json.loads(res.stdout)
                if isinstance(data, list) and len(data) > 0 and "src" in data[0]:
                    return f"{IMGBED_HOST}{data[0]['src']}"
                elif isinstance(data, dict) and "src" in data:
                    return f"{IMGBED_HOST}{data['src']}"
            except json.JSONDecodeError:
                pass
        print(f"  Attempt {attempt + 1} failed for {file_path}, stdout: {res.stdout.strip()[:100]}, stderr: {res.stderr.strip()[:100]}. Retrying...")
        time.sleep(2)
        
    raise RuntimeError(f"Failed to upload {file_path} after 3 attempts")

def upload_url_to_imgbed(remote_url):
    print(f"Downloading remote image: {remote_url}")
    ext = os.path.splitext(remote_url.split("?")[0])[1] or ".webp"
    with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
        tmp_path = tmp.name
        
    cmd_dl = ["curl", "-sL", remote_url, "-o", tmp_path]
    res_dl = subprocess.run(cmd_dl, capture_output=True)
    if res_dl.returncode != 0 or os.path.getsize(tmp_path) == 0:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise RuntimeError(f"Failed to download {remote_url}")
        
    try:
        new_url = upload_file_to_imgbed(tmp_path)
        return new_url
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

def main():
    # 1. Local image files to upload
    exts = (".png", ".jpg", ".jpeg", ".webp", ".avif", ".gif")
    target_dirs = [
        "src/assets/images",
        "public/assets/images",
        "public/assets/music/cover",
        "src/content/posts",
        "public/gallery",
        "docs/images",
        "public/favicon"
    ]
    
    local_files = []
    for tdir in target_dirs:
        if not os.path.exists(tdir):
            continue
        for root, dirs, files in os.walk(tdir):
            for f in files:
                if f.lower().endswith(exts):
                    p = os.path.normpath(os.path.join(root, f))
                    local_files.append(p)
                    
    local_files.sort()
    print(f"Found {len(local_files)} local image files to process.")
    
    # Process local files
    for idx, filepath in enumerate(local_files):
        if filepath in upload_map:
            print(f"[{idx+1}/{len(local_files)}] Already uploaded: {filepath} -> {upload_map[filepath]}")
            continue
            
        print(f"[{idx+1}/{len(local_files)}] Uploading: {filepath} ...")
        new_url = upload_file_to_imgbed(filepath)
        upload_map[filepath] = new_url
        print(f"  -> {new_url}")
        
        # Save map incrementally
        with open(MAP_FILE, "w", encoding="utf-8") as f:
            json.dump(upload_map, f, indent=2, ensure_ascii=False)
            
    # 2. Remote image URLs from ax1x.com in dynamic & gallery
    remote_urls = [
        "https://s41.ax1x.com/2026/05/13/peXsfit.webp",
        "https://s41.ax1x.com/2026/05/13/peXs2dA.webp",
        "https://s41.ax1x.com/2026/05/13/peXshJP.webp",
        "https://s41.ax1x.com/2026/05/13/peXsRII.webp",
        "https://s41.ax1x.com/2026/05/13/peXyWm4.jpg",
        "https://s41.ax1x.com/2026/05/13/peXyf0J.jpg",
        "https://s41.ax1x.com/2026/05/13/peXyh79.jpg"
    ]
    
    print(f"\nProcessing {len(remote_urls)} remote image URLs...")
    for idx, r_url in enumerate(remote_urls):
        if r_url in upload_map:
            print(f"[{idx+1}/{len(remote_urls)}] Already uploaded: {r_url} -> {upload_map[r_url]}")
            continue
        print(f"[{idx+1}/{len(remote_urls)}] Uploading remote URL: {r_url} ...")
        try:
            new_url = upload_url_to_imgbed(r_url)
            upload_map[r_url] = new_url
            print(f"  -> {new_url}")
            with open(MAP_FILE, "w", encoding="utf-8") as f:
                json.dump(upload_map, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"  Failed: {e}")

    print(f"\nAll uploads completed! Total mapped items: {len(upload_map)}")

if __name__ == "__main__":
    main()
