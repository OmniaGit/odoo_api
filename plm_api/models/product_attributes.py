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
from odoo import api, fields, models

class ProductAttribute(models.Model):
    _inherit = 'product.attribute'
    
    api_name = fields.Char("Engine Name")

    def get_api_parameter(self,
                          api_name, 
                          api_data):
        """
            PARAMETER_WIDGET_TYPE = {'EDITCOMBOBOX': 0,
                                     'COMBOBOX': 1,
                                     'TEXT': 2,
                                     'RGB': 3}
            COMBO * Radio
            COMBO * Pills
            COMBO * Select
            
            * Color
            * Multi-checkbox
            * Image
            TEXT is_custom
        """
        #
        tag, \
        valueToDisplay, \
        values, \
        description, \
        help, \
        widgetType = api_data
        display_type = 'select'
        #
        is_custom = False
        if widgetType==0:
            is_custom = True
        elif widgetType==1:
            pass
        elif widgetType==2:
            pass
        elif widgetType==3:
            display_type = 'color'
        #
        p_attribute_id=None
        for p_attribute_id in self.search([('name','=', api_name)]):
            break
        if not p_attribute_id:
            p_attribute_id = self.create({'name': api_name,
                                          'display_type': display_type,
                                          'create_variant': 'no_variant'
                                          })
        pr_at_val_id = self.env['product.attribute.value']
        if not values:
            values=[valueToDisplay]
        for value in values:
            pr_at_val_id.add_api_value(p_attribute_id,
                                       value,
                                       is_custom)
        return p_attribute_id

class ProductAttribute(models.Model):
    _inherit = 'product.attribute.value'
    
    def add_api_value(self,
                      p_attribute_id,
                      value,
                      is_custom):
        value_id = None
        for value_id in self.search([('attribute_id','=',p_attribute_id.id),
                                     ('name','=',value),
                                     ]):
            break
        if not value_id:
            self.create({'attribute_id': p_attribute_id.id,
                         'name': value,
                         'is_custom': is_custom
                })
