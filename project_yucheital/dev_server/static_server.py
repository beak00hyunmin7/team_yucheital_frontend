"""화면(yuche_frontend) 정적 파일 서버.

python -m http.server 와 같지만 모든 응답에 Cache-Control: no-cache 를 붙인다.
http.server 는 캐시 헤더를 안 보내서 브라우저가 style.css 같은 파일을 '추측'으로 한동안 재사용하고,
그래서 화면을 고친 뒤 새로고침해도 예전 CSS 로 보이는 일이 생긴다.
no-cache 는 매번 서버에 바뀌었는지 물어보게 할 뿐이라(안 바뀌면 304) 느려지지 않는다.

사용법 (yuche_frontend 폴더를 서비스):
    python dev_server/static_server.py              # 0.0.0.0:8080
    python dev_server/static_server.py 8080 127.0.0.1
"""
import functools
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "yuche_frontend"


class NoCacheHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    host = sys.argv[2] if len(sys.argv) > 2 else "0.0.0.0"
    handler = functools.partial(NoCacheHandler, directory=str(ROOT))
    with ThreadingHTTPServer((host, port), handler) as httpd:
        print(f"Serving {ROOT} on http://{host}:{port}/vtkjs.html (no-cache)")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
