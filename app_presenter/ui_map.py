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
        "options":["DPM Agreements", "Customer Profile", "Deviation Loads", "Account Assignments", "DPM Org"],
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
        "table": None,
        "date": [],
        "hidden": [0]
    },
    "Costing": {
        "sub_header": "Costing",
        "table": None,
        "date": [],
        "hidden": [0]
    },
    "Audit History": {
        "sub_header": "Audit History",
        "table": None,
        "date": [],
        "hidden": [0]
    },
    "Account Assignments": {
        "sub_header": "Deviated Account Assignments",
        "table": "cal_account_assignments",
        "date": [],
        "hidden": [0,18,19,20,21,22]
    },
    "REBA Tracker": {
        "sub_header": "REBA Tracker",
        "table": None,
        "date": [],
        "hidden": [0]
    },
    "CIR Agreements": {
        "sub_header": "Agreements",
        "table": None,
        "date": [],
        "hidden": [0]
    },
    "DPM Agreements": {
        "sub_header": "Agreements",
        "table": "cal_programs",
        "date": [4,5],
        "hidden": [0]
    },
    "Customer Profile": {
        "sub_header": "Customer Profile",
        "table": "cal_customer_profile", 
        "date": [],
        "hidden": [0]
    },
    "Deviation Loads": {
        "sub_header": "Deviation Loads",
        "table": "cal_deviation_loads",
        "date": [],
        "hidden": [0]
    },
    "DPM Org": {
        "sub_header": "Team Org",
        "table": "team_org",
        "date": [],
        "hidden": [0]
    },
    "USDA Agreements": {
        "sub_header": "Agreements",
        "table": None,
        "date": [],
        "hidden": [0]
    },
    "Bot Tracker": {
        "sub_header": "Bot Tracker",
        "table": None,
        "date": [],
        "hidden": [0]
    },
    # STOPPED HERE - PICK BACK UP ON OPTIONS DROPDOWNS. ######################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    "Price Rule Approval": {
        "sub_header": "Price Rule Approval Tracker",
        "table": "pr_master",
        "options": {
            5: "APPROVER",
            6: "APP_STATUS",
            9: "AUDIT_FLAG",
            18: "SALES_POSTED_OT",
            21: "APP_BASE",
            23: "PTF",
            24: "DPM_ASS",
            28: "MOD_TYPE",
            29: "PRN_ATTACHED",
            30: "MTRCS_SUBMIT",
            31: "MTRCS_NOTES",
            32: "MTRCS_SPLITS",
            33: "MTRCS_BASE",
            34: "MTRCS_FREQ",
            35: "MTRCS_UPCH",
            36: "MTRCS_AUDIT_N",
            37: "MTRCS_ITM",
            38: "MTRCS_BACKUP",
            39: "MTRCS_DOWNLOAD",
            40: "MTRCS_POSTED",
            41: "MTRCS_GRADE"
        },
        "date": [8,16,25,26],
        "hidden": [0,1,2]
    },
    "Quality: Agreement": {
        "sub_header": "Quality Metrics: Agreement Entry",
        "table": "dash_agreement",
        "options": {
            4: "ASSOCIATE",
            5: "TEAM_LEAD",
            6: "TEAM",
            7: "NOTES",
            10: "ERROR"
        },
        "hidden": [0,14,15,16,17]
    },
    "Quality: Inquiry": {
        "sub_header": "Quality Metrics: Inquiry Timeliness",
        "table": "dash_inquiry",
        "options": {
            1: "ASSOCIATE",
            2: "TEAM_LEAD",
            4: "TYPE"
        },
        "date": [5,6],
        "hidden": [0,11,12,13]
    },
    "Quality: Price Rule": { 
        "sub_header": "Quality Metrics: Price Rule Accuracy",
        "table": "dash_pricerule",
        "hidden": [0]
    },
}