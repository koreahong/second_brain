import os
import re
from collections import defaultdict, Counter
import json

vault_base = "/Users/qraft_hongjinyoung/Second-Brain"

print("=" * 100)
print("🔗 세컨드 브레인 연결성 분석")
print("=" * 100)

# Data structures
all_notes = {}  # path -> {title, links, backlinks, tags, type}
wikilinks = defaultdict(set)  # source -> {targets}
backlinks = defaultdict(set)  # target -> {sources}
orphans = []
weak_connections = []
topic_clusters = defaultdict(set)

# Scan all notes
for root, dirs, files in os.walk(vault_base):
    # Skip automation and hidden directories
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
        
        # Extract wikilinks [[...]]
        links = set(re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content))
        
        # Store note info
        all_notes[note_name] = {
            'path': rel_path,
            'full_path': full_path,
            'title': title,
            'type': doc_type,
            'tags': tags,
            'links': links,
            'content_length': len(content)
        }
        
        # Build link graph
        for target in links:
            # Clean target (remove path if present)
            clean_target = target.split('/')[-1]
            wikilinks[note_name].add(clean_target)
            backlinks[clean_target].add(note_name)

# Calculate backlinks for each note
for note_name, note_info in all_notes.items():
    note_info['backlinks'] = backlinks.get(note_name, set())
    note_info['total_connections'] = len(note_info['links']) + len(note_info['backlinks'])

# Identify orphans and weak connections
for note_name, note_info in all_notes.items():
    total_conn = note_info['total_connections']
    
    if total_conn == 0:
        orphans.append(note_name)
    elif total_conn <= 2:
        weak_connections.append(note_name)

# Group by topic (using tags)
for note_name, note_info in all_notes.items():
    for tag in note_info['tags']:
        topic_clusters[tag].add(note_name)

# Print results
print(f"\n📊 전체 통계")
print("-" * 100)
print(f"전체 노트: {len(all_notes)}개")
print(f"전체 연결 (wikilinks): {sum(len(links) for links in wikilinks.values())}개")
print(f"평균 연결/노트: {sum(len(links) for links in wikilinks.values()) / len(all_notes):.1f}개")

print(f"\n⚠️  연결성 문제")
print("-" * 100)
print(f"Orphan 노트 (연결 0개): {len(orphans)}개")
print(f"Weak 연결 (1-2개): {len(weak_connections)}개")

if orphans:
    print(f"\n📌 Orphan 노트 샘플 (TOP 10):")
    for note in orphans[:10]:
        note_info = all_notes[note]
        print(f"  - {note} ({note_info['type']}) - {note_info['path']}")

# Experience-Knowledge-Project mapping analysis
print(f"\n\n🔺 Experience ↔ Knowledge ↔ Project 연결성")
print("-" * 100)

experience_notes = {n: info for n, info in all_notes.items() if info['type'] in ['weekly-reflection', 'experience', 'insight', 'reflection']}
knowledge_notes = {n: info for n, info in all_notes.items() if info['type'] in ['resource', 'technical', 'concept']}
project_notes = {n: info for n, info in all_notes.items() if info['type'] == 'project'}

print(f"Experience 노트: {len(experience_notes)}개")
print(f"Knowledge 노트: {len(knowledge_notes)}개")
print(f"Project 노트: {len(project_notes)}개")

# Check how many experiences link to knowledge
exp_to_knowledge = 0
exp_to_project = 0
for note_name, note_info in experience_notes.items():
    links_to_knowledge = any(target in knowledge_notes for target in note_info['links'])
    links_to_project = any(target in project_notes for target in note_info['links'])
    
    if links_to_knowledge:
        exp_to_knowledge += 1
    if links_to_project:
        exp_to_project += 1

print(f"\nExperience → Knowledge 연결: {exp_to_knowledge}/{len(experience_notes)} ({exp_to_knowledge/len(experience_notes)*100:.1f}%)")
print(f"Experience → Project 연결: {exp_to_project}/{len(experience_notes)} ({exp_to_project/len(experience_notes)*100:.1f}%)")

# Top connected notes
print(f"\n\n⭐ 가장 잘 연결된 노트 TOP 10")
print("-" * 100)
sorted_notes = sorted(all_notes.items(), key=lambda x: x[1]['total_connections'], reverse=True)
for i, (note_name, note_info) in enumerate(sorted_notes[:10], 1):
    print(f"{i:2}. {note_name:50} ({note_info['total_connections']}개 연결)")
    print(f"    Type: {note_info['type']:20} | Links: {len(note_info['links'])}개 | Backlinks: {len(note_info['backlinks'])}개")

# Save detailed data for further analysis
output_data = {
    'total_notes': len(all_notes),
    'orphans': [all_notes[n]['path'] for n in orphans],
    'weak_connections': [all_notes[n]['path'] for n in weak_connections],
    'top_connected': [(n, all_notes[n]['path'], all_notes[n]['total_connections']) for n, _ in sorted_notes[:20]],
    'stats': {
        'total_links': sum(len(links) for links in wikilinks.values()),
        'avg_links_per_note': sum(len(links) for links in wikilinks.values()) / len(all_notes),
        'experience_to_knowledge_rate': exp_to_knowledge / len(experience_notes) * 100 if experience_notes else 0,
        'experience_to_project_rate': exp_to_project / len(experience_notes) * 100 if experience_notes else 0,
    }
}

with open('/tmp/connection_analysis.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print(f"\n\n💾 상세 데이터가 /tmp/connection_analysis.json에 저장되었습니다.")

