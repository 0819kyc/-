# 고급계산과학 3주 차 주별 과제

# 몬테카를로 방법(Monte Carlo Method)

# Q1

# Q1 - (a)

'''
import numpy as np
import matplotlib.pyplot as plt

def estimate_pi_visualize(N):
    # 1. [-1, 1] 사이의 랜덤한 x, y 좌표 생성
    x = np.random.uniform(-1, 1, N)
    y = np.random.uniform(-1, 1, N)
    
    # 2. 원 내부에 있는지 확인 (x^2 + y^2 <= 1)
    # distance_from_center는 시각화할 때 색상을 구분하기 위해 사용
    distance_from_center = x**2 + y**2
    inside_circle = (distance_from_center <= 1)
    M = np.sum(inside_circle)
    
    # 3. pi 추정치 계산 (A * M/N, 여기서 사각형 넓이 A = 4)
    pi_s = 4 * (M / N)
    
    # --- 시각화 부분 ---
    plt.figure(figsize=(8, 8)) # 정사각형 비율 유지
    
    # 원 내부의 점은 파란색(blue), 외부의 점은 빨간색(red)으로 표시
    plt.scatter(x[inside_circle], y[inside_circle], color='blue', s=1, label='Inside Circle')
    plt.scatter(x[~inside_circle], y[~inside_circle], color='red', s=1, label='Outside Circle')
    
    # 경계가 되는 원 그리기 (r=1)
    circle = plt.Circle((0, 0), 1, color='black', fill=False, linewidth=2)
    plt.gca().add_artist(circle)
    
    # 그래프 설정
    plt.xlim(-1.1, 1.1)
    plt.ylim(-1.1, 1.1)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'Monte Carlo Pi Estimation (N={N})\nEstimated Pi = {pi_s:.5f}')
    plt.legend(loc='upper right')
    plt.grid(True, linestyle='--')
    plt.axis('equal') # x, y축 비율을 1:1로 고정
    
    plt.show() # 그림 출력
    # ------------------
    
    return pi_s, M

# 설정된 점의 개수 (너무 많으면 그리는데 오래 걸리므로 10,000개 정도가 적당합니다)
N_visual = 10000 

# 실행 (그림도 함께 출력됩니다)
pi_s, M = estimate_pi_visualize(N_visual)
true_pi = np.pi
error = abs(true_pi - pi_s)

# 결과 출력
print(f"--- Q1 (a) 결과 ---")
print(f"전체 점의 수 (N): {N_visual}")
print(f"원 내부 점의 수 (M): {M}")
print(f"원주율 추정치 (pi_s): {pi_s:.5f}")
print(f"실제 pi 값: {true_pi:.5f}")
print(f"오차 (Error): {error:.5f}")
'''

# Q1 - (b) - 참값을 모른다고 가정했을 때 - \sqrt {R-1}로 나눔.

'''
import numpy as np

def run_pi_experiment(N, R):
    pi_results = []
    
    for i in range(R):
        # 1. [-1, 1] 사이의 난수 생성
        x = np.random.uniform(-1, 1, N)
        y = np.random.uniform(-1, 1, N)
        
        # 2. 원 내부 점(M) 판정
        inside_circle = (x**2 + y**2 <= 1)
        M = np.sum(inside_circle)
        
        # 3. 해당 회차의 pi_s 계산
        pi_s = 4 * (M / N)
        pi_results.append(pi_s)
        
    return np.array(pi_results)

# 파라미터 설정
N = 1000  # (a)에서 설정한 값
R = 10    # 반복 횟수

# 수치 실험 실행
pi_samples = run_pi_experiment(N, R)

# 4. 통계량 계산
mean_pi = np.mean(pi_samples)               # <pi_s>
var_pi = np.var(pi_samples, ddof=0)         # 불편 분산 (R-1로 나눔)
std_pi = np.sqrt(var_pi)                    # 표준편차 (sigma)
reporting_error = std_pi / np.sqrt(R - 1)   # 보고할 오차 범위 (교안 식 적용)

# 결과 출력
print(f"--- Q1 (b) 수치 실험 결과 (N={N}, R={R}) ---")
print(f"각 회차별 추정치: {pi_samples}")
print(f"평균 <pi>: {mean_pi:.6f}")
print(f"표준편차 (sigma): {std_pi:.6f}")
print(f"보고할 값: pi = {mean_pi:.6f} ± {reporting_error:.6f}")
'''


'''
# Q1 - (b) - 참값을 안다고 가정했을 때 - \sqrt {R}로 나눔.

import numpy as np

def run_pi_experiment(N, R):
    pi_results = []
    for _ in range(R):
        x = np.random.uniform(-1, 1, N)
        y = np.random.uniform(-1, 1, N)
        M = np.sum(x**2 + y**2 <= 1)
        pi_results.append(4 * (M / N))
    return np.array(pi_results)

# 설정
N, R = 1000, 10
true_pi = np.pi # 참값을 알고 있다고 가정 

# 1. 실험 수행
pi_samples = run_pi_experiment(N, R)

# 2. 참값 기준의 통계량 계산
mean_pi = np.mean(pi_samples)

# 참값(true_pi)과의 편차를 이용하여 분산을 계산 (이때는 R로 나눔) 
# np.mean((samples - true_pi)**2)와 같은 원리입니다.
var_true = np.mean((pi_samples - true_pi)**2) 
std_true = np.sqrt(var_true)

# 3. 오차 범위 보고 (분모를 sqrt(R)로 사용)
reporting_error_known = std_true / np.sqrt(R)

print(f"--- Q1 (b) 참값을 알 때의 분석 (N={N}, R={R}) ---")
print(f"각 회차별 추정치: {pi_samples}")
print(f"실제 pi 값: {true_pi:.6f}")
print(f"실험 평균 <pi>: {mean_pi:.6f}")
print(f"참값 기준 표준편차: {std_true:.6f}")
print(f"보고할 값 (R 사용): pi = {mean_pi:.6f} ± {reporting_error_known:.6f}")
'''

# Q1 - (b) - 참값을 모른다고 가정했을 때(\sqrt {R-1}로 나눔), 참값을 안다고 가정했을 때(\sqrt {R}로 나눔) 두 경우를 함께 보여줌.
'''
import numpy as np

def run_pi_experiment(N, R):
    pi_results = []
    for _ in range(R):
        x = np.random.uniform(-1, 1, N)
        y = np.random.uniform(-1, 1, N)
        M = np.sum(x**2 + y**2 <= 1)
        pi_results.append(4 * (M / N))
    return np.array(pi_results)

# 파라미터 설정
N = 1000
R = 10
true_pi = np.pi

# 1. 동일한 실험 샘플 생성 (비교의 일관성 유지)
pi_samples = run_pi_experiment(N, R)
mean_pi = np.mean(pi_samples)

# ---------------------------------------------------------
# Case 1: 참값을 모를 때 (교안 방식 - 불편 분산 사용)
# ---------------------------------------------------------
# 표본 평균과의 편차를 이용, 분모는 R-1 (ddof=1)
var_unknown = np.var(pi_samples, ddof=1) 
std_unknown = np.sqrt(var_unknown)
# 보고 오차 분모는 sqrt(R-1) 
error_unknown = std_unknown / np.sqrt(R - 1) 

# ---------------------------------------------------------
# Case 2: 참값을 알 때 (동료 논의 방식 - 모분산 추정)
# ---------------------------------------------------------
# 실제 참값(true_pi)과의 편차를 직접 이용, 분모는 R
var_known = np.mean((pi_samples - true_pi)**2)
std_known = np.sqrt(var_known)
# 보고 오차 분모는 sqrt(R)
error_known = std_known / np.sqrt(R)

# ---------------------------------------------------------
# 결과 출력 및 비교
# ---------------------------------------------------------
print(f"--- Q1-(b) 통계 계산 방식 비교 (N={N}, R={R}) ---")
print(f"동일 샘플 평균 <pi_s>: {mean_pi:.6f}")
print(f"실제 원주율 참값 pi: {true_pi:.6f}\n")

print(f"[방법 1] 참값을 모를 때 (교안 기준)")
print(f" - 사용 표준편차 (Unbiased): {std_unknown:.6f}")
print(f" - 보고할 값: {mean_pi:.6f} ± {error_unknown:.6f}")

print(f"\n[방법 2] 참값을 알 때 (동료 논의 기준)")
print(f" - 사용 표준편차 (Population): {std_known:.6f}")
print(f" - 보고할 값: {mean_pi:.6f} ± {error_known:.6f}")

print("-" * 50)
print(f"오차 범위 차이: {abs(error_unknown - error_known):.6f}")
'''

'''
import numpy as np
import matplotlib.pyplot as plt

def run_pi_experiment(N, R):
    """N회 샘플링 실험을 R회 반복하여 pi 추정치 배열을 반환"""
    pi_results = []
    for _ in range(R):
        # [-1, 1] 사이의 난수 생성 및 원 내부 점 판정
        x, y = np.random.uniform(-1, 1, N), np.random.uniform(-1, 1, N)
        M = np.sum(x**2 + y**2 <= 1)
        pi_results.append(4 * (M / N))
    return np.array(pi_results)

# 1. 파라미터 설정 (b: N=1000, R=10 / c: N=100, R=100)
N, R = 1000, 10
true_pi = np.pi
pi_samples = run_pi_experiment(N, R)
mean_pi = np.mean(pi_samples)

# Case 1: 참값을 모를 때 (교안 방식 - 불편 분산 사용)

# 표본 평균과의 편차 이용, 자유도 보정 ddof=1 (R-1로 나눔)
var_unknown = np.var(pi_samples, ddof=1) 
std_unknown = np.sqrt(var_unknown)
# 보고 오차 분모: sqrt(R-1)
error_unknown = std_unknown / np.sqrt(R - 1)

# Case 2: 참값을 알 때 (동료 논의 방식 - 모분산 직접 추정)

# 실제 참값(true_pi)과의 편차 직접 이용, 분모는 R (자유도 손실 없음)
var_known = np.mean((pi_samples - true_pi)**2)
std_known = np.sqrt(var_known)
# 보고 오차 분모: sqrt(R)
error_known = std_known / np.sqrt(R)

# 결과 출력

print(f"--- Q1-(b) 통계 계산 방식 비교 (N={N}, R={R}) ---")
print(f"동일 샘플 평균 <pi_s>: {mean_pi:.6f}")
print(f"실제 원주율 참값 pi: {true_pi:.6f}\n")

print(f"[방법 1] 참값을 모를 때 (교안 기준)")
print(f" - 사용 표준편차 (Unbiased): {std_unknown:.6f}")
print(f" - 보고할 값: {mean_pi:.6f} ± {error_unknown:.6f}")

print(f"\n[방법 2] 참값을 알 때 (동료 논의 기준)")
print(f" - 사용 표준편차 (Population): {std_known:.6f}")
print(f" - 보고할 값: {mean_pi:.6f} ± {error_known:.6f}")

print("-" * 55)
print(f"오차 범위 차이 (|Err1 - Err2|): {abs(error_unknown - error_known):.6f}")

# 시각화 비교 (Error Bar) - IndexError 방지 안전 코드

labels = ['Method 1\n(Unknown $\pi$, $R-1$)', 'Method 2\n(Known $\pi$, $R$)']
means = [mean_pi, mean_pi]
errors = [error_unknown, error_known]

plt.figure(figsize=(9, 6))

# 에러바 생성 (LineCollection 구조 분해)
_, caplines, barlinecols = plt.errorbar(labels, means, yerr=errors, fmt='o', color='black', 
                                       elinewidth=3, capsize=12, label='Estimated $\pi \pm$ Error')

# 오차 막대(세로선) 색상 개별 지정
barlinecols[0].set_color('red')   # Method 1
if len(barlinecols) > 1:
    barlinecols[1].set_color('blue') # Method 2

# 막대 끝 가로선(Caps) 색상 지정
for i, cap in enumerate(caplines):
    cap.set_color('red' if i < 2 else 'blue')

plt.axhline(true_pi, color='green', linestyle='--', linewidth=2, label=f'True $\pi$ ({true_pi:.5f})')
plt.title(f'Visual Comparison of Error Estimation (N={N}, R={R})', fontsize=14)
plt.ylabel('Value of $\pi$', fontsize=12)
plt.grid(axis='y', linestyle=':', alpha=0.7)
plt.legend()

# 수치 텍스트 표시
plt.text(0.1, mean_pi + error_unknown, f'  $\pm${error_unknown:.5f}', va='center', color='red', fontweight='bold')
plt.text(1.1, mean_pi + error_known, f'  $\pm${error_known:.5f}', va='center', color='blue', fontweight='bold')

plt.tight_layout()
plt.show()
'''

# Q1 - (c) - 참값을 모른다고 가정했을 때 - \sqrt {R-1}로 나눔. | N = 100, R = 100
'''
import numpy as np

def run_pi_experiment(N, R):
    pi_results = []
    
    for i in range(R):
        # 1. [-1, 1] 사이의 난수 생성
        x = np.random.uniform(-1, 1, N)
        y = np.random.uniform(-1, 1, N)
        
        # 2. 원 내부 점(M) 판정
        inside_circle = (x**2 + y**2 <= 1)
        M = np.sum(inside_circle)
        
        # 3. 해당 회차의 pi_s 계산
        pi_s = 4 * (M / N)
        pi_results.append(pi_s)
        
    return np.array(pi_results)

# 파라미터 설정 (c번 조건)
N = 100  # 점의 개수 축소
R = 100  # 반복 횟수 증가

# 수치 실험 실행
pi_samples = run_pi_experiment(N, R)

# 4. 통계량 계산
mean_pi = np.mean(pi_samples)               # 평균 <pi>
# 교안에 따라 표본의 표준편차는 N으로 나누어 구함 (ddof=0)
std_pi = np.std(pi_samples, ddof=0)         # 표준편차 (sigma)
# 보고할 값의 오차 범위 계산 (참값을 모른다고 가정)
reporting_error = std_pi / np.sqrt(R - 1)   

# 결과 출력
print(f"--- Q1 (c) 수치 실험 결과 (N={N}, R={R}) ---")
print(f"평균 <pi>: {mean_pi:.6f}")
print(f"표준편차 (sigma): {std_pi:.6f}")
print(f"보고할 값: pi = {mean_pi:.6f} ± {reporting_error:.6f}")
'''



# Q2 - 반지름 R = 2인 4차원 구의 부피를 몬테카를로 방법으로 구하라.

'''
import numpy as np

def calculate_4d_sphere_volume(R, N):
    # 1. 4차원 공간(-R ~ R)에 N개의 랜덤 포인트 생성
    # x1, x2, x3, x4 좌표를 가진 N개의 점을 한 번에 생성합니다.
    points = np.random.uniform(-R, R, (N, 4))
    
    # 2. 각 점의 원점으로부터의 거리 제곱 합 계산 (x1^2 + x2^2 + x3^2 + x4^2)
    radius_squared = np.sum(points**2, axis=1)
    
    # 3. 4차원 구 내부에 있는 점(M) 판정 및 개수 카운트
    inside_sphere = (radius_squared <= R**2)
    M = np.sum(inside_sphere)
    
    # 4. 4차원 상자의 부피 (한 변의 길이가 2R인 4차원 큐브)
    V_box = (2 * R) ** 4
    
    # 5. 몬테칼로 부피 추정치 계산 (상자 부피 * 구 내부 점의 비율)
    V_estimated = V_box * (M / N)
    
    return V_estimated, M

# 파라미터 설정
R = 2
N = 1000000  # 정확도를 높이기 위해 N을 100만 개로 넉넉히 설정

# 수치 실험 실행
V_est, M = calculate_4d_sphere_volume(R, N)

# 참값 계산 (4차원 구의 부피 공식: 1/2 * pi^2 * R^4)
V_true = 0.5 * (np.pi ** 2) * (R ** 4)
error = abs(V_est - V_true)

# 결과 출력
print(f"--- Q2. 4차원 구의 부피 몬테칼로 적분 (R={R}, N={N}) ---")
print(f"4차원 큐브 내 전체 점의 개수 (N): {N:,}개")
print(f"4차원 구 내부의 점의 개수 (M): {M:,}개")
print(f"추정된 4차원 구의 부피: {V_est:.6f}")
print(f"이론적인 4차원 구의 부피: {V_true:.6f}")
print(f"참값과의 오차: {error:.6f}")
'''



# Q5 : 구간 $I = (0,1)$을 $M = 50$개의 균등한 구간 $I_i \ (i \in \{1,2,\dots,M\})$으로 나눈 후, 구간 $I$에서 균일한 확률로 난수 $z$를 $N = 10^5$ 뽑자.

# (a) 구간 $I_i$에 속한 $z$의 갯수 $N_i$를 출력하라.

# (b) $N_i$ $vs$ $i$를 그래프 그리고 상수 함수 $y = C$와 비교하라. ($C$값은 얼마가 되어야 하는가?)

# (c) 구간 $I_i$에 속한 $z^2$의 갯수 $n_i$를 출력하라.

# (d) $n_i$ $vs$ $i$를 그래프 그리고 함수 $y = \frac{c}{2\sqrt{x}}$와 비교하라. ($C$값은 얼마나 되어야 하는가?)

'''
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# --- 0. 공통 파라미터 설정 ---
N = 10**5  # 난수 총 개수 (100,000개)
M = 50     # 구간 개수
C_theoretical = N / M  # 이론적 상수 C (100000 / 50 = 2000)

# --- 1. 난수 생성 및 데이터 처리 ---
# 균일 난수 z 생성 (a, b 용도)
z = np.random.uniform(0, 1, N)
N_i, bin_edges = np.histogram(z, bins=M, range=(0, 1))

# 비균일 난수 x = z^2 생성 (c, d 용도)
x = z**2
n_i, _ = np.histogram(x, bins=M, range=(0, 1))

# 구간의 중간값(center) 배열 생성 (수치 해석 및 그래프 용도)
x_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

# --- 2. 수치적 C값 찾기 (Curve Fitting - 개선된 버전) ---
def target_function(x, C_fit):
    return C_fit / (2 * np.sqrt(x))

# 핵심 포인트: x가 0에 가까워질 때의 극단적인 비선형성(Singularity) 오차를 피하기 위해
# 앞의 2개 구간(인덱스 0, 1)을 피팅 대상에서 제외하고 3번째 구간부터 사용!
optimal_params, _ = curve_fit(target_function, x_centers[2:], n_i[2:], p0=[C_theoretical])
C_empirical = optimal_params[0]
error_rate = abs(C_theoretical - C_empirical) / C_theoretical * 100

# --- 3. 콘솔 결과 출력 및 보고서 문구 자동 생성 ---
print("="*50)
print(f"--- Q5 (a) 구간별 z의 개수 N_i ---")
print(N_i)
print(f"\n--- Q5 (c) 구간별 z^2의 개수 n_i ---")
print(n_i)
print("="*50)

print(f"\n[이론 및 수치 해석 결과]")
print(f"이론적 기댓값 상수 C: {int(C_theoretical)}")
print(f"Curve Fitting 수치적 상수 C: {C_empirical:.4f}")
print(f"오차율: {error_rate:.4f}%\n")

# --- 4. 시각화 (b & d 비교) ---
i_indices = np.arange(1, M + 1) # x축: 구간 인덱스 i (1 ~ 50)
y_expected = C_theoretical / (2 * np.sqrt(x_centers)) # (d) 이론적 기댓값 곡선

plt.figure(figsize=(14, 6))

# [첫 번째 그래프: (b) N_i vs i]
plt.subplot(1, 2, 1)
plt.bar(i_indices, N_i, color='skyblue', edgecolor='black', alpha=0.7, label='Actual $N_i$')
plt.axhline(y=C_theoretical, color='red', linestyle='--', linewidth=2, label=f'Expected $y = {int(C_theoretical)}$')
plt.xlabel('Interval index ($i$)')
plt.ylabel('Count ($N_i$)')
plt.title('$N_i$ vs $i$ (Uniform $z$)')
plt.xlim(0, M + 1)
plt.ylim(0, max(N_i) * 1.5) 
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.6)

# [두 번째 그래프: (d) n_i vs i]
plt.subplot(1, 2, 2)
plt.bar(i_indices, n_i, color='lightgreen', edgecolor='black', alpha=0.7, label='Actual $n_i$')
plt.plot(i_indices, y_expected, color='red', linestyle='-', linewidth=2, marker='o', markersize=4, label=r'Expected $y = \frac{C}{2\sqrt{x}}$')
plt.xlabel('Interval index ($i$)')
plt.ylabel('Count ($n_i$)')
plt.title('$n_i$ vs $i$ (Non-uniform $x = z^2$)')
plt.xlim(0, M + 1)
plt.ylim(0, max(n_i) * 1.05)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()
'''