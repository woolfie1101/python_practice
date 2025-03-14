from fileinput import filename

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
    #리스트 컴프리헨션 코드 사용
    users_to_update = [user for user in all_users if should_update_user(user)]
    total_matching = len(users_to_update)
    logging.info(f"조건에 맞는 사용자 수: {total_matching}명")

    #처음 10명만 선택
    preview_users = users_to_update[:10]

    logging.info("\n=== 테스트 모드에서 변경될 처음 10명의 사용자 목록 ===")
    #enumerate(리스트, 시작번호)
    #1. enumerate(preview_users, 1): 0번째 인덱스부터 가져오지만, i의 값만 1부터 시작
    #2. enumerate(preview_users[1:], 1): 1번째 요소부터 시작
    #3. enumerate(islice(preview_users, 1, None), 1): 리스트가 매우 클 경우 2번(슬라이싱)보다 itertools.islice 이 메모리 효율이 좋다.
    for i, user in enumerate(preview_users, 1):
        logging.info(f"{i}. 사용자명: {user.name}")
        logging.info(f"   표시이름: {user.fullname}")
        logging.info(f"   현재역할: {user.site_role}")
        logging.info(f"   마지막로그인: {user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else '없음'}")
        logging.info("---")

    #csv 파일로 저장
    filename = f'test_users_preview_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    """
    - with 문을 쓰면 파일을 열고 사용한 후 자동으로 닫아줌. f.close()를 명시적으로 호출할 필요가 없다.
        예시)
            f = open(filename, 'w', encoding='utf-8')
            f.write("데이터")  
            f.close()  # 직접 닫아줘야 함!
    
    - 'w' 쓰기모드 (생성 or 덮어씀)
    """
    with open(filename, 'w', encoding="utf-8") as f:
        f.write("번호, 사용자명, 표시이름, 현재역할, 마지막로그인\n")
        for i, user in enumerate(preview_users, 1):
            last_login = user.last_login.strftime("%Y-%m-%d %H:%M:%S") if user.last_login else "없음"
            f.write(f"{i},{user.name},{user.fullname},{user.site_role},{last_login}\n")
    logging.info(f"\n테스트 대상 사용자 목록이 {filename} 파일로도 저장되었습니다.")
    logging.info("\n실제 역할 변경을 진행하려면 다음 명령어를 실행하세요:")
    logging.info("python update_user_roles.py --update --role Explorer --test")

def check_users_to_update(server):
    """조건에 맞는 사용자 목록 추출 및 저장"""
    all_users = get_all_users(server)
    total_users = len(all_users)
    logging.info(f"총 {total_users}명의 사용자를 찾았습니다.")

    # 조건에 맞는 사용자 필터링
    users_to_update = [user for user in all_users if should_update_user(user)]
    matching_users_count = len(users_to_update)
    logging.info(f"조건에 맞는 사용자 수: {matching_users_count}명")

    # CSV 파일로 저장
    filename = filename = f'users_to_check_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    with open(filename, 'w', encoding='UTF-8') as f:
        f.write("사용자명,표시이름,현재역할,마지막로그인\n")
        for user in users_to_update:
            last_login = user.last_login.strftime("%Y-%m-%d %H:%M:%S") if user.last_login else "없음"
            f.write(f"{user.name},{user.fullname},{user.site_role},{last_login}\n")
    logging.info(f"사용자 목록이 {filename} 파일로 저장되었습니다.")
    logging.info("\n테스트 모드로 처음 10명의 목록을 확인하려면 --preview 옵션을 사용하세요:")
    logging.info("python update_user_roles.py --preview")

def update_user_roles(server, new_role, test_mode=False):
    """조건에 맞는 사용자의 역할 업데이트"""
    all_users = get_all_users(server)
    total_users = len(all_users)
    logging.info(f"총 {total_users}명의 사용자를 찾았습니다.")

    # 조건에 맞는 사용자 필터링
    users_to_update = [user for user in all_users if should_update_user(user)]
    total_matching = len(users_to_update)

    if test_mode:
        users_to_update = users_to_update[:10]
        logging.info(f"테스트 모드: 조건에 맞는 전체 {total_matching}명 중 처음 10명만 변경합니다.")
    logging.info(f"변경 대상 사용자 수: {len(users_to_update)}명")

    # 변경 전 확인을 위한 사용자 목록 저장
    filename = f'users_to_update_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("사용자명,표시이름,현재역할,마지막로그인\n")
        for user in users_to_update:
            last_login = user.last_login.strftime("%Y-%m-%d %H:%M:%S") if user.last_login else "없음"
            f.write(f"{user.name},{user.fullname},{user.site_role},{last_login}\n")
    logging.info(f"변경 대상 사용자 목록이 {filename} 파일로 저장되었습니다.")

    # 역할 업데이트
    success_count = 0
    error_count = 0

    for user in users_to_update:
        try:
            original_role = user.site_role
            user.site_role = new_role
            server.users.update(user)
            success_count += 1
            logging.info(f"사용자 업데이트 성공: {user.name} ({original_role} -> {new_role})")
            logging.info(f"표시 이름: {user.fullname}")
        except Exception as e:
            error_count += 1
            logging.error(f"사용자 {user.name} 업데이트 실패: {str(e)}")

    logging.info(f"업데이트 완료: 성공 {success_count}건, 실패 {error_count}건")

"""
argparse.ArgumentParser : python에서 명령줄 인자를 쉽게 처리할 수 있도록 도와주는 모듈
"""
def main():
    # 1. ArgumentParser 객체 생성
    parser = argparse.ArgumentParser(description='태블로 서버 사용자 역할 일괄 변경')
    # 2. 명령줄 옵션 추가
    #python update_user_roles.py --update --role Explorer --test (처음 10명의 사용자만 역할 변경 (테스트 목적))
    #python update_user_roles.py --update --role Explorer (모든 대상 사용자의 역할 변경)
    parser.add_argument('--update', action='store_true', help='실제 역할 변경 수행 여부')
    parser.add_argument('--role', help='새로운 역할 (예: Explorer, Viewer, Creator)')
    parser.add_argument('--test', action='store_true', help='테스트 모드: 처음 10명만 변경')
    #python update_user_roles.py --preview
    parser.add_argument('--preview', action='store_true', help='테스트 모드에서 변경될 10명의 목록 미리보기')
    # 3. 입력된 명령줄 인자 분석
    args = parser.parse_args()

    if args.update and not args.role:
        parser.error("역할 변경 시에는 --role 옵션이 필요합니다.")

    try:
        server = connect_to_server()
        if args.preview:
            preview_test_users(server)
        elif args.update:
            update_user_roles(server, args.role, args.test)
        else:
            #python update_user_roles.py
            check_users_to_update(server)
    finally:
        if server is not None:
            server.auth.sign_out()

if __name__ == '__main__':
    main()