from PyQt6.QtGui import QIcon


button_map = {
    "btnSMS": {
        "text":"SMS & Costing",
        "icon":QIcon("icons/sms_costing.svg"),
        "tables":{
            "SMS Agreements": None,
            "Costing": None
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

filter_map = {
    "Metrics Agreement": ['VA_NUM','CA_NUM','SR','PERIOD','WEEK'],
    "Metrics Inquiry": ['ASSOCIATE','TEAM_LEAD','SR','PERIOD','WEEK'],
    "Metrics Price Rule": ['ASSOCIATE','CUSTOMER','NAME','PERIOD','WEEK'],
    "Price Rule Tracker": ['CUSTOMER','CONCEPT','PRICE_RULE','APPROVER','SR'],
    "DPM Agreements": ['CUSTOMER','PROGRAM_DESCRIPTION','T1_USER','T2_USER','T3_USER'],
    "Customer Profile": ['CUSTOMER','ALT_NAME','T1_USER','T2_USER','T3_USER'],
    "Deviation Loads": ['CUSTOMER','PROGRAM','T1_USER','T2_USER','T3_USER'],
    "Account Assignments": ['CUSTOMER','TEAM_LEAD','T1_USER','T2_USER','T3_USER'],
    "Org Chart": ['TEAM_LEAD','ASSOCIATE']
}