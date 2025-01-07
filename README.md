필요한 라이브러리 설치
pip install tkinter serial

exe 파일을 생성하기 위해
pip install pyinstaller
실행 하여 설치 후
vs code 아래 커맨드 창에서
exe파일로 만들 파이썬 파일이 있는 폴더로 이동해
pyinstaller --onefile 파일명.py 입력하면
해당 폴더에 dist 폴더가 생성되고 그 안에 exe 파일이 생성됨

pyinstaller --noconsole --onefile로 하면
exe 파일 실행시 콘솔창이 같이 생성되지 않음

만약 해당 브레이크 아두이노 보드에 다른 아두이노 코드가
컴파일 되어 있다면 여기에 있는 ino 파일을 다운 받아
컴파일 한 후 실행해야 함
