from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag"
    
    name = fields.Char(required=True)


    def action_estate_property_tag(self):
        return {
            'name': ('Estate Property Tag'),
            'view_mode': 'tree,form',
            'res_model': 'estate.property.tag',
            'type': 'ir.actions.act_window',

        }