# -*- coding: utf-8 -*-

from odoo import models, fields, api

# sale_session, cierre_dia, registro_diario

class DailyOperations(models.Model):
	_name = 'local.daily.operations'
	_description = 'Accounts used to store cash realeted to users'

	date = fields.Date(string="Date", required=True, default=fields.Date.today())
	account_id = fields.Many2one('vm.account.control', string='Cuenta')
	operation_desc = fields.Char(size=99, string='Descripción')
	# type of account: cliente, usuario, control
	user_id = fields.Many2one('res.users', string='Responsable')
	acc_incomes = fields.Monetary(string='Ingreso', required=False)
	acc_outcomes = fields.Monetary(string='Egreso', required=False)
	operation_id = fields.Many2one('cash.register.closure', string='Operation Id')
	currency_id = fields.Many2one('res.currency')
	notes = fields.Text(string='Nota')
