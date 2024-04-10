## Cross Validation in Finance

### Motivation

교차 검증의 목적은 Machine learning 알고리즘의 일반화 오차를 알아내 overfitting을 막는 것이다. 하지만 교차검증은 표준 머신러닝 기법을 금융 문제에 적용했을 때 실패하는 또 하나의 사례다. Overfitting이 발생해도 Cross validation이 이를 탐지하지 못한다.
사실 Cross Validation은 Hyper parameter 튜닝으로 과적합에 기여를 한다. Chapter 7에서는 표준 Cross validation이 금융에서 실패하는 이유를 배우고, 어떻게 대처할 수 있는지 알아본다.