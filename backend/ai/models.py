from pydantic import BaseModel, Field
from typing import List, Optional

class Complainant(BaseModel):
    name: str = Field(default="Not Provided", description="Name of the victim/complainant")
    father_or_spouse_name: str = Field(default="Not Provided", description="Father's or Spouse's name")
    age: str = Field(default="Not Provided", description="Age of the victim/complainant")
    gender: str = Field(default="Not Provided", description="Gender of the victim/complainant")
    mobile: str = Field(default="Not Provided", description="Mobile number of the victim/complainant")
    email: str = Field(default="Not Provided", description="Email ID of the victim/complainant")
    address: str = Field(default="Not Provided", description="Residential or permanent address of the victim/complainant")
    occupation: str = Field(default="Not Provided", description="Occupation of the victim/complainant")

class Accused(BaseModel):
    name: str = Field(default="Unknown", description="Name of the accused person(s) or 'Unknown'")
    details: str = Field(default="Not Provided", description="Physical features, contact info, IP addresses, or other identification details of the accused")
    vehicle: str = Field(default="Not Provided", description="Details of any vehicle involved (number, color, make)")
    phone: str = Field(default="Not Provided", description="Accused phone number(s) if known")
    email: str = Field(default="Not Provided", description="Accused email(s) if known")
    weapon: str = Field(default="Not Provided", description="Details of any weapon used during the crime")

class Incident(BaseModel):
    date: str = Field(default="Not Provided", description="Date of occurrence of the incident")
    time: str = Field(default="Not Provided", description="Time of occurrence of the incident")
    place: str = Field(default="Not Provided", description="Place of occurrence / location of the incident")
    description: str = Field(default="Not Provided", description="Brief summary describing the circumstances of the incident")

class PropertyInvolved(BaseModel):
    amount_lost: str = Field(default="Not Provided", description="Amount of financial loss in INR")
    bank_account: str = Field(default="Not Provided", description="Bank account number involved in the fraud")
    upi_id: str = Field(default="Not Provided", description="UPI ID involved in the transaction")
    transaction_id: str = Field(default="Not Provided", description="Transaction ID of the fraudulent transaction(s)")
    mobile_number: str = Field(default="Not Provided", description="Mobile number used by the fraudster or linked to the transaction")
    other_details: str = Field(default="Not Provided", description="Any other property details involved (laptops, phones, profiles, etc.)")

class FIRDraft(BaseModel):
    fir_number: str = Field(default="Draft", description="The draft serial or reference number")
    police_station: str = Field(default="Cyber Crime Cell", description="Target police station having jurisdiction")
    district: str = Field(default="Not Provided", description="District")
    state: str = Field(default="Not Provided", description="State")
    
    date_of_report: str = Field(default="", description="Date when complaint is being filed/reported (YYYY-MM-DD)")
    time_of_report: str = Field(default="", description="Time when complaint is being filed/reported (HH:MM)")
    
    mode_of_reporting: str = Field(default="Online", description="Mode of receipt of information (e.g. Online, Written, Oral)")
    
    complainant: Complainant = Field(default_factory=Complainant, description="Details of the informant/complainant")
    accused: Accused = Field(default_factory=Accused, description="Details of the accused suspect(s)")
    
    incident: Incident = Field(default_factory=Incident, description="Incident parameters")
    
    property_involved: PropertyInvolved = Field(default_factory=PropertyInvolved, description="Details of properties/financials stolen/involved")
    
    digital_evidence: List[str] = Field(default_factory=list, description="List of digital evidence (screenshots, URLs, logs, chats)")
    witnesses: List[str] = Field(default_factory=list, description="Witness names or statements, if any")
    
    crime_category: str = Field(default="Cyber Crime", description="Category of cybercrime based on standard government classification")
    
    suggested_bns_sections: List[str] = Field(default_factory=list, description="Suggested sections under Bharatiya Nyaya Sanhita (BNS), 2023")
    suggested_bnss_procedure: List[str] = Field(default_factory=list, description="Applicable procedure sections under Bharatiya Nagarik Suraksha Sanhita (BNSS), 2023")
    
    cognizable: bool = Field(default=True, description="True if the offence is Cognizable (police can arrest without warrant), False otherwise")
    confidence_score: float = Field(default=0.85, description="AI confidence score for the analysis (0.0 to 1.0)")
    
    recommended_department: str = Field(default="Cyber Crime Unit", description="Investigating unit recommended to handle the case")
    investigation_priority: str = Field(default="Medium", description="Priority level of investigation (Low, Medium, High)")
    investigation_recommendation: str = Field(default="Not Provided", description="Suggested actions for the investigating officer")
    
    documents_received: List[str] = Field(default_factory=list, description="Verification documents or annexures attached")
    officer_remarks: str = Field(default="", description="Initial notes/instructions by the receiving officer")
    
    formal_fir_text: str = Field(default="", description="Detailed draft of the FIR in formal legal police language conforming to BNSS 2023 structure")
