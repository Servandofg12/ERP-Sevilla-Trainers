from odoo import api, fields, models, exceptions, Command
import datetime
import re
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class CustomerMonthlyPayment(models.TransientModel):
    _name = "customer.monthly.payment"
    _description = "To make more than one payment if necessary."

    #Atributes ------------------------------------------------------------------------------------------------------
    
    name = fields.Char(string="Name", required=True)
    customer_id = fields.Many2one("customer.customer", string="Customer")
    amount_months = fields.Integer(string="Amount of Months", required=True)

    #Constraints---------------------------------------------------------------------------------------------------------------------------
    _sql_constraints = [
        ('check_amount_months', 'CHECK(amount_months > 0)', 'The amount of months must be positive and greater than 0.'),
        
    ]


    def action_monthly_payment_2(self):
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        for record in self:
            record.customer_id = self.env["customer.customer"].search([("id", "=", self.env.context.get('active_id'))])

            partner = self.env["res.partner"].search([("name", "=", record.customer_id.user_id.name)], limit=1)

            if(record.customer_id.registered):
                next_payday = record.customer_id.payday + relativedelta(months=record.amount_months)
                record.customer_id.payday = next_payday

                account_move = self.env["account.move"].create(
                    {
                        "name": record.name,
                        "partner_id": partner,
                        "move_type": "out_invoice",
                        "journal_id": journal.id,
                        "customer_id": record.customer_id.id,
                        "invoice_line_ids": 
                            Command.create(
                                {
                                    "name": record.customer_id.name,
                                    "quantity": record.amount_months,
                                    "price_unit": record.customer_id.season_pass_cost,
                                })
                    }
                )
                
                account_move.action_post()#to post it
                account_move.action_register_payment()#to make it paid
                return account_move
            
            else:
                raise UserError("This customer isn't registered.")
        