import os
from dotenv import load_dotenv

load_dotenv()

class GeminiDocumentGenerator:
    """
    Gemini-powered document generator.
    If GEMINI_API_KEY is not configured, LegalEase uses a local
    template fallback so the project can still be demonstrated.
    """

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
        self.model = None

        if self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(self.model_name)
            except Exception:
                self.model = None

    def generate_document(self, document_type, parties, terms, dates):
        prompt = f"""
You are a legal-document drafting assistant.

Create a structured DRAFT of the requested legal document.
Do not claim that the document is legal advice or guaranteed to be legally valid.
Use clear professional language and include appropriate headings.

Document Type: {document_type}
Parties: {parties}
Terms and Conditions: {terms}
Effective Date: {dates}

Return plain text only with:
1. Title
2. Effective Date
3. Parties
4. Recitals / Purpose
5. Main Terms and Conditions
6. Responsibilities / Obligations
7. Termination, where applicable
8. Confidentiality, where applicable
9. Signatures

Clearly mark placeholders such as [ADDRESS], [AMOUNT], or [NOTICE PERIOD]
when the user has not supplied enough information.
"""

        if self.model is not None:
            response = self.model.generate_content(prompt)
            text = getattr(response, "text", None)
            if text:
                return text.strip()

        return self._local_fallback(document_type, parties, terms, dates)

    def _local_fallback(self, document_type, parties, terms, dates):
        term_items = [t.strip() for t in terms.split(";") if t.strip()]
        bullets = "\n".join(f"{i+1}. {item}" for i, item in enumerate(term_items))

        if not bullets:
            bullets = "1. [Insert agreed terms and conditions]"

        return f"""# {document_type}

## Effective Date
{dates}

## Parties
{parties}

## Purpose
This document records the terms agreed between the parties for the above-mentioned {document_type.lower()}.

## Terms and Conditions
{bullets}

## Responsibilities
Each party shall perform the responsibilities agreed in this document and provide information reasonably required for performance.

## Confidentiality
Where confidential information is exchanged, the parties should maintain its confidentiality subject to the agreed terms and applicable law.

## Termination
Either party may terminate this agreement according to the notice period and conditions agreed by the parties.

## General
Any missing details should be completed before the document is signed.

## Signatures

Party 1: ______________________________
Name: _________________________________
Date: __________________________________

Party 2: ______________________________
Name: _________________________________
Date: __________________________________
"""
