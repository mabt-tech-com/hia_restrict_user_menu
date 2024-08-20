from odoo import fields, models, api


class CustomUser(models.Model):
    """
    Model to handle restricting specific menu items for certain users.
    """
    _inherit = 'res.users'

    def write(self, vals):
        """
         Write method for the CustomUser model.
         Ensure the menu will not remain restrict after removing it from the list.
           """
        res = super(CustomUser, self).write(vals)
        for record in self:
            for menu in record.hidden_menu_items:
                menu.write({
                    'restricted_users': [fields.Command.link(record.id)]
                })
        return res

    def _get_is_admin(self):
        """
        Compute method to check if the user is an admin.
        The Hide specific menu tab will be restrict for the Admin user form.
        """
        for rec in self:
            rec.is_admin = False
            if rec.id == self.env.ref('base.user_admin').id:
                rec.is_admin = True

    hidden_menu_items = fields.Many2many(
        'ir.ui.menu', string="Hidden Menu",
        store=True, help='Select menu items that need to '
                         'be hidden to this user.')
    is_admin = fields.Boolean(compute=_get_is_admin, string="Is Admin",
                              help='Check if the user is an admin.')


class CustomUiMenu(models.Model):
    """
    Model to restrict the menu for specific users.
    """
    _inherit = 'ir.ui.menu'

    restricted_users = fields.Many2many(
        'res.users', string="Restricted Users",
        help='Users restricted from accessing this menu.')


    root_id = fields.Many2one('ir.ui.menu', string="Application", compute='_compute_root_id', store=True)

    @api.depends('parent_id')
    def _compute_root_id(self):
        """
        Computes root element for every record and stores in root_id field.
        """
        for record in self:
            current_record = record
            while current_record.parent_id:
                current_record = current_record.parent_id
            record.root_id = current_record.id
        return True
