from PyQt6.QtGui import QIcon


navi_map = {
    "navi_sms": {
        "page_header": "Costing & SMS Agreements Team",
        "text":"SMS & Costing",
        "icon":QIcon("app_view/icons/sms-costing.svg"),
        "options":["SMS Agreements", "Costing"]
    },
    "nav_cad": {
        "page_header": "Customer Audits & Disputes Team",
        "text":"Customer Disputes",
        "icon":QIcon("app_view/icons/customer-disputes.svg"),
        "options":["Audit History", "Account Assignments"],
    },
    "navi_cir": {
        "page_header": "Customer Incentives & Rebates Team",
        "text":"Customer Incentives",
        "icon":QIcon("app_view/icons/customer-incentives.svg"), 
        "options":["REBA Tracker", "CIR Agreements"],
    },
    "navi_dpm": {
        "page_header": "Deviated Agreements Team",
        "text":"Deviated Agreements",
        "icon":QIcon("app_view/icons/deviated-agreements.svg"),
        "options":["DPM Agreements", "Customer Profile", "Deviation Loads", "Org Chart"],
    },
    "navi_usda": {
        "page_header": "USDA Agreements Team",
        "text":"USDA Agreements",
        "icon":QIcon("app_view/icons/usda.svg"),
        "options":["USDA Agreements", "Bot Tracker"],
    },
    "navi_qa": {
        "page_header": "Quality Assurance Team",
        "text":"Quality Assurance",
        "icon":QIcon("app_view/icons/quality-assurance.svg"),
        "options":["Price Rule Approval", "Quality: Agreement", "Quality: Inquiry", "Quality: Price Rule"],
    }
}

combo_map = {
    "SMS Agreements": {
        "sub_header": "SMS Agreements",
        "table": None
    },
    "Costing": {
        "sub_header": "Costing",
        "table": None
    },
    "Audit History": {
        "sub_header": "Audit History",
        "table": None
    },
    "Account Assignments": {
        "sub_header": "Deviated Account Assignments",
        "table": "cal_account_assignments"
    },
    "REBA Tracker": {
        "sub_header": "REBA Tracker",
        "table": None
    },
    "CIR Agreements": {
        "sub_header": "Agreements",
        "table": None
    },
    "DPM Agreements": {
        "sub_header": "Agreements",
        "table": "cal_programs"
    },
    "Customer Profile": {
        "sub_header": "Customer Profile",
        "table": "cal_customer_profile"
    },
    "Deviation Loads": {
        "sub_header": "Deviation Loads",
        "table": "cal_deviation_loads"
    },
    "Org Chart": {
        "sub_header": "Org Chart",
        "table": "ul_org"
    },
    "USDA Agreements": {
        "sub_header": "Agreements",
        "table": None
    },
    "Bot Tracker": {
        "sub_header": "Bot Tracker",
        "table": None
    },
    "Price Rule Approval": {
        "sub_header": "Price Rule Approval Tracker",
        "table": "pr_master"
    },
    "Quality: Agreement": {
        "sub_header": "Quality Metrics: Agreement Entry",
        "table": "dash_agreement"
    },
    "Quality: Inquiry": {
        "sub_header": "Quality Metrics: Inquiry Timeliness",
        "table": "dash_inquiry"
    },
    "Quality: Price Rule": {
        "sub_header": "Quality Metrics: Price Rule Accuracy",
        "table": "dash_pricerule"
    },
}