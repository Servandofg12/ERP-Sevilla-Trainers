from odoo import api, fields, models, exceptions
import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError


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
    
    #Many2One
    property_type_id = fields.Many2one("estate.property.type", string="Type")#muchos ESTATE.PROPERTY pueden tener un unico TYPE
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True, default=lambda self: self.env.user, readonly=True)
    partner_id = fields.Many2one('res.partner', string='Customer', index=True, tracking=10)

    #Many2Many
    property_tag_ids = fields.Many2many("estate.property.tag", string="Tag")#muchos ESTATE.PROPERTY pueden tener uno o más TAG

    #One2Many
    property_offer_ids = fields.One2many("estate.property.offer", "estate_property_id")

    #Computed fields
    total_area = fields.Float(compute="_compute_total_area")
    best_offer_price = fields.Float(compute="_compute_best_offer_price")

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0)','The expected price must be positive.'),
        ('check_selling_price', 'CHECK(selling_price>=0)', 'The selling price must be postive.'),
    ]


    @api.constrains("selling_price")#the selling price cannot be lower than 90% of the expected price.
    def _check_selling_price(self):
        for record in self:
            offers = record.property_offer_ids
            for offer in offers:
                selling = offer.price
                expected = record.expected_price
                if (selling < 0.9 * expected):
                    raise ValidationError("The selling price must be higher than the 90 percent of the expected price")


    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("property_offer_ids.price")
    def _compute_best_offer_price(self):
        for record in self:
            lista_offer_prices = record.property_offer_ids.mapped('price')
            if len(lista_offer_prices) > 0:
                record.best_offer_price = max(lista_offer_prices)
            else:
                record.best_offer_price = 0

            '''lista_offer = record.property_offer_ids
            best_offer_price = 0
            for element in lista_offer:
                if element.price > best_offer_price:
                    best_offer_price = element.price
            record.best_offer_price = best_offer_price'''

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
            return {'warning': {
                'title': ("Info"),
                'message': ('It would make deafult values for Area and Orientation')}}
        else:
            self.garden_area = 0
            self.garden_orientation = ''
            return {'warning': {
                'title': ("Info"),
                'message': ('It would unset or clear the fields Are and Orientation')}}

    def action_sold_estate(self):
        for record in self:
            if record.estate == "canceled":
                raise exceptions.UserError("Canceled properties can't be sold")
            else:
                record.estate = "sold"
        return True


    def action_cancel_estate(self):
        for record in self:
            if record.estate == "sold":
                raise exceptions.UserError("Sold properties can't be canceled")
            else:
                record.estate = "canceled"
        return True



    def action_estate_property(self):
        return {
            'name': ('Estate Property'),
            'view_mode': 'tree,form',
            'res_model': 'estate.property',
            'type': 'ir.actions.act_window',

        }





