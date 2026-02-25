from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "dev-type-test-key-1234"

# 1. 유형 정의
TYPES = ["frontend", "backend", "fullstack", "mobile", "game", "embedded", "data_ai"]

# 2. 질문 데이터 (작성해주신 질문들 유지)
QUESTIONS = [
    {
        "text": "강의실에 도착해 노트북을 꺼냈다! 배경화면 상태는?",
        "image": "img/q1.png",
        "options": [
            {"text": "폴더별로 완벽 정리!", "add": {"frontend": 2, "mobile": 1}},
            {"text": "기본 배경화면 혹은 터미널 창만 띄워져 있음", "add": {"backend": 2, "embedded": 1}},
            {"text": "직접 만든 배경화면이나 게임 일러스트", "add": {"game": 2, "data_ai": 1}}
        ]
    },
    {
        "text": "옆자리 동기가 아주 느린 구형 노트북으로 낑낑대고 있다면?",
        "image": "img/q2.png",
        "options": [
            {"text": "램 부족인가? 백그라운드 프로세스를 다 꺼준다", "add": {"embedded": 2, "backend": 1}},
            {"text": "요즘은 클라우드 환경이 좋으니 웹에서 하라고 제안한다", "add": {"frontend": 1, "fullstack": 1}},
            {"text": "이참에 아이패드나 최신 폰으로 하는 앱을 추천해준다", "add": {"mobile": 2}}
        ]
    },
    {
        "text": "동아리 홍보 포스터를 봤다. 가장 눈길이 가는 문구는?",
        "image": "img/q3.png",
        "options": [
            {"text": "\"누구나 눈이 번쩍 뜨일 화려한 결과물을 만듭니다!\"", "add": {"frontend": 2, "game": 2}},
            {"text": "\"보이지 않는 곳에서 세상을 움직이는 엔진이 됩니다.\"", "add": {"backend": 2, "embedded": 1}},
            {"text": "\"데이터 속에서 미래를 예측하는 마법사가 됩니다.\"", "add": {"data_ai": 2, "fullstack": 2}}
        ]
    },
    {
        "text": "점심시간, 학생식당 키오스크 한 대가 고장 나있다. 당신의 반응은?",
        "image": "img/q4.png",
        "options": [
            {"text": "버튼 위치나 결제 UI가 구려서 터진 게 분명하다고 분석한다", "add": {"frontend": 2, "mobile": 1}},
            {"text": "내부 DB 통신 오류인가? 서버 터진 건지 궁금해한다", "add": {"backend": 2, "fullstack": 2}},
            {"text": "이거 뜯어보면 기판이 어떻게 생겼을지 궁금해한다", "add": {"embedded": 2, "game": 2}}
        ]
    },
    {
        "text": "팀플 시작! 내가 맡고 싶은 역할은?",
        "image": "img/q5.png",
        "options": [
            {"text": "발표 자료와 PPT 디자인 (사용자가 볼 모든 것)", "add": {"frontend": 2, "mobile": 2}},
            {"text": "자료 조사와 전체적인 논리 구조 짜기 (내부 로직)", "add": {"backend": 1, "data_ai": 2}},
            {"text": "팀장 맡아서 그냥 내가 다 해버리기 (전체 총괄)", "add": {"fullstack": 2}}
        ]
    },
    {
        "text": "공강 시간에 게임을 한다면 어떤 스타일?",
        "image": "img/q6.png",
        "options": [
            {"text": "화려한 그래픽과 타격감이 살아있는 액션 게임", "add": {"game": 2, "frontend": 1}},
            {"text": "철저한 빌드업과 자원 관리가 중요한 전략 게임", "add": {"backend": 1, "data_ai": 2, "embedded": 1}},
            {"text": "장소 불문! 폰으로 가볍게 즐기는 모바일 게임", "add": {"mobile": 2, "fullstack": 1}}
        ]
    },
    {
        "text": "교수님이 '자유 주제' 과제를 내주셨다. 당신은?",
        "image": "img/q7.png",
        "options": [
            {"text": "사람들이 실제로 써보고 '와!' 할 만한 서비스 기획", "add": {"frontend": 1, "fullstack": 1, "mobile": 2}},
            {"text": "최신 딥러닝 모델을 돌려서 결과 뽑아보기", "add": {"data_ai": 2}},
            {"text": "기존 시스템의 성능을 2배로 올리는 최적화 실험", "add": {"backend": 1, "embedded": 2}}
        ]
    },
    {
        "text": "술자리에서 안주를 고를 때 당신의 기준은?",
        "image": "img/q8.png",
        "options": [
            {"text": "인스타에 올리기 좋은 비주얼이 예쁜 안주", "add": {"frontend": 2, "mobile": 1}},
            {"text": "가성비 좋고 든든해서 배를 확실히 채워주는 안주", "add": {"backend": 1, "embedded": 1, "fullstack": 1}},
            {"text": "매번 먹던 거 말고, 처음 보는 특이한 퓨전 안주", "add": {"game": 2, "data_ai": 2}}
        ]
    },
    {
        "text": "과제가 막혔다! 구글링을 하던 중 당신의 스타일은?",
        "image": "img/q9.png",
        "options": [
            {"text": "스택오버플로우의 답변 코드를 일단 복붙해서 돌려본다", "add": {"fullstack": 2, "mobile": 1, "game": 2}},
            {"text": "공식 문서(Documentation)를 처음부터 정독한다", "add": {"backend": 1, "embedded": 2}},
            {"text": "왜 안되는지 데이터 로그를 끝까지 추적한다", "add": {"data_ai": 2, "backend": 1}}
        ]
    },
    {
    "text": "드디어 종강! 당신이 꿈꾸는 완벽한 방학 생활은?",
    "image": "img/q10.png",
    "options": [
        {
            "text": "요즘 뜨는 핫플레이스 투어! 예쁜 사진 찍어서 SNS에 기록하기", 
            "add": {"frontend": 2, "mobile": 2, "fullstack": 1}
        },
        {
            "text": "방에 틀어박혀 나만의 취미에 몰두하기", 
            "add": {"backend": 1, "embedded": 2, "data_ai": 2}
        },

        {
            "text": "현실은 잊는다! 게임하며 밤새기", 
            "add": {"game": 2, "fullstack": 1}
        }
    ]
}
]

# 3. 결과 데이터
RESULTS = {
  "frontend": {
    "title": "프론트엔드 개발자",
    "tagline": "세상의 모든 첫인상을 책임질게!",
    "points": [
      {"headline": "🎨 미적 감각으로 UX를 선물하는 타입!", "desc": "사용자가 즐거운 경험을 하도록 화면의 디테일을 끝까지 다듬어요."},
      {"headline": "🔍 눈에 보이는 결과물에서 짜릿함을 느껴요.", "desc": "레이아웃/인터랙션/애니메이션이 ‘딱’ 맞을 때 행복해합니다."},
      {"headline": "🤝 소통으로 불편함을 가장 먼저 캐치!", "desc": "사용자 피드백을 빠르게 반영하고 더 좋은 흐름을 제안해요."},
    ],
    "roadmap_title": "프론트엔드 개발자가 되려면?",
    "roadmap": [
      "기초 언어: JavaScript, TypeScript",
      "필수 지식: HTML/CSS, 웹 성능 최적화, 브라우저 구조",
      "추천 스택: React, Next.js, Vue.js, Tailwind CSS",
    ],
  },

  "backend": {
    "title": "백엔드 개발자",
    "tagline": "뒤에서 전부 다 받쳐줄게!",
    "points": [
      {"headline": "🦁 어떤 상황에서도 효율을 뽑아내는 전략가!", "desc": "반복 작업은 자동화하고, 로직은 정리해서 안정적으로 굴려요."},
      {"headline": "🧠 폭넓은 이해력 + 뛰어난 설계 능력!", "desc": "보이지 않는 구조를 머릿속에 그리며 API/DB 구조를 탄탄히 잡아요."},
      {"headline": "⚓ 쉽게 포기하지 않는 묵직한 끈기!", "desc": "에러 로그와 씨름해도 결국 원인을 찾아내는 집요함이 있어요."},
    ],
    "roadmap_title": "백엔드 개발자가 되려면?",
    "roadmap": [
      "기초 언어: Java, Python, Go, Node.js",
      "필수 지식: 통신개념(HTTP), 데이터베이스(DB), 운영체제(OS)",
      "추천 스택: Spring Boot, Django, Nest.js, Flask",
    ],
  },

  "fullstack": {
    "title": "풀스택 개발자",
    "tagline": "나 혼자서도 세상을 바꿀 수 있어!",
    "points": [
      {"headline": "🛠️ 뭐든 뚝딱 만드는 ‘0순위’ 해결사!", "desc": "기획→화면→서버까지 연결해서 ‘되는 것’을 빠르게 만듭니다."},
      {"headline": "🗺️ 전체 흐름을 읽는 넓은 시야!", "desc": "프론트/백/배포까지 서비스 흐름을 한 번에 이해하는 편이에요."},
      {"headline": "🚀 새로운 기술 흡수 속도가 광속!", "desc": "필요하면 바로 배우고 적용해서 MVP를 완성해버립니다."},
    ],
    "roadmap_title": "풀스택 개발자가 되려면?",
    "roadmap": [
      "기초 언어: JS/TS, Python",
      "필수 지식: Web Architecture, 클라우드(AWS), DB 설계",
      "추천 스택: Next.js + Prisma, MERN Stack, DevOps",
    ],
  },

  "mobile": {
    "title": "모바일 개발자",
    "tagline": "당신의 손안에 온 세상을 담아줄게!",
    "points": [
      {"headline": "📱 ‘한 손의 경험’을 중요하게 여겨요!", "desc": "휴대성/접근성/동선을 고려한 UX에 진심입니다."},
      {"headline": "✨ 트렌드와 디바이스에 민감한 타입!", "desc": "새 기능/새 기기 나오면 바로 만져보고 적용해보고 싶어해요."},
      {"headline": "⚡ 부드러운 애니메이션에서 안정감을 느껴요.", "desc": "스크롤/전환/로딩의 ‘체감 품질’ 올리는 걸 좋아합니다."},
    ],
    "roadmap_title": "모바일 개발자가 되려면?",
    "roadmap": [
      "기초 언어: Kotlin, Swift, Dart",
      "필수 지식: Mobile UX, 비동기, 앱 스토어 배포",
      "추천 스택: Android SDK, SwiftUI, Flutter, React Native",
    ],
  },

  "game": {
    "title": "게임 개발자",
    "tagline": "내가 만든 세계에서 마음껏 뛰어놀아봐!",
    "points": [
      {"headline": "🎮 재미를 ‘논리적으로’ 설계하는 몰입가!", "desc": "재미 요소를 구조화하고 시스템으로 구현하는 데 신나요."},
      {"headline": "⚙️ 실시간 로직/물리/연산을 사랑해요.", "desc": "프레임, 충돌, 입력, 최적화 같은 실시간 요소에 강합니다."},
      {"headline": "🔥 경험을 위해 밤새도 즐거운 타입!", "desc": "유저가 ‘와!’ 하는 순간을 만들기 위해 끝까지 다듬어요."},
    ],
    "roadmap_title": "게임 개발자가 되려면?",
    "roadmap": [
      "기초 언어: C++, C#, Python",
      "필수 지식: 자료구조, 선형대수, 컴퓨터 그래픽스",
      "추천 툴: Unity, Unreal Engine, DirectX",
    ],
  },

  "embedded": {
    "title": "임베디드 개발자",
    "tagline": "기계에 영혼을 불어넣는 장인!",
    "points": [
      {"headline": "🔌 HW/SW 경계를 넘나드는 테크니션!", "desc": "센서/신호/제어 흐름을 이해하고 기계가 ‘말’을 듣게 만들어요."},
      {"headline": "💎 1KB도 낭비하지 않는 효율 중시!", "desc": "메모리/전력/성능을 끝까지 아끼는 최적화에 강합니다."},
      {"headline": "🛡️ 24시간 안 죽는 안정성을 추구해요.", "desc": "예외 상황까지 꼼꼼히 챙기며 ‘안정적 시스템’을 만듭니다."},
    ],
    "roadmap_title": "임베디드 개발자가 되려면?",
    "roadmap": [
      "기초 언어: C, C++, Assembly",
      "필수 지식: 전자회로, MCU/RTOS, 메모리 아키텍처",
      "추천 스택: Firmware, Linux Kernel, AUTOSAR",
    ],
  },

  "data_ai": {
    "title": "데이터/AI 개발자",
    "tagline": "데이터 속에 숨겨진 미래를 읽어줄게!",
    "points": [
      {"headline": "🔮 무질서 속에서 패턴을 찾아내는 통찰력!", "desc": "데이터를 보면 ‘의미 있는 신호’가 어디 있는지 찾고 싶어해요."},
      {"headline": "📉 감보다 숫자를 믿는 논리형!", "desc": "지표/검증/비교로 결론을 내리는 편입니다."},
      {"headline": "🤖 가설-실험-검증 루프를 즐겨요.", "desc": "계속 돌려보고 개선하면서 정답에 가까워지는 과정이 재밌어요."},
    ],
    "roadmap_title": "데이터/AI 개발자가 되려면?",
    "roadmap": [
      "기초 언어: Python, R, SQL",
      "필수 지식: 통계, 선형대수, 알고리즘, 전처리",
      "추천 스택: PyTorch, TensorFlow, Pandas, Spark",
    ],
  },
}
# --- 로직 함수 ---

def get_init_scores():
    return {t: 0 for t in TYPES}

def pick_result(scores):
    # 가장 높은 점수를 가진 키를 찾음
    return max(scores, key=scores.get)

# --- 라우팅 ---

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/start")
def start():
    session["idx"] = 0
    session["scores"] = get_init_scores()
    return redirect(url_for("test"))

@app.route("/test", methods=["GET", "POST"])
def test():
    idx = session.get("idx", 0)
    if idx >= len(QUESTIONS):
        return redirect(url_for("result"))

    if request.method == "POST":
        # 선택한 옵션의 인덱스를 가져옴 (0, 1, 2 중 하나)
        choice_idx = int(request.form.get("answer"))
        selected_option = QUESTIONS[idx]["options"][choice_idx]
        
        # 해당 옵션에 지정된 점수들을 세션에 합산
        current_scores = session["scores"]
        for type_key, score_val in selected_option["add"].items():
            current_scores[type_key] += score_val
        
        session["scores"] = current_scores
        session["idx"] = idx + 1
        return redirect(url_for("test"))

    q = QUESTIONS[idx]
    progress = {
        "current": idx + 1,
        "total": len(QUESTIONS),
        "percent": int((idx + 1) / len(QUESTIONS) * 100),
    }
    return render_template("one_question.html", q=q, progress=progress)

@app.route("/result")
def result():
    scores = session.get("scores")
    if not scores:
        return redirect(url_for("home"))
    
    result_key = pick_result(scores)
    content = RESULTS[result_key]
    return render_template("result.html", result=content, key=result_key)

@app.route("/restart")
def restart():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)