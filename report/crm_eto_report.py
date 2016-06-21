# -*- coding: utf-8 -*-
##############################################################################
#
#    Transformix Engineering Inc.
#    Copyright (C) 2016-today Transformix Engineering (<http://www.transformix.com>)
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

class crm_opportunity_report(osv.Model):
    """ CRM Opportunity Analysis """
    name = "crm.opportunity.report"
    _rec_name = 'date_deadline'
    _inherit = ["crm.opportunity.report"]

    project_code = fields.Char('Project Code',readonly=True )
    project_name = fields.Char('Project Name',readonly=True )
    machine_rate = fields.Char('Machine Rate (PPM)',readonly=True )
    scrap_rate = fields.Char('Scrap Rate',readonly=True )
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
                                            ], string="Reason For Change",readonly=True)
    oppor_other_reason = fields.Char('Other Reason',readonly=True)
    booked_revenue = fields.Float('Booked Value',digits=(16,2),readonly=True, group_operator="avg")
    price_model = fields.Selection([
                                         ('fixed_price', 'Fixed Price'),
                                            ('t&m','T&M'),
                                            ('budgetary','Budgetary'),
                                            ('other','Other')
                                            ], string="Cost Model",readonly=True)

    oppor_job_type = fields.Selection([     ('retrofit', 'Retrofit'),
                                            ('budgetary', 'Budgetary'),
                                            ('build_only','Build Only'),
                                            ('design_and_build','Design and Build'),
                                            ('engineering_only','Engineering Only'),
                                            ('other','Other')
                                            ], string="Job Type",readonly=True)

    rfq_date = fields.Date('RFQ Date',readonly=True)
    concept_date = fields.Date('Concept Date',readonly=True)
    animation_date = fields.Date('Animation Date',readonly=True)
    decision_date = fields.Date('Decision Date',readonly=True)
    delivery_date = fields.Date('Delivery Date',readonly=True)
    rfq_fiscal_yr = fields.Char('RFQ Fiscal Year',readonly=True)
    rfq_fiscal_qtr = fields.Selection([('Q1','Q1'),('Q2','Q2'),('Q3','Q3'),('Q4','Q4')],'RFQ Qtr',readonly=True)
    proposal_date = fields.Date('Proposal Date',readonly=True)
    proposal_fiscal_yr = fields.Char('Proposal Fiscal Year',readonly=True)
    proposal_fiscal_qtr = fields.Selection([('Q1','Q1'),('Q2','Q2'),('Q3','Q3'),('Q4','Q4')],'Proposal Qtr',readonly=True)
    po_date = fields.Date('PO Date',readonly=True)
    po_fiscal_yr = fields.Char('PO Fiscal Year',readonly=True)
    po_fiscal_qtr = fields.Selection([('Q1','Q1'),('Q2','Q2'),('Q3','Q3'),('Q4','Q4')],'PO Qtr',readonly=True)
    delivery = fields.Integer('Time to delivery',readonly=True)
    delivery_yr = fields.Char('Delivery Year',readonly=True )
    delivery_qtr = fields.Selection([('Q1','Q1'),('Q2','Q2'),('Q3','Q3'),('Q4','Q4')],'Delivery Qtr',readonly=True)
    }

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'crm_opportunity_report')
        cr.execute("""
 CREATE OR REPLACE VIEW crm_opportunity_report AS (
                SELECT
                    id,
                    c.date_deadline,
                    count(id) as nbr_cases,

                    c.date_open as opening_date,
                    c.date_closed as date_closed,

                    c.date_last_stage_update as date_last_stage_update,

                    c.user_id,
                    c.probability,
                    c.stage_id,
                    c.type,
                    c.company_id,
                    c.priority,
                    c.section_id,
                    c.campaign_id,
                    c.source_id,
                    c.medium_id,
                    c.partner_id,
                    c.country_id,
                    c.planned_revenue as total_revenue,
                    c.planned_revenue*(c.probability/100) as expected_revenue,
                    c.create_date as create_date,
                    extract('epoch' from (c.date_closed-c.create_date))/(3600*24) as  delay_close,
                    abs(extract('epoch' from (c.date_deadline - c.date_closed))/(3600*24)) as  delay_expected,
                    extract('epoch' from (c.date_open-c.create_date))/(3600*24) as  delay_open
                    
                    c.project_code,
                    c.project_name,
                    c.machine_rate,
                    c.scrap_rate,
                    c.oppor_change_reason,
                    c.oppor_other_reason,
                    c.booked_revenue,
                    c.price_model,
                    c.oppor_job_type,
                    c.rfq_date,
                    c.concept_date,
                    c.animation_date,
                    c.decision_date,
                    c.delivery_date,
                    c.rfq_fiscal_yr,
                    c.rfq_fiscal_qtr,
                    c.proposal_date,
                    c.proposal_fiscal_yr,
                    c.proposal_fiscal_qtr,
                    c.po_date,
                    c.po_fiscal_yr,
                    c.po_fiscal_qtr,
                    c.delivery,
                    c.delivery_yr,
                    c.delivery_qtr,

                FROM
                    crm_lead c
                WHERE c.active = 'true'
                GROUP BY c.id
            )""")
