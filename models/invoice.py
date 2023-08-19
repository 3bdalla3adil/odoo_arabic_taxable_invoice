# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

from odoo import api, fields, models
import base64


class Invoice(models.Model):
    _inherit = 'account.move'

    invoice_date = fields.Date('Invoice Date')
    einv_sa_confirmation_datetime = fields.Datetime(string='Confirmation Date', readonly=True, copy=False)

    payment_method = fields.Char('Payment Method')


    def get_total_discount(self):
        total_disc = 0
        for rec in self:
            for line in rec.invoice_line_ids:
                total_disc += (((line.discount * line.price_unit) * line.quantity) / 100)
        return total_disc

    def get_address(self, partner, company=False):
        partner_address = []
        if partner.street:
            partner_address.append(partner.street)
        if partner.street2:
            partner_address.append(partner.street2)
        if not company and partner.city:
            partner_address.append(partner.city)
        if not company and partner.country_id:
            partner_address.append(partner.country_id.name)
        if not company and partner.zip:
            partner_address.append(partner.zip)
        partner_add = ','.join(str(e) for e in partner_address)
        return partner_add

    
    @api.model
    def get_qr_code(self):
        def get_qr_encoding(tag, field):
            company_name_byte_array = field.encode('UTF-8')
            company_name_tag_encoding = tag.to_bytes(length=1, byteorder='big')
            company_name_length_encoding = len(company_name_byte_array).to_bytes(length=1, byteorder='big')
            return company_name_tag_encoding + company_name_length_encoding + company_name_byte_array
        for record in self:
            qr_code_str = ''
            seller_name_enc = get_qr_encoding(1, record.company_id.display_name)
            company_vat_enc = get_qr_encoding(2, record.company_id.vat or '')
            # date_order = fields.Datetime.from_string(record.create_date)
            time_sa = fields.Datetime.context_timestamp(self.with_context(tz='Asia/Riyadh'), record.create_date)
            timestamp_enc = get_qr_encoding(3, time_sa.isoformat())
            invoice_total_enc = get_qr_encoding(4, str(record.amount_total))
            total_vat_enc = get_qr_encoding(5, str(record.currency_id.round(record.amount_total - record.amount_untaxed)))

            str_to_encode = seller_name_enc + company_vat_enc + timestamp_enc + invoice_total_enc + total_vat_enc
            qr_code_str = base64.b64encode(str_to_encode).decode('UTF-8')
            return qr_code_str