---
title: filter, pivot_table, round 사용
created: 2025-11-28
tags: ["reference", "migrated", "resource", "pandas", "leetcode"]
PARA: Resource
구분: ["pandas", "leetcode"]
---

# filter, pivot_table, round 사용

## 📝 내용

## filter

filter는 특정 값을 기준으로 행렬 인덱싱을 하게 해주는 기능임

return 값은 dataframe임

```python
# groupby 단위로 인덱싱하는 경우
## paid가 하나라도 있는 user_id 추출
user_activity = user_activity.groupby('user_id').filter(lambda x: 'paid' in x['activity_type'].values)
## paid가 3개만 있는 user_id의 행 추출
user_activity = user_activity.groupby('user_id').filter(lambda x: (x['activity_type'] == 'paid').sum() == 3)  
```

## pivot_table

pivot_table은 sql에서 case when 역할을 할 수 있음

```python
user_activity = pd.pivot_table(user_activity, values = 'activity_duration', index = 'user_id', columns = 'activity_type').reset_index(
```

## round

round로 소숫점을 처리할 때, 부동소숫점으로 인해서 5같은 경우를 올림하지 않을 때가 있음.

그럴 경우 엄청 작은 수를 더하고 나서 round 처리를 해야함

```python
user_activity = user_activity.rename(columns = {'free_trial':'trial_avg_duration', 'paid':'paid_avg_duration'})
```

## between

sql과 동일하게 between 기능 사용가능

```python
trips.request_at.between("2013-10-01", "2013-10-03")
```

## agg

agg는 groupby를 활용하여 각 행에 원하는 집계를 진행할 수 있게 해주는 기능임

특히, agg 안에 딕셔너리 형태로 만든다음에 lambda함수를 사용할 수 있음

```python
result = (
    pre_trips
    .groupby('request_at', as_index=False)
    .agg({
        'is_cancelled': ["mean", lambda x: round(x.sum() / len(x), 2)]
    })
)
```

## size

size는 그룹별로 개수가 몇개인지 알고 싶을때 사용

- groupby().size() → 그 그룹에 몇 개의 행이 있는지 알고 싶을 때

- groupby()[column].count() → NaN 제외하고 특정 컬럼 값이 몇 개인지 알고 싶을 때

- .size() → 전체 셀 개수를 알고 싶을 때

```python
df = pd.DataFrame({
    "team": ["A", "A", "B", "B", "B"],
    "score": [1, None, 2, None, 3]
})

# size(): 그룹별 전체 행 수
print(df.groupby("team").size())
# 출력
# team
# A    2
# B    3

# count(): 그룹별 NaN 제외한 score 수
print(df.groupby("team")["score"].count())
# 출력
# team
# A    1
# B    2
```

## 🏷️ 분류

- **PARA**: Resource
- **구분**: pandas, leetcode

## 🔗 연결

**활용 프로젝트**:
- (아직 없음)

**관련 레퍼런스**:
- (아직 없음)

---

*Notion에서 재마이그레이션됨 (2025-11-28)*
