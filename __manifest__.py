# -*- coding: utf-8 -*-

{
    "name": "Arabic Invoice Report",
    "version": "15.0.1.1",
    "summary": "Arabic Invoice Report",
    "author": "Manoj Khadka",
    "category": "Accounting",
    "depends": ["account"],
    "data": [
        "data/report_paperformat.xml",
        "report/account_report.xml",
        "views/invoice_report.xml",
        #"views/custom_report_layout.xml",
        # "views/invoice_view.xml",
        "views/res_company.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
