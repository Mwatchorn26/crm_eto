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
    machine_rate = fields.Char('Machine Rate (PPM)', required=False, help="Number of parts per minute requested by the client.")
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
                                            ], required=False, string="Reason For Change")
    oppor_other_reason = fields.Char('Other Reason', size=25, help="Enter the reason for the state change")
    booked_revenue = fields.Float('Booked Value', required=False, help="The confirmed value of an opportunity that has been won.")
    price_model = fields.Selection([
                                            ('fixed_price', 'Fixed Price'),
                                            ('t&m','T&M'),
                                            ('budgetary','Budgetary'),
                                            ('other','Other')
                                            ], required=False, string="Cost Model")


    oppor_job_type = fields.Selection([     ('retrofit', 'Retrofit'),
                                            ('budgetary', 'Budgetary'),
                                            ('build_only','Build Only'),
                                            ('design_and_build','Design and Build'),
                                            ('engineering_only','Engineering Only'),
                                            ('other','Other')
                                            ], required=False, string="Job Type")
#    email_status = fields.Selection([
#                                            ('unknown', 'Unknown'),
#                                            ('valid', 'Valid'),
#                                            ('accepted', 'Server Accepted'),
#                                            ('bad_mailbox', 'Bad Mailbox')
#                                            ], required=False, string="Email Status", default='unknown', track_visibility='onchange')


    #Project Dates:
    rfq_date = fields.Date('RFQ Date', help="Date the RFQ was received.")
    proposal_date = fields.Date('Proposal Date', help="Date the [next] proposal is due.")
    concept_date = fields.Date('Concept Date', help="Date the concept drawings are due.")
    animation_date = fields.Date('Animation Date', help="Date the animation file(s) are due.")
    decision_date = fields.Date('Decision Date', help="Date the client anticipates a decision will be made.")
    delivery_date = fields.Date('Delivery Date', help="Date the client anticipates delivery to their facility.")
    rfq_fiscal_yr = fields.Char('RFQ Fiscal Year', size=4, required=False, help="4 digit year (like: '2018')")
    rfq_fiscal_qtr = fields.Selection([('Q1','Q1'),('Q2','Q2'),('Q3','Q3'),('Q4','Q4')],'RFQ Qtr')
    proposal_date = fields.Date('Proposal Date', help="Date the Proposal was submitted.")
    proposal_fiscal_yr = fields.Char('Proposal Fiscal Year', size=4, required=False, help="4 digit year (like: '2018')")
    proposal_fiscal_qtr = fields.Selection([('Q1','Q1'),('Q2','Q2'),('Q3','Q3'),('Q4','Q4')],'Proposal Qtr')
    po_date = fields.Date('PO Date', help="Date the PO was received.")
    po_fiscal_yr = fields.Char('PO Fiscal Year', size=4, required=False, help="4 digit year (like: '2018')")
    po_fiscal_qtr = fields.Selection([('Q1','Q1'),('Q2','Q2'),('Q3','Q3'),('Q4','Q4')],'PO Qtr')
    delivery = fields.Integer('Time to delivery', required=False, help="A calculated time to delivery based on the divery quarter selected")
    delivery_yr = fields.Char('Delivery Year', size=4, required=False, help="4 digit year (like: '2018')")
    delivery_qtr = fields.Selection([('Q1','Q1'),('Q2','Q2'),('Q3','Q3'),('Q4','Q4')],'Delivery Qtr')

    #Machine Specs:

    machine_spec_ids = fields.One2many('crm_eto.machine_spec', 'opportunity_id',
        help="This links the various machine specs to a specific opportunity.")

    component_ids = fields.One2many('crm_eto.product_component', 'opportunity_id',
        help="This links the various parts/components being assembled by this machine.")

    operation_ids = fields.One2many('crm_eto.operation', 'opportunity_id',
        help="This links the various operations and processes required to assemble this machine.")

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

    #Misc fields



    business_type = fields.Selection([('new','New Business'),('existing','Existing Business')])
    prob_of_occurrence = fields.Char(string = "Probability of Occurrence")
    prob_of_our_business = fields.Char(string="Probability it's our business")
    oppor_currency = fields.Char(string="Currency")
    business_unit = fields.Char(string="Business Unit")
    prod_line = fields.Char(string="Product Line")
    prototyping = fields.Char(string="Prototyping")
    proposal_type = fields.Char(string="Proposal Type")
    confidentiality_covers = fields.Char(string="Confidentiality Covers")
    nda = fields.Char(string="NDA")
    num_of_machines = fields.Char(string="Number of machines needed")
    client_budget = fields.Char(string="Client's Budget")
    project_is_funded = fields.Char(string="Project is Funded")
    client_labour_cost = fields.Char(string="Client's Labour Cost")
    payback_required = fields.Char(string="Payback Required")
    new_product = fields.Char(string="New Product")
    process_improvement = fields.Char(string="Improving Existing Process")
    replacing_process = fields.Char(string="Replacing a process")
    automate_manual_process = fields.Char(string="Automating a Manual Process")
    general_machine_specs = fields.Char(string="General Machine Specs")
    detailed_project_specs = fields.Char(string="Detailed Projected Specs")
    product_drawings = fields.Char(string="Product Drawings")
    sample_parts = fields.Char(string="Sample Parts")
    an_prod_vol = fields.Char('Annual Production Volume', required=False, help="(whole number).")
    shifts_per_day = fields.Integer('Usage: Shifts Per Day', required=False, help="(whole number).")
    days_per_week = fields.Integer('Usage: Days Per Week', required=False, help="(whole number).")
    spec_eff = fields.Char('Specified Efficiency', required=False, help="(whole number.")
    spec_oee = fields.Integer('Specified OEE', required=False, help="(whole number).")
    #scrap_rate see above
    power = fields.Char('Power', required=False, help="(whole number).")
    spec_mtbf = fields.Char('Specified MTBF', required=False, help="(whole number).")
    spec_mttr = fields.Char('Specified MTTR', required=False, help="(whole number).")
    spec_cpk = fields.Char(string="Specified CPK")
    max_db = fields.Integer('Max Noise Level', required=False, help="Max DB Level (whole number).")
    integrate_w_other_machines = fields.Char(string="Will the Machine Integrate with Others")
    machine_mobile = fields.Char(string="Will the Machine be Mobile")
    size_or_weight_constraints = fields.Char(string="Size or Weight Constraints")
    climate_controlled = fields.Char(string="Climate Controlled")
    budgeted_eng_hrs = fields.Integer('Budgeted Engineering Hours', required=False, help="(whole number).")
    act_eng_hrs = fields.Integer('Actual Engineering Hours', required=False, help="(whole number).")
    materials_to_avoid = fields.Char(string="Materials to Avoid")
    materials_to_use = fields.Char(string="Materials to Use")

    relative_increment = fields.Selection([('TBD','TBD'),('$','$'),('$$','$$'),('$$$','$$$'),('$$$$','$$$$')], 'Relative Increment')
    engines = fields.Integer('# Engines', required=False, help="Number of Engines use for this machine.")







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

class product_component(models.Model):
    """ A list of componets assembled by the machine.

    The list of components or parts (as named by the customer) that the machine will assemble.
    Usually this list is 2 to 4 items long.
    """
    _name = "crm_eto.product_component"
    opportunity_id = fields.Many2one('crm.lead')
    part=fields.Text('Component or Part')

class operation(models.Model):
    """Operations or Process

    An step in the list of operations and processes required to assemble the components into a finished product.
    Usually this list is 2 to 4 items long.
    """
    _name = "crm_eto.operation"
    opportunity_id = fields.Many2one('crm.lead')
    operation=fields.Text('Operation or Process')

class res_partner_linkedin(models.Model):
    """Adding LinkedIn functionality to all partners (companies and people).
    """
    _inherit="res.partner"
    linkedin_url = fields.Char(string="LinkedIn URL")
