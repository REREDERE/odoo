from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Activity(models.Model):
    _name = 'school.activity'
    _description = 'Activity'
    # _inherit = ['mail.thread', 'mail.activity.mixin']  # Habilitar el seguimiento y notificaciones    

    name = fields.Char(string='Description', required=True)
    activity_type = fields.Selection([
        ('task', 'Tarea'),
        ('sports', 'Deportes'),
        ('games', 'Juegos'),
        ('selling', 'Vender')],
        string='Tipo de Actividad', required=True)
    start_time = fields.Datetime(string='Hora de Inicio', required=True)
    end_time = fields.Datetime(string='Hora de Finalización', required=True)
    completed = fields.Boolean(string='Actividad Completada', default=False)
    schedule_id = fields.Many2one('school.schedule', string='Schedule', required=True)
    user_id = fields.Many2one('res.users', string='Assigned User', required=True, default=lambda self: self.env.user)

    @api.constrains('start_time', 'end_time')
    def _check_time(self):
        for record in self:
            if record.start_time >= record.end_time:
                raise UserError("La hora de inicio debe ser menor que la hora de finalización.")
                
    # @api.model
    # def create(self, vals):
    #     record = super(Activity, self).create(vals)
        
    #     record.message_post(
    #         body=_("Se ha creado una nueva actividad: %s") % record.name,
    #         subject="Nueva actividad creada",
    #         message_type='notification',
    #         partner_ids=[(4, record.user_id.partner_id.id)],  # Notificar al usuario asignado
    #     )
    #     return record
    @api.model
    def create(self, vals):
        # Elimina el método message_post para no enviar notificaciones automáticas
        return super(Activity, self).create(vals)