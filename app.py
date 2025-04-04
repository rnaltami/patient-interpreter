import streamlit as st
from gpt_utils import rewrite_symptoms, suggest_follow_up_questions
import pandas as pd
import os
from datetime import datetime
import openai 
from pathlib import Path

# --- Sidebar Navigation ---
page = st.sidebar.radio(
    "📂 Navigate",
    [
        "🩺 Patient Interpreter",
        "📝 My Next Visit Notes",
        "📁 My Health Summary",
        "🔍 Symptoms Chat"
    ],
    index=0
)

# ---------------------
# PAGE: Patient Interpreter
# ---------------------
if page == "🩺 Patient Interpreter":
    st.title("Patient Interpreter 🩺")

    user_id = st.text_input("Enter your name or ID (for saving visit notes):", value="roxana")

    if "symptoms_text" not in st.session_state:
        st.session_state.symptoms_text = ""
    if "rewritten" not in st.session_state:
        st.session_state.rewritten = None
    if "questions" not in st.session_state:
        st.session_state.questions = None

    st.text_area(
        label="",
        placeholder="Write what you want to tell your doctor. Not sure yet? Symptoms Chat can help you figure it out.",
        key="symptoms_text",
        height=200
    )

    api_key = st.secrets["openai"]["api_key"]

    if st.button("Rewrite for Doctor"):
        if not st.session_state.symptoms_text:
            st.warning("Add a few thoughts and we’ll help you organize them.")
        elif not api_key:
            st.warning("Please enter your OpenAI API key.")
        else:
            with st.spinner("Rewriting..."):
                try:
                    rewritten = rewrite_symptoms(st.session_state.symptoms_text, api_key)
                    questions = suggest_follow_up_questions(st.session_state.symptoms_text, api_key)

                    st.session_state.rewritten = rewritten
                    st.session_state.questions = questions
                except Exception as e:
                    st.error(f"Something went wrong: {e}")

    if st.session_state.rewritten:
        st.subheader("💬 Here's What to Tell Your Doctor:")
        st.success(st.session_state.rewritten)

    if st.session_state.questions:
        st.subheader("💡 Questions to Ask Your Doctor:")
        st.info(st.session_state.questions)

    if st.session_state.rewritten and st.session_state.questions:
        if st.button("💾 Save This Visit Note"):
            os.makedirs("visit_logs", exist_ok=True)
            filename = f"visit_logs/{user_id}_visit_log.csv"

            visit_data = {
                "timestamp": datetime.now().isoformat(),
                "user_input": st.session_state.symptoms_text,
                "rewritten_summary": st.session_state.rewritten,
                "follow_up_questions": st.session_state.questions
            }

            if os.path.exists(filename):
                df = pd.read_csv(filename)
                df = pd.concat([df, pd.DataFrame([visit_data])], ignore_index=True)
            else:
                df = pd.DataFrame([visit_data])

            df.to_csv(filename, index=False)
            st.success("✅ Visit note saved!")

# ---------------------
# PAGE: My Next Visit Notes
# ---------------------
elif page == "📝 My Next Visit Notes":
    st.title("My Next Visit Notes 📝")
    st.caption("These are your recent saved notes — ready to use for your next appointment.")

    user_id = st.text_input("Enter your name or ID to view notes:", value="roxana")

    filename = f"visit_logs/{user_id}_visit_log.csv"
    summary_path = f"visit_summary/{user_id}_summary.csv"
    os.makedirs("visit_summary", exist_ok=True)

    if os.path.exists(filename):
        df = pd.read_csv(filename)
        df = df.sort_values("timestamp", ascending=False).reset_index(drop=True)

        st.subheader("🗂️ Your Most Recent Saved Notes:")

        for i, row in df.iterrows():
            try:
                date = datetime.fromisoformat(row['timestamp']).strftime("%B %d, %Y")
            except Exception:
                date = row['timestamp'][:10]

            snippet = row['user_input']
            snippet_preview = " ".join(snippet.strip().split()[:10])
            if len(snippet.strip().split()) > 10:
                snippet_preview += "..."

            with st.expander(f"🕒 {date} – \"{snippet_preview}\""):
                st.markdown(f"**📝 What You Wrote:**\n\n{row['user_input']}")
                st.markdown(f"**💬 What to Tell Your Doctor:**\n\n{row['rewritten_summary']}")
                st.markdown(f"**💡 Questions to Ask:**\n\n{row['follow_up_questions']}")

                # Form fields
                add_date = st.checkbox("Add a Visit Date?", key=f"add_date_{i}")
                visit_date = None
                if add_date:
                    visit_date = st.date_input("Visit Date:", key=f"date_{i}")
                
                doctor_name = st.text_input("Doctor's Name (optional):", key=f"doc_{i}", value=row.get("doctor_name", ""))
                more_notes = st.text_area("Additional Notes (optional):", key=f"more_{i}", value=row.get("additional_notes", ""), height=100)
                doctor_said = st.text_area("What the Doctor Said (optional):", key=f"said_{i}", value=row.get("doctor_said", ""), height=100)

                # Save updated data to this note
                if st.button("💾 Save Note", key=f"save_note_{i}"):
                    df.at[i, "doctor_name"] = doctor_name
                    df.at[i, "additional_notes"] = more_notes
                    df.at[i, "doctor_said"] = doctor_said
                    if visit_date:
                        df.at[i, "visit_date"] = visit_date.strftime("%Y-%m-%d")
                    else:
                        df.at[i, "visit_date"] = ""

                    df.to_csv(filename, index=False)
                    st.success("✅ Note updated!")

                # Log the full note as a summary visit
                if st.button("📁 Log This Visit in My Health Summary", key=f"log_visit_{i}"):
                    summary_entry = {
                        "timestamp": row['timestamp'],
                        "visit_date": visit_date.strftime("%Y-%m-%d") if visit_date else "",
                        "doctor_name": doctor_name,
                        "what_you_wrote": row['user_input'],
                        "rewritten_summary": row['rewritten_summary'],
                        "follow_up_questions": row['follow_up_questions'],
                        "additional_notes": more_notes,
                        "doctor_said": doctor_said
                    }

                    if os.path.exists(summary_path):
                        summary_df = pd.read_csv(summary_path)
                        summary_df = pd.concat([summary_df, pd.DataFrame([summary_entry])], ignore_index=True)
                    else:
                        summary_df = pd.DataFrame([summary_entry])

                    summary_df.to_csv(summary_path, index=False)
                    st.success("✅ Visit saved to Health Summary!")

    else:
        st.info("No visit notes found yet. Go to 'Patient Interpreter' to create one.")

# ---------------------
# PAGE: My Health Summary (placeholder)
# ---------------------
elif page == "📁 My Health Summary":
    st.title("My Health Summary 📁")
    st.caption("A record of visits you've logged — your personal health timeline.")

    user_id = st.text_input("Enter your name or ID to view summary:", value="roxana")
    summary_path = f"visit_summary/{user_id}_summary.csv"

    if os.path.exists(summary_path):
        summary_df = pd.read_csv(summary_path)
        summary_df = summary_df.sort_values("visit_date", ascending=False)

        st.subheader("🧾 Logged Visits:")

        for i, row in summary_df.iterrows():
            # Clean date display
            try:
                date_label = datetime.fromisoformat(row['visit_date']).strftime("%B %d, %Y") if row['visit_date'] else "Date not provided"
            except:
                date_label = row.get('timestamp', '')[:10]

            doc_label = row['doctor_name'] if row['doctor_name'] else "Doctor not specified"
            title = f"🗓️ {date_label} — {doc_label}"

            with st.expander(title):
                st.markdown(f"**📝 What You Wrote:**\n\n{row['what_you_wrote']}")
                st.markdown(f"**💬 What You Told the Doctor:**\n\n{row['rewritten_summary']}")
                st.markdown(f"**💡 Questions You Asked:**\n\n{row['follow_up_questions']}")
                
                if row.get("doctor_said"):
                    st.markdown(f"**🩺 What the Doctor Said:**\n\n{row['doctor_said']}")
                if row.get("additional_notes"):
                    st.markdown(f"**🗒️ Additional Notes:**\n\n{row['additional_notes']}")
    else:
        st.info("No visits logged yet. You can log a visit from the 'My Next Visit Notes' page.")


# ---------------------
# PAGE: Symptom Explorer (chat-style)
# ---------------------
elif page == "🔍 Symptoms Chat":
    st.title("Symptoms Chat 🔍")
    st.caption("🤔 Not sure what might be causing your symptoms? Chat here to explore possible explanations and get ideas for what to ask your doctor.")

    api_key = st.secrets["openai"]["api_key"]

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []

    with st.container():
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.chat_message("user").write(msg["content"])
            else:
                st.chat_message("assistant").write(msg["content"])

    user_message = st.chat_input("Describe a symptom or ask a question...")

    if user_message:
        st.session_state.chat_history.append({"role": "user", "content": user_message})
        st.chat_message("user").write(user_message)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    client = openai.OpenAI(api_key=api_key)
                    messages = [
                        {
                            "role": "system",
                            "content": (
                                "You are a helpful assistant who listens to symptoms and offers possible causes, systems, or conditions to consider. "
                                "You always remind the user to follow up with a healthcare professional. Do not panic the user, but be specific and informative."
                            )
                        }
                    ] + st.session_state.chat_history

                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=messages,
                        temperature=0.7,
                        max_tokens=600
                    )

                    reply = response.choices[0].message.content.strip()
                    st.write(reply)

                    st.session_state.chat_history.append({"role": "assistant", "content": reply})

                except Exception as e:
                    st.error(f"Something went wrong: {e}")
