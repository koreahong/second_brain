#!/usr/bin/env python3
"""
Analyze all files in Resources/References to categorize them
"""
import os
from pathlib import Path
import re

def analyze_file(filepath):
    """Analyze a single markdown file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove YAML frontmatter
    content_no_yaml = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

    # Remove markdown headers and empty lines
    lines = [line.strip() for line in content_no_yaml.split('\n') if line.strip()]

    # Filter out common template text
    template_markers = [
        '📝 내용', '🏷️ 분류', '🔗 연결', 'PARA', '구분',
        'Hub:', '활용 프로젝트', '관련 레퍼런스', '(아직 없음)',
        'Notion에서 재마이그레이션됨', '---', '#'
    ]

    real_content_lines = [
        line for line in lines
        if not any(marker in line for marker in template_markers)
        and len(line) > 10  # Ignore very short lines
    ]

    # Calculate metrics
    total_chars = len(content_no_yaml.strip())
    real_content_chars = sum(len(line) for line in real_content_lines)
    num_real_lines = len(real_content_lines)

    return {
        'filename': filepath.name,
        'total_chars': total_chars,
        'real_content_chars': real_content_chars,
        'real_content_lines': num_real_lines,
        'has_substance': real_content_chars > 100 and num_real_lines > 3
    }

def main():
    refs_dir = Path('/Users/qraft_hongjinyoung/DAE-Second-Brain/Resources/References')

    files_analysis = []

    for filepath in sorted(refs_dir.glob('*.md')):
        if filepath.name.startswith('_HUB'):
            continue  # Skip hub files for now

        analysis = analyze_file(filepath)
        files_analysis.append(analysis)

    # Separate substantial from empty files
    substantial = [f for f in files_analysis if f['has_substance']]
    empty = [f for f in files_analysis if not f['has_substance']]

    print(f"📊 분석 결과")
    print(f"=" * 80)
    print(f"총 파일 수: {len(files_analysis)}")
    print(f"내용 있는 파일: {len(substantial)}")
    print(f"내용 부실한 파일: {len(empty)}")
    print()

    print(f"🗑️  삭제 후보 (내용 부실한 파일 {len(empty)}개)")
    print(f"=" * 80)
    for f in empty:
        print(f"  - {f['filename']:<60} (chars: {f['real_content_chars']}, lines: {f['real_content_lines']})")

    print()
    print(f"✅ 유지할 파일 ({len(substantial)}개)")
    print(f"=" * 80)
    for f in substantial[:10]:  # Show first 10
        print(f"  - {f['filename']:<60} (chars: {f['real_content_chars']}, lines: {f['real_content_lines']})")
    print(f"  ... and {len(substantial) - 10} more")

if __name__ == '__main__':
    main()
