import streamlit as st
import matplotlib.pyplot as plt
import random

# 질문 리스트
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

# 초기화
if "initialized" not in st.session_state:
    st.session_state.questions = questions.copy()
    random.shuffle(st.session_state.questions)
    
    values = set([q[1] for q in questions] + [q[2] for q in questions])
    st.session_state.scores = {v: 0 for v in values}
    
    st.session_state.current = 0
    st.session_state.history = []
    st.session_state.initialized = True

st.title("💭 가치관 테스트")

total = len(st.session_state.questions)
current = st.session_state.current

# 질문 진행
if current < total:
    q, yes_val, no_val = st.session_state.questions[current]
    
    st.write(f"{current+1} / {total}")
    st.subheader(q)
    
    col1, col2, col3 = st.columns(3)
    
    # YES
    with col1:
        if st.button("YES"):
            st.session_state.scores[yes_val] += 1
            st.session_state.history.append(("yes", yes_val, no_val))
            st.session_state.current += 1
            st.rerun()
    
    # NO
    with col2:
        if st.button("NO"):
            st.session_state.scores[no_val] += 1
            st.session_state.history.append(("no", yes_val, no_val))
            st.session_state.current += 1
            st.rerun()
    
    # 뒤로가기
    with col3:
        if st.button("⬅️ 뒤로가기"):
            if st.session_state.current > 0:
                st.session_state.current -= 1
                last = st.session_state.history.pop()
                
                if last[0] == "yes":
                    st.session_state.scores[last[1]] -= 1
                else:
                    st.session_state.scores[last[2]] -= 1
                
                st.rerun()

# 결과
else:
    st.header("✨ 결과")
    
    sorted_scores = sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True)
    
    st.write("### 당신이 행복하다고 느끼는 가치의 우선순위는:")
    
    for i, (v, s) in enumerate(sorted_scores):
        st.write(f"{i+1}. {v} ({s}점)")
    
    # 해석
    top3 = [v[0] for v in sorted_scores[:3]]
    
    st.write("### 🔍 해석")
    
    if "자유" in top3:
        st.write("- 스스로 선택하고 통제하는 삶에서 만족을 느끼는 경향이 있습니다.")
    if "성취" in top3:
        st.write("- 목표를 이루고 성장하는 과정에서 보람을 느끼는 타입입니다.")
    if "안정감" in top3:
        st.write("- 안정적이고 예측 가능한 환경을 중요하게 생각합니다.")
    if "사랑" in top3:
        st.write("- 가까운 사람과의 관계가 삶의 중심입니다.")
    if "건강" in top3:
        st.write("- 몸과 마음의 균형을 중요하게 생각합니다.")
    if "돈" in top3:
        st.write("- 현실적인 안정과 경제적 여유를 중요하게 여깁니다.")
    if "지식" in top3:
        st.write("- 배우고 이해하는 과정에서 즐거움을 느낍니다.")
    if "커뮤니티" in top3:
        st.write("- 사람들과의 연결과 소속감을 중요하게 생각합니다.")
    
    # 그래프
    values = [v[0] for v in sorted_scores]
    scores = [v[1] for v in sorted_scores]
    
    fig, ax = plt.subplots()
    ax.bar(values, scores)
    plt.xticks(rotation=45)
    st.pyplot(fig)
