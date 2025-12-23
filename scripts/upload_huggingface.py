#!/usr/bin/env python3
"""
Upload dataset to HuggingFace Hub.

Prerequisites:
    pip install huggingface_hub
    huggingface-cli login

Usage:
    ./venv/bin/python scripts/upload_huggingface.py

Or manually:
    huggingface-cli upload ldiaby/idf-footballers data/huggingface --repo-type dataset
"""

import sys
from pathlib import Path

try:
    from huggingface_hub import HfApi, login
except ImportError:
    print("Error: huggingface_hub not installed")
    print("Run: pip install huggingface_hub")
    sys.exit(1)


def main():
    # Config
    repo_id = "ldiaby/idf-footballers"
    data_dir = Path(__file__).parent.parent / "data" / "huggingface"

    print("=" * 60)
    print("Upload to HuggingFace Hub")
    print("=" * 60)

    # Check data exists
    if not data_dir.exists():
        print(f"Error: Data directory not found: {data_dir}")
        sys.exit(1)

    files = list(data_dir.glob("*"))
    print(f"\nFiles to upload from {data_dir}:")
    for f in files:
        print(f"  - {f.name}")

    # Login check
    print("\n1. Checking authentication...")
    try:
        api = HfApi()
        user = api.whoami()
        print(f"   Logged in as: {user['name']}")
    except Exception as e:
        print(f"   Not logged in. Run: huggingface-cli login")
        sys.exit(1)

    # Create repo if needed
    print(f"\n2. Creating/checking repo: {repo_id}")
    try:
        api.create_repo(repo_id, repo_type="dataset", exist_ok=True)
        print("   Repo ready")
    except Exception as e:
        print(f"   Error: {e}")
        sys.exit(1)

    # Upload files
    print(f"\n3. Uploading files...")
    try:
        api.upload_folder(
            folder_path=str(data_dir),
            repo_id=repo_id,
            repo_type="dataset",
        )
        print("   Upload complete!")
    except Exception as e:
        print(f"   Error: {e}")
        sys.exit(1)

    print("\n" + "=" * 60)
    print(f"Dataset available at: https://huggingface.co/datasets/{repo_id}")
    print("=" * 60)


if __name__ == "__main__":
    main()
