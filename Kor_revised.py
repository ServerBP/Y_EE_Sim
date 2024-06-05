import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# 상수
AU = 1.496e+11  # 천문단위 (미터)
year_in_seconds = 365.25 * 24 * 3600  # 일 년의 초
seconds_in_day = 24 * 3600  # 하루의 초

# 지구 궤도를 위한 매개변수
a = AU  # 반주축 (태양까지의 평균 거리)
e = 0.0167  # 지구의 실제 이심률
b = a * np.sqrt(1 - e**2)  # 준주축

# 초와 일 단위의 시간 배열
t_seconds = np.linspace(0, year_in_seconds, 1000)
t_days = t_seconds / seconds_in_day

# 평균 근점 (M)
M = 2 * np.pi * t_seconds / year_in_seconds

# 이심 근점 (E) (뉴튼 방법 사용)
E = M
for _ in range(10):  # E를 해결하기 위해 반복
    E = M + e * np.sin(E)

# 진근점 (ν)
nu = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))

# 태양으로부터의 거리
r = a * (1 - e**2) / (1 + e * np.cos(nu))
distance_km = r / 1e3  # 킬로미터로 변환

# 그래프를 위한 천문단위로 위치 변환
x_au = r * np.cos(nu) / AU
y_au = r * np.sin(nu) / AU

# 천문단위에서의 2D 궤도 그리기
plt.figure(figsize=(8, 8))
plt.plot(x_au, y_au, label="지구의 궤도")
plt.plot(0, 0, 'yo', label="태양")  # 태양은 원점에 위치
plt.xlabel('X 위치 (AU)')
plt.ylabel('Y 위치 (AU)')
plt.title('태양 주위를 도는 지구의 2D 궤도 (실제)')
plt.legend()
plt.axis('equal')
plt.grid(True)
plt.show()

# 일별 시간에 따른 거리 그래프
plt.figure(figsize=(10, 6))
plt.plot(t_days, distance_km / 1e6, label="거리 (실제)")  # 기가미터 단위
plt.xlabel('시간 (일)')
plt.ylabel('거리 (Gm)')
plt.title('시간에 따른 지구와 태양 사이의 거리')
plt.grid(True)
plt.show()

# 사인 함수 회귀 함수
def sinusoidal(t, A, B, C, D):
    return A * np.sin(B * t + C) + D

# 일별 시간을 사용하여 거리 데이터에 사인 모델 피팅
initial_guess = [1e8, 2 * np.pi / 365.25, 0, AU / 1e3]  # A, B, C, D의 초기 추정값 (킬로미터 단위)
params, params_covariance = curve_fit(sinusoidal, t_days, distance_km, p0=initial_guess)

# 피팅된 거리 데이터 생성
fitted_distance_km = sinusoidal(t_days, *params)

# 비교를 위한 원본 및 피팅 데이터 그리기
plt.figure(figsize=(10, 6))
plt.plot(t_days, distance_km / 1e6, label="거리 (실제)")  # 기가미터 단위
plt.plot(t_days, fitted_distance_km / 1e6, label="거리 (피팅)", linestyle='--')  # 기가미터 단위
plt.xlabel('시간 (일)')
plt.ylabel('거리 (Gm)')
plt.title('사인 함수 피팅을 통한 지구와 태양 사이의 거리')
plt.legend()
plt.grid(True)
plt.show()

# 피팅된 매개변수 출력
A, B, C, D = params
print(f"피팅된 매개변수: A = {A} km, B = {B} rad/day, C = {C} rad, D = {D} km")
print(f"사인 함수 방정식: distance(t) = {A:.2e} * sin({B:.2e} * t + {C:.2e}) + {D:.2e} km")
