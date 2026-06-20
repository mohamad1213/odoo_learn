"""
Example Model untuk pembelajaran Odoo development

Model ini mendemonstrasikan:
- Definisi model dengan _name dan _description
- Berbagai tipe fields (Char, Text, Integer, Float, Date, Many2one, etc)
- Computed fields dengan @api.depends
- Onchange methods dengan @api.onchange
- Custom methods dan business logic
- SQL constraints dan Python constraints
"""

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime


class ExampleModel(models.Model):
    """
    Model contoh untuk pembelajaran
    
    _name: Unique identifier untuk model (gunakan dot notation)
    _description: Deskripsi model yang tampil di UI
    _order: Default ordering untuk records
    _rec_name: Field yang digunakan sebagai display name (default: 'name')
    """
    
    _name = 'example.model'
    _description = 'Example Model for Learning'
    _order = 'sequence, id'
    _rec_name = 'title'

    # ==================================================================
    # BASIC FIELDS
    # ==================================================================
    
    # Char field - Teks singkat
    title = fields.Char(
        string='Title',  # Label yang tampil di UI
        required=True,   # Field wajib diisi
        help='Masukkan judul contoh'  # Help text
    )
    
    # Text field - Teks panjang
    description = fields.Text(
        string='Description',
        help='Deskripsi detail'
    )
    
    # Integer field
    quantity = fields.Integer(
        string='Quantity',
        default=0,
        help='Jumlah item'
    )
    
    # Float field dengan decimal precision
    price = fields.Float(
        string='Price',
        digits=(12, 2),  # (total digits, decimal places)
        default=0.0
    )
    
    # Boolean field - Checkbox
    is_active = fields.Boolean(
        string='Active',
        default=True,
        help='Aktifkan atau nonaktifkan record ini'
    )
    
    # Selection field - Dropdown
    status = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        required=True,
        help='Status dari record'
    )
    
    # Date field
    date_start = fields.Date(
        string='Start Date',
        default=fields.Date.today,
        help='Tanggal mulai'
    )
    
    # DateTime field
    date_created = fields.Datetime(
        string='Created Date',
        default=fields.Datetime.now,
        readonly=True
    )
    
    # Sequence field - untuk ordering
    sequence = fields.Integer(
        string='Sequence',
        default=10
    )
    
    # ==================================================================
    # RELATION FIELDS
    # ==================================================================
    
    # Many2one - Foreign key relationship (Many records ke 1 record)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )
    
    # Many2many - Multiple relationships (Many to Many)
    tag_ids = fields.Many2many(
        'example.tag',
        'example_model_tag_rel',  # Relation table name
        'model_id',  # Column name di relation table untuk model ini
        'tag_id',    # Column name di relation table untuk tag
        string='Tags',
        help='Select multiple tags'
    )
    
    # One2many - Reverse relationship (1 record ke Many records)
    line_ids = fields.One2many(
        'example.line',  # Target model
        'model_id',      # Field di target model yang merge ke model ini
        string='Lines',
        help='Detail lines'
    )
    
    # ==================================================================
    # COMPUTED FIELDS & ONCHANGE
    # ==================================================================
    
    # Computed field - Nilai dihitung secara otomatis
    @api.depends('quantity', 'price')
    def _compute_total(self):
        """Hitung total dari quantity * price"""
        for record in self:
            record.total = record.quantity * record.price
    
    total = fields.Float(
        string='Total',
        compute='_compute_total',  # Fungsi yang menghitung nilai
        store=True,  # Simpan di database
        readonly=True,  # Field readonly
        help='Total amount (qty * price)'
    )
    
    # Onchange method - Update field saat field lain berubah
    @api.onchange('quantity', 'price')
    def _onchange_update_total(self):
        """Update total saat quantity atau price berubah"""
        if self.quantity and self.price:
            self.total = self.quantity * self.price
            # Bisa juga tampilkan warning
            # self.env.user.notify_info(f"Total updated to {self.total}")
    
    @api.onchange('title')
    def _onchange_title(self):
        """Validasi title onchange"""
        if self.title:
            self.title = self.title.strip().upper()
    
    # ==================================================================
    # SQL CONSTRAINTS (Database level)
    # ==================================================================
    
    _sql_constraints = [
        ('title_unique', 'unique(title)', 'Title harus unik!'),
        ('positive_quantity', 'CHECK(quantity >= 0)', 'Quantity tidak boleh negatif'),
        ('positive_price', 'CHECK(price >= 0)', 'Price tidak boleh negatif'),
    ]
    
    # ==================================================================
    # PYTHON CONSTRAINTS
    # ==================================================================
    
    @api.constrains('quantity')
    def _check_quantity(self):
        """Validasi quantity melalui Python"""
        for record in self:
            if record.quantity < 0:
                raise ValidationError('Quantity tidak boleh negatif!')
            if record.quantity > 10000:
                raise ValidationError('Quantity tidak boleh lebih dari 10000!')
    
    @api.constrains('status')
    def _check_status_change(self):
        """Validasi perubahan status"""
        for record in self:
            # Cek jika ada perubahan status dari database
            old_status = record._origin.status if hasattr(record, '_origin') else None
            if old_status == 'done' and record.status != 'done':
                raise ValidationError('Tidak bisa ubah status dari Done ke status lain!')
    
    # ==================================================================
    # CRUD METHODS
    # ==================================================================
    
    @api.model_create_multi
    @api.returns('self', lambda value: value.id)
    def create(self, vals_list):
        """Override create method"""
        # Lakukan sesuatu sebelum create
        for vals in vals_list:
            # Normalize title
            if 'title' in vals:
                vals['title'] = vals['title'].strip()
        
        # Call parent create
        records = super().create(vals_list)
        
        # Lakukan sesuatu setelah create
        for record in records:
            print(f"Record {record.id} dibuat dengan title {record.title}")
        
        return records
    
    def write(self, vals):
        """Override write method (update)"""
        # Lakukan validasi sebelum update
        if 'status' in vals and vals['status'] == 'cancelled':
            if self.quantity > 0:
                raise ValidationError('Tidak bisa cancel jika masih ada quantity!')
        
        # Call parent write
        result = super().write(vals)
        
        # Lakukan log setelah update
        print(f"Record {self.id} diupdate")
        
        return result
    
    def unlink(self):
        """Override delete method"""
        # Validasi sebelum delete
        for record in self:
            if record.status == 'done':
                raise ValidationError(f'Tidak bisa hapus record dengan status Done!')
        
        # Call parent unlink
        return super().unlink()
    
    # ==================================================================
    # CUSTOM BUSINESS LOGIC METHODS
    # ==================================================================
    
    def action_confirm(self):
        """Custom action - Confirm record"""
        self.status = 'confirmed'
        return {'type': 'ir.actions.client', 'tag': 'reload'}
    
    def action_done(self):
        """Custom action - Mark as Done"""
        for record in self:
            record.status = 'done'
    
    def action_cancel(self):
        """Custom action - Cancel record"""
        for record in self:
            if record.quantity > 0:
                raise ValidationError('Tidak bisa cancel jika masih ada quantity!')
            record.status = 'cancelled'
    
    def get_summary(self):
        """Method untuk return data summary"""
        return {
            'title': self.title,
            'quantity': self.quantity,
            'price': self.price,
            'total': self.total,
            'status': self.status,
        }
    
    # ==================================================================
    # SEARCH & FILTER METHODS
    # ==================================================================
    
    @api.model
    def search_by_title(self, title):
        """Custom search method"""
        return self.search([('title', 'ilike', title)])
    
    @api.model
    def get_active_records(self):
        """Get hanya active records"""
        return self.search([('is_active', '=', True)], order='sequence')


class ExampleTag(models.Model):
    """Model untuk Many2many relationship"""
    _name = 'example.tag'
    _description = 'Example Tag'
    
    name = fields.Char(string='Tag Name', required=True, unique=True)
    color = fields.Integer(string='Color', default=0)


class ExampleLine(models.Model):
    """Model untuk One2many relationship"""
    _name = 'example.line'
    _description = 'Example Line'
    
    model_id = fields.Many2one(
        'example.model',
        string='Parent Model',
        required=True,
        ondelete='cascade'  # Delete line saat parent dihapus
    )
    
    name = fields.Char(string='Description', required=True)
    quantity = fields.Integer(string='Quantity', default=1)
    price = fields.Float(string='Price')
