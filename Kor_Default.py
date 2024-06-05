import numpy as np
import matplotlib.pyplot as plt

# 매개변수 설정
a = 1.496e8  # km, 반장축
e = 0.0167  # 이심률

# 반단축 계산
def calculate_b(a, e):
    return a * np.sqrt(1 - e**2)

b = calculate_b(a, e)

# 각도 배열 생성 (0에서 2pi까지)
theta = np.linspace(0, 2 * np.pi, 1000)

# 타원 좌표 계산
x = a * np.cos(theta)
y = b * np.sin(theta)

# 태양의 위치
focus_x = a * e
focus_y = 0

# 각 점에서 태양까지의 거리 계산
r = np.sqrt((x - focus_x)**2 + (y - focus_y)**2)

# 그래프 그리기
plt.figure(figsize=(10, 6))
plt.plot(x, y, label='지구의 공전 궤도')
plt.plot(focus_x, focus_y, 'ro', label='태양')
for i in range(0, 1000, 100):
    plt.plot([focus_x, x[i]], [focus_y, y[i]], 'g--', lw=0.5)  # 태양에서 각 점까지의 거리

plt.xlabel('x (km)')
plt.ylabel('y (km)')
plt.legend()
plt.title('지구의 타원 궤도와 태양에서 각 점까지의 거리')
plt.grid(True)
plt.axis('equal')
plt.show()

# 시간에 따른 거리 변화를 시각화
plt.figure(figsize=(10, 6))
plt.plot(theta, r)
plt.xlabel('각도 (라디안)')
plt.ylabel('태양과 지구 사이의 거리 (km)')
plt.title('각도에 따른 태양과 지구 사이의 거리 변화')
plt.grid(True)
plt.show()
