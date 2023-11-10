from PyQt6.QtGui import QIcon


navi_map = {
    "navi_sms": {
        "page_label": "Costing & SMS Agreements Team",
        "text":"SMS & Costing",
        "icon":QIcon("app_view/icons/sms-costing.svg"),
        "options":["SMS Agreements", "Costing"]
    },
    "nav_cad": {
        "page_label": "Customer Audits & Disputes Team",
        "text":"Customer Disputes",
        "icon":QIcon("app_view/icons/customer-disputes.svg"),
        "options":["Audit History", "Account Assignments"],
    },
    "navi_cir": {
        "page_label": "Customer Incentives & Rebates Team",
        "text":"Customer Incentives",
        "icon":QIcon("app_view/icons/customer-incentives.svg"), 
        "options":["REBA Tracker", "CIR Agreements"],
    },
    "navi_dpm": {
        "page_label": "Deviated Agreements Team",
        "text":"Deviated Agreements",
        "icon":QIcon("app_view/icons/deviated-agreements.svg"),
        "options":["DPM Agreements", "Customer Profile", "Deviation Loads", "Org Chart"],
    },
    "navi_usda": {
        "page_label": "USDA Agreements Team",
        "text":"USDA Agreements",
        "icon":QIcon("app_view/icons/usda.svg"),
        "options":["USDA Agreements", "Bot Tracker"],
    },
    "navi_qa": {
        "page_label": "Quality Assurance Team",
        "text":"Quality Assurance",
        "icon":QIcon("app_view/icons/quality-assurance.svg"),
        "options":["Price Rule Approval", "Quality: Agreement", "Quality: Inquiry", "Quality: Price Rule"],
    }
}

combo_map = {
    "SMS Agreements": {
        "sub_label": "SMS Agreements",
        "table": None
    },
    "Costing": {
        "sub_label": "Costing",
        "table": None
    },
    "Audit History": {
        "sub_label": "Audit History",
        "table": None
    },
    "Account Assignments": {
        "sub_label": "Deviated Account Assignments",
        "table": "cal_account_assignments"
    },
    "REBA Tracker": {
        "sub_label": "REBA Tracker",
        "table": None
    },
    "CIR Agreements": {
        "sub_label": "Agreements",
        "table": None
    },
    "DPM Agreements": {
        "sub_label": "Agreements",
        "table": "cal_programs"
    },
    "Customer Profile": {
        "sub_label": "Customer Profile",
        "table": "cal_customer_profile"
    },
    "Deviation Loads": {
        "sub_label": "Deviation Loads",
        "table": "cal_deviation_loads"
    },
    "Org Chart": {
        "sub_label": "Org Chart",
        "table": "ul_org"
    },
    "USDA Agreements": {
        "sub_label": "Agreements",
        "table": None
    },
    "Bot Tracker": {
        "sub_label": "Bot Tracker",
        "table": None
    },
    "Price Rule Approval": {
        "sub_label": "Price Rule Approval Tracker",
        "table": "pr_master"
    },
    "Quality: Agreement": {
        "sub_label": "Quality Metrics: Agreement Entry",
        "table": "dash_agreement"
    },
    "Quality: Inquiry": {
        "sub_label": "Quality Metrics: Inquiry Timeliness",
        "table": "dash_inquiry"
    },
    "Quality: Price Rule": {
        "sub_label": "Quality Metrics: Price Rule Accuracy",
        "table": "dash_pricerule"
    },
}