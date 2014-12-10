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
    scrap_rate = fields.Char('Scrap Rate', size=50, required=False, help="The acceptable scrap rate as defined by the customer at the outset of the project.")

    #Project Dates:
    proposal_date = fields.Date('Proposal Date', help="Date the [next] proposal is due.")
    concept_date = fields.Date('Concept Date', help="Date the concept drawings are due.")
    animation_date = fields.Date('Animation Date', help="Date the animation file(s) are due.")
    decision_date = fields.Date('Decision Date', help="Date the client anticipates a decision will be made.")
    delivery_date = fields.Date('Delivery Date', help="Date the client anticipates delivery to their facility.")
      
    #Machine Specs:
    machine_spec_ids = fields.One2many('crm_eto.machine_spec', 'opportunity_id',
        help="This links the various machine specs to a specific opportunity.")
    
    #With automated lead collection techniques it may be required to validate the legitimacy of the leads:
    lead_validated_by = fields.Char(string='Validated By', default='')
    
    #@api.model
    def action_button_validate_lead(self, cr, uid, ids, context=None):
        """
        Validate a particular Lead, assign the current user to that lead as the validator.
        """
        #print self.env
        #print self.env.user
        #print self.env.user.id
        self.lead_validated_by=uid
        #return self.pool.get('crm.lead').redirect_opportunity_view(cr, uid, opportunity_dict[ids[0]], context)


class machine_spec(models.Model):
    """ Class Summary Description Missing.
   
    Class Details Missing.....
    """
    _name = "crm_eto.machine_spec"
    opportunity_id = fields.Many2one('crm.lead')
    spec_variant=fields.Many2one('crm_eto.spec_variant')
    spec_variant_pq=fields.Selection(string='Type', related='spec_variant.process_or_quality', readonly=True)
    desc=fields.Text('Specification or Requirement Details')


class spec_variant(models.Model):
    """ Individual Machine Specifications.
    
    Each Individual Spec variation for a machine.
    """
    _name = "crm_eto.spec_variant"
    name = fields.Char('Name of Process or Quality Test', required=True)
    
    process_or_quality = fields.Selection([
                             ('process','Process Detail'),
                             ('quality','Quality Control')
                             ], required=True)


class product_model(models.Model):
    """Product model for the potential sale 
    
    Various models of engineer to order products may be available for 
    the sales team to sell. If this is the case, then in the opportunity the 
    salesman can select which model the opportunity is for."""
    _name = "crm_eto.eto_model"
    name = fields.Char('Model', required=True)
    description = fields.Text('Description')
