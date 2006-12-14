# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2004-2006 TINY SPRL. (http://tiny.be) All Rights Reserved.
#
# $Id: account.py 1005 2005-07-25 08:41:42Z nicoe $
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from osv import fields, osv

class hr_timesheet_invoice_factor(osv.osv):
	_name = "hr_timesheet_invoice.factor"
	_description = "Invoice rate"
	_columns = {
		'name': fields.char('Internal name', size=128, required=True),
		'customer_name': fields.char('Visible name', size=128),
		'factor': fields.float('Discount (%)', required=True),
	}
	_defaults = {
		'factor': lambda *a: 0.0,
	}
hr_timesheet_invoice_factor()

class account_analytic_account(osv.osv):
	def _invoiced_calc(self, cr, uid, ids, name, arg, context={}):
		res = {}
		for account in self.browse(cr, uid, ids):
			invoiced = {}
			cr.execute('select distinct l.invoice_id from hr_analytic_timesheet h left join account_analytic_line l on (h.line_id=l.id) where account_id=1', (account.id,))
			invoice_ids = filter(None, map(lambda x: x[0], cr.fetchall()))
			for invoice in self.pool.get('account.invoice').browse(cr, uid, invoice_ids, context):
				res.setdefault(account.id, 0.0)
				res[account.id] += invoice.amount_untaxed
		for id in ids:
			res[id] = round(res.get(id, 0.0),2)
		return res

	_inherit = "account.analytic.account"
	_columns = {
		'pricelist_id' : fields.many2one('product.pricelist', 'Sale Pricelist'),
		'amount_max': fields.float('Max. Invoice Price'),
		'amount_invoiced': fields.function(_invoiced_calc, method=True, string='Invoiced Amount'),
		'to_invoice': fields.many2one('hr_timesheet_invoice.factor','Invoicing'),
		'state': fields.selection([
			('open','Open'),
			('pending','Pending'),
			('close','Close'),
			], 'State', required=True),
	}
	_defaults = {
		'state' : lambda *a : 'open',
	}
account_analytic_account()

class account_analytic_line(osv.osv):
	_inherit = 'account.analytic.line'
	_columns = {
		'invoice_id': fields.many2one('account.invoice', 'Invoice'),
		'to_invoice': fields.many2one('hr_timesheet_invoice.factor', 'Invoicing'),
	}
account_analytic_line()

class account_analytic_line(osv.osv):
	_name = "hr.analytic.timesheet"
	_inherit = "hr.analytic.timesheet"
	def on_change_account_id(self, cr, uid, ids, account_id):
		res = super(account_analytic_line,self).on_change_account_id(cr, uid, ids, account_id)
		if not account_id:
			return res
		res.setdefault('value',{})
		st = self.pool.get('account.analytic.account').browse(cr, uid, account_id).to_invoice.id
		res['value']['to_invoice'] = st or False
		return res
account_analytic_line()

