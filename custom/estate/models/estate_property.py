from odoo import fields, models
import datetime
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property test"
    
    name = fields.Char(default="Unknown", required=True)
    description = fields.Text("Description")
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=datetime.date.today() + relativedelta(months=3)) 
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string = 'Type garden orientation',
        selection=[('north', 'North'), ('south','South'), ('east','East'), ('west','West')],
        help = "Type is used to separate"
        )
    estate = fields.Selection(
        copy = False,
        required = True,
        default = "new",
        string='Type estate',
        selection=[('new', 'New'), ('offer received','Offer Received,'), ('offer aceppted','Offer Accepted',), ('sold','Sold'), ('canceled', 'Canceled')],
        help = "Type is used to separate"
        )
    
    property_type_id = fields.Many2one("estate.property.type", string="Type")#muchos ESTATE.PROPERTY pueden tener un unico TYPE
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True, default=lambda self: self.env.user, readonly=True)
    partner_id = fields.Many2one('res.partner', string='Customer', index=True, tracking=10)


    def action_estate_property(self):
        return {
            'name': ('Estate Property'),
            'view_mode': 'tree,form',
            'res_model': 'estate.property',
            'type': 'ir.actions.act_window',

        }





