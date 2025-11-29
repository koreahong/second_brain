---
title: DW, DM
type: resource
tags:
- db
created: '2025-11-30'
updated: '2025-11-30'
aliases: []
---

# 레퍼런스

# 개념정리

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/1015f006-5818-41f3-a45f-dc51ac449539/6badaed0-029d-4d93-aff2-c8076958573d/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466YI7BUYP3%2F20251129%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251129T021230Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIQC%2FbLtPfDXcx%2FKsdyIJnYcUy8lllnL3SogL3wE82HgsGwIgChEz53DuHzfiAI8FQzJmo3twNIfXvP60xrSEV4IPYBQqiAQIwv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDOfIuHB4mlA6Did6WircA8E0cgs97yrsM%2FnANiabC1EuQDEiNCdJ823i0yNapUWerqXpfyUE71Z4uflUZWH2DAAFI6PCkj3L%2FaCf%2BAcM1NIJ7mZ5EgfDZJyRMTYYymdjXIxtBbj05TMyfO91ZWH6ngY8T0cUalEw5rl4SVA4A%2FYxuypAJeO0pr9XkJ2%2FzH2tP73WqkrDwDlGwfW84a%2B9qlvce6J4ZLdwPRzrfiS2GWygOYHaA9lmr5%2BOs2m72OKjWhIa5fMVrIuAvYAv3le%2BbLQ%2FvNlkcEDi9eut8Rc1L9HZwfrsRjisWAmSGcWaQNgdZ67IqedvWQ3UDPYBH7Go%2Bn6UeelgudaNf%2FO3pZBWyvPPYFcF%2FE5pSkwnc6egHM3KDP7qVrx0Qvz3LhqGqGlBbQ%2BU7EFzJ2pBf7HZUmu%2BOyp693DA1hFuAmQq3%2FdUrqRznKj9YVh%2BbN8%2FY8%2F5N8W%2B9oCNJ4ijx2ghFtBJb9sYz46qPoU7OGZStOSCohnCG7dDTNh49zaEZZ1SO5KvTWoDJpe4w%2BL0%2Fq31mWwH5TufFLP%2BlyvjtZ4kHt%2B2dVNtUA%2FIvT8VquwSEdJHBP8zDxWDzO%2FCkBY0veuEwM5zyB9oqyIXV0sOARkJNPs3GKc2AhfkDjYS9HP8o2pfqZXlMN%2F8qMkGOqUB0NqHQEjgJTNV57oZPwNstGtWtxNLaZMsZrbpUMf0t2OKH7Nh2KOwQIZvT9m2ZEeM9jhZbYq8rIupy3omOYXmT5L0w%2FIuWjr80KX4xJCKzjEGl%2BY1IsAjwYyGycwg3ubuCr1iDazLcOzTxI%2FvKzADZtYynPfZ5XTYkU7Rtmf%2ByOzptgBThCPs6n9szT0VHwHwNuFERpaAaJ1TsgaESPw4qzgv%2FcoO&X-Amz-Signature=3e0f5a30365e22efca52b6104c6181752cc5b772b3caf9985a51d26a2b396662&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/1015f006-5818-41f3-a45f-dc51ac449539/1f0e99c4-7c50-4153-bb9a-5432ec07ada1/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466YI7BUYP3%2F20251129%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251129T021230Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIQC%2FbLtPfDXcx%2FKsdyIJnYcUy8lllnL3SogL3wE82HgsGwIgChEz53DuHzfiAI8FQzJmo3twNIfXvP60xrSEV4IPYBQqiAQIwv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDOfIuHB4mlA6Did6WircA8E0cgs97yrsM%2FnANiabC1EuQDEiNCdJ823i0yNapUWerqXpfyUE71Z4uflUZWH2DAAFI6PCkj3L%2FaCf%2BAcM1NIJ7mZ5EgfDZJyRMTYYymdjXIxtBbj05TMyfO91ZWH6ngY8T0cUalEw5rl4SVA4A%2FYxuypAJeO0pr9XkJ2%2FzH2tP73WqkrDwDlGwfW84a%2B9qlvce6J4ZLdwPRzrfiS2GWygOYHaA9lmr5%2BOs2m72OKjWhIa5fMVrIuAvYAv3le%2BbLQ%2FvNlkcEDi9eut8Rc1L9HZwfrsRjisWAmSGcWaQNgdZ67IqedvWQ3UDPYBH7Go%2Bn6UeelgudaNf%2FO3pZBWyvPPYFcF%2FE5pSkwnc6egHM3KDP7qVrx0Qvz3LhqGqGlBbQ%2BU7EFzJ2pBf7HZUmu%2BOyp693DA1hFuAmQq3%2FdUrqRznKj9YVh%2BbN8%2FY8%2F5N8W%2B9oCNJ4ijx2ghFtBJb9sYz46qPoU7OGZStOSCohnCG7dDTNh49zaEZZ1SO5KvTWoDJpe4w%2BL0%2Fq31mWwH5TufFLP%2BlyvjtZ4kHt%2B2dVNtUA%2FIvT8VquwSEdJHBP8zDxWDzO%2FCkBY0veuEwM5zyB9oqyIXV0sOARkJNPs3GKc2AhfkDjYS9HP8o2pfqZXlMN%2F8qMkGOqUB0NqHQEjgJTNV57oZPwNstGtWtxNLaZMsZrbpUMf0t2OKH7Nh2KOwQIZvT9m2ZEeM9jhZbYq8rIupy3omOYXmT5L0w%2FIuWjr80KX4xJCKzjEGl%2BY1IsAjwYyGycwg3ubuCr1iDazLcOzTxI%2FvKzADZtYynPfZ5XTYkU7Rtmf%2ByOzptgBThCPs6n9szT0VHwHwNuFERpaAaJ1TsgaESPw4qzgv%2FcoO&X-Amz-Signature=2537a2139a5f26736e0fc6865b776a5d3788d9eed2cbd8a7ce8048283aa0515b&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

기억해야 하는 개념

- 데이터 마트는 데이터 웨어하우스보다 규모가 작고, 특정한 목적에 초점을 맞춘 데이터 모음을 제공
  - DW → DM, DM → DW 가능, 근데 나는 주로 DW → DM
요기요 빅쿼리 쿼리 최적화

브로드 캐스트 조인

---

## 📎 Related

<!-- 자동 생성된 섹션 - 수동으로 링크를 추가하세요 -->

### Projects

### Knowledge

### Insights

