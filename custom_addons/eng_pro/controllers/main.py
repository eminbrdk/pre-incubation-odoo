import base64
from odoo import http
from odoo.http import request
from datetime import date


class ApplyWebsite(http.Controller):

    # user yaptık çünkü sadece giriş yapanlar erişsin istedik
    # public yaparsak herkes erişir
    @http.route("/apply", type="http", auth="user", website=True, methods=["GET", "POST"])
    def create_property_tag(self, **post):
        vals = {}

        if request.httprequest.method == "POST":
            if request.env["project.application"].sudo().search([("portal_user_id", "=", request.env.user.id)]):
                vals['alert'] = "Kullanıcı daha önceden başvuru yapmış. Tekrar yapamaz!"
            else:
                name = post.get("name")
                surname = post.get("surname")
                email = post.get("email")
                phone = post.get("phone")

                project_name = post.get("project_name")
                project_description = post.get("project_description")
                project_sector = post.get("project_sector")

                canvas = post.get("canvas")
                business_plan = post.get("business_plan")
                fsmh = post.get("fsmh")
                incentives = post.get("incentives")
                resumes = request.httprequest.files.getlist('resumes')
                project_information = post.get("project_information")
                gallery = request.httprequest.files.getlist("gallery")
                reference = post.get("reference")

                apply_date = date.today()

                if (
                     not name
                     or not surname
                     or not email
                     or not phone

                     or not project_name
                     or not project_description
                     or not project_sector

                     or not canvas
                     or not business_plan
                     or not resumes
                     or not project_information
                     or not gallery
                     or not reference
                ):
                    vals['alert'] = "Beklenmeyen bir hata oluştu"

                else:

                    canvas_data = base64.b64encode(canvas.read()) if canvas else False
                    business_plan_data = base64.b64encode(business_plan.read()) if business_plan else False
                    fsmh_data = base64.b64encode(fsmh.read()) if fsmh else False
                    incentives_data = base64.b64encode(incentives.read()) if incentives else False
                    project_information_data = base64.b64encode(project_information.read()) if project_information else False
                    gallery_data = [(0, 0, {
                        'data': base64.b64encode(g.read()) if g else False
                    }) for g in gallery]
                    resumes_data = [(0, 0, {
                        'data': base64.b64encode(r.read()) if r else False
                    }) for r in resumes]
                    reference_data = base64.b64encode(reference.read()) if reference else False

                    questions = request.env["jury.question"].sudo().search([])

                    new_application = request.env["project.application"].sudo().create({
                        "name": name,
                        "surname": surname,
                        "email": email,
                        "phone": phone,

                        "project_name": project_name,
                        "project_description": project_description,
                        "project_sector": project_sector,

                        "canvas": canvas_data,
                        "business_plan": business_plan_data,
                        "fsmh": fsmh_data,
                        "incentives": incentives_data,
                        "resumes": resumes_data,
                        "project_information": project_information_data,
                        "gallery": gallery_data,
                        "reference": reference_data,

                        "apply_date": apply_date,
                        "questions": questions,
                    })

                    new_application["portal_user_id"] = request.env.user

                    vals['alert'] = "Başvuru başarıyla tamamlandı"

        return request.render("eng_pro.12", vals)

    @http.route("/create_portal_user", type="http", auth="public", website=True, methods=["GET", "POST"])
    def create_portal_user(self, **post):
        if request.httprequest.method == "POST":

            name = post.get("name")
            password = post.get("password")
            email = post.get("email")

            new_portal_user = request.env["portal.user.creator"].sudo().create({
                "name": name,
                "email": email,
                "password": password
            })

            new_portal_user.create_portal_user()
            return request.redirect("/create_user_success")

        return request.render("eng_pro.cpu")

    @http.route("/create_user_success", type="http", auth="public", website=True, methods=["GET", "POST"])
    def create_user_success(self, **post):
        if request.httprequest.method == "POST":
            return request.redirect("/apply")

        return request.render("eng_pro.cus")

    @http.route("/apply_success", type="http", auth="user", website=True, methods=["GET", "POST"])
    def apply_success(self, **post):
        if request.httprequest.method == "POST":
            return request.redirect("/my/home")

        return request.render("eng_pro.as")
