# Setup Minimum Odoo untuk Developer Pemula

Panduan lengkap untuk setup Odoo development environment menggunakan Docker.

## 📋 Prasyarat

- **Docker Desktop** (Windows/Mac) atau Docker Engine (Linux)
- **Git** untuk version control
- **VS Code** atau editor pilihan Anda
- **Terminal/PowerShell** (Windows) atau Terminal (Mac/Linux)

## 🚀 Quick Start

### 1. Clone Repository
```bash
# Jika menggunakan git
git clone <repository-url>
cd Odoo
```

### 2. Konfigurasi Environment
Edit file `.env` dengan konfigurasi database Anda:

```env
HOST=odoo-postgres
USER=odoo
PASSWORD=odoo
POSTGRES_DB=postgres
POSTGRES_PASSWORD=odoo
POSTGRES_USER=odoo
PGDATA=/var/lib/postgresql/data/pgdata
```

### 3. Jalankan Container
```bash
# Pull image terbaru
docker-compose pull

# Jalankan container
docker-compose up -d

# Lihat status
docker-compose ps
```

### 4. Akses Odoo
- **URL**: http://localhost:8069
- **Master Password**: (jika diminta, biarkan kosong atau cek di `etc/odoo/odoo.conf`)
- **Database**: postgres (atau custom sesuai `.env`)
- **Username**: admin
- **Password**: admin

### 5. Buat Database Baru
Jika ingin membuat database baru:

```bash
# Masuk ke container Odoo
docker-compose exec odoo bash

# Buat database (opsional)
# Database akan dibuat otomatis saat setup wizard
```

## 📁 Struktur Folder

```
Odoo/
├── docker-compose.yml    # Konfigurasi Docker services
├── .env                  # Environment variables
├── .gitignore           # Git ignore rules
├── README.md            # File ini
├── addons/              # Custom modules/addons
│   └── .gitkeep
├── etc/
│   └── odoo/
│       └── odoo.conf    # Konfigurasi Odoo server
└── var/
    └── lib/
        ├── odoo/        # Data Odoo (filestore, sessions)
        └── postgresql/  # Data PostgreSQL
```

## 📝 Cara Membuat Custom Module

### 1. Buat Direktori Module
```bash
cd addons
mkdir my_custom_module
cd my_custom_module
```

### 2. Struktur Module Minimal
```
my_custom_module/
├── __init__.py          # Inisialisasi Python
├── __manifest__.py      # Metadata module
├── models/
│   ├── __init__.py
│   └── my_model.py      # Definisi model
└── views/
    ├── __init__.py
    └── my_view.xml      # View XML
```

### 3. Template `__manifest__.py`
```python
{
    'name': 'My Custom Module',
    'version': '17.0.1.0.0',
    'category': 'Uncategorized',
    'summary': 'Deskripsi singkat module',
    'author': 'Your Name',
    'website': 'https://yourwebsite.com',
    'depends': [
        'base',
        'sale',  # tambahkan dependency sesuai kebutuhan
    ],
    'data': [
        'views/my_view.xml',
    ],
    'installable': True,
}
```

### 4. Template Model (`models/my_model.py`)
```python
from odoo import models, fields

class MyModel(models.Model):
    _name = 'my.custom.model'
    _description = 'My Custom Model'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
```

## 🛠 Command Penting

```bash
# Lihat log Odoo real-time
docker-compose logs -f odoo

# Lihat log PostgreSQL
docker-compose logs -f odoo-postgres

# Restart Odoo container
docker-compose restart odoo

# Stop semua container
docker-compose down

# Stop dan hapus semua data
docker-compose down -v

# Masuk ke shell Odoo
docker-compose exec odoo bash

# Jalankan Odoo dengan mode development
docker-compose exec odoo odoo -d postgres -i my_module

# Update module
docker-compose exec odoo odoo -d postgres -u my_module
```

## 📚 Menu Instalasi Module

1. Buka Odoo di browser: http://localhost:8069
2. Login dengan username: `admin`, password: `admin`
3. Klik **Settings** (gear icon di kanan atas)
4. Aktifkan **Developer Mode** (pilih di bagian bawah)
5. Masuk ke **Apps** → **Update Apps List**
6. Cari module Anda di search box
7. Klik pada module dan tekan **Install**

## 🔍 Troubleshooting

### Container tidak jalan
```bash
# Check status
docker-compose ps

# Lihat error detail
docker-compose logs odoo
```

### Database permission error
```bash
# Reset permission
docker-compose down -v
docker-compose up -d
```

### Port 8069 sudah digunakan
Edit `docker-compose.yml`:
```yaml
ports:
  - "8070:8069"  # Ganti 8070 dengan port lain
```

## 📖 Resource Belajar

- **Official Docs**: https://www.odoo.com/documentation/17.0/
- **Development Guide**: https://www.odoo.com/documentation/17.0/developer/
- **GitHub Odoo**: https://github.com/odoo/odoo
- **Community**: https://www.odoo.com/forum

## ✨ Best Practices

- ✅ Selalu gunakan Git untuk version control
- ✅ Buat branch baru untuk setiap fitur
- ✅ Test module secara lokal sebelum push
- ✅ Update database dependencies di `__manifest__.py`
- ✅ Gunakan database terpisah untuk development dan testing
- ✅ Backup data secara regular

## 🤝 Kontribusi

Silakan submit issue atau pull request untuk improvements.

---

**Happy Coding! 🎉**

Untuk pertanyaan, silakan buka issue atau hubungi team development.
