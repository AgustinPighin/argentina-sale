##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from numpy import rate
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    price_unit_ars = fields.Float('Precio Unitario en Ars', compute='_compute_prices_ars', inverse='_inverse_compute_prices_ars', store=True, tracking=True, default=0.0)

    @api.depends('price_unit')
    def _compute_prices_ars(self):

        print_currency_id = self.env['res.currency'].search([('name', '=', 'ARS')], limit=1)[0]
        for line in self.filtered('product_id'):
            price_unit_aux = round(line.price_unit_ars / print_currency_id.rate,print_currency_id.decimal_places)
            if round(price_unit_aux,2) != round(line.price_unit,2):
                line.price_unit_ars = round(line.price_unit * print_currency_id.rate,print_currency_id.decimal_places)


    @api.onchange('price_unit_ars')
    def _on_change_price_unit_ars(self):
        self._inverse_compute_prices_ars()

    def _inverse_compute_prices_ars(self):
        print_currency_id = self.env['res.currency'].search([('name', '=', 'ARS')], limit=1)[0]
        for line in self.filtered('product_id'):
            price_unit_ars_aux = round(line.price_unit * print_currency_id.rate,print_currency_id.decimal_places)
            if round(price_unit_ars_aux,2) != round(line.price_unit_ars,2):
                line.price_unit = round(line.price_unit_ars / print_currency_id.rate,print_currency_id.decimal_places)