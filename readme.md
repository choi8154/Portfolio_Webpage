# 파일 구조
```
project/
├── run.py
├── projects.json
└── app/
    ├── schemas/
    ├── routers/
    │   └── home.py
    ├── templates/
    │   └── home.html
    └── static/
        ├── css.html
        ├── js.html
        └── images.html
```

# 포트폴리오 웹 사이트 라우트 명세서
```
```

# 알게된 팁 들
## 0. 현재 프로젝트를 하면서 불편했던 사항들.
1. poetry를 vscode로 사용함으로서 pycham에서 설정했던 poetry .venv 가상환경 폴더 경로가 달라 외부 폴더로 생성됨. 그때문에 if __name__ ... 으로 uvicorn.run(...)을 못 씀.
2. 배포 하는 중에 rootpage를 설정하지 않아서 notfound가 뜸.
3. root에서 /home을 RedirectResponse해서 구현
    - include_in_schema = False 를 줘서 docs로 해당 라우트를 api 문서화를 함.
    - run.py 에서 static 경로를 인식을 못해 notfounderror 발생함
    - Path(__file__), DIR / "app"/"static" 으로 해결함.
4. .env랑 config.py가 루트 폴더에 있었는데 그걸 app/routers/...에서 부르려고 ...config를 하니 "top-level package(=app)" 오류 터짐
    - .env, config.py 파일을 app에 넣어서 관리, .gitignore 수정
5. form을 html에서 받으려면 poetry add python-multipart 이게 필요함.
6. poetry export -f requirements.txt -o requirements.txt --without-hashes : 라이브러리 설치하고 수정 했으면 배포에서 오류날 수 있으니 꼭 할 것
7. 환경변수 를 render에 안넣어서 오류남.
8. render가 587, 465, 25 포트로 나가는 연결을 차단해서 await는 올리 없는 응답을 기다리다가 런타임 에러를 배출함.
    - Gmail에서도 클라우드 ip 접근을 차단함;; 로컬로 서버를 열면 괜찮은 이유임...
    - SendGrid를 사용해서 하면 되는데...

## 1. jinja2template vs htmlresponse
- htmlresponse : 정적인 응답을 보낼 때 사용함.
- jinja2template : 조건문 반복문 등을 사용해 동적인 웹 페이지를 구현할 때 사용
- htmlresponse는 api 테스트 때나 사용하고 현업에서는 jinja2를 동적이든 아니든 사용함.

## 2. 그렇다면 jinja2template의 사용법은?
- responsemodel = htmlresponse를 사용해도 됨.
- 세팅
    0. fastapi 내장 라이부러리가 아니기에 poetry add jinja2로 설치 해야함.
    1. from fastapi.templiting import jinja2Template
    2. template = jinja2Template
    3. 라우트의 엔드포인트 : return template.TemplateResponse("home.html", {"request":request}) 
        -해당 라우트로 들어온 요청의 정보를 동적으로 같이 받아 html에서 처리 해야하기 때문에 받은 요청을 보내줘야함.

## 3. 실행 환경과 templates와 같은 파일의 루트 폴더 위치가 다를때 발생하는 오류로 인한 Internal Server Error 해결 과정.
- os로 절대경로를 지정함.
- BASE_DIR = os.path.dirname(os.path.abspath(__file__)) : 현재 실행 파일의 절대경로를 추출하고 거기서 파일의 디렉터리 이름을 추출함.
- template = Jinja2Template(directory = os.path.join(BASE_DIR, "../templates")) : BASE_DIR에 ../templates라는 경로를 합침. 

## 4. staticfiles : static파일은 html에서 바로 사용하는거면 상관 없지면 images파일처럼 라우트가 직접 읽어야 할 때 사용.
- import fastapi.staticfiles import StaticFiles
- app.mount("/static", StaticFiles(directory="app/static"), name="static")
- "/static" : 브라우저에서 접근할 때 쓰는 경로
- StaticFiles(directory="app/static") : 실제 파일이 들어있는 경로
- name="static" : 별칭, 이름표, url_for등에서 사용.

## 5. requirements.txt 만들기
- poetry 1.9 이상 부터는 requirements.txt를 만드려면 별도의 플러그인이 필요함.
- Render / Vercel / AWS / Docker 등은 여전히 requirements.txt를 요구함;;
- 설정 방법
    1. poetry self add poetry-plugin-export
    2. poetry export -f requirements.txt --output requirements.txt --without-hashes

## 6. 배포 방법
- render을 사용해서 배포할 예정
0. run.py에 uvicorn.run("run:app", host-"0.0.0.0" port = 10000) 으로 설정
1. .gitignore 생성하여 env나 poetry, pip, IDE 등의 파일을 등록
2. requirements.txt 생성
3. git init -> add -> commit -> remote -> push 하기
4. http://render.com 로그인/회원가입.
5. +New -> Web Service -> 레포지토리 
6. 여러 설정들 
    - Name : (원하는 이름)
    - Region : Singapore (Asia, 빠름)
    - Start Command : uvicorn run:app --host 0.0.0.0 --port 10000

## 7. static파일을 처리하는 방식에 대한 정리
- 이 프로젝트는 정적 파일을 직접 서버에서 처리해야 하므로 run.py에 static의 절대경로를 지정해 줬음.
- 사실 Nginx 같은 프록시 서버는 사실 프론트에서 관리하는게 맞지만 지금은 솔로 프로젝트이므로 알아두는게 좋을 것 같음.
- static 파일을 서버에서 처리하는 방법은 2가지가 있음.
    1. 프록시 서버를 통해서 바로 클라이언트에게 제공되기
    2. 서버에서 다른 동적파일들과 함께 필요없는 가공단계를 거쳐 처리하기(트레픽이 많아지면 서버에 부하를 줌)
- 정적 파일들은 얼마나 빨리, 효율적으로 클라이언트에게 제공되냐가 서버의 수준을 결정함.
- 그래서 사용하는 오픈소스 웹 서버 소프트웨어인 Nginx(비동기), Apache(동기)를 사용함.
- 프록시 서버는 2가지 구동 방법이 있는데 단일서버와 분리서버임.
    1. 단일서버 : 하나의 서버 내에서 Nginx와 Fastapi를 각각 실행.(Render)
    2. 분리서버 : 서로 다른 서버에서 실행.(AWS(?정확하지 않음))
- Render에서는 기본적으로 nginx 서비스가 내장되어있음. 그래서 따로 nginx 설치는 필요 없음. 무료서비스는 nginx가 구동은 되지만 static같은 정적 파일을 처리하도록 하려면 유료플렌 가입 해야함...

## 8. 이메일 라우터 생성 및 환경변수 사용방법
- `from fastapi_mail import ConnectionConfig` : 라이브러리 사용.
- `from dotenv import load_dotenv` : 환경변수를 로드함
- `import os` : 환경변수에 접근하기위해 사용. `os.getenv("KEY")`로 .env에서 읽은 값을 꺼낼 수 있음.
- 

## 9. render와 vercel 차이
- render : python등 런타임 서버가 실제로 실행됨. 동적인 서버.
- vercel : 요청 들어올 때 정적 파일만 전달. 정적 중심.
- vercel 실시간 API, 웹소켓, 스트리밍이 불가능함. 그대신 vercel은 서버를 여는 시간이 없는데 render를 무료로 사용한다면 15분 동안 요청이 없으면 서버가 자동으로 꺼짐.
- 하지만 은혜롭게도 이를 편법으로 서버가 꺼지지 않게 하는 방법이 있음. 바로 10분마다 요청을 계속 주는 uptimerobot을 사용하면 됨
    - http://uptimerobot.com/ : 회원가입
    - Create your first monitor. : monitor설정 그대로 HTTP로 두고, URL to monitor에 요청을 보낼 url 입력.
    - create 누르면 끝 : 이제 5분마다 요청을 자동으로 보내줌.

# 개선사항
- 창 크기에 따라서 글자가 끊기지 않도록 블록을 늘린다. 유동적으로.
- 프로젝트 페이지에서 목록으로 돌아가기 위치 통일.
- 사용한 툴을 포트폴리오마다 항목단위로 넣을 수 있도록 수정.(완료)
- 포트폴리오 이미지마다 github 링크 달기.(완료)
- 이미지 개수와 현재 페이지 넘버링을 추가 [1/4]이런식으로