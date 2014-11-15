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

#Security example:
#access_crm_eto_eto_model,access_crm_eto_eto_model,model_crm_eto_eto_model,,1,1,1,1

class leads(models.Model):
    """Engineered To Order Custom CRM Opportunity Additions
    
    This module adds custom CRM extras specific to the Engineer-To-Order manufacturing company. 
    Project specific information is included regarding the opportunity."""
    _inherit = "crm.lead"
    #Add the new columns to the database table. (These are specifically for 
    #opportunities, but  Opportunities and Leads share the same table.)
    project_code = fields.Char('Project Code', size=7, required=False, help="Six digit code for each project like 'ABC026'")    
    project_name = fields.Char('Project Name', size=128, required=False, help="Typically the customer's name for the product or their name for the machine.")
    machine_rate = fields.Integer('Machine Rate', required=False, help="Number of parts per minute requested by the client.")
    machine_model= fields.Many2one('crm_eto.eto_model', string="Machine Model",required=False, help="Select the most appropriate model")

    #Project Dates:
    proposal_date = fields.Date('Proposal Date', help="Date the [next] proposal is due.")
    concept_date = fields.Date('Concept Date', help="Date the concept drawings are due.")
    animation_date = fields.Date('Animation Date', help="Date the animation file(s) are due.")
    decision_date = fields.Date('Decision Date', help="Date the client anticipates a decision will be made.")
    delivery_date = fields.Date('Delivery Date', help="Date the client anticipates delivery to their facility.")
    
    #Process Details:
    detailed_specs = fields.Boolean('Detailed Specs', 
        help="Detailed specifications are provided.")
    detailed_specs_desc = fields.Text('Detailed Spec Requirements', 
        help="Describe the Detailed Sspec requirements.")
    cad_model = fields.Boolean('CAD Model', help="CAD models are provided.")
    cad_model_desc = fields.Text('CAD Model Details', 
        help="Describe the CAD model requirements.")
    part_drawings = fields.Boolean('Part Drawings', 
        help="Detailed specifications are provided.")
    part_drawings_desc = fields.Text('Part Drawing Requirements', 
        help="Describe the Part Drawing requirements.")
    axial_orientation = fields.Boolean('Vision', 
        help="Detailed specifications are provided.")
    axial_orientation_desc = fields.Text('Vision Details', 
        help="Describe the Detailed Spec requirements.")
    samples = fields.Boolean('Vision', 
        help="Detailed specifications are provided.")
    samples_desc = fields.Text('Vision Details', 
        help="Describe the Detailed Spec requirements.")
    mbu_axis = fields.Boolean('MBU Axis', 
        help="Detailed specifications are provided.")
    mbu_desc = fields.Text('MBU Axis Details', 
        help="Describe the Detailed Spec requirements.")
    silicone = fields.Boolean('Silicone', 
        help="Detailed specifications are provided.")
    silicone_desc = fields.Text('Silicone Requirements', 
        help="Describe the silicone requirements.")
    torque = fields.Boolean('Torque', 
        help="Detailed specifications are provided.")
    torque_desc = fields.Text('Torque Requirements', 
        help="Describe the torque requirements.")
    other_proc = fields.Boolean('Other Process', 
        help="The product requires another type of test.")
    other_proc_desc = fields.Text('Other Process Details', 
        help="Describe the other process.")

    #Quality Control:
    vision = fields.Boolean('Vision', 
        help="The product requires vision inspection.")
    vision_desc = fields.Text('Vision Details', 
        help="Describe the vision inspection requirements.")
    flow_test = fields.Boolean('Flow Test', 
        help="The product requires a flow test.")
    flow_desc = fields.Text('Flow Details', 
        help="Describe the flow test requirements.")
    leak_test = fields.Boolean('Leak Test', 
        help="The product requires a leak test.")
    leak_desc = fields.Text('Leak Details', 
        help="Describe the leak test requirements.")
    prime_test = fields.Boolean('Prime Test', 
        help="The product requires a prime test.")
    prime_desc = fields.Text('Prime Details', 
        help="Describe the prime test requirements.")
    other_test = fields.Boolean('Other Test', 
        help="The product requires another type of test.")
    other_test_desc = fields.Text('Other Test Details', 
        help="Describe the other test requirements.")

    #Machine Specs:
    machine_spec_ids = fields.One2many('crm_eto.machine_spec', 'opportunity_id',
        help="This links the various machine specs to a specific opportunity.")

class machine_spec(models.Model):
    """ Class Summary Description Missing.
   
    Class Details Missing.....
    """
    _name = "crm_eto.machine_spec"
    opportunity_id = fields.Many2one('crm.lead')
    spec=Many2one('crm_eto.spec_type')
    Desc=fields.Text('Specification or Requirement Details')


class spec_type(models.Model):
    type = fields.Selection([
                             ('process','Process Detail'),
                             ('quality','Quality Control')
                             ], readonly=True, required=True, copy=False)
    name = fields.Char('Name of Process or Quality Test', required=True)


class product_model(models.Model):
    """Product model for the potential sale 
    
    Various models of engineer to order products may be available for 
    the sales team to sell. If this is the case, then in the opportunity the 
    salesman can select which model the opportunity is for."""
    _name = "crm_eto.eto_model"
    name = fields.Char('Model', required=True)
    description = fields.Text('Description')
