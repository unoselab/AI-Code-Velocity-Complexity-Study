## 💡 Equation 5: Pre-Trend Test (가정 검증 모델)

$$Y_{it} = \hat{\mu}_i + \hat{\lambda}_t + \hat{\Gamma}'Z_{it} + \sum_{h=-k}^{-2}\hat{\tau}_h 1[t=E_i+h] + \epsilon_{it}$$

이 식의 핵심 목적은 단 하나입니다. "Cursor를 도입하기 전부터 치료군(Treatment) 저장소들이 대조군(Control) 저장소와 다르게 움직이고 있었는지 확인하는 것"입니다.

만약 Cursor를 도입하기 전부터 치료군 저장소의 코드 추가량이 이미 더 빠르게 성장하고 있었거나 경고(Warnings)가 늘고 있었다면, 도입 후에 나타난 변화를 오직 'Cursor 때문'이라고 말하기 어렵습니다. 그래서 Equation 5는 "도입 전에도 이미 가짜 효과가 존재했는가?"를 현미경처럼 검사합니다.

---

## 1. Equation 5의 수식 구조 이해하기

이 식은 기본적으로 이전에 보았던 Equation 4(반사실 예측 모델)와 뼈대가 같습니다.

$$\text{[Equation 4]} \quad \hat{Y}_{it}(0) = \hat{\mu}_i + \hat{\lambda}_t + \hat{\Gamma}'Z_{it} + \epsilon_{it}$$

$$\text{[Equation 5]} \quad Y_{it} = \hat{\mu}_i + \hat{\lambda}_t + \hat{\Gamma}'Z_{it} + \mathbf{\sum_{h=-k}^{-2}\hat{\tau}_h 1[t=E_i+h]} + \epsilon_{it}$$

Equation 5는 기존 식에 **시그마($\sum$) 가 포함된 보라색 파트가 추가**된 구조입니다. 이 추가된 부분이 바로 Cursor 도입 전 특정 달들을 표시하는 사전 처치 더미 변수(Pre-treatment Dummy Variables)입니다.

---

## 2. 주요 구성 요소 파헤치기

### 📊 $Y_{it}$ : 실제 결과 지표 (Actual Outcome)

* 저장소 $i$가 $t$번째 달에 실제로 기록한 Outcome 데이터입니다.
* **Outcome = Lines Added:** 저장소 $i$가 $t$월에 실제로 추가한 코드 라인 수
* **Outcome = Static Analysis Warnings:** 저장소 $i$가 $t$월에 실제로 기록한 소나큐브 경고 수



### 🛠️ 고정 효과 및 공변량 (통제 장치)

* **$\hat{\mu}_i$ (Repository Fixed Effect):** "이 저장소는 원래 대형 프로젝트인가, 소형인가?" 같은 **저장소 고유의 성격**을 통제합니다.
* **$\hat{\lambda}_t$ (Month Fixed Effect):** "이 달에는 연말 연휴가 있었는가, 새해 버프가 있었는가?" 같은 **해당 월의 GitHub 공통 트렌드**를 통제합니다.
* **$Z_{it}$ (Time-varying Covariates):** 기여자 수, 스타 수 등 **시간에 따라 변하는 저장소의 실시간 상태**를 반영합니다.

---

## 3. 핵심 타임라인 개념: $E_i$ 와 $h$

* **$E_i$ (Treatment Time):** 저장소 $i$가 Cursor를 도입한 '기준월' (Adoption Month)을 의미합니다.
* **$h$ (Relative Time):** 도입 기준월($E_i$)로부터 **몇 개월 전/후**에 위치하는지 나타내는 상대적 시간입니다.

| 달력상 실제 년월 (Calendar Month) | 상대적 시간 ($h$) | 실제 의미 |
| --- | --- | --- |
| **2024년 10월** | $h = -3$ | Cursor 도입 3개월 전 |
| **2024년 11월** | $h = -2$ | Cursor 도입 2개월 전 |
| **2024년 12월** | $h = -1$ | Cursor 도입 1개월 전 (**★제외 대상**) |
| **2025년 01월 ($E_i$)** | $h = 0$ | **Cursor를 처음 도입한 기준월** |
| **2025년 02월** | $h = +1$ | Cursor 도입 1개월 후 |

---

## 4. $1[t=E_i+h]$ : 인디케이터 더미 (스위치 역할)

이 표기법은 통계학에서 쓰이는 지시 함수(Indicator Function)로, 아주 단순한 온/오프 스위치입니다.

> **뜻:** "현재 관찰 중인 달($t$)이, 저장소 $i$의 Cursor 도입월($E_i$)로부터 정확히 $h$개월 떨어진 달이 **맞으면 1, 틀리면 0**을 반환하라."

예를 들어 **Repo A**가 2025년 1월에 Cursor를 도입했으므로 $E_i = \text{2025-01}$입니다. 이때 $h = -2$인 스위치 $1[t = E_i - 2]$의 작동 방식은 다음과 같습니다.

$$\text{Target Month} = \text{2025-01} - \text{2개월} = \text{2024-11}$$

| 관찰 중인 실제 월 ($t$) | 스위치 $1[t=E_i-2]$의 값 | 판단 이유 |
| --- | --- | --- |
| **2024-10** | **0** | 도입 2개월 전이 아니라 3개월 전이므로 0 |
| **2024-11** | **1** | **도입 2개월 전이 정확히 맞으므로 1** |
| **2024-12** | **0** | 도입 1개월 전이므로 0 |
| **2025-01** | **0** | 도입 당월이므로 0 |

즉, 이 더미 변수는 "지금 분석 중인 데이터가 하필 'Cursor 도입 2개월 전'의 데이터인가?"를 컴퓨터에게 알려주는 라벨입니다.

---

## 5. $\hat{\tau}_h$ : 도입 전 가짜 효과 (Placebo Effect)

Equation 5의 최종 주인공입니다. **$\hat{\tau}_h$는 Cursor 도입 $h$개월 전 시점에서 치료군과 대조군 사이의 실제 데이터 격차**를 의미합니다.

* **인과추론의 이상적인 상태:** Cursor를 도입하기 전인 과거($h < 0$)에는 양쪽 그룹 모두 AI를 안 썼으므로 $\hat{\tau}_h = 0$이어야 정상입니다.
* **만약 $\hat{\tau}_h \neq 0$ 이라면?** Cursor를 쓰지도 않았는데 도입 3~4개월 전부터 치료군의 코드 생산성이 대조군보다 훨씬 더 가파르게 증가하고 있었다는 뜻이 됩니다. 이는 DiD의 대전제인 평행 추세 가정(Parallel Trends Assumption)을 무너뜨리는 위험 신호입니다.

---

## 6. 왜 하필 $h = -k$ 부터 $-2$ 까지만 더할까?

$$\sum_{h=-k}^{-2}$$

연구진이 만약 분석 범위를 도입 전 6개월($k=6$)로 잡았다면, 모델에는 $h = -6, -5, -4, -3, -2$에 해당하는 5개의 스위치와 그에 따른 가짜 효과들($\hat{\tau}_{-6} \dots \hat{\tau}_{-2}$)이 탑재됩니다.

### ⚠️ 왜 $h = -1$ (도입 직전 달)은 쏙 뺐을까?

논문에서 언급한 **Anticipation Concern(사전 반영 우려)** 때문입니다.
개발자가 `.cursorrules` 파일을 저장소에 공식적으로 커밋한 달은 2025년 1월($h=0$)이지만, 실제로는 **그 직전 달인 2024년 12월($h=-1$)부터 이미 Cursor를 깔아서 개인적으로 테스트해 보았을 확률**이 높습니다.

| 상대적 시간 ($h$) | 오염 가능성 | 처리 방식 |
| --- | --- | --- |
| $h = -2$ 이하 | Cursor의 영향이 전혀 없는 청정 과거 기간 | **Pre-trend 테스트에 포함** |
| **$h = -1$** | 공식 커밋 전 AI를 미리 만져보아 **오염되었을 구역** | **테스트에서 완전 제외** |

---

## 7. 가설 검증과 위약 테스트 (Placebo Test)

저자들은 통계 모델을 가동하여 다음 귀무가설(Null Hypothesis)이 채택되는지 시험합니다.

$$H_0: \hat{\tau}_h = 0 \quad (\text{for } h = -k, \dots, -2)$$

> **쉬운 의미:** "Cursor 도입 전 6개월 전부터 2개월 전까지 발생한 모든 가짜 효과들($\hat{\tau}_h$)은 **전부 통계적으로 0이 맞다.**"

실제 효과가 없어야 하는 청정 과거 구역에서 효과가 진짜로 0으로 나오는지 확인하므로, 이를 의학계 용어를 빌려 위약 테스트(Placebo Test)라고 부릅니다. 이 가설이 통과되어야만 치료군과 대조군의 과거 트렌드가 일치했다는 증거가 되며, 이후에 발견한 Cursor 효과가 진짜 AI 덕분이라는 인과적 주장이 힘을 얻습니다.

---

## 8. 이벤트 스터디 그래프(Event Study Plot)와의 연결

여기서 추정된 $\hat{\tau}_h$ 값들은 논문의 핵심 시각화 자료인 **이벤트 스터디 그래프**의 도입 전(왼쪽 쪽) 플롯을 형성합니다.

* **도입 전 ($h < 0$ 구역):** 가짜 효과 $\hat{\tau}_h$ 값들이 **0을 중심으로 수평선**을 그려야 가정이 통과됩니다. (Placebo 가설 합격)
* **도입 후 ($h \ge 0$ 구역):** 실제 Cursor 효과($ATT$)가 위나 아래로 튀어 오르는 진짜 인과적 변화가 관찰됩니다.

---

## 9. 쉬운 숫자 시뮬레이션

### 👍 이상적인 합격 시나리오 (Lines Added 분석 예시)

* $\hat{\tau}_{-5} = +2$, $\hat{\tau}_{-4} = -1$, $\hat{\tau}_{-3} = +3$, $\hat{\tau}_{-2} = +1$
* **해석:** 과거 격차가 0에 수렴하므로, 두 그룹은 Cursor 도입 전까지 완벽하게 평행하게 달리고 있었습니다. **(Parallel Trends 가증 성립, Causal Claim 성공)**

### 👎 불합격 시나리오

* $\hat{\tau}_{-5} = +100$, $\hat{\tau}_{-4} = +180$, $\hat{\tau}_{-3} = +250$, $\hat{\tau}_{-2} = +320$
* **해석:** AI를 쓰기도 전부터 치료군 저장소가 매달 70~80줄씩 대조군보다 더 가파르게 성장하고 있었습니다. 이 상태에서는 도입 후에 생산성이 폭발해도 그것이 Cursor 때문인지 원래 잘 나가던 프로젝트여서 그런 것인지 증명할 수 없습니다.

---

## 📌 Equation 4 vs Equation 5 최종 요약

| 구분 | **Equation 4** | **Equation 5** |
| --- | --- | --- |
| **주요 목적** | Cursor가 없었을 때의 **가상 결과(Counterfactual) 예측** | Cursor 도입 전 **평행 추세 가정이 맞는지 검증** |
| **주요 역할** | **진짜 AI 효과($ATT$)를 정밀하게 추정**하는 모델 | 통계 분석 결과에 꼬투리가 잡히지 않게 **방어하는 모델** |

### 🧭 기호 최종 속성 표

$$\text{Term} \qquad \text{Property}$$

| 수식 기호 | 쉬운 의미 | 역할 종류 |
| --- | --- | --- |
| **$Y_{it}$** | 이번 달에 실제로 관찰된 결과 데이터 | 분석 타깃 (Outcome) |
| **$\hat{\mu}_i$** | 저장소별 태생적인 체급 차이 | 저장소 고정 효과 (Control) |
| **$\hat{\lambda}_t$** | 해당 월의 전체 GitHub 트렌드 | 시간 고정 효과 (Control) |
| **$Z_{it}$** | 스타 수, 기여자 수 등 실시간 변수 | 시간 가변 공변량 (Control) |
| **$E_i$** | 각 저장소가 Cursor를 공식 채택한 달 | 기준 시점 (Event) |
| **$h$** | 기준월로부터 떨어진 상대적 개월 수 | 상대 시간 (Timeline) |
| **$1[t=E_i+h]$** | 분석 데이터가 '도입 $h$개월 전'인지 켜지는 스위치 | 더미 변수 (Switch) |
| **$\mathbf{\hat{\tau}_h}$** | **도입 전 과거 구역에 존재하는 가짜 효과** | **검증 대상 (Placebo)** |
| **$\epsilon_{it}$** | 모델이 잡지 못한 무작위 미세 오차 | 잔여 노이즈 (Residual) |

저자들은 이 가짜 효과들($\hat{\tau}_h$)이 한꺼번에 모두 0에 가까운지 통과시키기 위해, 앞서 배웠던 **'오차 크기가 제각각이고 패밀리끼리 뭉쳐 있는 현실'을 방어하는 Heteroscedasticity- and cluster-robust Wald test**를 가동하여 완벽한 면죄부를 받아낸 것입니다.

---
---
---
---

## 💡 "Fit the model"의 진짜 의미

질문하신 대로, 논문에서 “fit the following model(다음 모델을 적합시키다)”라고 표현한 것은 "현실의 데이터를 바탕으로 이 회귀 방정식의 파라미터(계수)들을 추정한다"는 뜻입니다.

결코 수식을 이용해 좌변의 $Y_{it}$ 값을 새로 계산해 내는 대입 연산이 아닙니다.

---

## 1. 현실 데이터 ($Y_{it}$)는 이미 주어져 있다

$Y_{it}$ 값은 우리가 수식으로 만들어내는 것이 아니라, **이미 데이터베이스(CSV)에 찍혀 있는 고정된 결과물**입니다.

| 저장소 (Repo) | 년월 (Month) | **$Y_{it}$ (실제 측정된 Lines Added)** |
| --- | --- | --- |
| **Repo A** | 2024-10 | **120 줄** |
| **Repo A** | 2024-11 | **150 줄** |
| **Repo A** | 2024-12 | **100 줄** |

저자들은 Equation 5를 사용해 이 120, 150, 100이라는 숫자를 만들어낸 것이 아닙니다. 대신 컴퓨터에게 이렇게 명령하는 것입니다.

> *"여기 이미 수집된 진짜 $Y_{it}$ 값들이 있어. 자, 이제 이 값들이 **저장소 효과($\hat{\mu}_i$), 월 효과($\hat{\lambda}_t$), 통제 변수($Z_{it}$), 그리고 도입 전 마네킹 스위치들($\hat{\tau}_h$)**에 의해 각각 몇 퍼센트씩 설명되는지 그 영향력(무게추)을 거꾸로 계산해 봐."*

이것이 통계학에서 말하는 '모델을 적합(Fit)시킨다'의 본질입니다.

---

## 2. 그렇다면 무엇을 '추정(Estimate)'하는가?

Equation 5를 데이터에 핏(Fit)하고 나면, 컴퓨터는 좌변과 우변의 균형을 맞추기 위해 다음 파라미터들의 최적 값을 알아냅니다.

* **$\hat{\mu}_i$ :** 저장소 고유의 기본 체급 (Repository effect)
* **$\hat{\lambda}_t$ :** 해당 월의 전체 GitHub 트렌드 (Month effect)
* **$\hat{\Gamma}$ :** 스타 수, 기여자 수 등이 미치는 자연 영향도 (Covariate effects)
* **$\hat{\tau}_h$ :** **Cursor 도입 전 과거 구역의 가짜 효과 (Pre-treatment effects)**

연구진이 현미경을 들이대고 검사하는 핵심 타깃은 바로 마지막 **$\hat{\tau}_h$** 입니다. 이 과거의 가짜 효과들이 전부 `0`에 가깝게 딱 붙어 있는지를 확인하여, DiD의 대전제인 '평행 추세 가정(Parallel Trend Assumption)'의 정당성을 증명해 냅니다.

---

## 3. 💻 개발자 친화적 버전 (CS-Friendly Translation)

파이썬 코드 구조로 매핑해 보면 연구진이 한 작업의 흐름이 한눈에 들어옵니다.

```python
# 1. 깃허브에서 수집한 실제 결과(Y_it)는 이미 데이터셋에 '상수'로 존재합니다.
observed_y = data["Y_it"]

# 2. Equation 5라는 통계 모델에 독립 변수들을 집어넣고 핏(fit)시킵니다.
#    이 과정에서 모델 내부의 계수들(weights)이 자동으로 계산됩니다.
model.fit(
    X=[
        repo_fixed_effects,   # mu_i
        month_fixed_effects,  # lambda_t
        covariates,           # Z_it
        pre_treatment_dummies # 1[t = E_i + h]
    ],
    y=observed_y
)

# 3. 핏이 완료된 후, 도입 전 마네킹(더미)들에 매달린 가짜 효과(tau_h)들을 추출합니다.
#    그리고 이 값들이 collectively 0이 맞는지 위약 테스트(Placebo Test)를 던집니다.
assert_all_close(model.coef_["tau_h"], 0, comment="Parallel Trends Pass!")

```

---

## 📌 한 줄 최종 요약

"Fit Equation 5"는 $Y_{it}$라는 정답지를 먼저 펼쳐놓고 "그 정답이 나오게 만든 백엔드 원인들($\hat{\mu}, \hat{\lambda}, \hat{\Gamma}, \hat{\tau}$)의 수치적 영향력을 역추적해 내는 최적화 과정"을 의미합니다. 귀하의 해석이 100% 정확합니다!

---
---
---
---

기존의 구체적인 파일 소스코드 매핑 정보와 핵심 통계 개념을 온전히 보존하면서, R 수식 파싱 구조와 텍스트 레이아웃을 정돈하여 시각적 전달력을 극대화한 버전입니다.

---

## 💡 "Fit the Model"의 소스코드 매핑 가이드

이 내용은 논문의 핵심 수식인 Equation 5(Pre-trend Test)가 저자들의 실제 R 소스코드(`DiffInDiffTWFE.Rmd`, `DiffInDiffAll.Rmd`)에서 어떻게 구현되어 가동되는지 보여주는 백엔드 지도입니다.

공식의 수학 기호들이 실제 코드 내에서 `lead_`와 **`lag_`** 변수, 그리고 **`feols()`** 함수로 어떻게 치환되는지 1:1로 매핑해 드립니다.

---

## 1. 핵심 매핑: 이벤트 스터디 함수 구조

저자들은 전통적인 TWFE 방식으로 평행 추세를 검증할 때 다음과 같은 R 함수를 선언해 모델을 핏(Fit)했습니다.

### 🔍 [DiffInDiffTWFE.Rmd (line 238)](https://www.google.com/search?q=/Users/myoungkyu/Documents/0-git-repo/cursor_study/notebooks/DiffInDiffTWFE.Rmd:238)

```R
fit_event_study <- function(outcome_var, data) {
    formula_str <- paste0(
        outcome_var, " ~ lead_6 + lead_5 + lead_4 + lead_3 + lead_2 +
        lag_0 + lag_1 + lag_2 + lag_3 + lag_4 + lag_5 + lag_6 +
        log(ncloc + 1) + log(age + 1) + log(contributors + 1) + log(stars + 1) +
        log(issues + 1) | repo_name + time"
    )

    model <- feols(as.formula(formula_str), data = data)
    return(model)
}

```

### 🔤 코드 파라미터 1:1 수식 매핑

* **`outcome_var` $\rightarrow Y_{it}$ (실제 결과 데이터):** 좌변에 위치한 고정된 로우 데이터입니다.
* **`lead_6` ... `lead_2` $\rightarrow 1[t=E_i+h]$ ($h < 0$ 구간의 사전 더미):** 수식의 **$\hat{\tau}_h$** 계수가 계산될 마네킹 스위치들입니다. (도입 6개월 전부터 2개월 전까지)
* **`lag_0` ... `lag_6` $\rightarrow$ 사후 처치 더미:** Cursor 도입 당월($h=0$)부터 도입 6개월 후까지의 실제 효과를 측정하는 스위치들입니다.
* **`log(ncloc + 1)` 등 $\rightarrow Z_{it}$ (시간 가변 공변량):** 왜곡을 막기 위해 로그($\log$)를 씌워 정규화한 통제 변수 세트입니다.
* **`| repo_name + time` $\rightarrow \hat{\mu}_i + \hat{\lambda}_t$ (고정 효과):** 파이프라인(`|`) 우측에 위치하여 저장소 고유 체급과 월별 트렌드를 강제로 격리(통제)하는 고정 효과 팩터입니다.
* **`feols(...)` $\rightarrow$ 최적화 추정 연산:** `fixest` 패키지의 함수로, 좌변의 데이터를 바탕으로 우변의 모든 계수들을 수학적으로 역추적하여 적합(Fit)시킵니다.

---

## 2. 실제 데이터 ($Y_{it}$)의 출처 및 변수 목록

앞서 설명한 대로 $Y_{it}$는 코드가 임의로 가공하는 값이 아니라 CSV 파일에서 읽어온 원본 컬럼입니다.

### 💾 [DiffInDiffTWFE.Rmd (line 25)](https://www.google.com/search?q=/Users/myoungkyu/Documents/0-git-repo/cursor_study/notebooks/DiffInDiffTWFE.Rmd:25)

```R
panel_data <- fread("../data/panel_event_monthly.csv")

```

### 📈 [DiffInDiffTWFE.Rmd (line 55)](https://www.google.com/search?q=/Users/myoungkyu/Documents/0-git-repo/cursor_study/notebooks/DiffInDiffTWFE.Rmd:55)

분석에 투입된 $Y_{it}$ 타깃 변수들은 다음과 같이 로그 스케일로 정비되어 입력됩니다.

* `"log(commits + 1)"` $\rightarrow$ **Commits** (월간 커밋 수)
* `"log(lines_added + 1)"` $\rightarrow$ **Lines Added** (월간 코드 추가량)
* `"log(cognitive_complexity + 1)"` $\rightarrow$ **Cognitive Complexity** (SonarQube 인지 복잡도)

---

## 3. 과거 가짜 효과 ($\hat{\tau}_h = 0$)를 검증하는 코드

컴퓨터가 핏(Fit)을 끝내고 `lead_` 변수들의 계수들을 구하면, 연구진은 이 과거 값들이 일제히 0에 수렴하는지 통계 시험대에 올립니다.

### 🔬 [DiffInDiffAll.Rmd (line 508)](https://www.google.com/search?q=/Users/myoungkyu/Documents/0-git-repo/cursor_study/notebooks/DiffInDiffAll.Rmd:508)

```R
# TWFE: 도입 전 모든 leads 계수들이 Collectively 0인지 왈드 검정(Wald Test) 실행
twfe_pretrend_test <- function(outcome_var, data) {
    model <- feols(as.formula(formula_str), data = data)

    coefs <- coef(model)
    # 1. 계산된 전체 계수 중 과거 구역인 "lead_"로 시작하는 이름만 필터링 (tau_h 추출)
    lead_names <- names(coefs)[grepl("^lead_", names(coefs))]
    beta <- coefs[lead_names]
    
    # 2. 추출된 과거 가짜 효과들과 분산-공분산 행렬(V)을 들이받아 왈드 검정 점수 계산
    res <- compute_wald(beta, V)
}

```

---

## 4. 최신 보루시악(Borusyak) 대체 기법 버전

TWFE 방식 외에, 이 논문의 가장 강력한 무기인 **Borusyak et al.의 대체 추정량(Imputation Estimator)** 코드 역시 완벽하게 동일한 메커니즘 타임라인으로 설계되어 작동합니다.

### 🛡️ [DiffInDiffBorusyak.Rmd (line 167)](https://www.google.com/search?q=/Users/myoungkyu/Documents/0-git-repo/cursor_study/notebooks/DiffInDiffBorusyak.Rmd:167)

```R
dynamic_result <- did_imputation(
    data = data,
    yname = outcome_var,
    gname = "event",
    tname = "time",
    idname = "repo_name",
    first_stage = ~ age + ncloc + contributors + stars + issues | repo_name + time,
    horizon = -6:6,      # 전체 타임라인 범위: 도입 전 6개월 ~ 도입 후 6개월
    pretrends = -6:-2    # 평행 추세를 검증할 청정 과거 구역 (h = -1 구역 자동 제외)
)

```

---

## 📌 최종 요약

제시된 모든 소스코드는 "$Y_{it}$라는 정답지를 사전에 정해두고, 그 결과가 나오게 만든 과거의 가짜 스위치들(`lead_6` ~ `lead_2`)의 계수들을 `feols()`나 `did_imputation()`으로 역추적(Fit)한 뒤, 이 값들이 진짜 `0`에 수렴하는지 `compute_wald()`로 최종 테스트하는 구조"로 이루어져 있습니다. 수식의 의도가 코드와 완벽하게 1:1로 부합합니다.