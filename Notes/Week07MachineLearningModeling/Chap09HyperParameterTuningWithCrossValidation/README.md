### Motivation

Hyper parameter tuning은 머신러닝 알고리즘 적합화 단계에서 필수적인 과정이다. 이 단계가 적절히 이뤄지지 못한다면 알고리즘은 과적합되기 쉽고, 실제 성과는 실망스러울 것이다.
머신러닝 문헌들은 튜닝된 모든 Hyper parameter에 대해 Cross validation을 하는 것에 특별히 주목하고 있다.
Chapter 7에서 살표본 것처럼, 금융에서의 교차 검증은 특히 어려운 문제이고, 다른 분야에서 사용하는 해법은 실패하기 쉽다.
Chapter 9에서는 Purged K-Fold Cross Validation 방법을 사용해 Hyper parameter를 튜닝하는 방법을 알아본다.