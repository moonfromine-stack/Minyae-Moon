import streamlit as st
import random
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="가치관 테스트", page_icon="✨")

# ---------------------------
# 질문 리스트
# ---------------------------
questions = [
    ("돈을 더 벌기 위해 건강을 일부 희생할 수 있다", "돈", "건강"),
    ("건강을 위해서라면 수입이 줄어드는 선택도 할 수 있다", "건강", "돈"),

    ("안정적인 삶보다 내가 원하는 삶을 선택하는 것이 더 중요하다", "자유", "안정감"),
    ("불확실함보다는 안정적인 선택이 더 편하다", "안정감", "자유"),

    ("몸이 힘들어도 성과를 내는 것이 더 중요하다", "성취", "건강"),
    ("성과보다 몸과 컨디션을 유지하는 것이 더 중요하다", "건강", "성취"),

    ("커리어를 위해 연인이나 가족과의 시간을 줄일 수 있다", "성취", "사랑"),
    ("성과 기회를 포기하더라도 소중한 사람과의 시간을 지키고 싶다", "사랑", "성취"),

    ("성과를 위해 인간관계를 희생할 수 있다", "성취", "커뮤니티"),
    ("성과보다 사람들과의 관계를 유지하는 것이 더 중요하다", "커뮤니티", "성취"),

    ("돈보다 배우고 성장하는 경험이 더 중요하다", "지식", "돈"),
    ("배움보다 실질적인 수입이 더 중요하다", "돈", "지식"),

    ("위험을 감수하더라도 새로운 기회를 선택하고 싶다", "자유", "안정감"),
    ("굳이 위험을 감수하기보다 안정적인 길을 선택하겠다", "안정감", "자유"),

    ("내 만족보다 타인의 인정이 더 중요하다", "명예", "자유"),
    ("남들이 인정하지 않아도 내가 만족하면 괜찮다", "자유", "명예"),

    ("집단에서 영향력을 가지는 것이 중요하다", "권력", "커뮤니티"),
    ("영향력보다 편안한 인간관계가 더 중요하다", "커뮤니티", "권력"),

    ("혼자보다 사람들과 어울리는 삶이 더 좋다", "커뮤니티", "자유"),
    ("인간관계보다 혼자만의 시간이 더 중요하다", "자유", "커뮤니티"),

    ("스트레스를 감수하더라도 돈을 더 버는 것이 낫다", "돈", "건강"),
    ("돈이 적더라도 스트레스 적은 삶이 더 좋다", "건강", "돈"),

    ("깊이 이해하는 것이 빠른 성과보다 중요하다", "지식", "성취"),
    ("이해보다 결과를 내는 것이 더 중요하다", "성취", "지식"),
]

# ---------------------------
# 초기 상태 설정
# ---------------------------
if "initialized" not in st.session_state:
    random.shuffle(questions)
    st.session_state.questions = questions
    st.session_state.current = 0
    st.session_state.history = []
    
    values = set([q[1] for q in questions] + [q[2] for q in questions])
    st.session_state.scores = {v: 0 for v in values}
    st.session_state.initialized = True

# ---------------------------
# 선택 함수
# ---------------------------
def choose(answer):
    q, yes_val, no_val = st.session_state.questions[st.session_state.current]
    
    st.session_state.history.append((st.session_state.current, answer))
    
    if answer == "yes":
        st.session_state.scores[yes_val] += 1
    else:
        st.session_state.scores[no_val] += 1
    
    st.session_state.current += 1

# ---------------------------
# 뒤로가기
# ---------------------------
def go_back():
    if st.session_state.current == 0:
        return
    
    st.session_state.current -= 1
    
    prev_q, prev_answer = st.session_state.history.pop()
    q, yes_val, no_val = st.session_state.questions[st.session_state.current]
    
    if prev_answer == "yes":
        st.session_state.scores[yes_val] -= 1
    else:
        st.session_state.scores[no_val] -= 1

# ---------------------------
# UI
# ---------------------------
st.title("✨ 가치관 우선순위 테스트")

if st.session_state.current < len(st.session_state.questions):
    q, _, _ = st.session_state.questions[st.session_state.current]
    
    progress = (st.session_state.current) / len(st.session_state.questions)
    st.progress(progress)
    
    st.subheader(q)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("⬅️ 뒤로가기"):
            go_back()
    
    with col2:
        if st.button("YES"):
            choose("yes")
    
    with col3:
        if st.button("NO"):
            choose("no")

# ---------------------------
# 결과 화면
# ---------------------------
else:
    st.success("✨ 결과가 나왔습니다!")
    
    sorted_scores = sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True)
    
    for i, (v, s) in enumerate(sorted_scores):
        st.write(f"{i+1}. {v} ({s}점)")
    
    top3 = [v[0] for v in sorted_scores[:3]]
    
    st.markdown("## 🔍 해석")
    
    if "자유" in top3:
        st.write("- 스스로 선택하는 삶에서 만족을 느끼는 타입입니다.")
    if "성취" in top3:
        st.write("- 목표 달성과 성장에서 보람을 느낍니다.")
    if "안정감" in top3:
        st.write("- 안정적인 환경을 선호합니다.")
    if "사랑" in top3:
        st.write("- 인간관계를 중요하게 생각합니다.")
    if "건강" in top3:
        st.write("- 삶의 균형을 중요하게 여깁니다.")
    if "돈" in top3:
        st.write("- 현실적 안정과 경제력을 중시합니다.")
    if "지식" in top3:
        st.write("- 배우는 과정 자체를 즐깁니다.")
    if "커뮤니티" in top3:
        st.write("- 소속감과 관계를 중요하게 생각합니다.")



