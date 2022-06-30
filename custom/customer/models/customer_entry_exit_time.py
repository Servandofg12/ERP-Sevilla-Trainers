from odoo import api, fields, models, exceptions, Command
import datetime
import re
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class CustomerEntryExit(models.Model):
    _name = "customer.entry.exit"
    _description = "Customers timer for the entry and exit for the Sevilla Trainers gym customers."

    #Atributes ------------------------------------------------------------------------------------------------------

    last_entry_time = fields.Datetime()
    last_exit_time = fields.Datetime()


    #Relationship between tables-------------------------------------------------------------------------------------
    customer_id = fields.Many2one("customer.customer", string="Customer")



    #Actions---------------------------------------------------------------------------------------------------------

    def action_date_entry_to_gym(self):
        for record in self:
            print(record.last_entry_time)
            if record.customer_id.registered == False:
                raise exceptions.UserError("She is already unsubscribed.")
            elif record.last_entry_time:
                raise exceptions.UserError("There is already an entry time.")
            else:
                record.last_entry_time = datetime.datetime.now()
        return True

    def action_date_exit_to_gym(self):
        for record in self:
            if record.customer_id.registered == False:
                raise exceptions.UserError("She is already unsubscribed.")
            elif record.last_entry_time == False:
                raise exceptions.UserError("You haven't enter yet.")
            elif record.last_exit_time:
                raise exceptions.UserError("There is already an exit time.")
            else:
                record.last_exit_time = datetime.datetime.now()
        return True

