import os
import re
import json
from collections import defaultdict
from difflib import SequenceMatcher

vault_base = "/Users/qraft_hongjinyoung/Second-Brain"

print("=" * 100)
print("🔗 지능형 연결 제안 시스템")
print("=" * 100)

# Load previous analysis
with open('/tmp/connection_analysis.json', 'r', encoding='utf-8') as f:
    analysis = json.load(f)

# Re-scan for detailed analysis
all_notes = {}
for root, dirs, files in os.walk(vault_base):
    if 'automation' in root or '/.git' in root:
        continue
    
    for file in files:
        if not file.endswith('.md'):
            continue
        
        full_path = os.path.join(root, file)
        rel_path = full_path.replace(vault_base + '/', '')
        note_name = file.replace('.md', '')
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract metadata
        title_match = re.search(r'^title:\s*(.+)$', content, re.MULTILINE)
        title = title_match.group(1).strip('"\'') if title_match else note_name
        
        type_match = re.search(r'^type:\s*(\S+)', content, re.MULTILINE)
        doc_type = type_match.group(1) if type_match else 'unknown'
        
        tags_match = re.search(r'tags:\s*\[(.*?)\]', content, re.DOTALL)
        if not tags_match:
            tags_match = re.search(r'tags:\n((?:  - .*\n)*)', content)
        tags = []
        if tags_match:
            tags_str = tags_match.group(1)
            tags = [t.strip().strip('"').replace('  - ', '') for t in re.findall(r'["\']?([^,"\'\n]+)["\']?', tags_str) if t.strip()]
        
        # Extract keywords from content (simple approach)
        content_lower = content.lower()
        keywords = set()
        
        # Common tech terms
        tech_terms = ['airflow', 'dbt', 'snowflake', 'datahub', 'keycloak', 'gitlab', 
                      'postgres', 'python', 'sql', 'docker', 'kubernetes', 'aws']
        for term in tech_terms:
            if term in content_lower:
                keywords.add(term)
        
        all_notes[note_name] = {
            'path': rel_path,
            'full_path': full_path,
            'title': title,
            'type': doc_type,
            'tags': set(tags),
            'keywords': keywords,
            'content': content
        }

# Suggestion algorithm
suggestions = defaultdict(list)

# 1. Tag-based suggestions
print("\n🏷️  태그 기반 연결 제안")
print("-" * 100)

orphan_paths = set(analysis['orphans'])
orphan_notes = {n: info for n, info in all_notes.items() if info['path'] in orphan_paths}

tag_matches = 0
for orphan_name, orphan_info in list(orphan_notes.items())[:10]:  # Sample first 10
    print(f"\n📄 {orphan_name}")
    print(f"   Type: {orphan_info['type']} | Tags: {', '.join(orphan_info['tags']) if orphan_info['tags'] else 'None'}")
    
    # Find notes with overlapping tags
    candidates = []
    for note_name, note_info in all_notes.items():
        if note_name == orphan_name:
            continue
        
        common_tags = orphan_info['tags'] & note_info['tags']
        if common_tags:
            candidates.append((note_name, len(common_tags), list(common_tags)))
    
    if candidates:
        candidates.sort(key=lambda x: x[1], reverse=True)
        print(f"   💡 제안 연결:")
        for cand_name, num_common, common_tags in candidates[:3]:
            cand_info = all_notes[cand_name]
            print(f"      → {cand_name} ({cand_info['type']}) - 공통 태그: {', '.join(common_tags)}")
            suggestions[orphan_name].append({
                'target': cand_name,
                'reason': f'공통 태그: {", ".join(common_tags)}',
                'confidence': 'high' if num_common >= 2 else 'medium'
            })
            tag_matches += 1

print(f"\n태그 기반 매칭: {tag_matches}건")

# 2. Keyword-based suggestions
print(f"\n\n🔤 키워드 기반 연결 제안")
print("-" * 100)

keyword_matches = 0
for orphan_name, orphan_info in list(orphan_notes.items())[10:20]:  # Next 10
    if not orphan_info['keywords']:
        continue
    
    print(f"\n📄 {orphan_name}")
    print(f"   Keywords: {', '.join(orphan_info['keywords'])}")
    
    candidates = []
    for note_name, note_info in all_notes.items():
        if note_name == orphan_name:
            continue
        
        common_keywords = orphan_info['keywords'] & note_info['keywords']
        if common_keywords:
            candidates.append((note_name, len(common_keywords), list(common_keywords)))
    
    if candidates:
        candidates.sort(key=lambda x: x[1], reverse=True)
        print(f"   💡 제안 연결:")
        for cand_name, num_common, common_keywords in candidates[:2]:
            cand_info = all_notes[cand_name]
            print(f"      → {cand_name} ({cand_info['type']}) - 키워드: {', '.join(common_keywords)}")
            suggestions[orphan_name].append({
                'target': cand_name,
                'reason': f'공통 키워드: {", ".join(common_keywords)}',
                'confidence': 'medium'
            })
            keyword_matches += 1

print(f"\n키워드 기반 매칭: {keyword_matches}건")

# 3. Type-based suggestions (Experience ↔ Project ↔ Knowledge)
print(f"\n\n🔺 타입 기반 연결 제안 (Experience ↔ Project ↔ Knowledge)")
print("-" * 100)

# Weekly reflections should link to projects from the same time period
weekly_notes = {n: info for n, info in all_notes.items() if info['type'] == 'weekly-reflection'}
project_notes = {n: info for n, info in all_notes.items() if info['type'] == 'project'}

type_matches = 0
for weekly_name, weekly_info in list(weekly_notes.items())[:5]:
    # Extract date from title (e.g., "2025년 11월 24일")
    date_match = re.search(r'(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일', weekly_info['title'])
    if not date_match:
        continue
    
    year, month, day = date_match.groups()
    week_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    
    print(f"\n📅 {weekly_name} ({week_date})")
    
    # Find projects from similar time period
    candidates = []
    for proj_name, proj_info in project_notes.items():
        # Extract date from project
        proj_date_match = re.search(r'date:\s*["\']?(\d{4}-\d{2}-\d{2})', proj_info['content'])
        if proj_date_match:
            proj_date = proj_date_match.group(1)
            # Same month?
            if proj_date[:7] == week_date[:7]:
                candidates.append((proj_name, proj_date))
    
    if candidates:
        print(f"   💡 같은 시기 프로젝트:")
        for proj_name, proj_date in candidates[:3]:
            print(f"      → {proj_name} ({proj_date})")
            suggestions[weekly_name].append({
                'target': proj_name,
                'reason': f'같은 시기 ({proj_date})',
                'confidence': 'high'
            })
            type_matches += 1

print(f"\n타입 기반 매칭: {type_matches}건")

# Save suggestions
output = {
    'total_suggestions': sum(len(v) for v in suggestions.values()),
    'notes_with_suggestions': len(suggestions),
    'suggestions': {k: v for k, v in suggestions.items()}
}

with open('/tmp/connection_suggestions.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\n\n" + "=" * 100)
print(f"📊 제안 요약")
print("=" * 100)
print(f"전체 제안 수: {output['total_suggestions']}개")
print(f"제안 받은 노트: {output['notes_with_suggestions']}개")
print(f"\n상세 제안이 /tmp/connection_suggestions.json에 저장되었습니다.")

