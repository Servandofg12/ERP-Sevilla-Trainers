from odoo import api, fields, models
import datetime
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"
    
    price = fields.Float()
    status = fields.Selection(
        string = 'Status',
        selection=[('accepted', 'Accepted'), ('refused','Refused')],
        help = "Type is used to separate",
        copy=False
    )
    customer_id = fields.Many2one('res.partner', string='Customer', index=True, tracking=10)
    estate_property_id = fields.Many2one("estate.property", string="Property")

    validity = fields.Integer()
    date_deadline = fields.Date(compute="_compute_date", inverse="_inverse_date", default=datetime.date.today())

    @api.depends("validity")
    def _compute_date(self):
        hoy = datetime.date.today()
        for record in self:
            fecha = hoy + relativedelta(days=record.validity)
            record.date_deadline = fecha

    def _inverse_date(self):
        hoy = datetime.date.today()
        for record in self:
            validity = record.date_deadline - hoy
            record.validity = validity.days



    def action_estate_property_offer(self):
        return {
            'name': ('Estate Property Offer'),
            'view_mode': 'tree,form',
            'res_model': 'estate.property.offer',
            'type': 'ir.actions.act_window',

        }