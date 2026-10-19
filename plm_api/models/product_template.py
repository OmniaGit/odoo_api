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

class ProductProduct(models.Model):
    _inherit = "product.product"
    
    def action_fill_up_engines(self):
        for pp_id in self:
            pp_id.product_tmpl_id.action_fill_up_engines()

    def action_recover_engine_attributes(self):
        for pp_id in self:
            pp_id.product_tmpl_id.action_recover_engine_attributes()


class ProductTemplate(models.Model):
    _inherit = "product.template"

    api_engine_id = fields.Many2one("api.nodeengine", "Engine Name")
    api_server_id = fields.Many2one("api.server", "Server api di riferimento")
    
    def action_fill_up_engines(self):
        for pt_id in self:
            pt_id.api_server_id.fill_up_node_engine()
            
        
    def action_recover_engine_attributes(self):
        product_attribute = self.env['product.attribute']
        #
        for pt_id in self:
            if pt_id.api_engine_id and pt_id.api_server_id:
                for param_name, param_data in pt_id.api_server_id.get_indipendent_parameter(pt_id.api_engine_id.name).items():
                    product_attribute_id = product_attribute.get_api_parameter(param_name,
                                                                               param_data)
                    
                    create=True
                    for _ in self.env['product.template.attribute.line'].search([('product_tmpl_id','=', pt_id.id),
                                                                                  ('attribute_id','=', product_attribute_id.id)]):
                        create = False
                    if create:
                        self.env['product.template.attribute.line'].create({'product_tmpl_id': pt_id.id,
                                                                            'value_ids':[(6, 0, product_attribute_id.value_ids.ids)],
                                                                            'attribute_id': product_attribute_id.id})

    def api_configuration_product(self, combination):
        values = combination.mapped("name")
        param_names = combination.mapped("attribute_id.name")
        return self.api_server_id.create_configuration(self,
                                                       self.api_engine_id.name,
                                                       dict(zip(param_names,values)),
                                                       combination)

    def api_compute_update(self, 
                           combination):
        values = combination.mapped("name")
        param_names = combination.mapped("attribute_id.name")
        api_conf_object = self.api_server_id.get_configuration_object(self.api_engine_id.name,
                                                                      dict(zip(param_names,values)))
        #value shuld be like {'id': 251, 'description_sale': False, 'display_name': 'test ', 'price': 11.0}
        return {'id': self.id, 
                'description_sale': api_conf_object.get_attribute('name'), 
                'display_name': api_conf_object.get_attribute('name'), 
                'price': api_conf_object.get_all_level_summarized('qty',
                                                                  'price')}
    def get_indipendent_parameter(self):
        """
        get node related indipendent parameters
        """
        return self.api_server_id.get_indipendent_parameter(self.api_engine_id.name)

    def create_cad_web_model(self, parameters):
        """
        get node related indipendent parameters
        """
        return self.api_server_id.create_cad_web_model(self.api_engine_id.name,
                                                       parameters)
    
    def make_configuration(self, parameters):
        api_conf_object = self.api_server_id.get_configuration_object(self.api_engine_id.name,
                                                                      parameters)
        return {'id': self.id, 
                'description_sale': api_conf_object.get_attribute('name'), 
                'display_name': api_conf_object.get_attribute('name'), 
                'price': api_conf_object.get_all_level_summarized('qty',
                                                                  'price')}
        return self.api_server_id.create_cad_web_model(self.api_engine_id.name,
                                                       parameters)

        