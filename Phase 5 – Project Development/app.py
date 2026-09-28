import requests
import streamlit as st

from utils.formatters import format_docx, format_pdf, format_html_preview

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="centered"
)

st.markdown("""
<style>
body { background-color: #0e1117; }
.main-title {
    text-align: center;
    font-size: 34px;
    font-weight: 700;
}
.subtitle {
    text-align: center;
    color: #aab2c0;
    margin-bottom: 25px;
}
.preview {
    background: #1e2029;
    border: 1px solid #4b5263;
    border-radius: 12px;
    padding: 22px;
    color: #f1f3f5;
    max-height: 520px;
    overflow-y: auto;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">⚖️ LegalEase</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">AI-Powered Legal Document Generator</div>',
    unsafe_allow_html=True
)

document_type = st.text_input(
    "Document Type",
    placeholder="Example: Freelance Work Contract"
)

parties = st.text_area(
    "Parties Involved",
    placeholder="Example: Jane Doe (Service Provider), TechNova Inc. (Client)"
)

terms = st.text_area(
    "Terms & Conditions",
    placeholder="Separate each clause with a semicolon;\nPayment within 30 days; Confidentiality must be maintained; 15 days notice for termination"
)

dates = st.text_input(
    "Effective Date",
    placeholder="Example: 25/09/2026"
)

if st.button("✨ Generate Document", use_container_width=True):
    if not all([document_type.strip(), parties.strip(), terms.strip(), dates.strip()]):
        st.warning("Please fill in all fields.")
    else:
        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "dates": dates
        }

        try:
            with st.spinner("Generating your legal-document draft..."):
                response = requests.post(
                    f"{API_URL}/generate",
                    json=payload,
                    timeout=120
                )
                response.raise_for_status()
                st.session_state["generated_text"] = response.json()["document"]
                st.success("Document generated successfully.")
        except requests.RequestException as exc:
            st.error(f"Backend connection failed: {exc}")
            st.info("Start the FastAPI backend first: python main.py")

if "generated_text" in st.session_state:
    generated_text = st.session_state["generated_text"]

    st.subheader("Document Preview")
    html = format_html_preview(generated_text)
    st.markdown(f'<div class="preview">{html}</div>', unsafe_allow_html=True)

    st.subheader("✏️ Edit Document")
    edited_text = st.text_area(
        "Edit the generated content below",
        value=generated_text,
        height=400
    )
    st.session_state["generated_text"] = edited_text
    generated_text = edited_text

    st.subheader("Download / Save")

    txt_data = generated_text.encode("utf-8")
    docx_data = format_docx(generated_text, document_type or "Legal Document")
    pdf_data = format_pdf(generated_text, document_type or "Legal Document")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button(
            "📄 Download TXT",
            data=txt_data,
            file_name="LegalEase_Document.txt",
            mime="text/plain",
            use_container_width=True
        )

    with col2:
        st.download_button(
            "📝 Download DOCX",
            data=docx_data,
            file_name="LegalEase_Document.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )

    with col3:
        st.download_button(
            "📕 Download PDF",
            data=pdf_data,
            file_name="LegalEase_Document.pdf",
            mime="application/pdf",
            use_container_width=True
        )

st.caption("LegalEase creates AI-assisted document drafts. Review the content and obtain appropriate professional/legal review before relying on a document.")
