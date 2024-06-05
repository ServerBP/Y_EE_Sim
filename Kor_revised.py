import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# 상수
AU = 1.496e+11  # 천문단위 (미터)
year_in_seconds = 365.25 * 24 * 3600  # 1년 (초)

# 지구 궤도의 매개변수
a = AU  # 장반경 (태양까지의 평균 거리)
e = 0.5  # 타원 궤도를 위한 증가된 이심률
b = a * np.sqrt(1 - e**2)  # 단반경

# 시간 배열
t = np.linspace(0, year_in_seconds, 1000)

# 궤도 계산 (타원의 매개변수 방정식)
theta = 2 * np.pi * t / year_in_seconds
x = a * np.cos(theta)
y = b * np.sin(theta)

# 위치를 천문단위로 변환
x_au = x / AU
y_au = y / AU

# 태양과 지구 사이의 거리 계산
distance = np.sqrt(x**2 + y**2)  # 미터 단위
distance_km = distance / 1e3  # 킬로미터로 변환

# 천문단위로 2D 궤도 그리기
plt.figure(figsize=(8, 8))
plt.plot(x_au, y_au, label="지구의 궤도")
plt.plot(0, 0, 'yo', label="태양")  # 원점에 태양
plt.xlabel('X 위치 (천문단위)')
plt.ylabel('Y 위치 (천문단위)')
plt.title('태양 주위를 도는 지구의 2D 궤도 (더 타원형)')
plt.legend()
plt.axis('equal')
plt.grid(True)
plt.show()

# 시간에 따른 거리 그리기
plt.figure(figsize=(10, 6))
plt.plot(t / (24 * 3600), distance / 1e9, label="거리 (실제)")  # 기가미터 단위
plt.xlabel('시간 (일)')
plt.ylabel('거리 (Gm)')
plt.title('시간에 따른 지구와 태양 사이의 거리')
plt.grid(True)
plt.show()

# 사인 함수 회귀 함수
def sinusoidal(t, A, B, C, D):
    return A * np.sin(B * t + C) + D

# 거리 데이터에 사인 모델 피팅
initial_guess = [1e8, 2 * np.pi / year_in_seconds, 0, AU / 1e3]  # km 단위의 A, B, C, D에 대한 초기 추정값
params, params_covariance = curve_fit(sinusoidal, t, distance_km, p0=initial_guess)

# 피팅된 거리 데이터 생성
fitted_distance_km = sinusoidal(t, *params)

# 비교를 위한 원본 및 피팅 데이터 그리기
plt.figure(figsize=(10, 6))
plt.plot(t / (24 * 3600), distance / 1e9, label="거리 (실제)")  # 기가미터 단위
plt.plot(t / (24 * 3600), fitted_distance_km / 1e6, label="거리 (피팅)", linestyle='--')  # 기가미터 단위
plt.xlabel('시간 (일)')
plt.ylabel('거리 (Gm)')
plt.title('사인 함수 피팅을 통한 지구와 태양 사이의 거리')
plt.legend()
plt.grid(True)
plt.show()

# 피팅된 매개변수 출력
A, B, C, D = params
print(f"피팅된 매개변수: A = {A} km, B = {B} rad/s, C = {C} rad, D = {D} km")
print(f"사인 함수 방정식: distance(t) = {A:.2e} * sin({B:.2e} * t + {C:.2e}) + {D:.2e} km")
