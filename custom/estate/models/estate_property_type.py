from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"
    _order = "name"
    
    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")

    _sql_constraints = [
        ('check_name_uniq', 'UNIQUE(name)', 'The name must be unique.')
    ]

    def action_estate_property_type(self):
        return {
            'name': ('Estate Property Type'),
            'view_mode': 'tree,form',
            'res_model': 'estate.property.type',
            'type': 'ir.actions.act_window',

        }

