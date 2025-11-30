---
title: ACID 개념
type: resource
tags:
  - - data
  - - query
  - - technology
  - - study
  - - aws
  - database
  - acid
  - transaction
created: '2025-11-30'
updated: '2025-11-30'
aliases: []
status: seedling
maturity: 0
---

## 개념

- 개념에 대해서 한 줄로 작성하되, 반드시 내가 스스로 정리한 말로 작성할 것
## 목적

- DB 펀더멘털 공부
## 서칭내용

- 트랜잭션 개녕 ====
- A, Atomicity: 원자성, 같은 트랙잭션에 속한 쿼리들은 모두 성공하거나 실패해야 한다.
  - 실제 서비스 테이블에 새로운 데이터를 넣을 때, delete, update를 한 트랜잭션에 묶어서 한 개가 실패하면 나머지 쿼리도 롤백
- C, Consistency:  일관성, 데이터가 저장될 때는 기존의 데이터들의 조건에 맞게 저장되어야 한다
- I, Isolation: 고립성, 다른 트랜잭션에 영향을 끼치지 않게 함
  - 어느 단계에 있는 데이터를 읽느냐의 문제
    - dirty read, 수정중인 commit되지 않은 데이터를 읽음
  - MVCC 의 등장 ====
  - lost updates 발생 ==== 
    ![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/1015f006-5818-41f3-a45f-dc51ac449539/c2e22e94-8254-48e7-a4f6-e09fa9c1971c/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4663TUXRTLO%2F20251129%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251129T015754Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPX%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIQCiZucGsRt6cp0AxQTkjc72NM8kv5iq1koUwSIw4LNyvgIgGnp%2FOiRynTkNo%2BVZHFv4EANtQWEXmH7%2BHZ1N8qRJuA8qiAQIvv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDG9dGKsSaj1zza5EnircA3XDvm1B6Gqy52YWzgef4%2BG2p%2BLEb7kkgUR6grkXFWYP%2Bk3oyWqY1QZJ9PMz%2Fju6xbEmb7RAA7BPnsyCPGv33kj%2FWnGETT4X%2F3BChzaWz0YvYOwM7uT%2BbOeffMJm0GIh%2B0v8hPkApYFYtZ9TXWfqlNcSezrXZSgqMC5HxUjENb67a0aO6DL5lDGxlstUwAhgrYghsA39WfGQg%2FoXptubQs6yohtOqZJR%2Fh06vBGfOLl0Gycqvm0OcMJVrq2lJXq4hfxMDWH9F0R%2F9pcu%2F1fq2rWMh223%2FAh5V%2FBHM4%2FZSzi6Tjx%2F%2FJUJMnGyqkx2oCcXyshQs%2FETKD9zVitXVSoGbdIvmfuvrBVmdMmzpvatISSsZ6uhO5XsgkfYxIw0ETfgixKHlGDsiIKpkkWIE85tMfHEGxv8VQBNuFG5oqAUo5SWd%2FZRifiUBKOSD5U3rBpp0SFKrjX6JDJj2esBiUnBlzop0z4cpp%2FLqXQbgt%2B25koyLRVxegmtmYBTpyOIGYAqLT8OjYQ4eWRTiNGj%2B6RY%2FtaD8q4vNlM5gTaj5dd4a8GDvkm2H9lQp%2BUfooBNc01APwx2gNawcVHtaXut0yU6A4dLXh0MB%2Bf2YUzcCXP3fbkZX9XlW9ZVzBxjr%2FFjMMGWqMkGOqUBjJVZOJ%2Flbo%2Bf0a%2BduMcpH2rtAHtRPPO%2BUYWyTrfM2nacaxs%2Bq3noVEs1xDorik8COehk%2BCL%2BatEhkfmOIcXyrybzjzswDoc%2BXDyJ0QGAs5bVFGWR74GfH71XCgitCAwo0BwXTpujrHS%2BI0gJ20MhVF%2FkwKkqdiFOBtL2fpAfLFBOu%2BOTCww5n2NBmRcP%2BrilGXBb77qaP9%2FUyZwO9%2BCaef6vPvqP&X-Amz-Signature=c9995d23f087636d1682b5af3dd14c0c1827de8dfab5600447ac4cc03c5e084b&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

  - isolation 수준 결정
    ![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/1015f006-5818-41f3-a45f-dc51ac449539/114f2732-8e4c-41a8-a107-8240a3e84691/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4663QSBUEGY%2F20251129%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251129T015754Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJIMEYCIQCP6%2F7bIWEI3v293l%2F3z02GzhgsnUoWHdmUmpYNm%2BePLgIhANPrRSj9hxKpRuisXDMqYT9n8lT0D7w4ggQxg9GXn6F3KogECML%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1IgzO3zOyG0WFK665%2Ft4q3AOdDPppK8aUX7LVJltgeWBf%2BXIylmXlL7NpPiaPH6gboNcC5ga5TAeltnl4LwiVM6hFIoWt97i5%2B%2FHmJ%2FTJCTf66rQyC92bUH9d59Cwq1StcAb%2B%2FRX8GTXMW%2FiXC9tBX3R1RSdnjM%2BHRGCr9xsmi%2F8g3bLwAUjQkaXdlmuSbukbB6uf1hWB97nZsYofjbEnoO3kewV%2F7NS3fImJK6OuM5YKv9jgnwiCgvyzaZteMlTyGQr3TvaVfNidkzcnDQY6N0IUhpDsHijfW8%2BCQR%2BR12WmNjXliQt3UOKRMpTJV4BqtA7jKR4Q3IG3V%2By3BAfiyJmyXtNarvYozm5cIcyFTpR1mdUr9jFuL7Oh0OWMF4RgToBIkObDdq9MaT%2BtcYCFmz%2BqJF84o6zdg9RR506EBobRRcIZGZ7yOzC1zX1FM%2BCpI%2Bro9hJdDUq6aVyIlDmppoz0yiyOyki7VsPHwOcEaF7rvolWpVc34u173E0chYRPeWTRkHL%2Ft6RZRuGXWBtDalz7LO3kWeuxfZAdT9oFSWF7DT7LkvQaZ%2BpCTQ1JHtKRH9ga76sca5vq8nCrdCKp6H6VlhU95wh17Xor%2BglMDapipl2TPwHl0Q8UZmyyeWrt%2BLNjapFc%2Fq%2BPl9KzDTDj%2FajJBjqkASo%2FU8rECpzC6vbGXg1fSj%2FitOxjKHwCab2R78ikwjDEIr0qeUqgUipJZrTYTCWD1UjaXCiN2rMS3jbMp7OjlKmQr0cdM8Z%2Ba%2BW9bsG0i0xx919gX9WjAmAIRnfVrXa1aomNU78xhCOnKLsq6U4xv81n%2FekSWNqPylnUdthhLSnawO245Z9%2FHdM700E8zwekgG0g57PEITMdL4Lvj7YM2V3tkx8E&X-Amz-Signature=b1b8e494ffcb6fbfa3fa725ec416c6af224270a7bccbd6c89f6c4afc7f46f5cb&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

  - lock 수준 결정
    ![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/1015f006-5818-41f3-a45f-dc51ac449539/4d1276da-c9ac-4d5c-9ab4-231317744cdc/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466VB6LACAZ%2F20251129%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251129T015754Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJIMEYCIQDLmM0RvMVatL9tgMXDBuN29CQMqbKcTyKwsqk%2Fvh4vrwIhAPVWnFknRX7TcMPcc%2Bovrgzcurwz5Xqqj4Yx62ysMca%2FKogECML%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1IgwYitBnqXAc9Im1DGgq3ANWA9rF1qbiN8ok2oCp3TXllzsvV24Qaee6Rmj%2BV7Ee2sLJMs9eUoqaXfo9HMd%2BAcbKLMAET6p91ib8COPmrCVayoV50OOhD0m60CMJgSTMCUuQ10PiEJzbFDXoC%2FscoXmzLOW5WkZsaYGel5lvoh2ZjqRuKno9HYJR68NjO4M9L7NG73suRV7Bh42RdvVAsvmtQyTqA0XvtwRZIXmb6sjM%2BGr6MQ3Mf6NTCvr6U7QON078OZ%2BirFTwFX6dg53mDO%2BGdzJByFI%2FQSZmHHlZk4LxvmmT%2F0BgIaMkwoWhFhx80QMwwgTaisvyYv0YJCnDLWtWbF1%2F2L0JS%2BNDIx1bDZ0eDfsYonSD1zgONIr62Ii64a908qQNGOa7OaJ2HcBKzNWa4gdyAEpkjTd%2FCAVnH4wvckaJnI2teiFON1ePaPvCijnWlHBndpGtWhktN%2B4UoIzZX1CIRaL3j68gMvr4En%2FvL59ZUEAorrC401Lc%2FsQipo1lb603wE0ZW3xhaFaQwvpgul6BiQGtP15kfJ%2FSKVLt3VZqEwsP%2BWAxz4rEihYSAgKmEE%2Bh7LrGmXnRaZeyHQAuX3%2FeyeqxaO%2B8kYeKSW2vMO%2FwPdS22iD5xn4I%2FGNpMLK%2BnYuW4ONMklTwyjD3ianJBjqkAahwhCJlcSPehS%2BPWU7LybEqy%2FIOyN%2FUFmffDZwQb92V0RuHwX%2FsyO31cHDJPOfeopPTWP0kRib32EVZdjB0X4rNcmeIFflv0sKUDj47xBuGp1X%2ByyhshQ5NIyadjzAAgYX0phhqlBjIgd%2B0cZBfa7y1TaUvAqW4hQoSHyB1KnqDHE3%2BAgRXbVCKFIgd5ikz2b6dBvijsqT6Pkg2wkpZossmPswt&X-Amz-Signature=0d0a8ec5e0a7e02a90c468a6a674a455735f65eadd82457216c840bdf7827b47&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

- D, Durability, 지속성, 커밋을 하고 나서는 무슨 일이 있더라도 데이터가 그대로 저장되어 있어야 함.
  ![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/1015f006-5818-41f3-a45f-dc51ac449539/49898d03-6d6b-4886-a271-72b1a37f0c72/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466QC3XWUFF%2F20251129%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251129T015755Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPX%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIQCDsrQ6dBfiTa3I9Iw9mImfZCX%2FRVjP2%2B76t5S184gKxQIgYm2wVDK30xccbPFOo5Hvrh9OeUQntii6HdBPq0XFAX0qiAQIvv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDMAuj4%2FVag%2BydS6A8yrcA2emLjt%2F47Mro92Y63XbMscFvHddBIgfT2m5DaEHW13CJB99MkguOS9A0HeDwoSOFjQ4%2BiHRIkfIMlY84Mk4RMqaz8HamILV0LQlToXR2aMe3lkhE1WWxsyAWVrKYzhuZ4joC6SBWZpsJNgettsGjZVfGpTW7AAPMjGV4vWaa3oBQt7y0HEZVaPko1Kw9Otc33mHN7h3G%2BXyYeq7HBwhp2kObW%2F7VcCWc%2FV7ThzpJKFbevqc%2Fj0fXvnT%2B%2BFAjEyKPl%2Bati5o680ZBwD5Pnx9hxKY0IH%2BLlbH5zPQU3pU9vS8ZI%2FUKbryyb4HorY5cFTuq7Ip5NL2O5WDcS1pxHVm%2FxCUPiz%2F5JmfKAh7Jh0rbb%2FpoPaMWASMtv%2Fk8e76wuCj6ZrA8yppkMJnbQmSb21Xf2SKbSWDO7jRQmhVPvNi65Qw59ERzyqfP%2Fg1bkF1rW70cS0YjvQ4%2FBrav0yZbwpmwl2hytKmLjvfO8HwtAURzvLNCu1jQqeJdp9xw50DM%2FgXVV5dQbX00N6HEElmYiizjalFAK%2FuuzBXBYliZof7xVn6RDDfyyw096PI%2FXHub%2FNl4NsQuhh3FnWq6DsnQI8B9gsgPNOWW1fCRR8jlIo4Qw0%2FlbGQGaV6VDZDAYyZMOWQqMkGOqUBBL2mq9iDI1ShXqkpFfaUeWWQ5kWPt38XK8QuzNFZYUP5a60tB%2Ffntmx5NxumVLRXEBTqmFVvwu%2Blk7t1DJ3LzQwkx6e6HZQfeX1mSqX8E2Sus017wuGqqYLD5dv4qjiDmGt3YDUXiBQegK3G%2F%2BYmrCRfOEHFMWdoAegJ1Ohl6DFvsvNzpre9m7%2BfQ7B7J5jp%2BghhdoC3Nd0vsBV4RZjZS2x%2FbMSw&X-Amz-Signature=1cf6b1f08a7a49f984cefef6753b2f614245511fa1bac2ab68a4b61853ddfd8d&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

  - 
Eventual Consistency

여러 서버가 있을때, 특정 인스턴스만 업데이트 되고 나머지는 업데이트가 아직 안됐을때, 서버간의 inconsistency 발생

커밋할 때 발생하는 오류가 많기 때문에, 커밋이 진행되는 속도를 줄일 수 있어야 함.

---

## 📎 Related

<!-- 자동 생성된 섹션 - 수동으로 링크를 추가하세요 -->

### Projects

### Knowledge

### Insights

