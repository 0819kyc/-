# 고급계산과학 1주 차 주별 과제

# 지표면 중력장 운동 모델링 - 수치해석적 방법
# 목표 : 지표면 중력장에서 운동하는 물체의 위치와 속도를 계산하는 모델을 수치해석적으로 구현

# 문제 1 - 1

'''
# 필요한 라이브러리들 불러오기.
import numpy as np
import matplotlib.pyplot as plt


# 필요한 상수들 정리
g = 9.80665 #m/s² / 지구 표면에서의 중력 가속도 | Wikipedia에 나와있는 값을 가져왔다.
dt = 0.01 # 시간 간격 (s)


# 초기 조건

v0 = float(input("초기 속도 (m/s) : ")) # 초기 속도(m/s)
theta = float(input("초기 각도 (deg) : ")) # 발사 각도(degree)
theta_rad = np.radians(theta) # 발사 각도를 라디안으로 변환

vx = v0 * np.cos(theta_rad) # 초기 수평 속도
vy = v0 * np.sin(theta_rad) # 초기 수직 속도

x = 0.0 # 초기 수평 위치 (m)
y = 0.0 # 초기 수직 위치 (m)

t = 0.0 # 시작 시간


# 시뮬레이션을 위한 리스트 초기화

time = [] # 시간 값 저장할 리스트
position_x = [] # 수평 위치 x 저장할 리스트
position_y = [] # 수직 위치 x 저장할 리스트

velocity_x = [] # 수평 속도 vx 저장할 리스트
velocity_y = [] # 수직 속도 vy 저장할 리스트

while y >= 0: # 바닥에 도착할 때까지만 시작.
    time.append(t)
    position_x.append(x)
    position_y.append(y)
    velocity_y.append(vy)
    
    x += vx * dt
    y += vy * dt
    
    vy -= g * dt
    
    t += dt

# 시각화
plt.figure(figsize=(10, 5))

# 궤적 그래프
plt.plot(position_x, position_y)
plt.title('Projectile Trajectory')
plt.xlabel('Distance (m)')
plt.ylabel('Height (m)')
plt.grid(True)

plt.tight_layout()
plt.show()
'''



# 부가 사항 1 - 1 - 1) 초기 속도를 고정하고, 발사 각도만 변경하였을 때.

'''
import numpy as np
import matplotlib.pyplot as plt

# 필요한 상수 정리
g = 9.80665 # m/s²
dt = 0.01   # 시간 간격 (s)

# 고정된 초기 속도
v0 = 10.0

# 시뮬레이션할 발사 각도들 (degree)
angles = [15, 30, 45, 60, 75, 90]

plt.figure(figsize=(10, 6))

for theta in angles:
    # 초기 조건 설정
    theta_rad = np.radians(theta)
    vx = v0 * np.cos(theta_rad)
    vy = v0 * np.sin(theta_rad)
    
    # 위치 및 시간 초기화
    x, y = 0.0, 0.0
    t = 0.0
    
    # 각 각도별 궤적 저장을 위한 리스트
    pos_x = []
    pos_y = []
    
    # 시뮬레이션 루프 (지면에 닿을 때까지)
    while y >= 0:
        pos_x.append(x)
        pos_y.append(y)
        
        # 위치 업데이트 (현재 속도 기준)
        x += vx * dt
        y += vy * dt
        
        # 속도 업데이트 (중력 가속도 반영)
        vy -= g * dt
        
        t += dt
    
    # 그래프 그리기 (각도별로 레이블 설정)
    plt.plot(pos_x, pos_y, label=f'{theta}°')

# 그래프 꾸미기
plt.title(f'Projectile Trajectories ($v_0 = {v0}$ m/s)')
plt.xlabel('Distance (m)')
plt.ylabel('Height (m)')
plt.axhline(0, color='black', linewidth=1) # 지면 표시
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(title='Launch Angle') # 범례 추가
plt.axis('equal') # x축과 y축의 비율을 동일하게 설정

plt.tight_layout()
plt.show()
'''

# 부가 사항 1 - 1 - 2) 초기 속도를 고정하고, 발사 각도만 변경하였을 때. - 영상

'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 1. 시뮬레이션 환경 설정
g = 9.80665
dt = 0.02  # 애니메이션을 부드럽게 하기 위한 시간 간격
v0 = 10.0
angles = [15, 30, 45, 60, 75, 90]

# 2. 모든 데이터 미리 계산 (Pre-calculation)
all_trajectories = []
max_x, max_y = 0, 0

for theta in angles:
    theta_rad = np.radians(theta)
    vx = v0 * np.cos(theta_rad)
    vy = v0 * np.sin(theta_rad)
    
    x, y = 0.0, 0.0
    path_x, path_y = [], []
    
    while y >= -0.05:  # 지면에 거의 닿을 때까지
        path_x.append(x)
        path_y.append(y)
        x += vx * dt
        y += vy * dt
        vy -= g * dt
    
    all_trajectories.append((path_x, path_y))
    max_x = max(max_x, max(path_x))
    max_y = max(max_y, max(path_y))

# 3. 그래프 초기 설정
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, max_x * 1.1)
ax.set_ylim(0, max_y * 1.1)
ax.set_aspect('equal')
ax.grid(True, linestyle='--', alpha=0.5)
ax.set_title(f'Projectile Motion by Launch Angles ($v_0$ = {v0}m/s)', fontsize=14)
ax.set_xlabel('Distance (m)')
ax.set_ylabel('Height (m)')

# 애니메이션 요소: 각 선(line)과 현재 위치 점(dot) 생성
lines = [ax.plot([], [], label=f'{a}°', lw=1.5)[0] for a in angles]
dots = [ax.plot([], [], 'o')[0] for _ in angles]
ax.legend(title="Launch Angle", loc='upper right')

# 4. 애니메이션 업데이트 함수
def update(frame):
    for i, (path_x, path_y) in enumerate(all_trajectories):
        # 현재 프레임이 데이터 길이보다 길면 마지막 위치 유지
        current_idx = min(frame, len(path_x) - 1)
        
        lines[i].set_data(path_x[:current_idx], path_y[:current_idx])
        dots[i].set_data([path_x[current_idx]], [path_y[current_idx]])
    
    return lines + dots

# 5. 애니메이션 실행 및 저장 설정
max_frames = max(len(p[0]) for p in all_trajectories)
ani = FuncAnimation(fig, update, frames=max_frames, interval=25, blit=True)

# GIF로 저장하고 싶다면 아래 주석을 해제하세요 (pillow 설치 필요)
# ani.save('projectile_angles.gif', writer='pillow', fps=30)

plt.tight_layout()
plt.show()
'''



#부가 사항 1 - 2 - 1) 발사 각도는 고정하고, 초기 속도만 변경하였을 때.

'''
import numpy as np
import matplotlib.pyplot as plt

# 필요한 상수 정리
g = 9.80665 # m/s²
dt = 0.01   # 시간 간격 (s)

# 고정된 발사 각도 (45도)
theta = 45.0
theta_rad = np.radians(theta)

# 시뮬레이션할 초기 속도들 (m/s)
velocities = [5, 10, 15, 20, 25]

plt.figure(figsize=(10, 6))

for v0 in velocities:
    # 각 속도별 초기 속도 성분 계산
    vx = v0 * np.cos(theta_rad)
    vy = v0 * np.sin(theta_rad)
    
    # 위치 및 시간 초기화
    x, y = 0.0, 0.0
    t = 0.0
    
    # 데이터 저장을 위한 리스트
    pos_x = []
    pos_y = []
    
    # 시뮬레이션 루프
    while y >= 0:
        pos_x.append(x)
        pos_y.append(y)
        
        # 위치 업데이트
        x += vx * dt
        y += vy * dt
        
        # 속도 업데이트
        vy -= g * dt
        t += dt
    
    # 그래프 그리기 (속도별로 레이블 설정)
    plt.plot(pos_x, pos_y, label=f'$v_0 = {v0}$ m/s')

# 그래프 디자인
plt.title(f'Projectile Trajectories at {theta}° Launch Angle', fontsize=14)
plt.xlabel('Distance (m)')
plt.ylabel('Height (m)')
plt.axhline(0, color='black', linewidth=1) # 지면 표시
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(title='Initial Velocity')
plt.axis('equal') # 물리적 비율 유지

plt.tight_layout()
plt.show()
'''



#부가 사항 1 - 2 - 2) 발사 각도는 고정하고, 초기 속도만 변경하였을 때. - 영상
'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import Animation, FuncAnimation

# 1. 시뮬레이션 환경 설정
g = 9.80665
dt = 0.02  # 애니메이션 속도를 위해 시간 간격을 조금 조정했습니다.
theta = 45.0
theta_rad = np.radians(theta)
velocities = [5, 10, 15, 20, 25]

# 2. 모든 데이터 미리 계산 (Pre-calculation)
all_trajectories = []
max_x = 0
max_y = 0

for v0 in velocities:
    vx = v0 * np.cos(theta_rad)
    vy = v0 * np.sin(theta_rad)
    x, y = 0.0, 0.0
    
    path_x, path_y = [], []
    while y >= -0.1:  # 지면에 살짝 닿을 때까지
        path_x.append(x)
        path_y.append(y)
        x += vx * dt
        y += vy * dt
        vy -= g * dt
    
    all_trajectories.append((path_x, path_y))
    max_x = max(max_x, max(path_x))
    max_y = max(max_y, max(path_y))

# 3. 그래프 초기 설정
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, max_x * 1.1)
ax.set_ylim(0, max_y * 1.1)
ax.set_aspect('equal')
ax.grid(True, linestyle='--', alpha=0.5)
ax.set_title(f'Projectile Motion Animation at {theta}° launch angle', fontsize=14)
ax.set_xlabel('Distance (m)')
ax.set_ylabel('Height (m)')

# 애니메이션 요소: 선(line)과 점(point) 생성
lines = [ax.plot([], [], label=f'$v_0={v}$m/s', lw=1.5)[0] for v in velocities]
dots = [ax.plot([], [], 'o')[0] for _ in velocities]
ax.legend(loc='upper right')

# 4. 애니메이션 업데이트 함수
def update(frame):
    for i, (path_x, path_y) in enumerate(all_trajectories):
        # 프레임 번호가 데이터 길이보다 크면 마지막 위치에 고정
        current_idx = min(frame, len(path_x) - 1)
        
        # 지나온 궤적 그리기
        lines[i].set_data(path_x[:current_idx], path_y[:current_idx])
        # 현재 물체 위치 점으로 표시
        dots[i].set_data([path_x[current_idx]], [path_y[current_idx]])
    
    return lines + dots

# 5. 애니메이션 실행
# frames는 가장 긴 궤적의 길이를 기준으로 설정
max_frames = max(len(p[0]) for p in all_trajectories)
ani = FuncAnimation(fig, update, frames=max_frames, interval=20, blit=True)

plt.tight_layout()
plt.show()
'''



# 문제 1 - 2) 탄성 계수(Coefficient of Restitution)를 고려하여, 표면 중력장에서 운동하는 물체의 위치와 속도를 계산하는 모델을 수치해석적으로 구현.

'''
import numpy as np
import matplotlib.pyplot as plt

# 상수 설정
g = 9.80665
dt = 0.01
e = 0.8  # 탄성계수 (Coefficient of Restitution)

# 초기 조건 입력
v0 = float(input("초기 속도 (m/s) : "))
theta = float(input("초기 각도 (deg) : "))
theta_rad = np.radians(theta)

vx = v0 * np.cos(theta_rad)
vy = v0 * np.sin(theta_rad)

x, y = 0.0, 0.0
t = 0.0

# 저장용 리스트
pos_x = []
pos_y = []

# 시뮬레이션 (시간 제한을 두어 무한 루프 방지)
t_max = 10.0 
while t < t_max:
    pos_x.append(x)
    pos_y.append(y)
    
    # 위치 업데이트
    x += vx * dt
    y += vy * dt
    
    # 속도 업데이트 (중력 가속도)
    vy -= g * dt
    
    # 지면 충돌 처리 (바운딩)
    if y < 0:
        y = 0          # 지면 아래로 내려가지 않게 보정
        vy = -vy * e   # 수직 속도 반전 및 에너지 감쇄
        
        # 에너지가 너무 작아지면 멈춤 (선택 사항)
        if abs(vy) < 0.1: 
            break
            
    t += dt

# 시각화
plt.figure(figsize=(12, 5))
plt.plot(pos_x, pos_y, label=f'e = {e}')
plt.axhline(0, color='black', lw=2) # 지면
plt.title(f'Projectile Motion with Bouncing ($v_0 = {v0}$, angle = {theta}°, e = {e})')
plt.xlabel('Distance (m)')
plt.ylabel('Height (m)')
plt.grid(True, linestyle='--')
plt.legend()
plt.show()
'''



# 부가사항 2 - 1 - 1 - 1) 탄성 계수(Coefficient of Restitution)를 고려하에, 초기 속도를 고정하고, 발사 각도만 변경하였을 때.

'''
import numpy as np
import matplotlib.pyplot as plt

# 1. 상수 설정
g = 9.80665
dt = 0.005  # 충돌 지점의 정밀도를 위해 dt를 조금 더 줄였습니다.
e = 0.8     # 탄성계수
v0 = 10.0   # 초기 속도 고정
angles = [15, 30, 45, 60, 75, 90]

plt.figure(figsize=(12, 6))

# 2. 각 각도별 시뮬레이션 반복
for theta in angles:
    theta_rad = np.radians(theta)
    
    vx = v0 * np.cos(theta_rad)
    vy = v0 * np.sin(theta_rad)
    
    x, y = 0.0, 0.0
    t = 0.0
    t_max = 10.0  # 최대 시뮬레이션 시간
    
    pos_x = []
    pos_y = []
    
    while t < t_max:
        pos_x.append(x)
        pos_y.append(y)
        
        # 위치 업데이트
        x += vx * dt
        y += vy * dt
        
        # 속도 업데이트 (수직 방향 가속도)
        vy -= g * dt
        
        # 지면 충돌 처리
        if y < 0:
            y = 0          # 위치 보정
            vy = -vy * e   # 수직 속도 반전 및 감쇄
            
            # 에너지가 너무 작아져서 사실상 멈춘 경우 루프 탈출
            if abs(vy) < 0.05:
                break
        
        t += dt
    
    # 3. 각 궤적 그래프 그리기
    plt.plot(pos_x, pos_y, label=f'{theta}°')

# 4. 그래프 꾸미기
plt.title(f'Bouncing Projectile Trajectories ($v_0 = {v0}$ m/s, $e = {e}$)', fontsize=14)
plt.xlabel('Distance (m)')
plt.ylabel('Height (m)')
plt.axhline(0, color='black', lw=2)  # 지면 표시
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(title='Launch Angle', loc='upper right')
plt.axis('equal')  # 가로세로 비율 동일하게

plt.tight_layout()
plt.show()
'''



# 부가사항 2 - 1 - 1 - 2) 탄성 계수(Coefficient of Restitution)를 고려하에, 초기 속도를 고정하고, 발사 각도만 변경하였을 때. | 발사 이후 지면에 2번 닿을 때까지만.

'''
import numpy as np
import matplotlib.pyplot as plt

# 1. 상수 설정
g = 9.80665
dt = 0.005  
e = 0.8     
v0 = 10.0   
angles = [15, 30, 45, 60, 75, 90]

plt.figure(figsize=(12, 6))

# 2. 각 각도별 시뮬레이션 반복
for theta in angles:
    theta_rad = np.radians(theta)
    
    vx = v0 * np.cos(theta_rad)
    vy = v0 * np.sin(theta_rad)
    
    x, y = 0.0, 0.0
    bounce_count = 0  # 튕긴 횟수를 저장할 변수
    
    pos_x = []
    pos_y = []
    
    # 튕긴 횟수가 2회 미만일 때까지만 루프 실행
    while bounce_count < 2:
        pos_x.append(x)
        pos_y.append(y)
        
        # 위치 업데이트
        x += vx * dt
        y += vy * dt
        
        # 속도 업데이트
        vy -= g * dt
        
        # 지면 충돌 처리
        if y < 0:
            y = 0          
            vy = -vy * e   
            bounce_count += 1  # 충돌 시 카운트 증가
            
            # 에너지가 너무 작아지는 경우를 대비한 안전장치
            if abs(vy) < 0.05:
                break
    
    # 마지막 지점 저장 (바닥에 닿은 지점)
    pos_x.append(x)
    pos_y.append(y)
    
    # 3. 궤적 그래프 그리기
    plt.plot(pos_x, pos_y, label=f'{theta}°')

# 4. 그래프 디자인
plt.title(f'Projectile Trajectories: Up to 2 Bounces ($v_0 = {v0}$, $e = {e}$)', fontsize=14)
plt.xlabel('Distance (m)')
plt.ylabel('Height (m)')
plt.axhline(0, color='black', lw=2) 
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(title='Launch Angle', loc='upper right')
plt.axis('equal') 

plt.tight_layout()
plt.show()
'''



# 부가사항 2 - 1 - 1 - 3) 탄성 계수(Coefficient of Restitution)를 고려하에, 초기 속도를 고정하고, 발사 각도만 변경하였을 때. | 발사 이후 지면에 2번 닿을 때까지만. - 영상

'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 1. 상수 및 초기 설정
g = 9.80665
dt = 0.01  # 애니메이션 속도를 위해 dt를 약간 조절
e = 0.8     
v0 = 10.0   
angles = [15, 30, 45, 60, 75, 90]

# 각 각도별 궤적 미리 계산 (애니메이션 효율을 위함)
trajectories = []
max_len = 0

for theta in angles:
    theta_rad = np.radians(theta)
    vx, vy = v0 * np.cos(theta_rad), v0 * np.sin(theta_rad)
    x, y = 0.0, 0.0
    bounce_count = 0
    
    pos_x, pos_y = [0.0], [0.0]
    
    while bounce_count < 2:
        x += vx * dt
        y += vy * dt
        vy -= g * dt
        
        if y < 0:
            y = 0
            vy = -vy * e
            bounce_count += 1
            if abs(vy) < 0.1: break
            
        pos_x.append(x)
        pos_y.append(y)
    
    trajectories.append((pos_x, pos_y))
    max_len = max(max_len, len(pos_x))

# 2. 그래프 초기화
fig, ax = plt.subplots(figsize=(12, 6))
lines = [ax.plot([], [], label=f'{theta}°')[0] for theta in angles]
points = [ax.plot([], [], 'o')[0] for _ in angles] # 현재 위치를 나타낼 점

ax.set_xlim(0, 15)
ax.set_ylim(0, 6)
ax.set_aspect('equal')
ax.grid(True, linestyle='--', alpha=0.6)
ax.axhline(0, color='black', lw=2)
ax.legend(title='Launch Angle')
ax.set_title(f'Animated Projectile Trajectories (v0={v0}, e={e})')
ax.set_xlabel('Distance (m)')
ax.set_ylabel('Height (m)')

# 3. 애니메이션 업데이트 함수
def update(frame):
    for i, (px, py) in enumerate(trajectories):
        # 현재 프레임까지의 경로 업데이트
        if frame < len(px):
            lines[i].set_data(px[:frame], py[:frame])
            points[i].set_data([px[frame]], [py[frame]]) # 리스트 형태로 전달
        else:
            # 시뮬레이션 종료 후 마지막 위치 유지
            lines[i].set_data(px, py)
            points[i].set_data([px[-1]], [py[-1]])
            
    return lines + points

# 4. 애니메이션 실행
# frames는 가장 긴 궤적의 길이만큼, interval은 프레임 간격(ms)
ani = FuncAnimation(fig, update, frames=max_len, interval=15, blit=True)

plt.tight_layout()
plt.show()
'''



## 부가사항 2 - 1 - 2 - 1) 탄성 계수(Coefficient of Restitution)를 고려하에, 발사 각도를 고정하고, 초기 속도를 변경하였을 때.

'''
import numpy as np
import matplotlib.pyplot as plt

# 1. 상수 및 조건 설정
g = 9.80665
dt = 0.005  
e = 0.8     
angle = 45  
velocities = [5, 10, 15, 20, 25] 

plt.figure(figsize=(12, 6))

for v0 in velocities:
    theta_rad = np.radians(angle)
    vx = v0 * np.cos(theta_rad)
    vy = v0 * np.sin(theta_rad)
    
    x, y = 0.0, 0.0
    pos_x, pos_y = [0.0], [0.0]
    
    # 안전장치: 최대 시간(t_max) 설정 (무한 루프 방지)
    t = 0
    t_max = 20.0 
    
    while t < t_max:
        x += vx * dt
        y += vy * dt
        vy -= g * dt
        t += dt
        
        if y < 0:
            y = 0          
            vy = -vy * e   
            
            # 수직 에너지가 거의 다했을 때 확실히 종료
            if abs(vy) < 0.1:
                pos_x.append(x)
                pos_y.append(y)
                break
        
        pos_x.append(x)
        pos_y.append(y)
    
    plt.plot(pos_x, pos_y, label=f'$v_0$ = {v0} m/s')

plt.title(f'Projectile Trajectories (Angle = {angle}°, $e = {e}$)')
plt.xlabel('Distance (m)')
plt.ylabel('Height (m)')
plt.axhline(0, color='black', lw=2)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.axis('equal')

plt.tight_layout()
plt.show()
'''

## 부가사항 2 - 1 - 2 - 2) 탄성 계수(Coefficient of Restitution)를 고려하에, 발사 각도를 고정하고, 초기 속도를 변경하였을 때. | 발사 이후 지면에 2번 닿을 때까지만.

'''
import numpy as np
import matplotlib.pyplot as plt

# 1. 상수 및 조건 설정
g = 9.80665
dt = 0.005  
e = 0.8     # 탄성 계수
angle = 45  # 발사 각도
velocities = [5, 10, 15, 20, 25] 

plt.figure(figsize=(12, 6))

# 2. 각 속도별 시뮬레이션 반복
for v0 in velocities:
    theta_rad = np.radians(angle)
    vx = v0 * np.cos(theta_rad)
    vy = v0 * np.sin(theta_rad)
    
    x, y = 0.0, 0.0
    pos_x, pos_y = [0.0], [0.0]
    
    bounce_count = 0  # 충돌 횟수 카운터
    
    # 충돌 횟수가 2회 미만일 때까지만 실행 (0회: 첫 비행, 1회: 첫 바운스)
    # 2회째 지면에 닿는 순간 루프를 종료합니다.
    while bounce_count < 2:
        x += vx * dt
        y += vy * dt
        vy -= g * dt
        
        if y < 0:
            y = 0          # 위치 보정
            vy = -vy * e   # 속도 반전 및 감쇄
            bounce_count += 1  # 충돌 시 카운트 증가
            
            # 충돌 횟수를 채웠다면 루프 탈출
            if bounce_count >= 2:
                pos_x.append(x)
                pos_y.append(y)
                break
        
        pos_x.append(x)
        pos_y.append(y)
    
    # 3. 궤적 그래프 그리기
    plt.plot(pos_x, pos_y, label=f'$v_0$ = {v0} m/s', lw=2)

# 4. 그래프 디자인
plt.title(f'Projectile Trajectories: First 2 Bounces (Angle = {angle}°, $e = {e}$)', fontsize=14)
plt.xlabel('Distance (m)')
plt.ylabel('Height (m)')
plt.axhline(0, color='black', lw=2)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(title='Initial Velocity')
plt.axis('equal')

plt.tight_layout()
plt.show()
'''



## 부가사항 2 - 1 - 2 - 3) 탄성 계수(Coefficient of Restitution)를 고려하에, 발사 각도를 고정하고, 초기 속도를 변경하였을 때. | 발사 이후 지면에 2번 닿을 때까지만. - 영상

'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 1. 상수 및 시뮬레이션 설정
g = 9.80665
dt = 0.015  # 애니메이션 재생 속도 조절
e = 0.8     
angle = 45  
velocities = [5, 10, 15, 20, 25]
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

# 데이터 선행 계산
all_trajectories = []
max_len = 0

for v0 in velocities:
    theta_rad = np.radians(angle)
    vx, vy = v0 * np.cos(theta_rad), v0 * np.sin(theta_rad)
    x, y = 0.0, 0.0
    pos_x, pos_y = [0.0], [0.0]
    bounce_count = 0
    
    while bounce_count < 2:
        x += vx * dt
        y += vy * dt
        vy -= g * dt
        
        if y < 0:
            y = 0
            vy = -vy * e
            bounce_count += 1
            if bounce_count >= 2:
                pos_x.append(x)
                pos_y.append(y)
                break
        
        pos_x.append(x)
        pos_y.append(y)
    
    all_trajectories.append((pos_x, pos_y))
    max_len = max(max_len, len(pos_x))

# 2. 그래프 및 아티스트(Line, Point) 초기화
fig, ax = plt.subplots(figsize=(12, 6))
lines = [ax.plot([], [], color=colors[i], lw=2, label=f'{v} m/s')[0] for i, v in enumerate(velocities)]
points = [ax.plot([], [], 'o', color=colors[i])[0] for i in range(len(velocities))]

ax.set_xlim(0, 90)  # 25m/s가 두 번 튕겼을 때의 예상 거리
ax.set_ylim(0, 20)
ax.set_aspect('equal')
ax.grid(True, linestyle='--', alpha=0.5)
ax.axhline(0, color='black', lw=2)
ax.set_title(f'Projectile Animation: First 2 Bounces (Angle={angle}°, e={e})')
ax.legend(loc='upper right')

# 3. 애니메이션 업데이트 함수
def update(frame):
    for i, (px, py) in enumerate(all_trajectories):
        # 현재 프레임까지의 궤적 표시
        current_idx = min(frame, len(px) - 1)
        lines[i].set_data(px[:current_idx], py[:current_idx])
        points[i].set_data([px[current_idx]], [py[current_idx]])
    return lines + points

# 4. 애니메이션 실행
ani = FuncAnimation(fig, update, frames=max_len, interval=20, blit=True)

plt.tight_layout()
plt.show()
'''