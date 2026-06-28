from odoo import models, fields

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    title = fields.Char(required=True)
    author = fields.Char(required=True)
    price = fields.Float(required=True)
    published_year = fields.Integer()
    available = fields.Boolean(default=True)
    description = fields.Text()