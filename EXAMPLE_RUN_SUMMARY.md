# Atomic Tab 브라우저 수집 점검 (2026-02-16)

## 목적
Chrome Relay `tab not found` 재발 상황에서, **1 URL = 1 탭(open → snapshot → close)** 방식으로 Scholar/KAIST 페이지 수집 가능성 확인.

## 실행 범위
- Google Scholar: `start=0,10,20` (p1~p3)
- KAIST Primo: `offset=0,10,20` (p1~p3)

## 결과
- 총 캡처(제목 기준, 정제/중복제거 후): **30건**
- v3 마스터(`data/c1_assimilation_master_with_independent_additions_v3.csv`) 대비
  - 휴리스틱상 기존 포함 추정: 15건
  - 휴리스틱상 신규 추정: 15건
- 실행 에러: **0건** (재시도 포함 최종 성공)

## 산출물
- 전체 캡처: `reports/atomic_tab_capture_2026-02-16.csv`
- 신규 추정: `reports/atomic_tab_capture_2026-02-16_new_estimated.csv`

## 메모
- `in_master_estimate`는 제목-문자열 기반 휴리스틱 매칭 결과로, DOI 정규화 전 단계임.
- 다음 단계에서 Crossref/기타 소스로 DOI 정규화 후 최종 신규 여부 확정 필요.
