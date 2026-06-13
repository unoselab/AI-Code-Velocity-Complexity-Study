> **Cursor를 쓴 실제 결과와, Cursor를 안 썼다면 나왔을 가상의 결과를 비교해서 평균낸다.**

이게 수식 (2), (3)의 전부입니다. 

---

## 1. 먼저 (Y_{it})부터 이해하기

[
Y_{it}
]

이것은:

> repo (i)가 month (t)에 실제로 보인 결과

입니다.

예를 들어 outcome이 **Lines Added**라면:

[
Y_{it} = \text{repo i가 month t에 실제로 추가한 코드 라인 수}
]

예:

| Repo   | Month   |             (Y_{it}) |
| ------ | ------- | -------------------: |
| Repo A | 2025-01 | 실제 lines added = 500 |

즉 (Y_{it})는 **관찰 가능한 실제 값**입니다.

---

## 2. (Y_{it}(0))가 가장 중요합니다

[
Y_{it}(0)
]

이것은:

> repo (i)가 month (t)에 **Cursor를 쓰지 않았더라면** 나왔을 결과

입니다.

여기서 ((0))은 **treatment 없음**, 즉 Cursor adoption 없음이라는 뜻입니다.

예를 들어 Repo A가 2025년 1월에 Cursor를 도입했다고 합시다.

| Repo   | Month   | 실제 상황      |
| ------ | ------- | ---------- |
| Repo A | 2025-01 | Cursor 사용함 |

우리는 실제 값은 볼 수 있습니다.

[
Y_{it} = 500
]

하지만 이것은 볼 수 없습니다.

[
Y_{it}(0) = ?
]

왜냐하면 Repo A는 실제로 Cursor를 썼기 때문입니다.

즉 (Y_{it}(0))는 이런 질문입니다:

> Repo A가 2025년 1월에 Cursor를 안 썼다면 lines added가 몇 줄이었을까?

이건 현실에서 직접 볼 수 없기 때문에 **counterfactual**, 즉 “가상의 반대 상황”입니다.

---

## 3. 한 repo-month에서 Cursor 효과

한 관측치에서 Cursor의 효과는 이렇게 봅니다.

[
Y_{it} - Y_{it}(0)
]

쉽게 말하면:

> 실제 결과 − Cursor를 안 썼다면 나왔을 결과

예를 들어:

| 값           | 의미                           |  숫자 |
| ----------- | ---------------------------- | --: |
| (Y_{it})    | Cursor 사용 후 실제 lines added   | 500 |
| (Y_{it}(0)) | Cursor를 안 썼다면 예상 lines added | 200 |
| 차이          | Cursor 효과                    | 300 |

그러면:

[
Y_{it} - Y_{it}(0) = 500 - 200 = 300
]

즉 이 repo-month에서 Cursor 효과는 **+300 lines added**입니다.

---

# 수식 (2): ATT

수식 (2)는 이것입니다.

[
ATT =
\frac{1}{|\Omega_1|}
\sum_{it \in \Omega_1}
E[Y_{it} - Y_{it}(0)]
]

복잡해 보이지만, 뜻은:

> Cursor가 적용된 모든 repo-month에서 Cursor 효과를 구한 뒤 평균낸다.

즉:

[
ATT = \text{Cursor를 쓴 모든 관측치의 평균 효과}
]

---

## 4. (\Omega), (\Omega_1), (\Omega_0) 이해하기

### (\Omega)

[
\Omega = {it}
]

이것은 전체 관측치 집합입니다.

여기서 관측치 하나는:

> repo 하나 × month 하나

입니다.

예:

| Observation     | Meaning         |
| --------------- | --------------- |
| Repo A, 2024-12 | 하나의 observation |
| Repo A, 2025-01 | 하나의 observation |
| Repo B, 2025-01 | 하나의 observation |

---

### (\Omega_1)

[
\Omega_1
]

이것은 **treated observations**, 즉 Cursor가 적용된 관측치들입니다.

예를 들어 Repo A가 2025년 1월에 Cursor를 도입했다면:

| Repo   | Month   | Cursor 상태 | 포함 집합      |
| ------ | ------- | --------- | ---------- |
| Repo A | 2024-12 | 아직 안 씀    | (\Omega_0) |
| Repo A | 2025-01 | 사용함       | (\Omega_1) |
| Repo A | 2025-02 | 사용함       | (\Omega_1) |

중요한 점:

> Treatment repo라도 Cursor 도입 전 month는 (\Omega_1)이 아니라 (\Omega_0)입니다.

---

### (\Omega_0)

[
\Omega_0
]

이것은 untreated observations입니다.

여기에는 두 종류가 들어갑니다.

| Type            | Example                         |
| --------------- | ------------------------------- |
| never-treated   | control repo의 모든 month          |
| not-yet-treated | Cursor repo이지만 adoption 전 month |

예:

| Repo   | Month   | 상태                       | 포함         |
| ------ | ------- | ------------------------ | ---------- |
| Repo A | 2024-12 | Cursor 도입 전              | (\Omega_0) |
| Repo B | 2025-01 | control repo, Cursor 안 씀 | (\Omega_0) |
| Repo A | 2025-01 | Cursor 도입 후              | (\Omega_1) |

---

## 5. ATT 예시

세 개의 treated observations가 있다고 합시다.

| Repo | Month   | 실제 (Y_{it}) | Cursor 없었으면 (Y_{it}(0)) |   효과 |
| ---- | ------- | ----------: | ----------------------: | ---: |
| A    | 2025-01 |         500 |                     200 | +300 |
| A    | 2025-02 |         350 |                     220 | +130 |
| C    | 2025-03 |         600 |                     300 | +300 |

그러면 ATT는:

[
ATT = \frac{300 + 130 + 300}{3}
]

[
ATT = 243.3
]

즉:

> Cursor를 도입한 모든 post-adoption repo-month를 평균해보니, Cursor 효과는 약 +243 lines added이다.

이게 수식 (2)의 의미입니다.

---

# 수식 (3): (ATT_h)

수식 (3)은 이것입니다.

[
ATT_h =
\frac{1}{|\Omega_{1,h}|}
\sum_{it \in \Omega_{1,h}}
E[Y_{it} - Y_{it}(0)]
]

이건 ATT와 거의 같습니다.

차이는 하나입니다.

> 전체 treated observations를 다 평균내는 것이 아니라, Cursor 도입 후 (h)개월째 관측치만 평균낸다.

---

## 6. (h)가 무엇인가?

(h)는 Cursor 도입 후 몇 개월이 지났는지를 의미합니다.

| (h)     | 의미                |
| ------- | ----------------- |
| (h = 0) | Cursor 도입한 바로 그 달 |
| (h = 1) | Cursor 도입 1개월 후   |
| (h = 2) | Cursor 도입 2개월 후   |
| (h = 3) | Cursor 도입 3개월 후   |

예를 들어 Repo A가 2025년 1월에 Cursor를 도입했다면:

| Month   | Relative time |
| ------- | ------------- |
| 2025-01 | (h = 0)       |
| 2025-02 | (h = 1)       |
| 2025-03 | (h = 2)       |

---

## 7. (ATT_h) 예시

Repo A, C, D가 각각 다른 달에 Cursor를 도입했다고 합시다.

| Repo | Cursor adoption month |
| ---- | --------------------- |
| A    | 2025-01               |
| C    | 2025-02               |
| D    | 2025-03               |

이제 (h=0), 즉 도입한 달의 효과만 모읍니다.

| Repo | Adoption month | 실제 (Y_{it}) | 예상 (Y_{it}(0)) |   효과 |
| ---- | -------------- | ----------: | -------------: | ---: |
| A    | 2025-01        |         500 |            200 | +300 |
| C    | 2025-02        |         400 |            250 | +150 |
| D    | 2025-03        |         700 |            300 | +400 |

그러면:

[
ATT_0 = \frac{300 + 150 + 400}{3}
]

[
ATT_0 = 283.3
]

즉:

> Cursor 도입 첫 달의 평균 효과는 약 +283 lines added이다.

---

이번에는 (h=1), 즉 도입 1개월 후만 봅니다.

| Repo | 1개월 후 month | 실제 (Y_{it}) | 예상 (Y_{it}(0)) |   효과 |
| ---- | ----------- | ----------: | -------------: | ---: |
| A    | 2025-02     |         350 |            220 | +130 |
| C    | 2025-03     |         380 |            260 | +120 |
| D    | 2025-04     |         500 |            310 | +190 |

그러면:

[
ATT_1 = \frac{130 + 120 + 190}{3}
]

[
ATT_1 = 146.7
]

즉:

> Cursor 도입 1개월 후 평균 효과는 약 +147 lines added이다.

---

## 8. ATT와 (ATT_h)의 차이

가장 쉽게 비교하면 이렇습니다.

| Concept | Meaning                | 질문                           |
| ------- | ---------------------- | ---------------------------- |
| ATT     | 전체 post-adoption 평균 효과 | Cursor가 전체적으로 평균 얼마나 영향을 줬나? |
| (ATT_h) | 특정 시점의 효과              | Cursor 도입 후 h개월째 효과는 얼마인가?   |

ATT는 전체 평균입니다.

(ATT_h)는 시간별 효과입니다.

---

## 9. 왜 이 논문에서는 (ATT_h)가 특히 중요한가?

이 논문의 핵심 결과는:

> Cursor 효과가 처음에는 크지만, 오래가지 않는다.

즉, 효과가 시간에 따라 변합니다.

그래서 전체 ATT만 보면 중요한 정보를 놓칠 수 있습니다.

예를 들어:

| Time after Cursor | Effect |
| ----------------- | -----: |
| (h=0)             |   +300 |
| (h=1)             |   +150 |
| (h=2)             |    +20 |
| (h=3)             |      0 |

전체 ATT는 평균이라서 “조금 증가했다”처럼 보일 수 있습니다.

하지만 (ATT_h)를 보면 더 정확히 알 수 있습니다.

> 첫 달에는 크게 증가했지만, 몇 달 뒤에는 사라졌다.

이 논문의 “short-term velocity increase but not sustained productivity”라는 결론이 바로 (ATT_h) 분석에서 나옵니다.

---

## 10. 한 문장으로 정리

수식 (2)는:

> Cursor를 사용한 모든 repo-month에서 평균 효과를 구하는 식입니다.

수식 (3)은:

> Cursor 도입 후 (h)개월째의 평균 효과를 따로 구하는 식입니다.

가장 중요한 개념은 이것입니다:

[
Y_{it} - Y_{it}(0)
]

즉:

> 실제 결과 − Cursor를 안 썼다면 나왔을 가상의 결과

이 차이를 평균내면 ATT이고, 특정 (h)개월째만 평균내면 (ATT_h)입니다.
