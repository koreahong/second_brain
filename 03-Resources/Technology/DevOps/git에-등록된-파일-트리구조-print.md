---
title: git에 등록된 파일 트리구조 print
type: resource
tags:
- Directory
---

```bash
git ls-files | sort | tree -C --fromfile --noreport --charset ascii
```