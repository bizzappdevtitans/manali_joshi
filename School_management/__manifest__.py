{
    "name": "School Management",
    "version": "1.0",
    "category": "Management/Management",
    "summary": "School Management System",
    "author": "Manali Joshi",
    "description": """
    This module contains all the common features of School Management.
    """,
    "depends": ["mail", "sale"],
    "data": [
        "data/ir_sequence_data.xml",
        "security/ir.model.access.csv",
        "views/students_view.xml",
        "views/school_menu_submenu.xml",
        "views/desc_inherit.xml",
    ],
    "license": "LGPL-3",
}
