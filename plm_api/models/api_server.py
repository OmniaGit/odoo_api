# -*- coding: utf-8 -*-
##############################################################################
#
#    OmniaSoluproducttions, Your own solutions
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
import json
import xmlrpc.client
from odoo import api, fields, models

class NodeEngine(models.Model):
    _name = "api.nodeengine"
    _description = "api node"

    name = fields.Char("Name")

class ApiServer(models.Model):
    _name = "api.server"
    _description = "Api server configuration"

    schema = fields.Selection(string="Schema",
                              selection= [('http', 'Insicure'),
                                         ('https', 'Secure')],
                              default="http")
    name = fields.Char("Url", help="es: localhost", default="localhost", required=True)
    port = fields.Char("Port", help="es: 8000", default="8000", required=True)
    user = fields.Char("User", help="es: administrator", default="administrator", required=True)
    password = fields.Char("Password", help="es: administrator", default="administrator", required=True)
    connection_string = fields.Char("Connection String", compute="_compute_connection_string")
    
    @api.depends("schema",
             "name",
             "port",
             "user",
             "password",
             )
    def _compute_connection_string(self):
        for api_id in self:
            api_id.connection_string = f"{api_id.schema}://{api_id.user}:{api_id.password}@{api_id.name}:{api_id.port}"
    
    @property
    def connection(self):
        return xmlrpc.client.ServerProxy(self.connection_string,
                                         use_builtin_types=True)

    def check_connection(self):
        tile = "Info"
        message = "Unable to connect !!"
        try:
            if self.connection.serverIsUp():
                message = "Connection to the api server done !"
        except Exception as ex:
            logging.error(ex)
            tile = "Error"
            message = f"Unable to connect to the api server {ex}"
        return { 
                'type' : 'ir.actions.client' , 
                'tag' : 'display_notification' , 
                'params' : { 
                            'title' : title , 
                            'message' : message , 
                            'type' : 'warning' , 
                            'sticky' : True, 
                            } , 
                }
    
    def get_indipendent_parameter(self, engine_name):
        return json.loads(self.connection.getIndependentParametersFromNodeName(engine_name))
        
    def fill_up_node_engine(self):
        nodeengine = self.env['api.nodeengine']
        available_node = nodeengine.search([]).mapped("name")
        
        for data in self.connection.queryForQuery("",
                                                  ["NODEENGINE"],
                                                  False,
                                                  False,
                                                  False):
            name = data[0]
            if name not in available_node:
                nodeengine.sudo().create({'name':name})

    def get_configuration_object(self,
                                 engine_name,
                                 param_dict):
        """
        get the configutation object from the api server
        :engine_name Name of the engine to call
        :param_dict Dictionary of the parameters to use to make the configuration
        :return: the configured qpi object
        """
        ret = self.connection.computeCadConfiguration(engine_name,
                                                      json.dumps(param_dict),
                                                      json.dumps({'mode': 'run',
                                                                  'compute_cad': False}),  
                                                      True # plm_compute
                                          )
        ret = json.loads(ret)
        if ret.get('ERROR_STACK'):
            raise UserWarning(ret.get('ERROR_STACK'))
        bom_structure = ret.get('BOM_STRUCTURE')
        
        for obj_name, attributes in bom_structure.items():
            return apiRObject(obj_name, attributes)
        raise Exception(f"no bom structure available for node {engine_name}")

    def create_configuration(self,
                             root_product_template,
                             engine_name,
                             param_dict,
                             combination):
        """
        create the configutation from the api server
        :root_product_template root product template
        :engine_name Name of the engine to call
        :param_dict Dictionary of the parameters to use to make the configuration
        :return: the configured product
        """
        api_conf_object = self.get_configuration_object(engine_name, parma_dict)
        return api_conf_object.get_odoo_product_structure(root_product_template,
                                                   combination)

    def create_cad_web_model(self,
                             engine_name,
                             parameters):
        return self.connection.computeCadConfiguration(engine_name,
                                                       json.dumps(parameters),
                                                       json.dumps({'mode': 'run',
                                                                   'localServerName': 'LocalServerOn_Omnia',
                                                                   'alternative_format': '3mf',
                                                                   'compute_cad': True}),  
                                                       True # plm_compute
                                                       )

class apiRObject(object):
    def __init__(self, obj_name, attributes):
        self.NODE_NAME = obj_name
        self.PARAMETER_VALUES = attributes[0]      # out_function,
        self.ATTRIBUTES = attributes[1]            # out_attributes,
        self.PARAMETER_VALUES =  attributes[2]     # out_checkers,
        self.EDITOR_OBJECTS = attributes[3]        # out_referenceDocuments,
        # self.CHILDREN = attributes[4]              # out_children,
                    #                    attributes[5],     # out_function_path,
                    #                    attributes[6],     # out_checkers_path
                    #
        self.OPTIONS= attributes[8]
        #
        self._children = []
        #
        for child_obj_name, child_attributes in attributes[4].items():
            aro = apiRObject(child_obj_name, child_attributes)
            self.add_children(aro)

    @property
    def engineering_code(self):
        return self.ATTRIBUTES.get("ID",'no-code')

    def get_attribute(self, attribute_name):
        """
        get the attribute that belongs to the product
        :attribute_name name of the attribute that i wold like to have the value
        :return: the attribute value
        """
        return self.ATTRIBUTES.get(attribute_name,f"no_attribute_found {attribute_name}")

    def get_all_level_summarized(self, 
                                 attribute_qty, 
                                 attribute_name):
        """
        :attribute_qty is the define quantity attributes defined for api that must belong to the relation
        :attribute_name is the attribute that we whant to summarize
        :return: the value
        
        """
        #TODO: Perform the computation
        import random
        return  random.randrange(1,1000000)/100.0


    def add_children(self, api_resut_object):
        self._children.append(api_resut_object)

    def get_odoo_product_structure(self, 
                                   product_template_id,
                                   combination):
        odoo_env = product_template_id.env
        product_varinat_id = False
        search_combination = combination._ids2str()
        for pp_id in product_template_id.product_variant_ids:
            if pp_id.product_template_attribute_value_ids._ids2str()==search_combination:
                product_varinat_id = pp_id
                break
        if not product_varinat_id:
            variant_vals = product_template_id._prepare_variant_values(combination)
            product_varinat_id = odoo_env['product.product'].create(variant_vals)
        #
        children_products = []
        for child in self._children:
            children_products.append(child.create_product(odoo_env))
        #
        self.create_bom(product_template_id,
                        product_varinat_id, 
                        children_products,
                        odoo_env)
        return product_template_id
    
    def create_bom(self,
                   parent_tmpl_id,
                   product_varinat_id,
                   children_tmpl_id, 
                   odoo_env):
        bom_id = False
        for bom_id in parent_tmpl_id.bom_ids:
            break
        if not bom_id:
            bom_id =  odoo_env['mrp.bom'].create({'product_tmpl_id':parent_tmpl_id.id,
                                                  'product_id': product_varinat_id.id})
        for child_tmpl_id in children_tmpl_id:
            odoo_env['mrp.bom.line'].create({
                'bom_id':bom_id.id,
                'product_id': child_tmpl_id.product_variant_id.id,
                'product_uom_id':child_tmpl_id.uom_id.id, 
                'product_qty': 1 # this value must came from the relation attributes
                })
        
        
    def _get_default_value(self):
        out =   {
                'name':name,
                'engineering_code': self.engineering_code
                }
        for attribute in self.ATTRIBUTES:
            pass
        return out

    def create_product(self, odoo_env):
        product_template_id = odoo_env['product.template'].get_last_version(self.engineering_code)
        if not product_template_id:
            product_template_id = odoo_env['product.template'].create(self._get_default_value(self.engineering_code))
        return product_template_id


