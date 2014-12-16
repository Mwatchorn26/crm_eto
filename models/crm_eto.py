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
    project_code = fields.Char('Project Code', size=20, required=False, help="Six digit code for each project like 'ABC026'")    
    project_name = fields.Char('Project Name', size=128, required=False, help="Typically the customer's name for the product or their name for the machine.")
    machine_rate = fields.Integer('Machine Rate', required=False, help="Number of parts per minute requested by the client.")
    machine_model= fields.Many2one('crm_eto.eto_model', string="Machine Model",required=False, help="Select the most appropriate model")
    scrap_rate = fields.Char('Scrap Rate', size=50, required=False, help="The acceptable scrap rate as defined by the customer at the outset of the project.")
    oppor_change_reason = fields.Selection([
                                            ('concept', 'Concept'),
                                            ('delivery', 'Delivery'),
                                            ('distance','Distance'),
                                            ('lack_of_funding','Lack of Funding'),
                                            ('no_quote','No Quote'),
                                            ('poor_fit','Poor Fit'),
                                            ('price','Price'),
                                            ('re-opened','Re-Opened'),
                                            ('relationship','Relationship'),
                                            ('timing','Timing'),
                                            ('unknown','Unknown'),
                                            ('was_only_budgetary','Was only Budgetary'),
                                            ('other','Other')
                                            ], required=True, string="Reason For Change")
    oppor_other_reason = fields.Char('Other Reason', size=25, help="Enter the reason for the state change")
    price_model = fields.Selection([
                                            ('fixed_price', 'Fixed Price'),                                    
                                            ('t&m','T&M'),
                                            ('other','Other')
                                            ], required=True, string="Cost Model")
    
    
    oppor_job_type = fields.Selection([     ('retrofit', 'Retrofit'),
                                            ('budgetary', 'Budgetary'),
                                            ('build_only','Build Only'),
                                            ('design_and_build','Design and Build'),
                                            ('engineering_only','Engineering Only'),
                                            ('other','Other')
                                            ], required=True, string="Job Type")


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
    lead_validated_by = fields.Many2one('res.users', 'Validated By', select=True, track_visibility='onchange')
    linkedin_url = fields.Char(string="LinkedIn URL")
    email_domain = fields.Char(string="Email Domain")
    company_website = fields.Char(string="Company Website")
    
    def action_button_validate_lead(self, cr, uid, ids, context=None):
        """
        Validate a particular Lead, assign the current user to that lead as the validator.
        """
        #this shouldn't be looped (I don't think?) but this code works,..
        #I'm not sure why I had to revert to V7 API code for this part. (including the function parameters)
        for lead in self.browse(cr, uid, ids, context=context):
            values = {'lead_validated_by': uid}
            self.write(cr, uid, [lead.id], values, context=context)
        return True

class machine_spec(models.Model):
    """ One of one or many specifications required by the customer.
   
    The sales team set specifications for an opportunity. Each spec uses
    a base "spec variant" (like Vision) and allows the salesman to add
    specifics about that opportunity. ("Low res vision part present",...) 
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
