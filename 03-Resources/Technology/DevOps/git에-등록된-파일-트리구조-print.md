---
title: "git에 등록된 파일 트리구조 print"
source: notion
notion_id: 161c6d43-3b4d-80c0-a7c6-ebf668f3bdba
imported: 2025-11-29
database: 레퍼런스
하위 항목: []
구상기록: []
구분: ["Directory"]
링크: []
최종편집시각: "2024-12-19T07:20:00.000Z"
제목: ""
상위 항목: []
tags: ["레퍼런스", "Directory", "notion-import"]
---

```bash
git ls-files | sort | tree -C --fromfile --noreport --charset ascii
```

