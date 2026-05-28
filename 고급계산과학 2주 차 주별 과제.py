# 고급계산과학 2주 차 주별 과제

# 불꽃 놀이
# 목표 : 질량 M인 폭죽이 지표(y = 0)에서 V_0의 속력으로 수직 상승 후, 지상 y = H에서 폭발이 이루어지며 질량이 다른 N개의 파편으로 나누어진다. 폭발 에너지가 E_expo일 때, 파편의 궤도를 시늉내어라.

# 문제 1 - 1 - 1) 파편 개수 2개 / 파편 질량 = M/2, 최고 높이에서 vy = 0일 때 폭발.

'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- [1] 상수 및 초기 조건 설정 ---
g = 9.80665
M = 10.0
H = 50.0
E_expo = 5000.0
N = 2

# --- [2] 속도 및 비행 시간 계산 ---
v = np.sqrt(2 * E_expo / M)
theta = np.random.uniform(0, 2 * np.pi) 

v1_x = v * np.cos(theta)
v1_y = v * np.sin(theta)
v2_x = -v1_x
v2_y = -v1_y

t_fall_1 = (v1_y + np.sqrt(v1_y**2 + 2 * g * H)) / g
t_fall_2 = (v2_y + np.sqrt(v2_y**2 + 2 * g * H)) / g

V0 = np.sqrt(2 * g * H)
t_rise = V0 / g

# --- [3] 애니메이션 시간 배열 설정 ---
t_max_fall = max(t_fall_1, t_fall_2)
t_total = t_rise + t_max_fall
dt = 0.05
times = np.arange(0, t_total + dt, dt)

# --- [4] 애니메이션 캔버스 및 객체 준비 ---
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_title('Fireworks Animation with Dotted Trails (N=2)')
ax.set_xlabel('Horizontal Position (m)')
ax.set_ylabel('Vertical Position (m)')

max_x = max(abs(v1_x * t_fall_1), abs(v2_x * t_fall_2)) * 1.2
max_y = H + max(0, v1_y, v2_y)**2 / (2 * g) * 1.2
ax.set_xlim(-max_x, max_x)
ax.set_ylim(0, max_y if max_y > H else H * 1.2)
ax.grid(True)
ax.axhline(0, color='gray', linestyle='-', linewidth=2)

# 상승 자취(점선), 상승 중인 폭죽 본체(원)
rocket_line, = ax.plot([], [], 'k--', alpha=0.5)
rocket_point, = ax.plot([], [], 'ko', markersize=8)

# 파편 자취(점선), 파편 머리(원)
# plot() 함수의 세 번째 인자에 '--'를 추가하여 점선 스타일 지정!
frag1_line, = ax.plot([], [], 'r--', linewidth=2, alpha=0.7)
frag1_point, = ax.plot([], [], 'ro', markersize=6)

frag2_line, = ax.plot([], [], 'b--', linewidth=2, alpha=0.7)
frag2_point, = ax.plot([], [], 'bo', markersize=6)

explosion_mark, = ax.plot([], [], 'y*', markersize=20)

def update(frame):
    t = times[frame]
    
    # 1. 상승 중일 때
    if t <= t_rise:
        t_hist = times[:frame+1] 
        x_hist = np.zeros_like(t_hist)
        y_hist = V0 * t_hist - 0.5 * g * t_hist**2
        
        rocket_line.set_data(x_hist, y_hist)
        rocket_point.set_data([x_hist[-1]], [y_hist[-1]])
        
    # 2. 터진 후 파편이 날아갈 때
    else:
        t_rock_hist = times[times <= t_rise]
        rocket_line.set_data(np.zeros_like(t_rock_hist), V0 * t_rock_hist - 0.5 * g * t_rock_hist**2)
        rocket_point.set_data([], []) 
        explosion_mark.set_data([0], [H])
        
        t_frames = times[(times > t_rise) & (times <= t)] - t_rise
        
        # 파편 1 자취 업데이트
        t_frames_1 = np.minimum(t_frames, t_fall_1) 
        x1_hist = v1_x * t_frames_1
        y1_hist = H + v1_y * t_frames_1 - 0.5 * g * t_frames_1**2
        
        frag1_line.set_data(x1_hist, y1_hist)
        if len(x1_hist) > 0:
            frag1_point.set_data([x1_hist[-1]], [y1_hist[-1]])
            
        # 파편 2 자취 업데이트
        t_frames_2 = np.minimum(t_frames, t_fall_2)
        x2_hist = v2_x * t_frames_2
        y2_hist = H + v2_y * t_frames_2 - 0.5 * g * t_frames_2**2
        
        frag2_line.set_data(x2_hist, y2_hist)
        if len(x2_hist) > 0:
            frag2_point.set_data([x2_hist[-1]], [y2_hist[-1]])

    return rocket_line, rocket_point, frag1_line, frag1_point, frag2_line, frag2_point, explosion_mark

# 애니메이션 실행
ani = animation.FuncAnimation(fig, update, frames=len(times), interval=dt*1000, blit=True)

plt.show()
'''



# 문제 1 - 1 - 1) 파편 개수 3개 / 파편 질량 = M/2, 최고 높이에서 vy = 0일 때 폭발.
'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- [1] 상수 및 초기 조건 설정 ---
g = 9.80665
M = 10.0
H = 100.0
E_expo = 5000.0
N = 10 # 파편의 개수를 자유롭게 바꿔보세요!

# --- [2] N개의 파편 질량 및 초기 속도 계산 (질량중심 알고리즘) ---
# 1. 랜덤 질량 분배 (합이 M이 되도록)
m_rand = np.random.rand(N)
m = M * (m_rand / np.sum(m_rand))

# 2. 랜덤 운동량 부여 및 운동량 보존 (평균 빼기)
# 교안은 3차원이지만 우리는 2차원 그래프를 그리므로 (N, 2) 크기로 만듭니다.
p = np.random.randn(N, 2) 
p_avg = np.mean(p, axis=0)
p -= p_avg # 이제 모든 p의 합은 0 (운동량 보존)

# 3. 속도로 변환
# p의 크기는 (N, 2)이고 m의 크기는 (N,) 이므로 차원을 맞춰서 나눠줍니다.
u = p / m[:, np.newaxis]

# 4. 에너지 보존 스케일링
K_prime = np.sum(0.5 * m * np.sum(u**2, axis=1)) # 현재의 총 운동 에너지
scale = np.sqrt(E_expo / K_prime)
v = u * scale # 에너지 보존을 만족하는 최종 속도

# x, y 성분 분리
v_x = v[:, 0]
v_y = v[:, 1]

# --- [3] 비행 시간 계산 ---
# 각 파편별로 땅에 떨어지는 시간 계산 (배열 연산으로 한 번에!)
t_fall = (v_y + np.sqrt(v_y**2 + 2 * g * H)) / g

V0 = np.sqrt(2 * g * H)
t_rise = V0 / g

t_max_fall = np.max(t_fall)
t_total = t_rise + t_max_fall
dt = 0.05
times = np.arange(0, t_total + dt, dt)

# --- [4] 애니메이션 캔버스 준비 ---
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_title(f'Fireworks Animation with Dotted Trails (N={N})')
ax.set_xlabel('Horizontal Position (m)')
ax.set_ylabel('Vertical Position (m)')

# 그래프 범위 동적 설정
max_x = np.max(np.abs(v_x * t_fall)) * 1.2
max_y = H + np.max(np.maximum(0, v_y)**2 / (2 * g)) * 1.2
ax.set_xlim(-max_x, max_x)
ax.set_ylim(0, max_y if max_y > H else H * 1.2)
ax.grid(True)
ax.axhline(0, color='gray', linestyle='-', linewidth=2)

# 본체 객체
rocket_line, = ax.plot([], [], 'k--', alpha=0.5)
rocket_point, = ax.plot([], [], 'ko', markersize=8)
explosion_mark, = ax.plot([], [], 'y*', markersize=20)

# 💡 N개의 파편을 그리기 위한 리스트 생성!
frag_lines = []
frag_points = []
colors = plt.cm.plasma(np.linspace(0, 1, N)) # 파편마다 다른 예쁜 색상 부여

for i in range(N):
    # 각 파편별로 점선 객체와 원 객체를 생성해서 리스트에 보관
    line, = ax.plot([], [], '--', color=colors[i], linewidth=1.5, alpha=0.7)
    point, = ax.plot([], [], 'o', color=colors[i], markersize=m[i]/np.max(m)*8 + 2) # 질량이 클수록 점도 큼
    frag_lines.append(line)
    frag_points.append(point)

# --- [5] 화면 업데이트 함수 ---
def update(frame):
    t = times[frame]
    
    if t <= t_rise:
        t_hist = times[:frame+1] 
        x_hist = np.zeros_like(t_hist)
        y_hist = V0 * t_hist - 0.5 * g * t_hist**2
        
        rocket_line.set_data(x_hist, y_hist)
        rocket_point.set_data([x_hist[-1]], [y_hist[-1]])
        
        # 파편 숨기기
        for i in range(N):
            frag_lines[i].set_data([], [])
            frag_points[i].set_data([], [])
        explosion_mark.set_data([], [])
        
    else:
        # 본체 궤적 고정
        t_rock_hist = times[times <= t_rise]
        rocket_line.set_data(np.zeros_like(t_rock_hist), V0 * t_rock_hist - 0.5 * g * t_rock_hist**2)
        rocket_point.set_data([], []) 
        explosion_mark.set_data([0], [H])
        
        t_frames = times[(times > t_rise) & (times <= t)] - t_rise
        
        # 💡 N개의 파편을 반복문으로 한꺼번에 업데이트!
        for i in range(N):
            t_frames_i = np.minimum(t_frames, t_fall[i]) 
            x_hist = v_x[i] * t_frames_i
            y_hist = H + v_y[i] * t_frames_i - 0.5 * g * t_frames_i**2
            
            frag_lines[i].set_data(x_hist, y_hist)
            if len(x_hist) > 0:
                frag_points[i].set_data([x_hist[-1]], [y_hist[-1]])

    # 반환할 모든 객체들을 튜플로 묶어서 반환
    return (rocket_line, rocket_point, explosion_mark, *frag_lines, *frag_points)

# 애니메이션 실행
ani = animation.FuncAnimation(fig, update, frames=len(times), interval=dt*1000, blit=True)

plt.show()
'''

'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- [1] 상수 및 초기 조건 설정 ---
g = 9.80665
M = 10.0
E_expo = 5000.0
N = 15 # 파편의 개수

# 💡 수정된 부분: 초기 속도 V0를 먼저 설정합니다!
V0 = 25.0 # 지상에서의 초기 발사 속도 (m/s)

# 💡 V0에 의해 도달할 수 있는 최고 높이 H를 역학적 에너지 보존으로 자동 계산합니다.
# 1/2 * M * V0^2 = M * g * H  =>  H = V0^2 / (2 * g)
H = V0**2 / (2 * g)
print(f"초기 속도 {V0}m/s로 쏘아 올린 폭죽은 {H:.2f}m 높이에서 터집니다!")

# 상승에 걸리는 시간
t_rise = V0 / g

# --- [2] N개의 파편 질량 및 초기 속도 계산 (질량중심 알고리즘) ---
m_rand = np.random.rand(N)
m = M * (m_rand / np.sum(m_rand))

p = np.random.randn(N, 2) 
p_avg = np.mean(p, axis=0)
p -= p_avg 

u = p / m[:, np.newaxis]

K_prime = np.sum(0.5 * m * np.sum(u**2, axis=1)) 
scale = np.sqrt(E_expo / K_prime)
v = u * scale 

v_x = v[:, 0]
v_y = v[:, 1]

# --- [3] 비행 시간 계산 ---
t_fall = (v_y + np.sqrt(v_y**2 + 2 * g * H)) / g

t_max_fall = np.max(t_fall)
t_total = t_rise + t_max_fall
dt = 0.05
times = np.arange(0, t_total + dt, dt)

# --- [4] 애니메이션 캔버스 준비 ---
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_title(f'Fireworks Animation (V0={V0}m/s, H={H:.1f}m, N={N})')
ax.set_xlabel('Horizontal Position (m)')
ax.set_ylabel('Vertical Position (m)')

max_x = np.max(np.abs(v_x * t_fall)) * 1.2
max_y = H + np.max(np.maximum(0, v_y)**2 / (2 * g)) * 1.2
ax.set_xlim(-max_x, max_x)
ax.set_ylim(0, max_y if max_y > H else H * 1.2)
ax.grid(True)
ax.axhline(0, color='gray', linestyle='-', linewidth=2)

# 본체 객체
rocket_line, = ax.plot([], [], 'k--', alpha=0.5)
rocket_point, = ax.plot([], [], 'ko', markersize=8)
explosion_mark, = ax.plot([], [], 'y*', markersize=20)

# N개의 파편 객체 준비
frag_lines = []
frag_points = []
colors = plt.cm.plasma(np.linspace(0, 1, N))

for i in range(N):
    line, = ax.plot([], [], '--', color=colors[i], linewidth=1.5, alpha=0.7)
    point, = ax.plot([], [], 'o', color=colors[i], markersize=m[i]/np.max(m)*8 + 2) 
    frag_lines.append(line)
    frag_points.append(point)

# --- [5] 화면 업데이트 함수 ---
def update(frame):
    t = times[frame]
    
    if t <= t_rise:
        t_hist = times[:frame+1] 
        x_hist = np.zeros_like(t_hist)
        y_hist = V0 * t_hist - 0.5 * g * t_hist**2
        
        rocket_line.set_data(x_hist, y_hist)
        rocket_point.set_data([x_hist[-1]], [y_hist[-1]])
        
        for i in range(N):
            frag_lines[i].set_data([], [])
            frag_points[i].set_data([], [])
        explosion_mark.set_data([], [])
        
    else:
        t_rock_hist = times[times <= t_rise]
        rocket_line.set_data(np.zeros_like(t_rock_hist), V0 * t_rock_hist - 0.5 * g * t_rock_hist**2)
        rocket_point.set_data([], []) 
        explosion_mark.set_data([0], [H])
        
        t_frames = times[(times > t_rise) & (times <= t)] - t_rise
        
        for i in range(N):
            t_frames_i = np.minimum(t_frames, t_fall[i]) 
            x_hist = v_x[i] * t_frames_i
            y_hist = H + v_y[i] * t_frames_i - 0.5 * g * t_frames_i**2
            
            frag_lines[i].set_data(x_hist, y_hist)
            if len(x_hist) > 0:
                frag_points[i].set_data([x_hist[-1]], [y_hist[-1]])

    return (rocket_line, rocket_point, explosion_mark, *frag_lines, *frag_points)

# 애니메이션 실행
ani = animation.FuncAnimation(fig, update, frames=len(times), interval=dt*1000, blit=True)

plt.show()

'''

'''
import numpy as np
import matplotlib.pyplot as plt

# 상수
g = 9.80665 #m/s² / 지구 표면에서의 중력 가속도 | Wikipedia에 나와있는 값을 가져왔다.

# 초기 조건
M = int(input("폭죽의 질량 : ")) # 폭죽의 질량 (kg)
H = int(input("폭탄을 퍼트릴 높이 : ")) # 폭탄을 퍼트릴 높이 H(m)
E_expo = int(input("폭발 에너지 : ")) # 폭발 에너지(J)
N = 2 # 파편 개수


# 폭발 직후 파편의 속력 계산
# 두(N) 파편의 질량은 M/2로 같고, 에너지를 반반씩 나눠 가짐
v = np.sqrt(N * E_expo / M)

# 랜덤한 방향(각도) 설정 (남은 자유도 1개)
theta = np.random.uniform(0, 2 * np.pi) 

# 두 파편의 초기 속도 벡터 (x, y 성분) - 서로 정확히 반대 방향
v1_x = v * np.cos(theta)
v1_y = v * np.sin(theta)

v2_x = -v1_x
v2_y = -v1_y


# 파편이 땅에 떨어질 때까지의 비행 시간 계산
# 등가속도 운동 공식 y = H + v_y*t - 1/2*g*t^2을 t에 관해 정리해서 근의 공식을 사용하여 y = 0 이 되는 시간 t를 구함
t_fall_1 = (v1_y + np.sqrt(v1_y**2 + 2 * g * H)) / g
t_fall_2 = (v2_y + np.sqrt(v2_y**2 + 2 * g * H)) / g

# 각각의 시간에 맞는 배열 생성
t1 = np.linspace(0, t_fall_1, 100)
t2 = np.linspace(0, t_fall_2, 100)


# --- [5] 폭발 이후 두 파편의 궤적 계산 ---
# 파편 1 궤적
x1 = v1_x * t1
y1 = H + v1_y * t1 - 0.5 * g * t1**2

# 파편 2 궤적
x2 = v2_x * t2
y2 = H + v2_y * t2 - 0.5 * g * t2**2



# 상승 궤적 계산 | 지상에서의 총 에너지(운동 에너지만 있음) = 최고점 H에서의 총 에너지(위치 에너지만 있음) ; 1/2MV0^2 = MgH
V0 = np.sqrt(2 * g * H) # 최고점 H에 도달하기 위한 발사 속도
t_rise = V0 / g
t_up = np.linspace(0, t_rise, 50)
y_up = V0 * t_up - 0.5 * g * t_up**2
x_up = np.zeros_like(y_up) # 수직 상승이므로 x는 0



# 그래프 그리기
plt.figure(figsize=(10, 6))

plt.plot(x_up, y_up, 'k--', label='Rise Trajectory (Firework)') # 본체 상승
plt.plot(x1, y1, 'r--', linewidth=2, label='Fragment 1')         # 파편 1
plt.plot(x2, y2, 'b--', linewidth=2, label='Fragment 2')         # 파편 2
plt.plot(0, H, 'y*', markersize=20, label='Explosion Point')    # 폭발 지점

plt.title('Fireworks Trajectory (2 Fragments, Explodes at Max Height)')
plt.xlabel('Horizontal Position (m)')
plt.ylabel('Vertical Position (m)')
plt.axhline(0, color='gray', linestyle='-', linewidth=1) # 지면 표시
plt.grid(True)
plt.legend()

plt.show()
'''


'''
import numpy as np
import matplotlib.pyplot as plt

# 필요한 상수들 정리
g = 9.80665 #m/s² / 지구 표면에서의 중력 가속도 | Wikipedia에 나와있는 값을 가져왔다.


# 초기 조건

M = float(input("폭죽의 질량 : "))
v0 = float(input("초기 속도 :")) # 초기 속도(m/s)
theta = float(input("초기 각도 (deg) : ")) # 발사 각도(degree)
theta_rad = np.radians(theta) # 발사 각도를 라디안으로 변환
H = float(input("폭탄을 퍼트릴 높이 : ")) # 폭탄을 퍼트릴 높이 H
N = int(input("파편 개수 : ")) # 파편 개수 N
Explode_Energy = float(input("폭발 에너지 : ")) # 폭발 에너지(N)




vy = v0 * np.sin(theta_rad) # 초기 수직 속도

x = 0.0 # 초기 수평 위치 (m)
y = 0.0 # 초기 수직 위치 (m)

m = M / N # 각 파편의 질량

velocity_n = [] # 파편 n개의 각 속도를 저장할 리스트

# for i in range(N) :
'''

'''
#질량중심 좌표계 사용

#운동량 보존

for m_i = m
    
u = nr.rand(N,3)
au = np.mean(u, axis=0)
u -= au

for different m_i

n = nr.rand(N) ; m *= M/np.sum(m)
p = nr.rand(N, 3) ; u=np.zeros((N,3))
pac=np.mean(p,axis=0); p -= pav
for n in range(N) : u[n] = p[n]/m[n]

#에너지 보존
'''


# 문제 1 - 1 - 영상

'''
# 필요한 라이브러리들 불러오기.
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# 필요한 상수들 정리
g = 9.80665 # m/s² / 지구 표면에서의 중력 가속도
M = 10.0    # 임의의 질량 (kg)
V0 = 20.0   # 초기 발사 속력 (m/s)
H = 10.0    # 폭발 고도 (m)


# 에너지 계산
K_initial = 0.5 * M * V0**2 # 초기 운동에너지
E_expo = K_initial / 10.0 # 폭발 에너지 (초기 운동에너지의 1/10)


# 지상 10m 폭발 순간의 물리량 계산
# 10m까지 올라가는데 걸린 시간 (t_rise)
t_rise = (V0 - np.sqrt(V0**2 - 2 * g * H)) / g

# 10m 고도에서의 수직 상승 속도 (V_H)
V_H = V0 - g * t_rise 
print(f"폭발 시점의 높이: {H}m, 폭발 직전 본체의 상승 속도: {V_H:.2f} m/s")


# 질량중심(COM) 좌표계에서의 폭발
# 파편 질량은 M/2로 동일. 두 파편의 운동 에너지가 E_expo와 같아야 함.
u = np.sqrt(2 * E_expo / (M / 2))
print(f"질량중심 좌표계에서 파편이 튕겨 나가는 속력: {u:.2f} m/s")

# 랜덤한 폭발 방향 설정 (자유도 1개)
theta = np.random.uniform(0, 2 * np.pi)

# COM 좌표계에서의 파편 속도 (운동량 보존)
u1_x = u * np.cos(theta)
u1_y = u * np.sin(theta)
u2_x = -u1_x
u2_y = -u1_y

# 실험실 좌표계로 속도 변환
# 파편이 터지는 순간 본체가 가지고 있던 상승 속도(V_H)를 y성분에 더해줍니다.
v1_x = u1_x
v1_y = u1_y + V_H

v2_x = u2_x
v2_y = u2_y + V_H


# 바닥에 떨어질 때까지의 비행 시간 계산
t_fall_1 = (v1_y + np.sqrt(v1_y**2 + 2 * g * H)) / g
t_fall_2 = (v2_y + np.sqrt(v2_y**2 + 2 * g * H)) / g


# 애니메이션을 위한 전체 시간 배열
t_max_fall = max(t_fall_1, t_fall_2)
t_total = t_rise + t_max_fall
dt = 0.05
times = np.arange(0, t_total + dt, dt)

# 애니메이션 캔버스 및 시각화 준비
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_title(f'Firework Explosion ($V_0$=20m/s, H=10m)')
ax.set_xlabel('Horizontal Position (m)')
ax.set_ylabel('Vertical Position (m)')

# 그래프 범위 여유롭게 설정
max_x = max(abs(v1_x * t_fall_1), abs(v2_x * t_fall_2)) * 1.5 + 2
max_y = max(
    H + (v1_y**2) / (2 * g) if v1_y > 0 else H,
    H + (v2_y**2) / (2 * g) if v2_y > 0 else H
) * 1.2
ax.set_xlim(-max_x, max_x)
ax.set_ylim(0, max_y)
ax.grid(True)
ax.axhline(0, color='gray', linestyle='-', linewidth=2)

# 그리기 객체들
rocket_line, = ax.plot([], [], 'k--', alpha=0.5)
rocket_point, = ax.plot([], [], 'ko', markersize=8, label='Rocket')

frag1_line, = ax.plot([], [], 'r--', linewidth=2, alpha=0.7)
frag1_point, = ax.plot([], [], 'ro', markersize=6, label='Fragment 1')

frag2_line, = ax.plot([], [], 'b--', linewidth=2, alpha=0.7)
frag2_point, = ax.plot([], [], 'bo', markersize=6, label='Fragment 2')

explosion_mark, = ax.plot([], [], 'y*', markersize=20, label='Explosion Point')
ax.legend(loc='upper right')

# 화면 업데이트 함수
def update(frame):
    t = times[frame]
    
    # 1. 상승 중
    if t <= t_rise:
        t_hist = times[:frame+1]
        x_hist = np.zeros_like(t_hist)
        y_hist = V0 * t_hist - 0.5 * g * t_hist**2
        rocket_line.set_data(x_hist, y_hist)
        rocket_point.set_data([x_hist[-1]], [y_hist[-1]])
        
        frag1_line.set_data([], [])
        frag1_point.set_data([], [])
        frag2_line.set_data([], [])
        frag2_point.set_data([], [])
        explosion_mark.set_data([], [])
        
    # 2. 폭발 후
    else:
        t_rock_hist = times[times <= t_rise]
        rocket_line.set_data(np.zeros_like(t_rock_hist), V0 * t_rock_hist - 0.5 * g * t_rock_hist**2)
        rocket_point.set_data([], [])
        explosion_mark.set_data([0], [H])
        
        t_frames = times[(times > t_rise) & (times <= t)] - t_rise
        
        # 파편 1
        t_frames_1 = np.minimum(t_frames, t_fall_1)
        x1_hist = v1_x * t_frames_1
        y1_hist = H + v1_y * t_frames_1 - 0.5 * g * t_frames_1**2
        frag1_line.set_data(x1_hist, y1_hist)
        if len(x1_hist) > 0:
            frag1_point.set_data([x1_hist[-1]], [y1_hist[-1]])
            
        # 파편 2
        t_frames_2 = np.minimum(t_frames, t_fall_2)
        x2_hist = v2_x * t_frames_2
        y2_hist = H + v2_y * t_frames_2 - 0.5 * g * t_frames_2**2
        frag2_line.set_data(x2_hist, y2_hist)
        if len(x2_hist) > 0:
            frag2_point.set_data([x2_hist[-1]], [y2_hist[-1]])

    return rocket_line, rocket_point, frag1_line, frag1_point, frag2_line, frag2_point, explosion_mark

# 애니메이션 실행 및 화면 표시
ani = animation.FuncAnimation(fig, update, frames=len(times), interval=dt*1000, blit=True)
plt.show()
'''

# 문제 1 - 1 - 그림

'''
import numpy as np
import matplotlib.pyplot as plt

# --- [1] 문제의 초기 조건 설정 (임의의 질량 사용) ---
g = 9.80665
M = 10.0      # 임의의 질량 (kg). 양변에서 약분되므로 결과 궤적에 영향을 주지 않습니다.
V0 = 20.0     # 초기 발사 속력 (m/s)
H = 10.0      # 폭발 고도 (m)

# --- [2] 에너지 계산 ---
# 초기 운동 에너지 및 폭발 에너지 (초기 운동에너지의 1/10)
K_initial = 0.5 * M * V0**2
E_expo = K_initial / 10.0

# --- [3] 지상 10m 폭발 순간의 물리량 계산 ---
# 10m까지 올라가는데 걸린 시간 (t_rise) 
t_rise = (V0 - np.sqrt(V0**2 - 2 * g * H)) / g

# 10m 고도에서의 수직 상승 속도 (V_H)
V_H = V0 - g * t_rise 
print(f"폭발 시점의 높이: {H}m, 폭발 직전 본체의 상승 속도: {V_H:.2f} m/s")

# --- [4] 질량중심(COM) 좌표계에서의 폭발 ---
# 파편 질량은 M/2로 동일. 두 파편의 운동 에너지가 E_expo와 같아야 함.
u = np.sqrt(2 * E_expo / (M / 2))
print(f"질량중심 좌표계에서 파편이 튕겨 나가는 속력: {u:.2f} m/s")

# 랜덤한 폭발 방향 설정 (자유도 1개)
theta = np.random.uniform(0, 2 * np.pi)

# COM 좌표계에서의 파편 속도 (운동량 보존)
u1_x = u * np.cos(theta)
u1_y = u * np.sin(theta)
u2_x = -u1_x
u2_y = -u1_y

# --- [5] 실험실 좌표계로 속도 변환 (핵심!) ---
# 파편이 터지는 순간 본체가 가지고 있던 상승 속도(V_H)를 y성분에 더해줍니다.
v1_x = u1_x
v1_y = u1_y + V_H

v2_x = u2_x
v2_y = u2_y + V_H

# --- [6] 바닥에 떨어질 때까지의 비행 시간 계산 ---
t_fall_1 = (v1_y + np.sqrt(v1_y**2 + 2 * g * H)) / g
t_fall_2 = (v2_y + np.sqrt(v2_y**2 + 2 * g * H)) / g

# --- [7] 정지된 이미지를 그리기 위한 틀 설정 ---
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_title(f'Firework Explosion Trajectories ($V_0$=20m/s, H=10m)')
ax.set_xlabel('Horizontal Position (m)')
ax.set_ylabel('Vertical Position (m)')

# 그래프 범위 여유롭게 설정
max_x = max(abs(v1_x * t_fall_1), abs(v2_x * t_fall_2)) * 1.5 + 2
max_y = max(
    H + (v1_y**2) / (2 * g) if v1_y > 0 else H,
    H + (v2_y**2) / (2 * g) if v2_y > 0 else H
) * 1.2
ax.set_xlim(-max_x, max_x)
ax.set_ylim(0, max_y)
ax.grid(True)
ax.axhline(0, color='gray', linestyle='-', linewidth=2)

# --- [8] 전체 궤적 한꺼번에 그리기 ---

# 1. 로켓 본체 상승 궤적 (t=0부터 t=t_rise까지)
t_rock = np.linspace(0, t_rise, 100) # 촘촘한 시간 배열 생성
x_rock = np.zeros_like(t_rock)
y_rock = V0 * t_rock - 0.5 * g * t_rock**2
ax.plot(x_rock, y_rock, 'k--', alpha=0.5, label='Rocket Rise')
# 폭발 지점 표시 (최종점)
ax.plot(0, H, 'ko', markersize=8)

# 2. 파편 1 궤적 (폭발 시점 t_rise부터 t_rise+t_fall_1까지)
# 단, 그리기 계산을 위해 폭발 이후의 시간 t_frames를 0부터 시작한다고 가정합니다.
t_frag1 = np.linspace(0, t_fall_1, 150) # 촘촘한 시간 배열 생성
x1 = v1_x * t_frag1
y1 = H + v1_y * t_frag1 - 0.5 * g * t_frag1**2
ax.plot(x1, y1, 'r--', linewidth=2, alpha=0.7, label='Fragment 1')
# 최종 도달점 표시
ax.plot(x1[-1], y1[-1], 'ro', markersize=6)

# 3. 파편 2 궤적 (폭발 시점 t_rise부터 t_rise+t_fall_2까지)
t_frag2 = np.linspace(0, t_fall_2, 150) # 촘촘한 시간 배열 생성
x2 = v2_x * t_frag2
y2 = H + v2_y * t_frag2 - 0.5 * g * t_frag2**2
ax.plot(x2, y2, 'b--', linewidth=2, alpha=0.7, label='Fragment 2')
# 최종 도달점 표시
ax.plot(x2[-1], y2[-1], 'bo', markersize=6)

# 레전드(범례) 추가
ax.legend(loc='upper right')

# 💡 [9] 정지 이미지 파일로 저장하기! (plt.show() 전에 호출해야 합니다)
plt.savefig('firework_result.png')
print("성공적으로 'firework_result.png' 이미지 파일이 생성되었습니다!")

# 화면에 VERIFY를 위해 띄워보기 (Overleaf에서는 안 보일 수 있습니다)
plt.show()
'''



# 문제 1 - 2 - 그림

'''
import numpy as np
import matplotlib.pyplot as plt

# --- [1] 문제의 초기 조건 설정 ---
g = 9.80665
M = 10.0      # 임의의 폭죽 질량 (kg)
V0 = 20.0     # 초기 발사 속력 (m/s)
H = 10.0      # 폭발 고도 (m)
N = 10        # 파편의 개수

# --- [2] 에너지 계산 ---
# 초기 운동 에너지의 1/10을 폭발 에너지로 사용
K_initial = 0.5 * M * V0**2
E_expo = K_initial / 10.0 

# --- [3] 지상 10m 폭발 순간의 물리량 계산 ---
# 10m 고도 도달 시간 및 직전의 수직 상승 속도 (V_H)
t_rise = (V0 - np.sqrt(V0**2 - 2 * g * H)) / g
V_H = V0 - g * t_rise 

# --- [4] 질량 및 운동량 무작위 분배 (질량중심 알고리즘 적용) ---
# 1. 질량 무작위 분배 (총합이 M이 되도록)
m_rand = np.random.rand(N)
m = M * (m_rand / np.sum(m_rand))

# 2. 운동량 무작위 부여 및 평균 빼기 (운동량 보존)
p = np.random.randn(N, 2)
p_avg = np.mean(p, axis=0)
p -= p_avg

# 3. 속도로 변환
u = p / m[:, np.newaxis]

# 4. 에너지 보존 스케일링
K_prime = np.sum(0.5 * m * np.sum(u**2, axis=1)) # 현재의 총 운동 에너지
scale = np.sqrt(E_expo / K_prime)
u_scaled = u * scale # 에너지가 보존된 COM 기준 속도

v_x = u_scaled[:, 0]
v_y = u_scaled[:, 1]

# --- [5] 실험실 좌표계로 속도 변환 ---
# 파편이 터지는 순간 본체가 가지고 있던 상승 속도(V_H)를 y성분에 더해줌
v_y += V_H

# --- [6] 바닥에 떨어질 때까지의 비행 시간 계산 ---
t_fall = (v_y + np.sqrt(v_y**2 + 2 * g * H)) / g

# --- [7] 정지된 이미지를 그리기 위한 틀 설정 ---
fig, ax = plt.subplots(figsize=(10, 8))
ax.set_title('Firework Trajectories (10 Fragments, $V_0$=20m/s, H=10m)')
ax.set_xlabel('Horizontal Position (m)')
ax.set_ylabel('Vertical Position (m)')

# 궤적이 잘리지 않도록 그래프 범위 넉넉하게 설정
max_x = np.max(np.abs(v_x * t_fall)) * 1.2
max_y = np.max(np.maximum(0, v_y)**2 / (2 * g) + H) * 1.2
ax.set_xlim(-max_x, max_x)
ax.set_ylim(0, max_y)
ax.grid(True)
ax.axhline(0, color='gray', linestyle='-', linewidth=2)

# --- [8] 전체 궤적 그리기 ---
# 1. 로켓 본체 상승 궤적
t_rock = np.linspace(0, t_rise, 100)
x_rock = np.zeros_like(t_rock)
y_rock = V0 * t_rock - 0.5 * g * t_rock**2
ax.plot(x_rock, y_rock, 'k--', alpha=0.5, label='Rocket Rise')
ax.plot(0, H, 'ko', markersize=8, label='Explosion Point') # 폭발 지점 (별표 대신 검은 원)

# 2. 10개의 파편 궤적 그리기
colors = plt.cm.plasma(np.linspace(0, 1, N)) # 그라데이션 색상

for i in range(N):
    t_frag = np.linspace(0, t_fall[i], 150)
    x_frag = v_x[i] * t_frag
    y_frag = H + v_y[i] * t_frag - 0.5 * g * t_frag**2
    
    # 궤적 점선 
    ax.plot(x_frag, y_frag, '--', color=colors[i], linewidth=1.5, alpha=0.7)
    
    # 바닥에 닿은 최종 도달점 (질량이 클수록 동그라미가 크도록 계산)
    point_size = (m[i] / np.max(m)) * 8 + 3
    ax.plot(x_frag[-1], y_frag[-1], 'o', color=colors[i], markersize=point_size)

# 범례 추가 (파편이 많아 로켓 궤적과 폭발 지점만 표시)
ax.legend(loc='upper right')

plt.show()
'''




# 문제 1 - 2 - 영상

'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- [1] 문제의 초기 조건 설정 ---
g = 9.80665
M = 10.0      
V0 = 20.0     
H = 10.0      
N = 10        

# --- [2] 에너지 계산 ---
K_initial = 0.5 * M * V0**2
E_expo = K_initial / 10.0 

# --- [3] 지상 10m 폭발 순간의 물리량 계산 ---
t_rise = (V0 - np.sqrt(V0**2 - 2 * g * H)) / g
V_H = V0 - g * t_rise 

# --- [4] 질량 및 운동량 무작위 분배 (질량중심 알고리즘 적용) ---
m_rand = np.random.rand(N)
m = M * (m_rand / np.sum(m_rand))

p = np.random.randn(N, 2)
p_avg = np.mean(p, axis=0)
p -= p_avg

u = p / m[:, np.newaxis]

K_prime = np.sum(0.5 * m * np.sum(u**2, axis=1)) 
scale = np.sqrt(E_expo / K_prime)
u_scaled = u * scale 

v_x = u_scaled[:, 0]
v_y = u_scaled[:, 1]

# --- [5] 실험실 좌표계로 속도 변환 ---
v_y += V_H

# --- [6] 바닥에 떨어질 때까지의 비행 시간 계산 ---
t_fall = (v_y + np.sqrt(v_y**2 + 2 * g * H)) / g


# 💡 [새로 추가된 부분] 애니메이션을 위한 통합 시간 배열 생성
t_max_fall = np.max(t_fall)
t_total = t_rise + t_max_fall
dt = 0.05
times = np.arange(0, t_total + dt, dt)

# --- [7] 애니메이션 캔버스 준비 ---
fig, ax = plt.subplots(figsize=(10, 8))
ax.set_title('Firework Animation (10 Fragments, $V_0$=20m/s, H=10m)')
ax.set_xlabel('Horizontal Position (m)')
ax.set_ylabel('Vertical Position (m)')

max_x = np.max(np.abs(v_x * t_fall)) * 1.2
max_y = np.max(np.maximum(0, v_y)**2 / (2 * g) + H) * 1.2
ax.set_xlim(-max_x, max_x)
ax.set_ylim(0, max_y)
ax.grid(True)
ax.axhline(0, color='gray', linestyle='-', linewidth=2)

# 본체 및 폭발 지점 객체 (폭발 지점은 요청대로 검은 원으로 설정)
rocket_line, = ax.plot([], [], 'k--', alpha=0.5, label='Rocket Rise')
rocket_point, = ax.plot([], [], 'ko', markersize=8)
explosion_mark, = ax.plot([], [], 'ko', markersize=8, label='Explosion Point')

# 파편 10개를 담을 리스트 준비
frag_lines = []
frag_points = []
colors = plt.cm.plasma(np.linspace(0, 1, N))

for i in range(N):
    line, = ax.plot([], [], '--', color=colors[i], linewidth=1.5, alpha=0.7)
    point_size = (m[i] / np.max(m)) * 8 + 3 # 질량에 비례하는 크기
    point, = ax.plot([], [], 'o', color=colors[i], markersize=point_size)
    frag_lines.append(line)
    frag_points.append(point)

ax.legend(loc='upper right')

# --- [8] 매 프레임 업데이트 함수 ---
def update(frame):
    t = times[frame]
    
    # 1. 폭발 전 (상승 중)
    if t <= t_rise:
        t_hist = times[:frame+1]
        x_hist = np.zeros_like(t_hist)
        y_hist = V0 * t_hist - 0.5 * g * t_hist**2
        
        rocket_line.set_data(x_hist, y_hist)
        rocket_point.set_data([x_hist[-1]], [y_hist[-1]])
        
        # 파편 숨기기
        for i in range(N):
            frag_lines[i].set_data([], [])
            frag_points[i].set_data([], [])
        explosion_mark.set_data([], [])
        
    # 2. 폭발 후
    else:
        # 본체 자취 고정
        t_rock_hist = times[times <= t_rise]
        rocket_line.set_data(np.zeros_like(t_rock_hist), V0 * t_rock_hist - 0.5 * g * t_rock_hist**2)
        rocket_point.set_data([], [])
        explosion_mark.set_data([0], [H])
        
        # 터진 이후 흐른 시간 배열
        t_frames = times[(times > t_rise) & (times <= t)] - t_rise
        
        # 10개 파편 각각의 궤적 업데이트
        for i in range(N):
            t_frames_i = np.minimum(t_frames, t_fall[i])
            x_hist = v_x[i] * t_frames_i
            y_hist = H + v_y[i] * t_frames_i - 0.5 * g * t_frames_i**2
            
            frag_lines[i].set_data(x_hist, y_hist)
            if len(x_hist) > 0:
                frag_points[i].set_data([x_hist[-1]], [y_hist[-1]])

    return (rocket_line, rocket_point, explosion_mark, *frag_lines, *frag_points)

# --- [9] 애니메이션 실행 ---
ani = animation.FuncAnimation(fig, update, frames=len(times), interval=dt*1000, blit=True)

plt.show()
'''


'''
# 문제 1 - 3 그림

import numpy as np
import matplotlib.pyplot as plt

# --- [1] 문제의 초기 조건 설정 ---
g = 9.80665
M = 10.0      # 임의의 질량
V0 = 20.0     # 초기 발사 속력 (m/s)
H = 10.0      # 폭발 고도 (m)
N = 10        # 파편의 개수
theta_0 = np.radians(80) # 발사 각도 (80도를 라디안으로 변환)

# --- [2] 에너지 계산 ---
# 💡 폭발 에너지가 초기 운동에너지와 '같음' (100%)
K_initial = 0.5 * M * V0**2
E_expo = K_initial 

# --- [3] 비스듬히 쏘아올린 10m 폭발 순간의 물리량 계산 ---
# x, y축 초기 속도 분리
V0_x = V0 * np.cos(theta_0)
V0_y = V0 * np.sin(theta_0)

# 10m 고도 도달 시간 (y축 속도 기준)
t_rise = (V0_y - np.sqrt(V0_y**2 - 2 * g * H)) / g

# 폭발 직전 본체의 속도와 위치
V_Hx = V0_x                 # x축은 등속 운동이므로 속도 불변
V_Hy = V0_y - g * t_rise    # y축은 등가속도 운동
X_H = V0_x * t_rise         # 💡 터지는 순간의 x 좌표!

print(f"터지는 위치: x = {X_H:.2f}m, y = {H}m")
print(f"터지기 직전 본체 속도: Vx = {V_Hx:.2f}m/s, Vy = {V_Hy:.2f}m/s")

# --- [4] 질량 및 운동량 무작위 분배 (질량중심 알고리즘) ---
m_rand = np.random.rand(N)
m = M * (m_rand / np.sum(m_rand))

p = np.random.randn(N, 2)
p_avg = np.mean(p, axis=0)
p -= p_avg

u = p / m[:, np.newaxis]

K_prime = np.sum(0.5 * m * np.sum(u**2, axis=1)) 
scale = np.sqrt(E_expo / K_prime)
u_scaled = u * scale 

# --- [5] 실험실 좌표계로 속도 변환 ---
# 💡 x축과 y축 모두에 본체의 속도를 더해줍니다!
v_x = u_scaled[:, 0] + V_Hx
v_y = u_scaled[:, 1] + V_Hy

# --- [6] 바닥에 떨어질 때까지의 비행 시간 계산 ---
t_fall = (v_y + np.sqrt(v_y**2 + 2 * g * H)) / g

# --- [7] 정지된 이미지를 그리기 위한 틀 설정 ---
fig, ax = plt.subplots(figsize=(12, 8)) # 가로로 더 넓게 이동하므로 비율 조정
ax.set_title(f'Firework Trajectories (80 Degree Launch, $E_{{expo}}=K_0$, N=10)')
ax.set_xlabel('Horizontal Position (m)')
ax.set_ylabel('Vertical Position (m)')

# 그래프 범위 여유롭게 설정 (시작점 0부터 파편 도달점까지)
min_x = min(0, np.min(X_H + v_x * t_fall)) * 1.2
max_x = max(X_H, np.max(X_H + v_x * t_fall)) * 1.2
max_y = np.max(np.maximum(0, v_y)**2 / (2 * g) + H) * 1.1

ax.set_xlim(min_x, max_x)
ax.set_ylim(0, max_y)
ax.grid(True)
ax.axhline(0, color='gray', linestyle='-', linewidth=2)

# --- [8] 전체 궤적 그리기 ---
# 1. 로켓 본체 80도 상승 궤적
t_rock = np.linspace(0, t_rise, 100)
x_rock = V0_x * t_rock
y_rock = V0_y * t_rock - 0.5 * g * t_rock**2
ax.plot(x_rock, y_rock, 'k--', alpha=0.5, label='Rocket Rise (80°)')
ax.plot(X_H, H, 'ko', markersize=8, label='Explosion Point') # 폭발 위치 이동!

# 2. 10개의 파편 궤적 그리기
colors = plt.cm.plasma(np.linspace(0, 1, N)) 

for i in range(N):
    t_frag = np.linspace(0, t_fall[i], 150)
    # 💡 시작점이 (0, H)가 아니라 (X_H, H)입니다!
    x_frag = X_H + v_x[i] * t_frag
    y_frag = H + v_y[i] * t_frag - 0.5 * g * t_frag**2
    
    ax.plot(x_frag, y_frag, '--', color=colors[i], linewidth=1.5, alpha=0.7)
    
    point_size = (m[i] / np.max(m)) * 8 + 3
    ax.plot(x_frag[-1], y_frag[-1], 'o', color=colors[i], markersize=point_size)

ax.legend(loc='upper right')

# --- [9] 이미지 파일로 저장 ---
plt.savefig('firework_80deg_huge_explosion.png', dpi=300) 
print("성공적으로 'firework_80deg_huge_explosion.png' 파일이 생성되었습니다!")

plt.show()
'''