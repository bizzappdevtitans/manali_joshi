{
    "name": "School Management",
    "version": "1.0",
    "category": "Management/Management",
    "summary": "School Management System",
    "author": "BizzAppDev",
    "description": """
    This module contains all the common features of School Management.
    """,
    "depends": ["mail", "sale", "sale_project","mrp","stock_dropshipping"],
    "data": [
        "data/ir_sequence_data.xml",
        "data/cron.xml",
        "security/ir.model.access.csv",
        "security/school_security.xml",
        "views/students_view.xml",
        "views/school_menu_submenu.xml",
        "views/desc_inherit.xml",
        "wizard/student_wizard_view.xml",
        "wizard/teacher_wizard_view.xml",
    ],
    "license": "LGPL-3",
}
