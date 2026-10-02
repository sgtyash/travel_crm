# Travel Agency CRM

A Django-based CRM for managing travel customers, enquiries, quotations, and their trip costs.

## Local setup

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

4. Run the development server:

   ```bash
   python manage.py runserver 0.0.0.0:8765
   ```

Open the CRM at `http://127.0.0.1:8765/customers/`. The Django admin is available at `http://127.0.0.1:8765/admin/`; sign in with:

- Username: `admin`
- Email: `admin@example.com`
- Password: `admin1234`

## CRM pages

- Customers: `/customers/`
- Enquiries: `/enquiries/`
- Quotations: `/quotations/`
