# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution	
#    Copyright (C) 2004-2008 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name" : "Salesman on invoices",
    "version" : "1.0",
    "author" : "Tiny",
    "website" : "http://tinyerp.com",
    "depends" : ["account"],
    "category" : "Generic Modules/Accounting",
    "description": "This module adds a salesman on each invoice.",
    "init_xml" : [],
    "demo_xml" : [ ],
    "update_xml" : [
        "account_invoice_salesman_view.xml",
    ],
    "active": False,
    "installable": True,
    "certificate": "991173474815450893"
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

