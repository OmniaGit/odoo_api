# -*- coding: utf-8 -*-

# Matteo Boscolo
# matteo.boscolo@omniasolutions.eu
# 02.12.2025
import json
import logging
import datetime
#
from odoo.http import request, route
from odoo.tools import float_is_zero
from odoo.http import Controller, route, request, Response


class WebsiteSaleProductConfiguratorController(Controller):
    @route(
        route='/plm_api/product_configurator/create_web_model',
        type='jsonrpc',
        auth='public',
        methods=['POST'],
        website=True,
        readonly=True,
    )
    def plm_api_product_configurator_create_web_model(self, *args, **kwargs):
        start_date = datetime.datetime.now()
        pp_id = request.env['product.product'].search([("id","=",kwargs.get("product_id"))])
        parameters = kwargs.get("parameters")
        ret =  json.loads(pp_id.product_tmpl_id.create_cad_web_model(parameters))
        if 'CAD_RESOUT' in ret:
            odoo_name = ret['CAD_RESOUT'][0][1].split("\\")[-1]
        #
        # commit to go out of this transaction and accept reading the new data from the database
        #
        request.env.cr.commit()
        #
        document = False
        for document in request.env['ir.attachment'].search([('name','=', odoo_name)]):
            break
        if document:
            return {'url' : document.get_url_for_3dWebModel()}
        return {'message': "configuration not generated"}

    @route(
        route='/plm_api/product_configurator/get_indipendent_parameter',
        type='jsonrpc',
        auth='public',
        methods=['POST'],
        website=True,
        readonly=True,
    )
    def plm_api_product_configurator_get_indipendent_parameter(self, *args, **kwargs):
        
        pp_id = request.env['product.product'].search([("id","=",kwargs.get("product_id"))])
        return pp_id.product_tmpl_id.get_indipendent_parameter()
