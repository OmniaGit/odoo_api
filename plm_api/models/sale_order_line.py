# -*- coding: utf-8 -*-
##############################################################################
#
#    OmniaSolutions, Your own solutions
#    Copyright (C) 2020 OmniaSolutions (<https://omniasolutions.website>). All Rights Reserved
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
from odoo import _, fields, models, api

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    
    is_api_configurator = fields.Boolean("Is api configurator product",
                                          compute="_is_api_configurator")
    api_configurator_value = fields.Text("Api Configuration data")
    api_node_engine_name = fields.Char(related="product_id.product_tmpl_id.api_engine_id.name")
    
    def _is_api_configurator(self):
        for line in self:
            pt_id = line.product_id.product_tmpl_id
            line.is_api_configurator = pt_id.api_engine_id and pt_id.api_server_id
