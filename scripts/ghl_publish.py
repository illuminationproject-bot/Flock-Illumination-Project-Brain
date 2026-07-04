#!/usr/bin/env python3
"""Publish/schedule social posts through the GoHighLevel API.

Usage:
  python3 scripts/ghl_publish.py --check
      Verify the token works and list connected social accounts.

  python3 scripts/ghl_publish.py --queue 01-calendar/publish-queue.csv [--dry-run]
      Schedule every row in the queue CSV. With --dry-run, validate and
      print what would be scheduled without calling the write endpoints.

Environment:
  GHL_PI_TOKEN      Private Integration token (pit-...)
  GHL_LOCATION_ID   Sub-account location id

Queue CSV columns:
  schedule_at   ISO local datetime, e.g. 2026-07-10T11:00
  brand         IP | Flock
  platforms     pipe-separated account labels matched against --check output,
                e.g. "instagram:illuminationproject|youtube:illuminationproject"
  post_type     post | reel | short | story
  caption       full caption / title text ("" allowed for visual-only stories)
  media_path    local path or Drive-downloaded path of the media file
  first_comment optional pinned first comment (hashtags)
"""

import argparse
import csv
import json
import mimetypes
import os
import sys
import urllib.request

API_BASE = "https://services.leadconnectorhq.com"
API_VERSION = "2021-07-28"


def env(name: str) -> str:
    val = os.environ.get(name, "").strip()
    if not val:
        sys.exit(f"Missing environment variable {name}. "
                 "See 06-pipeline/ghl-api-publishing.md for setup.")
    return val


def request(method: str, path: str, body=None, content_type="application/json"):
    url = f"{API_BASE}{path}"
    data = None
    headers = {
        "Authorization": f"Bearer {env('GHL_PI_TOKEN')}",
        "Version": API_VERSION,
        "Accept": "application/json",
    }
    if body is not None:
        if content_type == "application/json":
            data = json.dumps(body).encode()
        else:
            data = body
        headers["Content-Type"] = content_type
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")
        raise RuntimeError(f"{method} {path} -> HTTP {e.code}: {detail}") from e


def list_accounts():
    loc = env("GHL_LOCATION_ID")
    return request("GET", f"/social-media-posting/{loc}/accounts")


def upload_media(path: str) -> str:
    """Upload a file to the GHL media library, return its hosted URL."""
    loc = env("GHL_LOCATION_ID")
    boundary = "----ghlpublish"
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    with open(path, "rb") as f:
        file_bytes = f.read()
    name = os.path.basename(path)
    parts = []
    for field, value in (("hosted", "true"), ("name", name)):
        parts.append(f"--{boundary}\r\nContent-Disposition: form-data; "
                     f"name=\"{field}\"\r\n\r\n{value}\r\n".encode())
    parts.append(f"--{boundary}\r\nContent-Disposition: form-data; "
                 f"name=\"file\"; filename=\"{name}\"\r\n"
                 f"Content-Type: {mime}\r\n\r\n".encode())
    body = b"".join(parts) + file_bytes + f"\r\n--{boundary}--\r\n".encode()
    resp = request("POST", f"/medias/upload-file?locationId={loc}", body,
                   content_type=f"multipart/form-data; boundary={boundary}")
    url = resp.get("url") or resp.get("fileUrl") or (resp.get("data") or {}).get("url")
    if not url:
        raise RuntimeError(f"Media upload response had no URL: {resp}")
    return url


def create_post(account_ids, caption, media_url, schedule_at, post_type):
    loc = env("GHL_LOCATION_ID")
    body = {
        "accountIds": account_ids,
        "summary": caption,
        "media": [{"url": media_url}],
        "status": "scheduled",
        "scheduleDate": schedule_at,
        "type": post_type,
    }
    return request("POST", f"/social-media-posting/{loc}/posts", body)


def resolve_accounts(accounts_resp, platform_labels):
    """Map 'platform:name-fragment' labels to GHL account ids."""
    accounts = (accounts_resp.get("results") or accounts_resp.get("accounts")
                or accounts_resp.get("data") or [])
    ids = []
    for label in platform_labels:
        platform, _, fragment = label.partition(":")
        match = None
        for acct in accounts:
            blob = json.dumps(acct).lower()
            if platform.lower() in blob and fragment.lower().replace(" ", "") in blob.replace(" ", ""):
                match = acct
                break
        if not match:
            raise RuntimeError(f"No connected account matches '{label}'. "
                               "Run --check to see available accounts.")
        ids.append(match.get("id") or match.get("_id") or match.get("accountId"))
    return ids


def run_queue(queue_path: str, dry_run: bool):
    accounts_resp = None if dry_run else list_accounts()
    scheduled, failed = [], []
    with open(queue_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            label = f"{row['schedule_at']} {row['brand']} {row['post_type']} -> {row['platforms']}"
            try:
                if dry_run:
                    if not os.path.exists(row["media_path"]):
                        raise RuntimeError(f"media file not found: {row['media_path']}")
                    print(f"[dry-run] OK  {label}")
                    scheduled.append(label)
                    continue
                account_ids = resolve_accounts(accounts_resp, row["platforms"].split("|"))
                media_url = upload_media(row["media_path"])
                create_post(account_ids, row["caption"], media_url,
                            row["schedule_at"], row["post_type"])
                print(f"scheduled  {label}")
                scheduled.append(label)
            except Exception as exc:
                print(f"FAILED     {label}\n           {exc}", file=sys.stderr)
                failed.append((label, str(exc)))
    print(f"\n{len(scheduled)} scheduled, {len(failed)} failed.")
    return 1 if failed else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--queue")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if args.check:
        resp = list_accounts()
        print(json.dumps(resp, indent=2))
        return 0
    if args.queue:
        return run_queue(args.queue, args.dry_run)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
