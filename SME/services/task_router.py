def detect_task(message: str):
    msg = message.lower()

    if "offer" in msg:
        return "Offer Letter", "offer_letter.docx", "HR"
    elif "appointment" in msg:
        return "Appointment Letter", "appointment_letter.docx", "HR"
    elif "invoice" in msg:
        return "Invoice", "invoice.docx", "Admin"
    elif "nda" in msg or "non disclosure" in msg:
        return "NDA", "nda.docx", "Admin"
    else:
        return None, None, None
