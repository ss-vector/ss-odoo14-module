# -*- coding: utf-8 -*-
# registro de cierre de caja
from odoo import api, fields, models, SUPERUSER_ID, _

from odoo.tools.misc import formatLang, get_lang


class CashRegisterClosure(models.Model):
    _name = 'cash.register.closure'
    _description = 'Cash register closure'

    # Overriding the create method to assign sequence for the record
    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('account.closure.sequence') or _('New')
        result = super(CashRegisterClosure, self).create(vals)
        return result

    @api.depends('sale_line.price_total')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_base = 0.0
            for line in order.sale_line:
                amount_base += line.price_subtotal
            order.update({
                'amount_total': amount_base,
            })

    closure_date = fields.Date(string='Date', required=True, default=fields.Date.today())

    state = fields.Selection([('draft', 'Borrador'), ('confirm', 'Confirmada'), ('canceled','Cancelada')], string='Status')

    # pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', check_company=True, required=True, readonly=True, help="If you change the pricelist, only newly added lines will be affected.")
    reference = fields.Char(string='Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    notes = fields.Text(string='Notes')
    operation_line = fields.One2many('local.daily.operations', 'operation_id', string='Operaciones')
    sale_line = fields.One2many('daily.sale.lines', 'order_id', string='Local Sales', copy=True, auto_join=True)
    currency_id = fields.Many2one('res.currency')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all', tracking=4)


class SaleOrderLines(models.Model):
    _name = 'daily.sale.lines'
    _description = 'Model for sale_line field'

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id )
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

    order_id = fields.Many2one('cash.register.closure', string='Daily Sales')
    name = fields.Char(string='Description')

    product_id = fields.Many2one('product.product', string='Producto', change_default=True, ondelete='restrict')
    # Impuestos
    tax_id = fields.Many2many('account.tax', string='Taxes', domain=['|', ('active', '=', False), ('active', '=', True)])

    discount = fields.Float(string='Discount (%)', digits='Discount', default=0.0)

    price_unit = fields.Float('Unit Price', required=True, digits='Product Price', default=0.0)
    product_uom_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True, default=1.0)
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]")

    currency_id = fields.Many2one('res.currency')
    price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', readonly=True, store=True)
    price_total = fields.Monetary(compute='_compute_amount', string='Total', readonly=True, store=True)
    price_tax = fields.Float(compute='_compute_amount', string='Total Tax', readonly=True, store=True)

    def get_product_name(self, product):
        """ Compute an automatic description for the selected product...

        """
        return product.get_product_multiline_description_sale()

    @api.onchange('product_id')
    def product_id_change(self):
        vals = {}

        product = self.product_id.with_context(
            quantity=vals.get('product_uom_qty') or self.product_uom_qty,
            date=self.order_id.closure_date,
           # pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id

        )

        vals.update(name=self.get_product_name(product))

        self.update(vals)