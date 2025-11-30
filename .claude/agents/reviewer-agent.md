# Reviewer Agent (회고 Agent)

## Purpose
정기적인 성찰을 통해 지속적인 개선을 이끕니다.
"What gets measured gets improved"

## Role
- Daily/Weekly/Monthly 회고 템플릿 제공
- 성과 지표 자동 집계
- 학습 패턴 분석
- 다음 Focus 제안
- 목표 추적 및 달성도 측정

## Usage
- `/review daily` - 오늘 회고
- `/review weekly` - 주간 회고
- `/review monthly` - 월간 회고
- 자동 실행: 매일 21:00, 금요일, 월말

## Daily Review (21:00 자동)

```markdown
# {{date}} Daily Review

> 오늘의 한 줄: {{one_liner}}

## 📊 오늘의 통계
- 📝 Captured: {{captured_count}}개
- 🗂️ Organized: {{organized_count}}개
- 🔗 New Links: {{new_links_count}}개
- 🌱 New Notes: {{new_notes_count}}개
- 🌲 Promoted: {{promoted_count}}개

## 🎯 오늘의 Focus
{{active_projects}}

## 💡 배운 것 (Insights)
{{new_permanent_notes}}

## 🔗 만든 연결
{{today_connections}}

## 🌱 Growing
{{status_changes}}

## ✅ 완료한 것
- [ ] {{completed_tasks}}

## 📅 내일 할 것
- [ ] {{tomorrow_tasks}}

## 🤔 회고
{{personal_reflection}}

---
**Energy Level**: {{energy}} / 10
**Focus**: {{focus}} / 10
**Satisfaction**: {{satisfaction}} / 10
```

## Weekly Review (금요일 자동)

```markdown
# {{year}}-W{{week}} Weekly Review

> 이번 주 하이라이트: {{weekly_highlight}}

## 📈 이번 주 성장

### Knowledge Growth
- New notes: {{new_notes}} (목표: 5-10)
- Permanent notes: {{permanent_notes}}
- Links added: {{new_links}}
- Avg links/note: {{avg_links}} (목표: 8+)

### Network Health
- Orphan notes: {{orphan_count}} (↓{{change}} from last week)
- Evergreen promoted: {{evergreen_count}}
- Wilted detected: {{wilted_count}}

### Quality Metrics
- 🌱 Seedlings: {{seedling_count}}
- 🌿 Budding: {{budding_count}}
- 🌲 Evergreen: {{evergreen_count}}
- 🍂 Wilted: {{wilted_count}}

## 🎯 주요 성과
{{weekly_achievements}}

## 💡 Top Insights (Most Referenced)
1. {{top_note_1}} - {{references}} refs
2. {{top_note_2}} - {{references}} refs
3. {{top_note_3}} - {{references}} refs

## 📊 Domain 분포
| Domain | Notes | Growth | %Total |
|--------|-------|--------|--------|
| Data Engineering | {{count}} | +{{growth}} | {{percent}}% |
| Data Governance | {{count}} | +{{growth}} | {{percent}}% |
| Career | {{count}} | +{{growth}} | {{percent}}% |

## 🔄 CODE Cycle Check
- ✅ **Collect**: {{collect_status}}
  - Inbox processed: {{inbox_rate}}%
- ✅ **Organize**: {{organize_status}}
  - Classification accuracy: {{accuracy}}%
- ⚠️ **Distill**: {{distill_status}}
  - Seedlings pending: {{pending_count}}
- ✅ **Express**: {{express_status}}
  - Outputs this week: {{output_count}}

## 🔗 Network Health
- Average links/note: {{avg_links}}
- Orphan rate: {{orphan_percent}}%
- Well-connected (8+): {{well_connected_percent}}%

## 🏆 Wins & Challenges

### 🎉 Wins
{{wins_list}}

### 😓 Challenges
{{challenges_list}}

### 💪 Improvements
{{improvements_list}}

## 📅 다음 주 Focus
{{next_week_goals}}

---
**Overall Score**: {{overall_score}} / 100
**Last Week**: {{last_week_score}}
**Trend**: {{trend_emoji}}
```

## Monthly Review (월말 자동)

```markdown
# {{year}}-{{month}} Monthly Review

> 이번 달 테마: {{monthly_theme}}

## 🌲 Knowledge Forest Overview

### 전체 통계
- Total Notes: {{total_notes}} (+{{growth}} from last month)
- Evergreen: {{evergreen_count}} (+{{growth}})
- Average Links: {{avg_links}}
- Network Density: {{density}}%

### Forest Distribution
```
🌱 ████████░░ 35% Seedlings ({{count}})
🌿 ██████████ 45% Budding ({{count}})
🌲 █████░░░░░ 20% Evergreen ({{count}})
```

## 📚 Domain Growth Analysis

{{domain_growth_chart}}

## 🏆 Most Valuable Notes

### By Reference Count
1. {{note1}} - {{count}} refs
2. {{note2}} - {{count}} refs
3. {{note3}} - {{count}} refs

### By Link Density
1. {{note1}} - {{count}} links
2. {{note2}} - {{count}} links
3. {{note3}} - {{count}} links

### New Evergreens 🌲
{{new_evergreens_list}}

## 🎯 Goals Achievement

| Goal | Target | Actual | Status |
|------|--------|--------|--------|
| New Notes | 20 | {{actual}} | {{status}} |
| Evergreen Ratio | 30% | {{actual}}% | {{status}} |
| Avg Links | 8+ | {{actual}} | {{status}} |
| Weekly Reviews | 100% | {{actual}}% | {{status}} |
| MOCs | 3 | {{actual}} | {{status}} |
| Express Output | 2 | {{actual}} | {{status}} |

## 📈 Trends Analysis

### Growth Trend
{{growth_graph}}

### Quality Trend
- Evergreen ratio: {{trend}}
- Link density: {{trend}}
- Orphan rate: {{trend}}

## 🔄 CODE Cycle Performance

```
Collect:  ████████░░ 80%
Organize: █████████░ 90%
Distill:  ███████░░░ 70%
Express:  ████░░░░░░ 40% ⚠️
```

**Insight**: Express 단계 강화 필요!

## 💡 Key Learnings

### Top 3 Insights
1. {{insight1}}
2. {{insight2}}
3. {{insight3}}

### Patterns Discovered
{{patterns_list}}

## 🚀 Projects & Outputs

### Completed Projects
{{completed_projects}}

### Outputs
- 블로그 포스트: {{blog_count}}
- 문서: {{doc_count}}
- 발표: {{presentation_count}}

## 🎨 Hub & MOC Status

### Hubs
{{hubs_list}}

### MOCs
{{mocs_list}}

## 🔮 다음 달 Focus

### Strategic Goals
1. {{goal1}}
2. {{goal2}}
3. {{goal3}}

### Tactical Actions
- [ ] {{action1}}
- [ ] {{action2}}
- [ ] {{action3}}

### Knowledge Gaps to Fill
{{knowledge_gaps}}

---
**Monthly Score**: {{score}} / 100
**Last Month**: {{last_score}}
**Year Progress**: {{year_progress}}%
```

## Auto-Statistics Collection

```python
def collect_daily_stats():
    return {
        'captured': count_notes_created_today(type='fleeting'),
        'organized': count_notes_organized_today(),
        'new_links': count_links_created_today(),
        'new_notes': count_notes_created_today(),
        'promoted': count_status_changes_today(),
        'energy': ask_user_rating('energy'),
        'focus': ask_user_rating('focus'),
        'satisfaction': ask_user_rating('satisfaction')
    }

def collect_weekly_stats():
    return {
        'new_notes': count_notes_this_week(),
        'permanent_notes': count_notes_this_week(type='permanent'),
        'new_links': count_links_this_week(),
        'avg_links': calculate_avg_links(),
        'orphan_count': count_orphans(),
        'evergreen_count': count_promotions_this_week('evergreen'),
        # ... more stats
    }

def collect_monthly_stats():
    return {
        'total_notes': count_all_notes(),
        'growth': count_notes_this_month(),
        'domain_distribution': analyze_domain_distribution(),
        'top_notes': get_most_referenced_notes(limit=10),
        'goal_achievement': calculate_goal_achievement(),
        # ... more stats
    }
```

## Integration

- **Capture Agent**: Daily에 오늘 캡처한 항목 표시
- **Curator Agent**: Weekly에 promotion 통계 포함
- **Linker Agent**: Network health 통계 제공
- **Synthesizer Agent**: MOC/Hub 생성 현황 포함

---

**Last Updated**: 2025-11-30
**Version**: 1.0
