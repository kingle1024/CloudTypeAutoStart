import requests
import json
import os

def get_token():
    # POST 요청을 보낼 URL
    url = "https://api.cloudtype.io/auth"

    if os.getenv('ENV') == 'local':
        # 로컬 환경 변수 직접 설정
        EMAIL = 'email@naver.com'  # 로컬 이메일
        PASSWORD = 'password'  # 로컬 비밀번호
    else:
        EMAIL = os.getenv('EMAIL')  # 프로덕션 환경에서 환경 변수 가져오기
        PASSWORD = os.getenv('PASSWORD')

    print(EMAIL + " | " + PASSWORD)

    # 요청할 데이터
    data = {
        "values": {
            "loginname": EMAIL,
            "password": PASSWORD,
            "deviceid": "dev-m6n0q2sicfdfa90a"
        }
    }

    # JSON으로 요청 보내기
    response = requests.post(url, json=data)

    # 응답 JSON 파싱
    if response.status_code == 200:
        try:
            response_data = response.json()
            token = response_data.get("token")  # token 값 추출
            if token:
                print(f"Token: {token}")
                return token  # token 반환
            else:
                print("Token not found in the response.")
        except json.JSONDecodeError:
            print("Failed to parse JSON response.")
    else:
        print(f"Request failed: {response.status_code}, content: {response.text}")

    return None  # token이 없는 경우 None 반환

def check_status(url, token):
    # GET 요청을 보낼 URL

    # 요청 헤더에 Authorization 추가
    headers = {
        "Authorization": token
    }

    # GET 요청 보내기
    response = requests.get(url, headers=headers)

    # 응답 처리
    if response.status_code == 200:
        try:
            response_data = response.json()
            # 'active' 값 확인
            for stat in response_data.get("stats", []):
                name = stat.get("name")
                active = stat.get("active")
                print(f"Check stats... {name} | Active: {active}")  # 상태 출력

                if name == "mariadb" and active == 0:
                    print("Active for mariadb is 0, proceeding to start deployment.")
                    start_deployment(token, "teran1024/db", "mariadb")
                elif name == "travel-service" and active == 0:
                    print("Active for travel-service is 0, proceeding to start deployment.")
                    start_deployment(token, "teran1024/db", "travel-service")
                elif name == "nklcbdty-service" and active == 0:
                    print("Active for nklcbdty-service is 0, proceeding to start deployment.")
                    start_deployment(token, "backend1024/server", "nklcbdty-service")
            return True
        except json.JSONDecodeError:
            print("Failed to parse JSON response.")
    else:
        print(f"Failed to check status: {response.status_code}, content: {response.text}")

    return False  # 상태 확인이 실패한 경우

def start_deployment(token, user, service_name):
    # PUT 요청을 보낼 URL
    url = f"https://api.cloudtype.io/project/{user}/stage/main/deployment/{service_name}/start"

    # 요청 헤더에 Authorization 추가
    headers = {
        "Authorization": token
    }

    # PUT 요청 보내기
    response = requests.put(url, headers=headers)

    # 응답 처리
    if response.status_code == 200:
        print(f"{service_name.capitalize()} deployment started successfully.")
    else:
        print(f"Failed to start {service_name} deployment: {response.status_code}, content: {response.text}")

if __name__ == "__main__":
    token = get_token()  # token 가져오기
    if token:
        check_status("https://api.cloudtype.io/project/teran1024/db/stage/main/stat", token)  # status 확인
        check_status("https://api.cloudtype.io/project/backend1024/server/stage/main/stat", token)  # status 확인
