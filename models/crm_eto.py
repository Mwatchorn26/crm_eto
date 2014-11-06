# -*- coding: utf-8 -*-
##############################################################################
#
#    Transformix Engineering Inc.
#    Copyright (C) 2004-today Transformix Engineering (<http://www.transformix.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import fields, models

#class crm_e2o(models.Model):
#    """Engineered To Order Custom CRM module""" 
#    _name = "crm_e2o.crm_e2o"
#
#    name = fields.Char()

class leads(models.Model):
    """Engineered To Order Custom CRM Opportunity Additions
    
    This module adds custom CRM extras specific to the Engineer-To-Order manufacturing company. 
    Project specific information is included regarding the opportunity."""
    _inherit = "crm.crm_lead"
    #Add the new columns to the database table. (These are specifically for opportunities, but  Opportunities and Leads share the same table.)
    project_code = fields.Char('Project Code', size=7, required=False, help="Six digit code for each project like 'ABC026'")    
    project_name = fields.Char('Project Code Name', size=128, required=False, help="Typically the customer's name for the product or their name for the machine.")
    machine_rate = fields.Integer('Machine Rate', required=False, help="Number of parts per minute requested by the client.")
    machine_model= fields.Selection([
                                       ('l2','Level 2'),
                                       ('l3','Level 3'),
                                       ('l3_polymist','L3 Polymist'),
                                       ('l3_one_and_done','L3 One and Done'),
                                       ('l3_pod_loader','L3 Pod Loader'),
                                       ('l3_loader_and_one','L3 Pod Loader & One and Done'),
                                       ('other','Other'),
                                       ], string='Model', default='l3_one_and_done', readonly=True, required=False, copy=False, help="Select the most appropriate model")
    

    