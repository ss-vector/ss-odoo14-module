# -*- coding: utf-8 -*-
from odoo import http

class NewModule(http.Controller):
     @http.route('/vm_accounts/vm_accounts/', auth='public')
     def index(self, **kw):
         return "Hello, world"

     @http.route('/vm_accounts/vm_accounts/objects/', auth='public')
     def list(self, **kw):
         return http.request.render('vm_accounts.listing', {
             'root': '/vm_accounts/vm_accounts',
             'objects': http.request.env['vm_accounts.vm_accounts'].search([]),
         })

     @http.route('/vm_accounts/vm_accounts/objects/<model("vm_accounts.vm_accounts"):obj>/', auth='public')
     def object(self, obj, **kw):
         return http.request.render('vm_accounts.object', {
             'object': obj
         })
