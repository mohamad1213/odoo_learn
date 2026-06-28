from odoo import models, fields

class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Type'
    
    name = fields.Char(required=True)
    description = fields.Text()
    property_ids = fields.One2many(
        'estate.property',
        'property_type_id',
        string='Properties',
    )

