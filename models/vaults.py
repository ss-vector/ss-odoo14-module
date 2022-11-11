

from odoo import models, fields, api

class CashVault(models.Model):
    _name = 'local.cash.vault'
    _description = 'Bills and coins daily registered'

    b_200 = fields.float(string="200")