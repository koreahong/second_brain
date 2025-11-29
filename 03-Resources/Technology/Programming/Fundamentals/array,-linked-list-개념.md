---
title: array, linked list 개념
type: resource
tags:
- algorithm
- 자료구조
created: '2025-11-30'
updated: '2025-11-30'
aliases: []
---

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
![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/1015f006-5818-41f3-a45f-dc51ac449539/f3f26014-882e-4395-8cad-837668483d07/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4663NHQQVYX%2F20251129%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251129T015801Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIQDByPz6qtcqSeiuhp16RRFdK0MaFDGmXx5VUzaSKUAl4AIgHFmJemejRxBsANk%2B2lvcnRYXFb%2B0gyNvRR1RDmK3q%2FwqiAQIwv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDOsTQaZ1CIunP2MaByrcA%2BI5xGoXrqpSq5T%2BjP%2B6KhpGocGfZt0NE8b4mH%2BaSiZubrCxk3d7USkXmgRccg8%2BHHlQaV%2BkgPJam5%2FgHOjP%2BElX3%2FBhUM%2FTQ7Yn4t3fwAA66K%2FkAX%2FF0ZNeD3vQ00e%2BeYK1Qu9LVRML7a25SqxORlZpkKq%2FNAK8TcGNt5osjvMFqsWsHvUUoikkgaI%2FcDI1iUDJKtzts%2B%2FXMiq1xzmTF5Pv60xSRCm7I9fMFGcbxaesb4IakT6vc2k5f8rIXXkQrMkmq6RE9Tp2L0nyY3C4fi0rIP5hEL9bTKb1PGglqcClbfDr4N6oILGqRNB4xuV7zzzC1f53kqkxz%2BfxpHO86sey6OLKgXev1KeNxMzVL56CUVWxl%2FUs9SDnBXqAj0uMHX8zNHy1YhcxznDsOunhygwQQZLKc4xpOwU0ybKK9oMexGUSukWUiZMC%2BX4qoE7dkh5ut6jzid%2F9ftr5hVojYhLKOWXP%2FQ6B9lDzaandpeVE0Mx8qco392VW2%2FgDoYY5HKaCqrurpdUmgEUso87mehNbye7jOb%2BYjb40oR%2BDINN%2FMtf4P4h7j6Kjjf31gYLjRFgMXX1GXmCpjOnj0RuaXvj56Y8TtKzM2Jh5B8IBqRkwrzoUlNHn3WvUlbiKMPKIqckGOqUBfbfNEIsczJzoUB%2B66CKgiq2MJynVfdi8gKD2WMuC2%2BId4ZTEFTmvc0Zrv64LYyGB6%2BLS%2B6vUJdbDzCkyReUPOSyPNYL1dLD5nwSxc2bMPvVIk0ksAL0KWaTV0sK09OBk9x6xn7RWNVTU9cPX%2BzclKs5rdAM3gXjZpVCHx43xtAQDgzRdrK3mBoq91UhxhNMi3DNaPEkbWqflTLY1GE%2BNeVAIVdNT&X-Amz-Signature=f1b5cf17cef18f508022fa5a770419d92da08bbf0be93034861af7a34d9f9103&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

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

---

## 📎 Related

<!-- 자동 생성된 섹션 - 수동으로 링크를 추가하세요 -->

### Projects

### Knowledge

### Insights

