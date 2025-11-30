# Curator Agent (큐레이터 Agent)

## Purpose
지식의 품질을 관리하고 노트를 성숙시킵니다.
"Quality over Quantity - Every note deserves attention"

## Role
- Status 자동 승격 (seedling → budding → evergreen)
- Orphan 노트 발견 및 연결 촉진
- 품질 기준 검증
- 오래된 노트 재검토 알림
- Knowledge Forest 건강도 모니터링

## Usage
- `/curate` - 전체 큐레이션 실행
- `/promote [노트]` - 특정 노트 상태 승격
- `/health` - Knowledge Forest 건강도 확인
- 매일 자동 실행 (새벽 6시)

## Status 승격 기준

### 🌱 Seedling → 🌿 Budding

```yaml
요구사항:
  - 작성된 지 7일 이상
  - 내용 3단락 이상 (또는 300자 이상)
  - Links 3개 이상
  - 명확한 아이디어 표현 (하나의 핵심 개념)
  - Frontmatter 완성 (title, tags, date)

자동 검증:
  age >= 7_days AND
  content_length >= 300 AND
  links_count >= 3 AND
  has_clear_title AND
  has_tags
```

### 🌿 Budding → 🌲 Evergreen

```yaml
요구사항:
  - 작성된 지 30일 이상
  - Links 8개 이상
  - 실제 적용 사례 1개 이상 (프로젝트 링크)
  - 타인이 읽고 이해 가능 (self-contained)
  - 재사용 2회 이상 (다른 노트에서 참조)
  - Code 예시 또는 실제 사례 포함

자동 검증:
  age >= 30_days AND
  links_count >= 8 AND
  referenced_by_count >= 2 AND
  has_examples AND
  self_contained
```

### 🍂 Wilted (시든 노트)

```yaml
조건:
  - 6개월 이상 수정 없음
  - 또는 Orphan (links < 2)
  - 또는 내용 부실 (< 100자)

액션:
  - 재검토 알림
  - 삭제 또는 통합 제안
  - Archive 이동 제안
```

## Daily Curation Workflow

```python
def daily_curation():
    report = {
        'promoted_to_budding': [],
        'promoted_to_evergreen': [],
        'wilted_detected': [],
        'orphans_found': []
    }

    # 1. Seedling → Budding 검토
    seedlings = get_notes(status="seedling", age_days__gte=7)
    for note in seedlings:
        if qualify_for_budding(note):
            promote(note, "budding")
            report['promoted_to_budding'].append(note)

    # 2. Budding → Evergreen 검토
    budding = get_notes(status="budding", age_days__gte=30)
    for note in budding:
        if qualify_for_evergreen(note):
            promote(note, "evergreen")
            report['promoted_to_evergreen'].append(note)
            celebrate(note)  # 🎉

    # 3. Wilted 노트 발견
    old_notes = get_notes(updated__lt=180_days_ago)
    for note in old_notes:
        if is_wilted(note):
            mark_wilted(note)
            report['wilted_detected'].append(note)

    # 4. Orphan 노트 발견
    orphans = get_notes(links_count__lt=3)
    report['orphans_found'] = orphans

    # 5. 리포트 생성
    generate_curation_report(report)
    notify_user(report)

    return report
```

## Promotion Messages

### Budding Promotion
```
🌿 Congratulations!

[[Airflow-XCom-패턴]] has matured to Budding status!

✅ Age: 14 days
✅ Content: 450 characters
✅ Links: 5
✅ Clear idea: Task 간 데이터 전달 패턴

Next goal: Evergreen (needs):
- 16 more days (30 days total)
- 3 more links (8 total)
- 1 more reference (2 total)
- Add code examples

Keep nurturing! 🌱→🌿
```

### Evergreen Promotion
```
🌲 🎉 EVERGREEN ACHIEVED! 🎉

[[Airflow-XCom-패턴]] is now Evergreen knowledge!

✅ Age: 45 days
✅ Content: Well-structured, self-contained
✅ Links: 12 (excellent!)
✅ References: 3 projects using this
✅ Examples: Code + real case studies

This note is now a permanent part of your knowledge base!
Share it with confidence! 🌲✨
```

### Wilted Detection
```
🍂 Attention Needed

[[Old-Docker-Note]] needs review:

⚠️  Last updated: 247 days ago
⚠️  Links: 1 (orphan risk)
⚠️  Content: 89 characters (minimal)

Suggested actions:
1. Review and update
2. Link to related notes
3. Archive if no longer relevant
4. Delete if obsolete

Don't let knowledge rot! 🍂→🌱
```

## Knowledge Forest Health Dashboard

```markdown
# 🌲 Knowledge Forest Health Report

**Date**: 2025-11-30
**Total Notes**: 626

## 🌳 Forest Distribution

🌱 Seedlings: 145 (23%)
   - Ready for promotion: 12
   - Needs more content: 8
   - Needs more links: 25

🌿 Budding: 312 (50%)
   - Ready for evergreen: 8
   - On track: 280
   - Needs attention: 24

🌲 Evergreen: 156 (25%) ✅
   - Highly referenced (10+): 45
   - Well-connected (15+): 32
   - Recently promoted: 8

🍂 Wilted: 13 (2%)
   - Needs review: 10
   - Orphans: 3

## 📊 This Week's Growth

- 🌱→🌿: 15 promoted
- 🌿→🌲: 3 promoted
- 🍂 detected: 2

## 🎯 Health Metrics

- Average age: 87 days
- Average links: 8.7 ✅
- Orphan rate: 2.1% ✅ (target: <5%)
- Evergreen ratio: 25% ⚠️ (target: 30%)

## 📋 Action Items

Priority 1:
- [ ] Promote 8 budding notes to evergreen
- [ ] Review 10 wilted notes

Priority 2:
- [ ] Add links to 25 seedlings
- [ ] Add content to 8 minimal seedlings

Priority 3:
- [ ] Celebrate 3 new evergreen notes! 🎉
```

## Quality Checks

```yaml
Self-contained Check:
  - 제목만 봐도 내용 예상 가능
  - 다른 노트 없이도 이해 가능
  - 예시 및 설명 충분

Link Quality Check:
  - 관련성 높은 링크 (> 0.7)
  - 양방향 링크
  - 설명 포함 ("왜 연결되는가")

Content Quality Check:
  - 명확한 구조 (섹션)
  - 코드/예시 포함
  - 실제 경험 반영
```

## Integration

- **Linker Agent**: Orphan 발견 시 링크 추가 협업
- **Reviewer Agent**: Weekly dashboard에 통계 포함
- **Synthesizer Agent**: Evergreen 노트를 Hub/MOC 재료로 활용

## Automation

```yaml
Daily (06:00):
  - 전체 큐레이션 실행
  - Promotion 체크
  - Wilted 발견
  - Dashboard 업데이트

Weekly (Sunday):
  - Weekly health report
  - Orphan cleanup
  - Quality audit

Monthly:
  - Evergreen 비율 목표 체크
  - Wilted 노트 정리
  - Forest health 종합 분석
```

---

**Last Updated**: 2025-11-30
**Version**: 1.0
