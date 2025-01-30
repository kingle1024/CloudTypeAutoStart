# Dockerfile
# 1. Python 이미지를 베이스로 사용
FROM python:3.9-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 요구 사항 파일 복사 (필요한 경우)
COPY requirements.txt .

# 4. 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 5. 애플리케이션 코드 복사
COPY app.py .

# 6. 컨테이너가 시작할 때 실행할 명령
CMD ["python", "app.py"]
