import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

if os.getenv('ENV') == 'local':
    # 로컬 환경 변수 직접 설정
    EMAIL = 'backend1024@naver.com'  # 로컬 이메일
    PASSWORD = 'djawldyd12!'  # 로컬 비밀번호
else:
    EMAIL = os.getenv('EMAIL')  # 프로덕션 환경에서 환경 변수 가져오기
    PASSWORD = os.getenv('PASSWORD')
print(EMAIL +" | " + PASSWORD)

# 헤드리스 옵션 설정
chrome_options = Options()
# chrome_options.add_argument("--headless")  # 헤드리스 모드
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")  # 창 크기 설정

# Chrome 드라이버 초기화
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://app.cloudtype.io/@teran1024/db:main")

try:
    #
    try:
        print("로그인 필드 확인 대기")
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="page"]/div/div[1]/div/div[2]/div/div[2]/form/div[1]/input'))
        )
        print("키입력 시작")
        email_field.send_keys(EMAIL)  # 환경 변수에서 이메일 가져오기
        print("키입력 완료")
    except Exception as e:
        print(f"아이디 입력 필드를 찾지 못했습니다: {e}")

    try:
        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="page"]/div/div[1]/div/div[2]/div/div[2]/form/div[2]/input'))
        )
        password_field.clear()  # 기존 내용 지우기 (필요한 경우)
        password_field.send_keys(PASSWORD)  # 환경 변수에서 비밀번호 가져오기
        print("비밀번호 입력 완료")

        # 엔터 키 입력
        password_field.send_keys(Keys.RETURN)
        print("로그인 시도")

    except Exception as e:
        print(f"패스워드 입력 필드를 찾지 못했습니다: {e}")

    # 첫 번째 요소가 생길 때까지 최대 10초 대기
    try:
        first_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="page"]/div/div[4]/div/div[1]/div/div/div/div[1]/div/div[2]/div[1]/a[1]'))
        )
        time.sleep(10)
        # 첫 번째 요소 클릭
        driver.execute_script("arguments[0].focus();", first_element)
        first_element.click()
        print("첫 번째 요소 클릭 완료")

    except Exception as e:
        print(f"첫 번째 요소를 클릭하는데 오류가 발생했습니다: {e}")

    # 두 번째 요소가 생길 때까지 최대 10초 대기
    try:
        driver.get("https://app.cloudtype.io/@teran1024/db:main")  # 원하는 URL로 변경
        print("이동 완료")
        second_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="page"]/div/div[4]/div/div[1]/div/div/div/div[2]/div/div[2]/div[1]/a[1]'))
        )
        time.sleep(10)
        driver.execute_script("arguments[0].focus();", second_element)
        second_element.click()

        print("두 번째 요소 클릭 완료")
    except Exception as e:
        print(f"두 번째 요소를 클릭하는데 오류가 발생했습니다: {e}")

except Exception as e:
    print(f"오류 발생: {e}")

print(driver.title)
driver.quit()