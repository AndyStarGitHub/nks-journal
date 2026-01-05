{
    "name": "Specialist Journal",
    "version": "19.0.1.0.0",
    "category": "CRM",
    "summary": "Specialist journal entries on customer card with templates",
    "license": "LGPL-3",
    "author": "Your Name",
    "depends": ["base", "contacts"],
    "data": [
        "security/security.xml",
        "security/rules.xml",
        "security/ir.model.access.csv",
        "views/journal_entry_views.xml",
        "views/journal_template_views.xml",

        "report/report.xml",
        "report/journal_report.xml",

        "views/res_partner_views.xml",
    ],
    "demo": [
    "demo/demo.xml",
    ],
    "application": False,
    "installable": True,
}
