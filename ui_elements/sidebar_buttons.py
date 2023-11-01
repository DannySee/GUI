from PyQt6.QtGui import QIcon


map = {
    "btnSMS": {
        "page_label": "Costing & SMS Agreements Team",
        "text":"SMS & Costing",
        "icon":QIcon("ui_elements/icons/sms_costing.svg"),
        "options":["SMS Agreements", "Costing"]
    },
    "btnCAD": {
        "page_label": "Customer Audits & Disputes Team",
        "text":"Customer Disputes",
        "icon":QIcon("ui_elements/icons/customer_disputes.svg"),
        "options":["Audit History", "Account Assignments"],
    },
    "btnCIR": {
        "page_label": "Customer Incentives & Rebates Team",
        "text":"Customer Incentives",
        "icon":QIcon("ui_elements/icons/customer_incentives.svg"), 
        "options":["REBA Tracker", "CIR Agreements"],
    },
    "btnDPM": {
        "page_label": "Deviated Agreements Team",
        "text":"Deviated Agreements",
        "icon":QIcon("ui_elements/icons/deviated_agreements.svg"),
        "options":["DPM Agreements", "Customer Profile", "Deviation Loads", "Org Chart"],
    },
    "btnUSDA": {
        "page_label": "USDA Agreements Team",
        "text":"USDA Agreements",
        "icon":QIcon("ui_elements/icons/usda.svg"),
        "options":["USDA Agreements", "Bot Tracker"],
    },
    "btnQA": {
        "page_label": "Quality Assurance Team",
        "text":"Quality Assurance",
        "icon":QIcon("ui_elements/icons/quality_assurance.svg"),
        "options":["Price Rule Approval", "Quality: Agreement", "Quality: Inquiry", "Quality: Price Rule"],
    }
}