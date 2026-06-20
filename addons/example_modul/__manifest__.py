{
    'name': 'Example Module for Beginners',
    'version': '17.0.1.0.0',
    'category': 'Uncategorized',
    'sequence': 1,
    'summary': 'Contoh module untuk pembelajaran pemula Odoo development',
    'description': '''
        Module ini berisi contoh implementasi dasar untuk pembelajaran:
        - Membuat model custom
        - Membuat view (form, tree, search)
        - Membuat action dan menu
        - Implementasi computed fields dan onchange
    ''',
    'author': 'Odoo Developer',
    'website': 'https://example.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'sale',
    ],
    'data': [
        # Security files
        'security/ir.model.access.csv',
        # Data files
        # 'data/example_data.xml',
        # Views
        'views/example_view.xml',
        'views/example_menu.xml',
    ],
    'demo': [
        # 'demo/demo_data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'images': [
        'static/description/icon.png',
    ],
}
