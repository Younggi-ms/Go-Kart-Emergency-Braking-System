Go-Kart-Emergency-Braking-System
===================================
## 프로젝트 개요

본 프로젝트는 교내 이동 수단의 안전성 문제를 해결하기 위해
초음파 센서를 이용한 장애물 인식 기반 고카트 긴급 제동 시스템을 개발하는 것을 목표로 하였습니다.

기존 자전거·킥보드는 충돌 위험이 높고, 수동 제동에 의존한다는 한계가 있었습니다.
이에 따라 주행 중 장애물 감지 시 자동으로 모터 출력을 차단하는 전자식 제동 시스템을 구현하였습니다.

## 🎯 개발 목표 (Objectives)

- 실사이즈 고카트 제작
- BLDC 모터 기반 구동계 전자화
- 초음파 센서를 이용한 1m 이내 장애물 인식
- 장애물 감지 시 즉각적인 모터 출력 0 제어
- 실제 주행 환경에서 제동 성능 검증

## 🛠️ 시스템 구성 (System Architecture)

### 하드웨어 구성
- Raspberry Pi 5 : 전체 제어 로직 처리
- 초음파 센서 : 전방 장애물 거리 측정
- BLDC 모터 + 모터 컨트롤러
- Throttle 입력 신호
- Hall Sensor (A, B, C) : 속도 및 회전 정보 피드백
- 실사이즈 고카트 프레임
### 소프트웨어 구성
- 장애물 감지 로직
- 주행 / 제동 상태 제어 FSM
- 모터 출력 제어 로직

### 회로도[약식]
![Image](https://github.com/user-attachments/assets/55ba1e9d-fd21-4d3d-9003-0aa8bb648c16)

## ⚙️ 동작 로직 (Control Logic)
<img width="285" height="224" alt="Image" src="https://github.com/user-attachments/assets/1ff7a3e2-3207-42a5-8f00-d888a044223e" />

핵심 포인트
- 제동 판단은 거리 기준 단일 조건
- 계산 지연 최소화를 위해 즉시 출력 차단 방식 채택
- 기계식 제동이 아닌 전자식 제동(Electric Braking)

##  회로 설계 개요
- 초음파 센서 → Raspberry Pi GPIO 연결
- BLDC 모터 컨트롤러
> - Throttle 신호 입력
> - Hall Sensor 신호 입력 (속도·회전 감지)
- 제동 시 Throttle 출력 강제 0

  회로 설계는 실제 고카트 환경을 고려하여 노이즈 및 지연 최소화에 중점

## 시연 영상
https://github.com/user-attachments/assets/570ec185-7b02-4f83-9312-627d023cba4e
  
## 실험 및 결과 (Results)

제동 거리 실험 결과
- 속도 증가에 따라 제동 거리 비례 증가
- 최소 안전 제동 거리: 약 2.5m

성능 분석
- 오차 발생 원인
- 노면 마찰 계수 변화
- 장애물 인식 → 제어까지의 시간 지연
- 전자식 제동의 반응 속도는 양호

### 한계점
- LiDAR 기반 장거리 인식 구현 실패
- 초음파 센서 특성상
> - 각도 민감
> - 반사체 재질 영향 존재
- Raspberry Pi 5의 전력·부피 문제

### 🚀 추후 발전 방향

- LiDAR 센서 적극 도입
- 제어 보드 경량화 (Raspberry Pi → MCU 계열)
- 다중 센서 융합 (Ultrasonic + LiDAR)
- 제동 거리 예측 기반 선제 제동 알고리즘
