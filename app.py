
import streamlit as st

from graph import app as workflow_app
from nodes import generate_interview_question


# Page configuration
st.set_page_config(
    page_title="PlacementAI | Interview Coach",
    page_icon="🎯",
    layout="wide"
)


# Session state
if "question" not in st.session_state:
    st.session_state.question = ""

if "student_answer" not in st.session_state:
    st.session_state.student_answer = ""

if "result" not in st.session_state:
    st.session_state.result = None

if "total_attempts" not in st.session_state:
    st.session_state.total_attempts = 0


# Sidebar
with st.sidebar:
    st.title("🎯 PlacementAI")
    st.caption("Your personal AI interview coach")

    page = st.radio(
        "Navigation",
        [
            "Interview Practice",
            "My Evaluation",
            "About Project"
        ]
    )

    st.divider()

    st.success("AI Model: GPT-OSS")
    st.info("Workflow: LangGraph")
    st.info("Monitoring: LangSmith")

    st.metric(
        "Completed Evaluations",
        st.session_state.total_attempts
    )


# Header
st.markdown(
    """
    <div style="
        background: linear-gradient(120deg,#172554,#2563EB);
        padding:30px;
        border-radius:15px;
        color:white;
    ">
        <h1>AI Placement Feedback Assistant</h1>
        <p>
        Practice technical interviews, evaluate your answers,
        and improve your placement preparation.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# Interview Practice
if page == "Interview Practice":

    st.subheader("🚀 Start Your Interview Practice")

    job_role = st.selectbox(
        "Select Your Job Role",
        [
            "Python Developer",
            "Data Scientist",
            "Machine Learning Engineer",
            "Full Stack Developer",
            "AI Engineer",
            "Software Developer",
            "Data Analyst",
            "Cloud Engineer"
        ]
    )

    st.subheader("📝 Interview Question")

    if st.button("✨ Generate Interview Question",
                 use_container_width=True):

        try:
            with st.spinner("Generating question..."):

                st.session_state.question = (
                    generate_interview_question(job_role)
                )

        except Exception as e:
            st.error(f"Question generation failed: {e}")

    question = st.text_area(
        "Your Interview Question",
        key="question",
        height=100
    )

    st.subheader("✍️ Submit Your Answer")

    student_answer = st.text_area(
        "Write Your Answer",
        key="student_answer",
        height=180,
        placeholder="Enter your interview answer here..."
    )

    st.caption(
        f"Word count: {len(student_answer.split())}"
    )

    if st.button(
        "🚀 Evaluate My Answer",
        type="primary",
        use_container_width=True
    ):

        if not question.strip():
            st.warning("Please generate or enter a question.")

        elif not student_answer.strip():
            st.warning("Please enter your answer.")

        else:

            initial_state = {
                "job_role": job_role,
                "question": question,
                "student_answer": student_answer,
                "analysis": "",
                "score": 0,
                "feedback": "",
                "final_report": ""
            }

            try:
                with st.spinner(
                    "LangGraph is evaluating your answer..."
                ):

                    result = workflow_app.invoke(
                        initial_state,
                        config={
                            "run_name": "PlacementAI Interview Evaluation",
                            "tags": [
                                "PlacementAI",
                                "interview-evaluation",
                                job_role
                            ],
                            "metadata": {
                                "application": "PlacementAI",
                                "job_role": job_role
                            }
                        }
                    )

                    st.session_state.result = result
                    st.session_state.total_attempts += 1

            except Exception as e:
                st.error(f"Evaluation failed: {e}")

    # Display evaluation
    if st.session_state.result is not None:

        result = st.session_state.result
        score = result["score"]

        st.divider()
        st.subheader("📊 Performance Dashboard")

        col1, col2, col3 = st.columns(3)

        col1.metric("Interview Score", f"{score}/10")

        col2.metric(
            "Performance",
            "Good" if score >= 7 else "Needs Improvement"
        )

        col3.metric("Status", "Completed")

        st.progress(score / 10)

        if score >= 7:
            st.success("Excellent work!")
        else:
            st.warning("Your answer needs improvement.")

        tab1, tab2, tab3 = st.tabs(
            [
                "Answer Analysis",
                "Improvement Feedback",
                "Final Report"
            ]
        )

        with tab1:
            st.write(result["analysis"])

        with tab2:
            if result.get("feedback"):
                st.markdown(result["feedback"])
            else:
                st.success("No additional feedback required.")

        with tab3:
            st.markdown(result["final_report"])

            st.download_button(
                "⬇️ Download Evaluation Report",
                data=result["final_report"],
                file_name="placement_feedback_report.txt",
                mime="text/plain"
            )


# Evaluation page
elif page == "My Evaluation":

    st.subheader("📊 My Evaluation")

    if st.session_state.result is None:

        st.info("Complete an interview evaluation first.")

    else:

        result = st.session_state.result

        st.metric(
            "Latest Score",
            f"{result['score']}/10"
        )

        st.write("Job Role:", result["job_role"])
        st.write("Question:", result["question"])

        st.markdown("### Latest Feedback")
        st.write(result.get("feedback") or "No additional feedback.")

        st.download_button(
            "Download Report",
            data=result["final_report"],
            file_name="placement_feedback_report.txt"
        )


# About page
elif page == "About Project":

    st.subheader("ℹ️ About PlacementAI")

    st.write(
        "PlacementAI is an AI-powered interview practice "
        "application that evaluates student answers and "
        "generates personalized feedback."
    )

    st.markdown("### Technology Stack")

    st.markdown("""
    - Python
    - Streamlit
    - LangChain
    - LangGraph
    - OpenRouter
    - LangSmith
    """)

    st.markdown("### Workflow")

    st.code("""
START
  |
Analyze Answer
  |
Evaluate Answer
  |
Conditional Routing
  |
Score < 7?
  |
Generate Feedback (if required)
  |
Generate Final Report
  |
END
    """)
