## Sample Weights

### Motivation

Chapter 3에서는 금융 데이터를 labeling하는 몇 가지 기법을 소개했다. Triple barrier methods와 Meta Labeling이라는 새로운 개념을 소개했고, 이들이 퀀터멘털 투자 전략을 포함한 여러 금융 응용에 얼마나 유용한지 설명했다

Chapter 4에서는 금융 응용에 늘 존재하는 또다른 문제(관측값이 IID 분포로부터 생성되지 않는 문제)를 해결하는 방법을 배운다.

대부분 Machine Learning 문헌은 IID 가정에 근거하는데, 많은 머신러닝 응용이 금융에서 실패하는 이유 중 하나는 이런 가정이 금융 시계열에 있어서 비현실적이기 때문이다

## Fractionally Differentiated Features

### Motivation

금융 시계열은 차익 거래의 결과로 인해 낮은 신호 대 잡음 비율을 보인다고 알려져 있다.(Lopez de Prado, 2015)

더 심각한 것은 정수 차분과 같은 Stationary process 변환 과정이 시장의 memory를 지움으로써 신호를 더 감소시킨다. prices series 데이터는 모든 값이 이전 가격 history에 종속되어 있으므로 기억을 가지고 있다. 반면, 수익률과 같은 정수 차분계열 데이터에서는 market memory는 전부 삭제된다. 샘플 기간 이후의 history는 완전히 무시된다. 정상적인 process로의 변환 때문에 데이터로부터 모든 memory를 지우고 난 이후에 통계학자들은 잔차 신호를 추출하고자 복잡한 수학 기법에 의존한다. 이렇게 복잡한 기법을 기억이 지워진 price series데이터에 적용하면 잘못된 결과를 얻게 될 것이라는 점은 그리 놀랍지 않다.

Chapter 5에서는 최대한 market memory를 보존하면서 데이터의 정상성을 보장하는 데이터 변환 기법을 소개한다.