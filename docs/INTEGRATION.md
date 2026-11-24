# 공개 데모 통합 검증

이 문서는 2026년 공개용으로 별도 구현한 데모의 실제 실행을 기록합니다. 2024년 회사 시스템의 연동 또는 성능 실적을 증명하지 않습니다. 모든 입력과 결과는 가상 데이터입니다.

## 2026-11-24 실행 결과

| 검사 | 결과 |
|---|---|
| ASF 후보 분류 및 CSV 출력 | 가상 후보 1개 |
| ASF 출력에서 HC 입력 선정 | 일치한 관찰 기록 2개 |
| HC 반복 적재 | 고유 이력 2개 유지 |
| Vling 가상 채널 및 영상 조회 | 채널 2개, 영상 3개 |
| Vling 재적재 후 수동 메모 | 보존 확인 |
| Flask 페이지 및 API | 3개 응답 확인 |
| DM, DB Operations, Threads | 각 CLI의 JSON 출력 확인 |

통합 실행은 ASF의 후보 CSV에서 코드를 읽어 HC의 가상 관찰 데이터 중 해당 후보를 선택합니다. Vling은 별도의 임시 SQLite 파일에서 데이터를 재적재하고 Flask 테스트 클라이언트를 통해 수동 메모가 보존되는지 확인합니다. DM, DB Operations, Threads는 독립 CLI의 실행 여부를 검사하며, 실제 소셜 플랫폼과 연동하지 않습니다.

## 검증한 기능별 코드 버전

| 공개 데모 커밋 | 해당 버전의 단위 테스트 통과 수 |
|---|---:|
| [dm-workflow-optimization-demo](https://github.com/Luriar/dm-workflow-optimization-demo/tree/84471c3d751040a60fbf987a2fb32345656ec9e1) | 8 |
| [seller-discovery-asf-demo](https://github.com/Luriar/seller-discovery-asf-demo/tree/dc280492cc71ef1cc0a33c1744fdfeb7b243fc52) | 5 |
| [seller-history-collector-demo](https://github.com/Luriar/seller-history-collector-demo/tree/1613db8f1baa409fde327e856914b6e7a4ba8fbc) | 8 |
| [mysql-campaign-operations-demo](https://github.com/Luriar/mysql-campaign-operations-demo/tree/74544ff200b859f8e0e0be5050de3bdb89242820) | 6 |
| [threads-workflow-automation-demo](https://github.com/Luriar/threads-workflow-automation-demo/tree/5a7e5c6d471c18ce2b4fc09c1874e072146fc443) | 7 |
| [vling-youtube-pipeline-demo](https://github.com/Luriar/vling-youtube-pipeline-demo/tree/596deb24c918dbe11c32035af7364be91d71abda) | 9 |

위 여섯 코드 버전에서 43개 단위 테스트가 통과했습니다. 통합 저장소의 문서 검사 2개는 별도입니다. 이 수치는 2026년 데모의 검증 건수입니다.

## 같은 조건에서 재현

Python 3.11 이상과 Git이 필요합니다. 아래 명령은 빈 작업 디렉터리에서 실행하며 여섯 기능 저장소와 메인 저장소를 같은 상위 디렉터리에 둡니다.

~~~bash
git clone https://github.com/Luriar/dinostudio-internship-portfolio.git
git clone https://github.com/Luriar/dm-workflow-optimization-demo.git
git -C dm-workflow-optimization-demo checkout --detach 84471c3d751040a60fbf987a2fb32345656ec9e1
git clone https://github.com/Luriar/seller-discovery-asf-demo.git
git -C seller-discovery-asf-demo checkout --detach dc280492cc71ef1cc0a33c1744fdfeb7b243fc52
git clone https://github.com/Luriar/seller-history-collector-demo.git
git -C seller-history-collector-demo checkout --detach 1613db8f1baa409fde327e856914b6e7a4ba8fbc
git clone https://github.com/Luriar/mysql-campaign-operations-demo.git
git -C mysql-campaign-operations-demo checkout --detach 74544ff200b859f8e0e0be5050de3bdb89242820
git clone https://github.com/Luriar/threads-workflow-automation-demo.git
git -C threads-workflow-automation-demo checkout --detach 5a7e5c6d471c18ce2b4fc09c1874e072146fc443
git clone https://github.com/Luriar/vling-youtube-pipeline-demo.git
git -C vling-youtube-pipeline-demo checkout --detach 596deb24c918dbe11c32035af7364be91d71abda
python -m pip install -r vling-youtube-pipeline-demo/requirements.txt
python dinostudio-internship-portfolio/run_integration.py --repos-root .
~~~

스크립트는 임시 디렉터리를 사용하고 실제 계정, API 키, 회사 자료를 요청하지 않습니다. 실행 과정에서 만들어지는 가상 CSV, SQLite 파일과 임시 입력은 Git에 추가하지 않습니다.

## 자동 검증

메인 저장소의 Integration workflow는 위 기능별 코드 버전을 가져와 동일한 통합 스크립트를 실행합니다. 실제 CI 결과는 [Actions](https://github.com/Luriar/dinostudio-internship-portfolio/actions)에서 확인할 수 있습니다.
