import tableauserverclient as TSC  # Tableau Server Client 라이브러리
import argparse  # 커맨드라인 인자 처리 : 명령줄에서 옵션을 받을 수 있도록 함
import logging  # 로그 기록 : 로그를 파일과 콘솔에 동시에 출력
from datetime import datetime  # 날짜 및 시간 활용 : 현재 날짜/시간을 사용해 로그 파일이나 CSV 파일의 이름을 생성
from config import config  # 설정 정보 로드 (서버 URL, 계정 정보 등) : 서버 정보(username, password 등)를 저장한 별도의 설정 파일 (config.py)


# TSC 모델 초기화
TSC.models.flow_item

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s', # ex) 2025-03-11 14:30:16,456 - ERROR - 사용자 목록 조회 실패: 인증 오류
    handlers=[ #handlers 리스트 : 로그 메세지를 출력할 대상(출력 경로)를 지정, 파일과 콘솔(터미널)에 동시에 로그를 남기는 설정
        #파일 저장 : role_check_20250311_144530.log(실행시간 기준으로 자동 생성)
        #실행할 때마다 다른 파일명이 자동 생성(로그 파일이 덮어씌어지지 않음)
        logging.FileHandler(f'role_check_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        #로그 메세지를 터미널(콘솔)에 출력
        #개발자가 로그를 실시간으로 확인 가능
        logging.StreamHandler()
    ]
)

#로깅 실행 예제
logging.info("서버 연결 성공")
logging.warning("네트워크 지연 발생")
logging.error("서버 연결 실패: 인증 오류")

#실행 결과(터미널 출력-콘솔, 로그 파일)
#2025-03-11 14:50:10,456 - INFO - 서버 연결 성공
#2025-03-11 14:50:12,789 - WARNING - 네트워크 지연 발생
#2025-03-11 14:50:15,123 - ERROR - 서버 연결 실패: 인증 오류

#파이썬 주석에 대해서
# : 일반주석
"""Docstring이라고 함수, 클래스, 모듈에 대한 설명을 작성하는 주석이다."""
'''이것도 마찬가지이고, Docstring은 함수 내부에 위치한다.'''

def connect_to_server():
    """태블로 서버에 연결"""
    env_config = config['my_env']
    tableau_auth = TSC.TableauAuth(
        username=env_config['username'],
        password=env_config['password'],
        site_id=''
    )
    #Tableau Server 객체 생성 -> 이 객체로 사용자 목록 조회, 역할 변경 등 API 요청 가능
    #use_server_version=True : Tableau Server의 버전을 자동 감지하여 사용
    server = TSC.Server(env_config['server'], use_server_version=True)
    try:
        server.auth.sign_in(tableau_auth)
        logging.info("서버 연결 성공")
        return server
    except Exception as e:
        logging.error(f"서버 연결 실패: {str(e)}")
        raise

def get_all_users(server):
    """모든 사용자 가져오기"""
    all_users = []
    req_option = TSC.RequestOptions(pagesize=1000)

    try:
        for user in TSC.Pager(server.users, req_option):
            all_users.append(user)
        return all_users
    except Exception as e:
        logging.error(f"사용자 목록 조회 실패: {str(e)}")
        raise

def should_update_user(user):
    """사용자가 업데이트 조건을 만족하는지 확인"""
    # 1. 현재 역할이 'ExplorerCanPublish'인지 확인
    if user.site_role != 'ExplorerCanPublish':
        return False
    if not user.name.lower().endwith('@test.com'):
        return False
    if '@tester.com' in (user.fullname or '').lower():
        return False
    return True

def preview_test_users(server):
    """테스트 모드에서 변경될 처음 10명의 사용자 목록 미리보기"""
    all_users = get_all_users(server)
    total_users = len(all_users)
    logging.info(f"총 {total_users}명의 사용자를 찾았습니다.")

    #조건에 맞는 사용자 필터링
    users_to_update = [user for user in all_users if should_update_user(user)]