#!/usr/bin/env python3
"""
Knowledge Curator 실행 스크립트

빠른 실행:
  python automation/run_curator.py score
  python automation/run_curator.py curate --auto-update
  python automation/run_curator.py review --save
  python automation/run_curator.py links --orphans
"""

import sys
from pathlib import Path

# knowledge_curator 패키지 경로 추가
sys.path.insert(0, str(Path(__file__).parent))

from knowledge_curator.cli.main import main

if __name__ == '__main__':
    main()
