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
# Matteo Boscolo
# matteo.boscolo@omniasolutions.eu
# 29.09.2026

from odoo import fields, models


class IrAttachment(models.Model):
    """
    The API configurator writes the id of a configured item (API_ID) into the
    document made for it, and finds that document again by it: the Odoo
    backend of DbWrapper (document_for_configuration) searches this field,
    its api_id_field default. A new revision keeps it, so the search finds
    the newest revision of the configured item's document.
    """
    _inherit = "ir.attachment"

    api_id = fields.Char("API Configuration Id",
                         index=True,
                         help="Id of the API configuration this document was made for")
