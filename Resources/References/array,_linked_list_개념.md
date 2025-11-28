---
title: array, linked list 개념
created: 2025-11-28
tags: ["reference", "migrated", "resource", "\uc54c\uace0\ub9ac\uc998", "\uc790\ub8cc\uad6c\uc870"]
PARA: Resource
구분: ["\uc54c\uace0\ub9ac\uc998", "\uc790\ub8cc\uad6c\uc870"]
---

# array, linked list 개념

## 📝 내용

## 개념

- array는 같은 공간 안에엇

## 목적

- 개념이 필요하게 된 배경을 작성할 것

## 서칭내용

# Array

### 개념

같은 자료형의 데이터를 연속된 메모리 공간에 나열한 자료구조입니다. 

- 정해진 크기: 책꽂이는 칸의 수가 정해져 있어서 책을 더 꽂으려면 다른 책꽂이를 가져와야 하는 것처럼, 어레이는 크기가 고정되어 있어요.

- 빠른 접근: "해리 포터 1권 줘" 하면 바로 꺼내줄 수 있듯이, 어레이의 특정 위치에 있는 데이터에 빠르게 접근할 수 있어요.

- 삽입/삭제의 어려움: 책 사이에 새 책을 넣으려면 공간을 만들기 위해 다른 책들을 옮겨야 하는 것처럼, 어레이 중간에 데이터를 삽입하거나 삭제하려면 다른 데이터를 이동시켜야 해서 번거로워요.

- 공간 추가의 비효율성: 책이 너무 많아서 책꽂이를 하나 더 사야 하는 것처럼, 어레이의 크기를 늘리려면 새로운 어레이를 만들고 기존의 데이터를 모두 옮겨야 해서 비효율적이에요.

### 구현

```python
my_list = [1, 2, 3, 4, 5]  # 정수형 리스트
my_list2 = ["apple", "banana", "cherry"]  # 문자열 리스트
my_list3 = [1, "apple", 3.14, True]  # 다양한 자료형 혼합linked list
```

### 개념

노드라고 불리는 데이터 요소들을 연결하여 만든 자료구조입니다.

- 유로운 크기: 화물 열차처럼, 링크드 리스트는 연결 고리만 있으면 얼마든지 칸을 늘리거나 줄일 수 있어요. 

- 느린 접근: 우편칸에 가려면 시멘트 칸, 자갈칸, 밀가루 칸을 지나가야 하는 것처럼, 링크드 리스트에서 특정 요소에 접근하려면 연결 고리(포인터)를 따라가야 해서 시간이 걸려요. 

- 유연한 삽입/삭제: 자갈칸과 밀가루칸 사이에 흑연칸을 넣거나 밀가루칸을 빼는 것처럼, 링크드 리스트는 연결 고리만 바꿔 주면 되기 때문에 요소를 중간에 넣거나 빼는 것이 쉬워요.

### 구현

```python
class Node:
    
    def __init__(self, data):

        self.data = data
        self.next = None

class linkedList:

    def __init__(self, data):

        self.head = Node(data)

    def append(self, data):

        cur = self.head

        while cur.next is not None:
            cur = cur.next

        cur.next = Node(data)

    def print_all(self):
        cur = self.head
        while cur is not None:
            print(cur.data)
            cur = cur.next

    def get_node(self, index):

        cur = self.head

        cur_index = 0
        while cur is not None:
            if cur_index == index:
                return cur
            else:
                cur = cur.next

    def add_node(self, index, value):

        new = Node(value)
        
        if index == 0:
            new.next = self.head.next
            self.head = new
            return

        prev = self.get_node(index - 1)

        new.next = prev.next
        prev.next = new

    def delete_node(self, index):

        if index == 0:
            self.head = self.head.next
            return

        prev = self.get_node(index - 1)
        prev.next = prev.next.next
```

## 🏷️ 분류

- **PARA**: Resource
- **구분**: 알고리즘, 자료구조

## 🔗 연결

**활용 프로젝트**:
- (아직 없음)

**관련 레퍼런스**:
- (아직 없음)

---

*Notion에서 재마이그레이션됨 (2025-11-28)*
