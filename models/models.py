# -*- coding: utf-8 -*-
from odoo import models, fields, api


class VmAccounts(models.Model):
    _name = 'vm.account.control'
    _description = 'Sistema de control de cuentas locales'

    name = fields.Char(string='Nombre de Cuenta', required=True)
    # Select type of account...
    date_created = fields.Date(string="Date Created", default=fields.Date.today())
    acc_type = fields.Selection([
        ('Administrativa', 'Administrativa'),
        ('Cliente', 'Cliente'),
        ('Control', 'Control')
    ], string='Tipo de cuenta', required=False, default='Cliente', help='Configuracion de cuentas')
    acc_owner_id = fields.Many2one('res.partner', string="Titular")
    description = fields.Text(String="Descripción")


@api.depends('ac_incomes')
def _value_pc(self):
    for record in self:
        # @example: create IGV calculator
        record.value2 = float(record.ac_incomes) / 1.18


# operaciones de caja tienda
class store_operations(models.Model):
    _name = "store.operations"
    _description = "Table of operations"

    op_name = fields.Char(string="Operación")
    op_code = fields.Char(string="Código")
    op_id = fields.Many2one('vm_accounts.vm_accounts', string="Operaciones")

# Tabla de Ventas Ferreteria que de el total de ventas por día
# Tabla de cuadre de caja: tabla.saldo.banco y tabla.caja.efectivo