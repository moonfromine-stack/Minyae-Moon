import random

# 질문 리스트 (질문, YES일 때 가치, NO일 때 가치)
questions = [
    # 돈 vs 건강
    ("돈을 더 벌기 위해 건강을 일부 희생할 수 있다", "돈", "건강"),
    ("건강을 위해서라면 수입이 줄어드는 선택도 할 수 있다", "건강", "돈"),

    # 자유 vs 안정감
    ("안정적인 삶보다 내가 원하는 삶을 선택하는 것이 더 중요하다", "자유", "안정감"),
    ("불확실함보다는 안정적인 선택이 더 편하다", "안정감", "자유"),

    # 성취 vs 건강
    ("몸이 힘들어도 성과를 내는 것이 더 중요하다", "성취", "건강"),
    ("성과보다 몸과 컨디션을 유지하는 것이 더 중요하다", "건강", "성취"),

    # 성취 vs 사랑
    ("커리어를 위해 연인이나 가족과의 시간을 줄일 수 있다", "성취", "사랑"),
    ("성과 기회를 포기하더라도 소중한 사람과의 시간을 지키고 싶다", "사랑", "성취"),

    # 성취 vs 커뮤니티
    ("성과를 위해 인간관계를 희생할 수 있다", "성취", "커뮤니티"),
    ("성과보다 사람들과의 관계를 유지하는 것이 더 중요하다", "커뮤니티", "성취"),

    # 지식 vs 돈
    ("돈보다 배우고 성장하는 경험이 더 중요하다", "지식", "돈"),
    ("배움보다 실질적인 수입이 더 중요하다", "돈", "지식"),

    # 자유 vs 안정감 (2)
    ("위험을 감수하더라도 새로운 기회를 선택하고 싶다", "자유", "안정감"),
    ("굳이 위험을 감수하기보다 안정적인 길을 선택하겠다", "안정감", "자유"),

    # 명예 vs 자유
    ("내 만족보다 타인의 인정이 더 중요하다", "명예", "자유"),
    ("남들이 인정하지 않아도 내가 만족하면 괜찮다", "자유", "명예"),

    # 권력 vs 커뮤니티
    ("집단에서 영향력을 가지는 것이 중요하다", "권력", "커뮤니티"),
    ("영향력보다 편안한 인간관계가 더 중요하다", "커뮤니티", "권력"),

    # 커뮤니티 vs 자유
    ("혼자보다 사람들과 어울리는 삶이 더 좋다", "커뮤니티", "자유"),
    ("인간관계보다 혼자만의 시간이 더 중요하다", "자유", "커뮤니티"),

    # 건강 vs 돈 (2)
    ("스트레스를 감수하더라도 돈을 더 버는 것이 낫다", "돈", "건강"),
    ("돈이 적더라도 스트레스 적은 삶이 더 좋다", "건강", "돈"),

    # 지식 vs 성취
    ("깊이 이해하는 것이 빠른 성과보다 중요하다", "지식", "성취"),
    ("이해보다 결과를 내는 것이 더 중요하다", "성취", "지식"),
]

# 가치 목록 추출
values = set([q[1] for q in questions] + [q[2] for q in questions])
scores = {v: 0 for v in values}

# 질문 섞기
random.shuffle(questions)
current = 0

# 버튼 생성
btn_yes = widgets.Button(description="YES", layout=widgets.Layout(width='150px', height='60px'))
btn_no = widgets.Button(description="NO", layout=widgets.Layout(width='150px', height='60px'))

question_box = widgets.HTML()
progress = widgets.HTML()

# 선택 처리
def choose(answer):
    global current
    
    q, yes_val, no_val = questions[current]
    
    if answer == "yes":
        scores[yes_val] += 1
    else:
        scores[no_val] += 1
    
    current += 1
    update()

btn_yes.on_click(lambda x: choose("yes"))
btn_no.on_click(lambda x: choose("no"))

# 화면 업데이트
def update():
    clear_output(wait=True)
    
    if current >= len(questions):
        show_result()
        return
    
    q, _, _ = questions[current]
    
    question_box.value = f"<h3>{q}</h3>"
    progress.value = f"<p>{current+1} / {len(questions)} ({int((current/len(questions))*100)}%)</p>"
    
    display(progress, question_box, btn_yes, btn_no, btn_back)


# 이전 선택 기록 저장
history = []

# 버튼 추가
btn_back = widgets.Button(description="⬅️ 뒤로가기", layout=widgets.Layout(width='150px', height='60px'))

def choose(answer):
    global current
    
    q, yes_val, no_val = questions[current]
    
    # 기록 저장
    history.append((current, answer))
    
    if answer == "yes":
        scores[yes_val] += 1
    else:
        scores[no_val] += 1
    
    current += 1
    update()

def go_back(b):
    global current
    
    if current == 0:
        return
    
    current -= 1
    
    prev_q, prev_answer = history.pop()
    q, yes_val, no_val = questions[current]
    
    # 점수 되돌리기
    if prev_answer == "yes":
        scores[yes_val] -= 1
    else:
        scores[no_val] -= 1
    
    update()

btn_back.on_click(go_back)

# 결과 출력
import matplotlib.pyplot as plt

def show_result():
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    # 🎯 결과 메시지
    print("✨ 당신이 행복하다고 느끼는 가치의 우선순위는...\n")
    
    for i, (v, s) in enumerate(sorted_scores):
        print(f"{i+1}. {v} ({s}점)")
    
    # 🧠 상위 가치 해석
    top3 = [v[0] for v in sorted_scores[:3]]
    
    print("\n🔍 해석")
    
    if "자유" in top3:
        print("- 당신은 스스로 선택하고 통제하는 삶에서 만족을 느끼는 경향이 있습니다.")
    if "성취" in top3:
        print("- 목표를 이루고 성장하는 과정에서 큰 보람을 느끼는 타입입니다.")
    if "안정감" in top3:
        print("- 예측 가능하고 안정적인 환경에서 편안함을 느끼는 성향입니다.")
    if "사랑" in top3:
        print("- 가까운 사람들과의 관계가 삶의 중요한 중심입니다.")
    if "건강" in top3:
        print("- 몸과 마음의 균형을 중요하게 생각하는 타입입니다.")
    if "돈" in top3:
        print("- 현실적인 안정과 경제적 여유를 중요하게 여깁니다.")
    if "지식" in top3:
        print("- 배우고 이해하는 과정 자체에서 즐거움을 느끼는 성향입니다.")
    if "커뮤니티" in top3:
        print("- 사람들과의 연결과 소속감을 중요하게 생각합니다.")
    
# 시작
update()
