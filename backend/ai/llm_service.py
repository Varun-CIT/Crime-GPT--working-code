import os
import json
import logging
import datetime
import re
from typing import Optional, Dict, Any
from openai import OpenAI
from ai.prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from ai.models import FIRDraft

logger = logging.getLogger(__name__)

def generate_mock_fir(complaint_text: str) -> Dict[str, Any]:
    """
    Generates a realistic, highly contextual mock FIR draft JSON in Demo Mode.
    Upgraded to conform with the new models.
    """
    # Normalize input for search
    text_lower = complaint_text.lower()
    
    # Extract potential amounts
    amounts = re.findall(r"(?:₹|rs\.?|rupees|rs|inr)\s*([\d,]+)", text_lower)
    if not amounts:
        # Fallback regex for pure numbers that look like an amount
        amounts = re.findall(r"\b\d{3,7}\b", text_lower)
        
    amount_str = f"₹{amounts[0]}" if amounts else "₹25,000"
    
    # Extract potential dates
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")
    
    # 1. Scenario: UPI Payment Fraud
    if "upi" in text_lower or "screenshot" in text_lower or "fake payment" in text_lower or "delivering" in text_lower:
        return {
            "fir_number": "Draft/MOCK/2026/101",
            "police_station": "Cyber Crime Cell, City HQ",
            "district": "Chennai",
            "state": "Tamil Nadu",
            "date_of_report": date_str,
            "time_of_report": time_str,
            "mode_of_reporting": "Online",
            "complainant": {
                "name": "Arjun Patel",
                "father_or_spouse_name": "Ramesh Patel",
                "age": "29",
                "gender": "Male",
                "mobile": "9876543210",
                "email": "arjun.patel@example.com",
                "address": "Flat 402, Green Meadows, Chennai",
                "occupation": "E-commerce Merchant"
            },
            "accused": {
                "name": "Unknown Buyer / Suspect",
                "details": "Suspect contacted via WhatsApp using mobile number 9988776655. Sent forged UPI payment screenshot.",
                "phone": "9988776655",
                "email": "Not Provided",
                "weapon": "Social Engineering / Forged Media",
                "vehicle": "Not Provided"
            },
            "incident": {
                "date": date_str,
                "time": time_str,
                "place": "Online Transaction / Complainant's Business",
                "description": "Complainant advertised an item online. Suspect contacted complainant to buy it, sent a forged UPI transaction screenshot claiming payment was successful, and picked up the item. Complainant later realized no amount was credited."
            },
            "property_involved": {
                "amount_lost": amount_str,
                "bank_account": "Not Provided",
                "upi_id": "suspect_buyer@upi",
                "transaction_id": "TXN9876543210 (Fake)",
                "mobile_number": "9988776655",
                "other_details": "Digital goods / Physical product delivered under false payment claims."
            },
            "digital_evidence": [
                "Forged UPI transaction screenshot",
                "WhatsApp chats with suspect",
                "Call history logs"
            ],
            "witnesses": [
                "Not Provided"
            ],
            "crime_category": "UPI Payment Fraud / Forgery",
            "suggested_bns_sections": [
                "Section 318(4) - Cheating",
                "Section 319(2) - Cheating by Personation",
                "Section 336(3) - Forgery"
            ],
            "suggested_bnss_procedure": [
                "Section 173 - Information in Cognizable Cases",
                "Section 106 - Attachment of Property (Freezing of suspected accounts)"
            ],
            "cognizable": True,
            "confidence_score": 0.88,
            "recommended_department": "Cyber Crime Cell",
            "investigation_priority": "Medium",
            "investigation_recommendation": "Liaison with UPI payment gateway to freeze suspect merchant wallet. Track caller CDR locations.",
            "documents_received": [
                "Copy of WhatsApp chat logs",
                "Digital image of fake UPI screenshot",
                "Complainant bank ledger statement"
            ],
            "officer_remarks": "Prima facie case of digital cheating and forgery is established. Request immediate details of UPI handle from the payment provider and call details (CDR) for the suspect's mobile number.",
            "formal_fir_text": f"To,\nThe Officer-in-Charge,\nCyber Police Station,\nChennai, Tamil Nadu\n\nSubject: First Information Report for cyber fraud and forgery of {amount_str} via fake UPI screenshot.\n\nSir/Madam,\n\nI, Arjun Patel, residing at Flat 402, Green Meadows, Chennai, hereby state that I was defrauded of my property valued at {amount_str} by an unknown buyer. The suspect contacted me online and sent a fabricated screenshot indicating successful UPI transfer to my bank. Relying on this, I handed over my product. Later, my bank statement showed no credit of the amount. The suspect's phone is now switched off.\n\nPlease register my complaint as an FIR under relevant sections of Bharatiya Nyaya Sanhita (BNS), 2023, and take immediate action.\n\nYours faithfully,\nArjun Patel"
        }

    # 2. Scenario: Bank Impersonation / OTP Vishing
    elif "otp" in text_lower or "bank" in text_lower or "deducted" in text_lower or "card" in text_lower:
        return {
            "fir_number": "Draft/MOCK/2026/102",
            "police_station": "Cyber Crime Cell, City HQ",
            "district": "Chennai",
            "state": "Tamil Nadu",
            "date_of_report": date_str,
            "time_of_report": time_str,
            "mode_of_reporting": "Online",
            "complainant": {
                "name": "Priya Shah",
                "father_or_spouse_name": "Kiran Shah",
                "age": "34",
                "gender": "Female",
                "mobile": "9812345678",
                "email": "priya.shah@example.com",
                "address": "Apartment 101, Sunnyside Residency, Chennai",
                "occupation": "Corporate Employee"
            },
            "accused": {
                "name": "Unknown Callers / Bank Impersonators",
                "details": "Called using phone number 9001122334, claiming to be bank verification department executives.",
                "phone": "9001122334",
                "email": "Not Provided",
                "weapon": "Social Engineering / Vishing Tool",
                "vehicle": "Not Provided"
            },
            "incident": {
                "date": date_str,
                "time": time_str,
                "place": "Telephonic call received at complainant's house",
                "description": "Complainant received a phone call from suspects posing as bank officials. Suspects claimed complainant's debit card/account was blocked and induced them to share OTP. Upon sharing, an unauthorized debit was executed."
            },
            "property_involved": {
                "amount_lost": amount_str,
                "bank_account": "XXXXXX1234 (Savings Account)",
                "upi_id": "Not Provided",
                "transaction_id": "TXN400912837",
                "mobile_number": "9001122334",
                "other_details": "Funds routed to an unknown beneficiary account."
            },
            "digital_evidence": [
                "Call logs containing phone number 9001122334",
                "OTP SMS screenshot",
                "Debit alert SMS screenshot from bank"
            ],
            "witnesses": [
                "Not Provided"
            ],
            "crime_category": "Vishing / Bank Impersonation Fraud",
            "suggested_bns_sections": [
                "Section 318(4) - Cheating",
                "Section 319(2) - Cheating by Personation"
            ],
            "suggested_bnss_procedure": [
                "Section 173 - Information in Cognizable Cases",
                "Section 106 - Attachment of Property (Fund Freezing request to nodal banks)"
            ],
            "cognizable": True,
            "confidence_score": 0.95,
            "recommended_department": "Cyber Crime Cell",
            "investigation_priority": "High",
            "investigation_recommendation": "Liaison with SBI and payment nodal gateway to freeze beneficiary account SBI XXXXXX9988. Track IMEI and tower location records.",
            "documents_received": [
                "Bank transaction statement",
                "Screenshots of SMS OTP details",
                "Call history logs"
            ],
            "officer_remarks": "Critical bank vishing incident. Liaison with nodal bank officers to block recipient accounts immediately and request KYC details of the suspect mobile number 9001122334.",
            "formal_fir_text": f"To,\nThe Officer-in-Charge,\nCyber Police Station,\nChennai, Tamil Nadu\n\nSubject: First Information Report regarding banking fraud (Vishing) of {amount_str}.\n\nSir/Madam,\n\nI, Priya Shah, aged 34, resident of Chennai, hereby report that an unknown individual impersonated my bank's executive via phone call and tricked me into sharing a OTP code under the guise of reactivating my card. Following this, {amount_str} was debited unauthorizedly from my account.\n\nI request you to register this FIR under BNS, 2023 and IT Act, and investigate immediately to halt the transfer.\n\nYours faithfully,\nPriya Shah"
        }

    # 3. Default General Fallback Scenario (Non-Cognizable Stalking)
    return {
        "fir_number": "Draft/MOCK/2026/103",
        "police_station": "Cyber Crime Cell, HQ",
        "district": "Chennai",
        "state": "Tamil Nadu",
        "date_of_report": date_str,
        "time_of_report": time_str,
        "mode_of_reporting": "Online",
        "complainant": {
            "name": "Shruthi Sen",
            "father_or_spouse_name": "A. Sen",
            "age": "24",
            "gender": "Female",
            "mobile": "9812300011",
            "email": "shruthi@example.com",
            "address": "15, 3rd Cross Street, Chennai",
            "occupation": "Student"
        },
        "accused": {
            "name": "Unknown Instagram Account Owner",
            "details": "Instagram handles: @spammer12, @spammer34",
            "phone": "Not Provided",
            "email": "Not Provided",
            "weapon": "Cyber Harassment / Social Media Platform",
            "vehicle": "Not Provided"
        },
        "incident": {
            "date": date_str,
            "time": time_str,
            "place": "Online / Instagram Social Media",
            "description": "Complainant is subjected to continuous stalking and abusive comments/messages on Instagram from anonymous handles."
        },
        "property_involved": {
            "amount_lost": "₹0 (Non-Financial)",
            "bank_account": "Not Provided",
            "upi_id": "Not Provided",
            "transaction_id": "Not Provided",
            "mobile_number": "Not Provided",
            "other_details": "N/A"
        },
        "digital_evidence": [
            "Screenshots of threat comments",
            "Screenshots of profile messages"
        ],
        "witnesses": [
            "None"
        ],
        "crime_category": "Cyber Bullying / Online Stalking",
        "suggested_bns_sections": [
            "Section 351(2) - Criminal Intimidation",
            "Section 78 - Stalking"
        ],
        "suggested_bnss_procedure": [
            "Section 174 - Information in Non-Cognizable Cases"
        ],
        "cognizable": False,
        "confidence_score": 0.78,
        "recommended_department": "Cyber Crime Cell",
        "investigation_priority": "Low",
        "investigation_recommendation": "File under Non-Cognizable Register. Complainant to obtain Magistrate order to investigate. Issue Section 105 notice to Intermediary (Meta/Instagram) to identify IP creation logs.",
        "documents_received": [
            "Complaint text transcript",
            "Screenshots of messages"
        ],
        "officer_remarks": "Case of online cyber stalking and intimidation. Offense is Non-Cognizable. Reference Magistrate.",
        "formal_fir_text": f"OFFICIAL REPORT OF NON-COGNIZABLE OFFENCE\n(Under Section 174 BNSS, 2023)\n\nTo,\nThe Judicial Magistrate,\nDistrict Court, Chennai\n\nSubject: Report on Non-Cognizable Offence under Sections 78 and 351(2) BNS, 2023.\n\nRespectfully State,\n\nI, Shruthi Sen, report that from anonymous profiles, I am being stalked online..."
    }

def generate_fir_draft(complaint_text: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Core function that calls OpenAI Chat Completions or falls back to local Mock Generator.
    """
    if not api_key:
        logger.info("OpenAI API key is missing. Using local Mock Generator (Demo Mode).")
        return generate_mock_fir(complaint_text)
        
    try:
        logger.info("Initializing OpenAI API client...")
        client = OpenAI(api_key=api_key)
        
        now = datetime.datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M")
        
        user_prompt = USER_PROMPT_TEMPLATE.format(
            complaint_text=complaint_text,
            current_date=current_date,
            current_time=current_time
        )
        
        logger.info("Sending prompt to OpenAI LLM...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content.strip()
        logger.info("Received response from OpenAI LLM.")
        
        # Load and validate JSON structure
        parsed_json = json.loads(content)
        
        # Validate against our Pydantic model to ensure all required fields are present
        validated_fir = FIRDraft(**parsed_json)
        return validated_fir.model_dump()
        
    except Exception as e:
        logger.error(f"Error calling OpenAI API or parsing response: {e}")
        logger.info("Falling back to local Mock Generator (Demo Mode) due to API failure.")
        return generate_mock_fir(complaint_text)
