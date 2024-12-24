# 1. Node.js 이미지
FROM node:18-alpine

# 2. 작업 디렉토리 설정
WORKDIR /usr/src/app

# 3. package.json 복사 및 의존성 설치
COPY package*.json ./
RUN npm install

# 4. 소스 코드 복사
COPY . .

# 5. NestJS 빌드
RUN npm run build

# 6. 포트 노출
EXPOSE 3000

# 7. NestJS 실행 명령어
CMD ["npm", "run", "start:prod"]
