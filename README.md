# Asset-Management-Considering-Financial-Regime-Change

논문링크 : https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE09272519

## 코드 설명 

### utils.py
백테스트에 필요한 성과지표들을 함수로 만들었다.
( Mdd, Sharpe, VaR, Mean, Std 등 )

### Regime_TDF_utils.py
국면전환 포착모형과 TDF, Glide-Path를 구현하는 코드를 함수로 만들었다.
( Turbulence Index, Absortion Ratio, weight of risky and safety assets )

### Regime-Based Asset Allocation.ipynb
논문의 전체적인 프로세스를 한국시장에 맞게 구현한 코드

### 데이터
데이터의 경우 kritzman_data.xlsx의 파일을 사용하며
각 시트별로 필요한 데이터를 분리해서 담아두었다.


## 국면전환을 고려한 생애주기별 자산관리 분석

• 생애주기별 자산관리는 투자목표 시점이 가까울 수록 위험자산의 비중을 줄여 나가는 특징을 지닌,
시간에 따른 자산 구성을 최적화하는 모델을 주로 적용한다.

• 자산배분 모델은 일반적으로 변동성 정상성 가정에 의해 잔여 투자기간만 고려하는 경향이 있는데,
실제 시장에서는 변동성 비정상 특성이 존재하고 이에 따른 시장국면 변화 현상이 발생할 수 있다.

• 특히, 일반적인 시장상태에서는 자산 간의 상관관계가 낮다가 변동성이 큰 시장국면에는
상관관계가 증가하는 경향이 존재한다.

• 본 연구에서는 이러한 상관관계를 반영할 수 있는 측정 지표를 산출하고 국면전환 모형을
생애주기별 자산관리의 자산배분에 적용하는 분석을 진행한다.


## 생애주기별 자산관리 ( TDF )
• 생애주기별 자산관리는 투자자가 정한 시점에 소득 확보를
위해 목표 기간별 글라이드패스(Glide Path)에 따라 자산배분
계획을 세우고, 목표시점이 가까워질수록 전체 자산 중
위험자산의 비중을 줄여 나가는 자산배분 패턴을 갖는
자산관리 방법이다.

• Kritzman은 위험자산과 안전자산의 비중을 결정하는
아래와 같은 공식을 활용하여 잔여 투자기간이 위험자산
투자 비중에 비례한다는 것을 보였다.

𝑊𝑅 =(ln 1 + 𝐿 𝑇 − 𝜇𝑆𝑇)/(𝑍𝜎𝑅 𝑇 + 𝜇𝑅𝑇 − 𝜇𝑆𝑇)

## 𝑇urbulence Index
• Turbulence는 자산 수익률 사이의 비정상적인
움직임을 측정하는 지표로서 특정 자산의 극단적인
가격 움직임 뿐만 아니라 포트폴리오 분산 효과에
영향을 미칠만한 이례적인 자산 간의 상관관계
변화를 포착한다.

• Turbulence를 산출하기 위해서 마할라노비스 거리를
이용하는데, 이는 유클리디언 거리에서 표본의
공분산 행렬을 이용함으로써 표준화된 값의 변수 간
유사성 정도를 고려하는 척도이다.

• 마할라노비스 거리 : 𝑀𝐷 = (𝑦 − 𝜇)Σ−1(𝑦 − 𝜇)𝑇

• 해당 척도를 응용하여 다음의 식을 계산하면 자산
간의 비정상적 움직임을 포착하는 Turbulence Index를
확인 할 수 있다.

## Absortion Ratio

• Absorption Ratio(AR)는 충격에 대한 민감성(susceptibility
to shocks)을 다루는 지표로서 ‘리먼 브라더스 사태’ 이후
리스크 관리 대책의 중요성이 커지면서 관심이
높아졌다.

• 또 한 AR 는 Information Processing Ratio(R/C) 와
마찬가지로, 데이터의 크기와 공분산이 제공되는 경우
체계적 시장 리스크의 정보로 활용된다.

• 즉, AR지표를 통해 시장상황에 대한 통일된 반응 정도를
측정 할 수 있으므로 시장 국면을 판단하는 지표로
사용할 수 있다.

## 기존 포트폴리오와 Regime Change를 반영한 포트폴리오를 비교

• Conventional Portfolio
- 기존 포트폴리오 운용 방식은 투자기간만을 고려하여
자산을 배분하는 방식이다.
- 따라서 시장의 국면 변화에 그대로 노출되어 있다.

• Regime-Sensitive Portfolio

- 앞의 소개한 두 가지의 국면 탐지 지표를 이용하여
투자기간에 따른 기존의 자산배분 프레임워크를 유지하되
국면 변화에 동적으로 대응하는 것을 확인할 수 있다.
- 이로써 금융 시장의 일시적 국면 변화에 따른 수익률 방어
포트폴리오를 구성할 수 있다.

![image](https://user-images.githubusercontent.com/80387630/121306786-389c8500-c93a-11eb-9e56-5d5536c52ae3.png)

## 두 포트폴리오의 Glide-Path 비교
![image](https://user-images.githubusercontent.com/80387630/121306882-59fd7100-c93a-11eb-87d4-dc6ee4f195d1.png)

• 국면 전환으로 고려하지 않는 기존 생애주기별 자산배분 프
레임워크 하의 Glide Path는 목표시점이 가까워질수록 전체
자산 중 위험자산의 투자 비중을 줄여 나가는 자산배분 패턴
을 갖는다.

• 그러나 이는 변동성이 큰 시장 국면을 잘 반영하지 못한다는
특징이 있다.

![image](https://user-images.githubusercontent.com/80387630/121306948-6a155080-c93a-11eb-8d75-c1bbae3f7a39.png)

• 국면 전환을 고려하는 Regime-Sensitive 생애주기별 자산배
분 프레임워크 하의 Glide path는 투자기간을 고려함과 동시
에 변동성 확대 국면에서 Risky asset의 비중을 축소한다.

## 두 포트폴리오의 Back-test 결과 비교
![image](https://user-images.githubusercontent.com/80387630/121307040-831e0180-c93a-11eb-9dbd-b4cf9099cb0e.png)

![image](https://user-images.githubusercontent.com/80387630/121307108-9c26b280-c93a-11eb-96df-c15360879761.png)

• Regime-sensitive 포트폴리오는 수익률 방어 측면에서 기존 포트폴리오 대비 개선된 성과를 보인다.

• 이는 시장 변동성의 정상성(stationary) 가정 하에서 시간 요인만 고려한 기존 자산배분 프레임워크와 달리,

• Turbulence Index와 Absorption Ratio를 이용한 시장 국면탐지 방법을 통해 변동성의 비정상성(non-stationary) 특징을 자산배분
프레임워크에 동적으로 반영한 효과로 해석할 수 있다.

• 이로써 시장 국면에 대응하는 변동성 방어 포트폴리오의 추가적 발전 가능성을 고려해볼 수 있을 것이다.

## 참고문헌

[1] 김태용, 이정은, & 이지연. (2016). 한· 미 목표만기펀드에 대한 비교사례 연구. 금융공학산학연구, 2, 43-72.
[2] 성주호. (2018). 퇴직연기금 디폴트 옵션 도입 방안 및 부채연계투자전략에 관한 연구. 보험연구원 연구보고서, 2018(23), 1-98.
[3] De Maesschalck, R., Jouan-Rimbaud, D., & Massart, D. L. (2000). The mahalanobis distance. Chemometrics and Intelligent 
Laboratory Systems, 50(1), 1-18.
[4] Elton, E. J., Gruber, M. J., de Souza, A., and Blake, C. R. (2015), Target date funds : Characteristics and performance, The Review of 
Asset Pricing Studies, 5(2), 254-272.
[5] Holmer, M. R. (2009). Estimating the accumulation risks of life-cycle funds. Policy Simulation Group Working Paper.
[6] Kritzman, M. (2017). Target-date funds: A regime-based approach. Journal of Retirement, 5(1), 96-105.
[7] Kritzman, M., & Li, Y. (2010). Skulls, financial turbulence, and risk management. Financial Analysts Journal, 66(5), 30-41.
[8] Pang, G., & Warshawsky, M. (2011). Target-date and balanced funds: Latest market offerings and risk-return analysis. Financial 
Services Review, 20(1), 21-34.
[9] Parker, E. (2017). The relationship between the US economy’s information processing and absorption ratio’s. Proceedings, 2(4), 160.
[10] Yoon, Y. (2010). Glide path and dynamic asset allocation of target date funds. Journal of Asset Management, 11(5), 346-360






