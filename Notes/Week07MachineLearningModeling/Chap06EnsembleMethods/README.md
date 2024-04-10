## Ensemble Methods

### Motivation

Chapter 6에서는 가장 유명한 두 가지 Machine Learning Ensemble Method를 알아본다. 목표는 Ensemble을 효과적으로 만드는 것이 무엇인지, 금융에서 흔히 잘못 사용하는 일반적 오류를 피하는 방법이 무엇인지 알아보는 것이다.

### The three sources of errors

Machine Learning 모델은 대개 세가지 오류 때문에 애를 먹는다

1. **bias** : 이 오류는 비현실적인 가정에서 비롯된다. 편향이 너무 크면 machine learning 알고리즘이 특성과 결과 간의 중요한 관계를 인식하는 데 실패한다. 이 상황에 알고리즘이 `underfitting`되었다고 한다.
2. **variance** : 이 오류는 훈련 데이터의 작은 변화에 대한 민감도에서 비롯된다. 분산이 높으면 알고리즘은 훈련 데이터셋을 과적합한 것이며, 이로인해 훈련 데이터셋의 아주 작은 변화에 대해서도 완전히 다른 예측을 할 수 있다. 훈련 데이터셋의 일반적인 패턴을 모델링하는 대신, 알고리즘은 신호를 잡음으로 간주한다.
3. **noise** : 예측하지 못한 변화나 측정 오류와 같은 관측값의 분산 때문에 발생한다. 더 이상 줄일 수 없는 오류이므로 어떤 모델로도 해결하지 못한다.

관측값 $(x_i)_{i=1, \dots, n}$의 훈련 데이터셋과 실수값 결과 $(y_i)_{i=1,\dots,n}$이 있다고 가정하자. 함수 $f[x]$가 있으며, $y = f[x] + \epsilon$이며, 여기서 $\epsilon$이며, 여기서 $\epsilon$은 $E[\epsilon_i] = 0$이고, $E[\epsilon_i^2] = \sigma_\epsilon^2$인 백색 잡음이다. 
$f[x]$를 가장 잘 적합화하는 함수 $\hat{f[x]}$를 추정하는데, 예측 오차의 분산을 최소화하는 방법을 활용한다. 이 평균 오차는 다음처럼 분해할 수 있다.

$$E \left[(y_i - \hat{f[x_i]})^2 \right] = \left(\left[ E[\hat{f[x_i]} - f[x_i]]\right]\right) + V\left[\hat{f[x_i]} \right] + \sigma_\epsilon^2$$

Ensemble methods는 일련의 모두 같은 학습 알고리즘을 기반으로 하는 약한 학습기들을 병합함으로써 개별 학습기보다 더 좋은 성능을 발휘하는 학습기를 생성하는 것이다. Ensemble method는 편향 또는 분산을 축소하는데 도움을 준다
