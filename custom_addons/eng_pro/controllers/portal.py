from odoo.addons.portal.controllers.portal import CustomerPortal, pager
from odoo.http import request
from odoo import http


class PreIncubationPortal(CustomerPortal):

    @http.route(["/my/application"], auth="user", type="http", website=True)
    def wb_student_list_view_portal(self, **kw):
        application = request.env["project.application"].sudo().search([("portal_user_id.id", "=", request.env.uid)], limit=1)
        vals = {"application": application, "page_name": "user_application_portal_view"}
        return request.render("eng_pro.pre_application_stat_view", vals)