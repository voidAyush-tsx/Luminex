"""
Shivaay AI Structured Extraction & AI Comparison Service
OpenAI-compatible client against Shivaay API endpoint
"""

import os
import base64
import json
from typing import Dict, Any

from openai import OpenAI

from src.services.rate_limiter import SimpleRateLimiter


class ShivaayAIService:
    """High-level wrapper over Shivaay AI for document extraction and AI comparison."""

    def __init__(self) -> None:
        self.client = OpenAI(
            api_key=os.getenv("SHIVAAY_API_KEY"),
            base_url=os.getenv("SHIVAAY_BASE_URL", "https://api.futurixai.com/api/shivaay/v1"),
        )
        self.model = os.getenv("SHIVAAY_MODEL", "shivaay")
        self.rate_limiter = SimpleRateLimiter()

    def encode_image(self, image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def extract_invoice_data(self, file_path: str, document_type: str = "invoice") -> Dict[str, Any]:
        """
        Extract structured data from invoice or purchase order using Shivaay AI.
        Returns normalized JSON including confidence and raw_response.
        """
        if not self.rate_limiter.can_make_request():
            return self._get_empty_extraction_result("Rate limit exceeded. Please try again later.")

        try:
            image_path = file_path
            if file_path.lower().endswith(".pdf"):
                image_path = self._convert_pdf_to_image(file_path)

            base64_image = self.encode_image(image_path)
            system_prompt = self._get_extraction_prompt(document_type)

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Extract all relevant information from this {document_type} document. Return the data in the exact JSON format specified.",
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                            },
                        ],
                    },
                ],
                temperature=0.2,
                max_tokens=1000,
            )

            extracted_text = response.choices[0].message.content
            data = self._parse_extraction_response(extracted_text)
            data["raw_response"] = extracted_text
            data["model_used"] = self.model

            self.rate_limiter.record_request()
            return data

        except Exception as e:
            return self._get_empty_extraction_result(str(e))

    def compare_documents_with_ai(self, invoice_data: Dict[str, Any], po_data: Dict[str, Any]) -> Dict[str, Any]:
        """Use LLM to compare two structured docs and return discrepancy report."""
        try:
            prompt = (
                "You are a financial auditor AI. Compare these two documents and identify discrepancies.\n\n"
                + "INVOICE DATA:\n" + json.dumps(invoice_data, indent=2) + "\n\n"
                + "PURCHASE ORDER DATA:\n" + json.dumps(po_data, indent=2) + "\n\n"
                + "Return ONLY valid JSON with: {\n"
                + "  \"overall_match\": boolean,\n"
                + "  \"confidence_score\": number,\n"
                + "  \"field_comparisons\": [{\n"
                + "    \"field\": string, \"match\": boolean, \"invoice_value\": any, \"po_value\": any, \"difference\": any, \"severity\": string, \"explanation\": string\n"
                + "  }],\n"
                + "  \"critical_issues\": [string],\n"
                + "  \"warnings\": [string],\n"
                + "  \"recommendations\": [string]\n"
                + "}"
            )

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert financial auditor."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.1,
                max_tokens=1500,
            )

            result_text = response.choices[0].message.content
            return json.loads(result_text)
        except Exception:
            return self._fallback_comparison(invoice_data, po_data)

    def _get_extraction_prompt(self, document_type: str) -> str:
        return (
            "You are an expert document analysis AI specializing in financial documents.\n\n"
            f"Your task is to extract structured information from {document_type} documents.\n\n"
            "Return ONLY valid JSON with the following schema (use null for missing fields):\n"
            "{\n"
            "  \"vendor_name\": string|null,\n"
            "  \"total_amount\": number|null,\n"
            "  \"currency\": string|null,\n"
            "  \"date\": string|null,\n"
            "  \"invoice_number\": string|null,\n"
            "  \"quantity\": number|null,\n"
            "  \"unit_price\": number|null,\n"
            "  \"service_description\": string|null,\n"
            "  \"tax_amount\": number|null,\n"
            "  \"subtotal\": number|null,\n"
            "  \"line_items\": [{ \"description\": string, \"quantity\": number, \"unit_price\": number, \"total\": number }],\n"
            "  \"confidence_score\": number,\n"
            "  \"notes\": string|null\n"
            "}\n\n"
            "Rules: Return ONLY JSON; dates in YYYY-MM-DD; numeric-only for amounts."
        )

    def _parse_extraction_response(self, response_text: str) -> Dict[str, Any]:
        try:
            json_start = response_text.find("{")
            json_end = response_text.rfind("}") + 1
            if json_start == -1 or json_end <= json_start:
                raise ValueError("No JSON found in response")
            data = json.loads(response_text[json_start:json_end])
            for key in ["vendor_name", "total_amount", "date", "confidence_score"]:
                if key not in data:
                    data[key] = None
            return data
        except Exception:
            return self._fallback_extraction(response_text)

    def _fallback_extraction(self, text: str) -> Dict[str, Any]:
        return {
            "vendor_name": None,
            "total_amount": None,
            "currency": None,
            "date": None,
            "invoice_number": None,
            "quantity": None,
            "unit_price": None,
            "service_description": None,
            "tax_amount": None,
            "subtotal": None,
            "line_items": [],
            "confidence_score": 0,
            "notes": "Extraction failed; fallback used",
            "error": "Could not parse structured data",
        }

    def _fallback_comparison(self, invoice_data: Dict[str, Any], po_data: Dict[str, Any]) -> Dict[str, Any]:
        comparisons = []
        def _num(v):
            try:
                return float(v) if v is not None else None
            except Exception:
                return None
        fields = [
            ("vendor_name", "Vendor"),
            ("total_amount", "Total"),
            ("date", "Date"),
            ("quantity", "Quantity"),
            ("unit_price", "Unit Price"),
            ("service_description", "Service"),
            ("tax_amount", "Tax"),
        ]
        for key, label in fields:
            inv_val = invoice_data.get(key)
            po_val = po_data.get(key)
            if inv_val is None and po_val is None:
                continue
            match = False
            if key in {"vendor_name", "service_description"}:
                match = str(inv_val).strip().lower() == str(po_val).strip().lower() if inv_val is not None and po_val is not None else False
            elif key in {"total_amount", "quantity", "unit_price", "tax_amount"}:
                a, b = _num(inv_val), _num(po_val)
                match = (a is not None and b is not None and abs(a - b) < 0.01)
            elif key == "date":
                match = str(inv_val).strip() == str(po_val).strip() if inv_val and po_val else False
            comparisons.append({
                "field": label,
                "match": match,
                "invoice_value": inv_val,
                "po_value": po_val,
                "difference": (_num(inv_val) - _num(po_val)) if (key in {"total_amount", "quantity", "unit_price", "tax_amount"} and _num(inv_val) is not None and _num(po_val) is not None) else None,
                "severity": "critical" if (not match and key in {"vendor_name", "total_amount"}) else "medium",
                "explanation": "",
            })
        matches = sum(1 for c in comparisons if c["match"]) if comparisons else 0
        confidence = int((matches / len(comparisons)) * 100) if comparisons else 0
        return {
            "overall_match": confidence > 85,
            "confidence_score": confidence,
            "field_comparisons": comparisons,
            "critical_issues": [c["field"] for c in comparisons if not c["match"] and c["severity"] == "critical"],
            "warnings": [c["field"] for c in comparisons if not c["match"] and c["severity"] != "critical"],
            "recommendations": ["Review highlighted discrepancies", "Verify with vendor if needed"],
        }

    def _convert_pdf_to_image(self, pdf_path: str) -> str:
        from pdf2image import convert_from_path
        import tempfile
        images = convert_from_path(pdf_path, first_page=1, last_page=1)
        temp_path = tempfile.mktemp(suffix=".jpg")
        images[0].save(temp_path, "JPEG")
        return temp_path


