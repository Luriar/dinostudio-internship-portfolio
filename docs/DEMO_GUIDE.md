# 기능별 독립 데모 실행 가이드

이 문서는 디노스튜디오 경력 사례를 설명하기 위해 2026년에 새로 작성한 데모 안내입니다. 2024년 실제 회사 코드를 공개한 것이 아닙니다. 각 GitHub 저장소는 독립적으로 설치하고 실행할 수 있습니다.

## 각 저장소

| 저장소 | 실행 명령 | 데모 기능 |
|---|---|---|
| dm-workflow-optimization-demo | python workflow.py | SQLite Outbox, 동의 확인, 중복 방지, 실패 재시도, 감사 이력 |
| seller-discovery-asf-demo | python run_pipeline.py --db synthetic_demo.sqlite --export result.csv | 가상 판매자 후보 분류, SQLite 저장, CSV, 재실행 시 중복 방지 |
| seller-history-collector-demo | python run_history.py --db synthetic_history.sqlite --export history.csv | 활동 스냅샷, 링크 정규화, 반복 적재, 시점별 비교 |
| mysql-campaign-operations-demo | python operations.py | 트랜잭션, 응답 완료 대상 관리, 데이터 백업 |
| threads-workflow-automation-demo | python review_queue.py | 위험 내용 확인, 사람 검토, 승인/거절, 감사 이력 |
| vling-youtube-pipeline-demo | python seed.py 후 python app.py | 가상 채널 및 영상 적재, SQLite, Flask 조회 화면, 수동 메모 관리 |

모든 저장소의 새 데모는 Python 3.11 이상으로 실행할 수 있습니다. Vling 데모의 로컬 웹 화면에는 Flask가 필요하며 해당 저장소에 requirements.txt가 있습니다.

## 테스트

각 기능별 저장소에서 다음 명령으로 로컬 테스트를 실행합니다.

    python -m unittest discover -s tests -v

Github Actions가 코드를 push할 때마다 동일한 단위 테스트를 실행하도록 구성했습니다. Actions 실행 결과는 해당 GitHub 저장소의 Actions 탭에서 확인할 수 있습니다. 실서비스 API, 플랫폼 계정 또는 회사 접근 권한이 필요하지 않습니다.

## 실무 경력과 데모를 구분

- 2024.07.01~09.30: 실무 인턴 기간.
- 2024년 10월 약 2주: Vling 데이터를 수집 및 저장하는 별도 프로젝트.
- Instagram DM은 기존에 있던 프로그램을 분석하고 최적화했으며, 신규 발송 프로그램 전체를 최초부터 개발한 것은 아닙니다.
- 기타 기능은 사용자 본인이 직접 작성하고 개선했다고 확인했습니다.
- 학교 실습일지 15개는 3개월간 한 일을 학교 제출 형식으로 나누어 쓴 기록입니다.
- 2026년 데모에 사용한 가상의 정량 값, 실행 시간, 코드 구현 범위를 2024년 업무 성과로 바꾸지 않습니다.

## 공개 범위

회사 원본 소스코드와 테이블, 영업 자료, 개인정보, 실제 계정 식별자, 크롤링 결과, 접속 인증정보, 실습 증빙 원본은 어떤 저장소에도 포함하지 않았습니다.
