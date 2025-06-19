import streamlit as st
# Make sure you have these files in your project directory
from form_rules import validate_form
from summarizer import summarize_form
from pdf_report import generate_pdf
from utils import send_email, generate_qr, save_to_csv
import os
from dotenv import load_dotenv
load_dotenv()

# Define the path for the CSV file. This makes it easy to reference.
CSV_FILE_PATH = "patient_data.csv"

# -------------------------------
# Session State Initialization
# -------------------------------
# These are the states we need to track across re-runs
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "pdf_path" not in st.session_state:
    st.session_state.pdf_path = ""

correct_password = os.getenv("FORM_PASSWORD")
# -------------------------------
# 🔐 Login Section
# -------------------------------
def login_section():
    st.title("🔐 Login")
    pwd = st.text_input("Enter password", type="password")
    if st.button("Login"):
        # Use a more secure password in a real application, e.g., from st.secrets
        if pwd == correct_password:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ Incorrect password")
            st.stop()


# -------------------------------
# 🧠 Smart Form Section
# -------------------------------
def form_section():
    st.title("🧠 AutoFormIQ - Smart Intake Form")

    # --- NEW: Sidebar for Admin actions like CSV download ---
    st.sidebar.header("📋 Data Export")

    # Check if the CSV file exists before showing the download button
    if os.path.exists(CSV_FILE_PATH):
        with open(CSV_FILE_PATH, "rb") as file:
            st.sidebar.download_button(
                label="⬇️ Download All Entries (CSV)",
                data=file,
                file_name="all_patient_data.csv", # The name for the downloaded file
                mime="text/csv"
            )
    else:
        st.sidebar.info("Submit at least one form to enable CSV download.")
    # --- End of new section ---


    # --- STATE 1: FORM IS NOT SUBMITTED, SHOW THE FORM ---
    if not st.session_state.submitted:
        with st.form("intake_form"):
            st.markdown("### Please fill in the patient details:")
            name = st.text_input("👤 Patient Name")
            age = st.number_input("🎂 Age", min_value=0, max_value=120)
            symptoms = st.text_area("🤒 Symptoms")
            duration = st.text_input("⏱️ Symptom Duration")
            temperature = st.number_input("🌡️ Temperature (°F)", min_value=90.0, max_value=110.0, format="%.1f")
            email = st.text_input("📧 Clinic Email to Receive PDF")
            
            submit_button = st.form_submit_button("Submit Form")

        if submit_button:
            form_data = {
                "name": name,
                "age": age,
                "symptoms": symptoms,
                "duration": duration,
                "temperature": temperature,
                "email": email
            }

            errors = validate_form(form_data)
            if errors:
                st.error("\n".join(errors))
            else:
                with st.spinner("Processing your submission..."):
                    summary = summarize_form(form_data)
                    pdf_path = generate_pdf(form_data, summary)
                    # Pass the defined CSV file path to the save function
                    save_to_csv(form_data, filename=CSV_FILE_PATH)

                    st.session_state.summary = summary
                    st.session_state.pdf_path = pdf_path
                    st.session_state.clinic_email = email

                    st.session_state.submitted = True
                
                st.rerun()

    # --- STATE 2: FORM IS SUBMITTED, SHOW THE RESULTS ---
    else:
        st.success("✅ Form submitted successfully!")
        st.markdown("### 📝 AI Summary:")
        st.info(st.session_state.summary)

        st.markdown("### 📄 Download & Share Report")
        with open(st.session_state.pdf_path, "rb") as f:
            st.download_button("⬇️ Download PDF Report", f, file_name="patient_report.pdf")

        if st.session_state.clinic_email:
            send_email(
                st.session_state.clinic_email, 
                "Patient Intake Summary", 
                "Attached is the intake summary PDF.", 
                st.session_state.pdf_path
            )
            st.success(f"📧 Email sent to {st.session_state.clinic_email}!")

        st.markdown("### 🔗 Shareable QR Code")
        qr_path = generate_qr("https://your-form-link.com")
        st.image(qr_path, width=150)

        st.markdown("---")
        if st.button("➡️ Start New Form for Next Patient"):
            st.session_state.submitted = False
            st.session_state.summary = ""
            st.session_state.pdf_path = ""
            st.session_state.clinic_email = ""
            st.rerun()


# -------------------------------
# 🔄 Render App
# -------------------------------
if not st.session_state.authenticated:
    login_section()
else:
    form_section()