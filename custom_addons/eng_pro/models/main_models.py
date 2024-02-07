from odoo import models, fields
from odoo.exceptions import ValidationError


class Application(models.Model):
    _name = "project.application"
    _description = "applications that come to project"

    name = fields.Char(string='Name', required=True)
    surname = fields.Char(string='Surname', required=True)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone Number")

    project_name = fields.Char(string='Project Name', required=True)
    project_description = fields.Text(string='Project Description', required=True)
    project_sector = fields.Char(string='Project Sector', required=True)

    canvas = fields.Binary(string='Canvas Business Model Evaluation Form', attachment=True, help="Upload a PDF file")
    business_plan = fields.Binary(string='Beneficiary Group Project Business Plan', attachment=True, help="Upload a PDF file")
    fsmh = fields.Binary(string='FSMH held or applied for (if any)', attachment=True, help="Upload a PDF file (optional)")
    incentives = fields.Binary(string='R&D government incentives (Tübitak, KOSGEB etc. - if any)', attachment=True, help="Upload a PDF files (optional)")
    resumes = fields.One2many('file.attachment', 'project_application_id', string='Project Team Resumes')
    project_information = fields.Binary(string='Project Information Presentation', attachment=True, help="Upload a Power Point file")
    reference = fields.Binary(string='Reference text', attachment=True, help="Upload a PDF file")
    gallery = fields.One2many("gallery.attachment", 'project_application_id', string='Visuals, pictures, videos of the project')

    status = fields.Selection(
        [
            ("not_evaluated", "Not Evaluated"),
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        default="not_evaluated"
    )
    apply_date = fields.Date(string="Application Date")
    decision_maker = fields.Many2one("res.users", string="Decision_maker")
    project_group = fields.Many2one("project.group", string="Project Group")

    def accept_pressed(self):
        if self.status != "accepted":
            ProjectGroup = self.env['project.group']
            new_group = ProjectGroup.create({
                'name': self.name,
                'surname': self.surname,
                'email': self.email,
                'phone': self.phone,

                'project_name': self.project_name,
                'project_description': self.project_description,
                'project_sector': self.project_sector,
            })

            self.project_group = new_group.id

        self.status = "accepted"
        self.decision_maker = self.env.user

    def reject_pressed(self):
        if self.status == "accepted":
            if self.project_group:
                self.project_group.unlink()

        self.status = "refused"
        self.decision_maker = self.env.user


class FileAttachment(models.Model):
    _name = 'file.attachment'
    _description = 'File Attachment'

    data = fields.Binary(string='File', attachment=True)
    project_application_id = fields.Many2one('project.application', string='Project Application')


class GalleryAttachment(models.Model):
    _name = "gallery.attachment"
    _description = "Gallery Attachment"

    data = fields.Binary(string="Photo or Video", attachment=True)
    project_application_id = fields.Many2one('project.application', string='Project Application')


class ProjectGroup(models.Model):
    _name = "project.group"
    _description = "Project group in pre-incubation"

    name = fields.Char(string='Name', required=True)
    surname = fields.Char(string='Surname', required=True)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone Number")

    project_name = fields.Char(string='Project Name', required=True)
    project_description = fields.Char(string='Project Description', required=True)
    project_sector = fields.Char(string='Project Sector', required=True)

    user_id = fields.Many2one("res.users", string="Grubun Sistem Kullanıcısı")


class PortalUserCreator(models.TransientModel):
    _name = 'portal.user.creator'

    name = fields.Char(string='Name')
    email = fields.Char(string='Email')
    password = fields.Char(string='Password')

    def create_portal_user(self):
        User = self.env['res.users'].sudo()

        # Create a new user with the portal group
        user_vals = {
            'name': self.name,
            'login': self.email,
            'email': self.email,
            'password': self.password,
            'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])],
        }
        new_user = User.create(user_vals)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'res.users',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': new_user.id,
            'target': 'current',
        }