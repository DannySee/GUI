from PyQt6.QtGui import QIcon


map = {
    "btnSMS": {
        "text":"SMS & Costing",
        "icon":QIcon("icons/sms_costing.svg"),
        "tables":{
            "SMS Agreements": "SMS_Agreements",
            "Costing": "Costing"
        }
    },
    "btnCAD": {
        "text":"Customer Disputes",
        "icon":QIcon("icons/customer_disputes.svg"),
        "tables":{
            "Audit History": None,
            "Account Assignments": "CAL_Account_Assignments",
        }
    },
    "btnCIR": {
        "text":"Customer Incentives",
        "icon":QIcon("icons/customer_incentives.svg"), 
        "tables": {
            "REBA Tracker": None,
            "Agreements": None,
        }
    },
    "btnDPM": {
        "text":"Deviated Agreements",
        "icon":QIcon("icons/deviated_agreements.svg"),
        "tables": {
            "DPM Agreements": "CAL_Programs",
            "Customer Profile": "CAL_Customer_Profile",
            "Deviation Loads": "CAL_Deviation_Loads",
            "Account Assignments": "CAL_Account_Assignments",
            "Org Chart": "UL_Org"
        }
    },
    "btnUSDA": {
        "text":"USDA Agreements",
        "icon":QIcon("icons/usda.svg"),
        "tables": {
            "Agreements": None,
            "Bot Tracker": None
        }
    },
    "btnQA": {
        "text":"Quality Assurance",
        "icon":QIcon("icons/quality_assurance.svg"),
        "tables": {
            "Metrics Agreement": "Dash_Agreement",
            "Metrics Inquiry": "Dash_Inquiry",
            "Metrics Price Rule": "Dash_PriceRule",
            "Price Rule Tracker": "PR_Master"
        }
    }
}