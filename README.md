# Travel Agency CRM

A web-based CRM for travel agencies. Staff can keep customer records, log travel enquiries, build island-trip quotations, and download a quotation PDF.

The CRM pages are open in the browser. Django’s admin site is separate and asks for a login.

| Guide | Who it is for |
|---|---|
| [Install on Windows](#local-installation) | Anyone setting the project up |
| [How to use the CRM](#how-to-use-the-crm) | Anyone adding customers, enquiries, and quotations |
| [CLIENT_SETUP.md](CLIENT_SETUP.md) | A shorter guide with the same steps in plain language |

On Windows, finish the [known WeasyPrint issue](#known-issues) before expecting the site to open.

## Overview

Travel Agency CRM is a Django application for day-to-day agency work. From the home page, staff can add customers, review enquiries, and open the quotation builder. A saved quotation can be turned into a PDF brochure that includes guest details, the day-by-day plan, accommodation, ferries, rates, and agency text.

The database configured in this repository is SQLite, stored in a local file named `db.sqlite3`. That file is not part of the Git repository.

## Features

These are the features present in the current code.

| Area | What the application does today |
|---|---|
| Customer management | List, add, and edit customers. Each record stores a name, phone, email, and notes. |
| Travel enquiries | List, add, and edit enquiries. The list can be searched by destination or customer name, and filtered by customer. An enquiry stores the customer, destination, dates, adults, children, and travel type (Moderate, Luxury, or Premium Luxury). |
| Quotations | List quotations and open a guided builder. Saving a quotation can create the linked customer and enquiry from the builder. |
| Itinerary management | The builder has a day-by-day plan with a title and morning, afternoon, and evening text. Day photos can be chosen from the photo library. |
| Island stays | Each stay stores the island, order, nights, hotel name, and room category. Rows can be added or removed in the builder. |
| Ferries | Each ferry leg stores the departure island, arrival island, operator, and class. Suggested island, operator, and class names are built into the form. |
| Pricing | The agent types the package price. The builder also stores adults, children, and a package tier of Luxury or Luxury+. |
| PDF generation | A saved quotation has a Download PDF action. The PDF is built from an HTML template. See [PDF Generation](#pdf-generation). |
| Agency content | Agency name, logo, welcome and closing text, inclusions, exclusions, payment terms, and contact details are edited in Django admin. The home page links to agency settings and the photo library. |
| Django admin | `/admin/` can manage the records above, plus older hotel, transport, activity, and itinerary-day records. |

Customer and enquiry screens do not include a delete button. Inside a quotation, island stays, ferry legs, and day-plan rows can be removed.

## Technology Stack

| Piece | Used by this project |
|---|---|
| Python | 3.12 or newer. Django 6.1.1 requires that. Checked locally with Python 3.13. |
| Django | 6.1.1 (`requirements.txt`) |
| Database | SQLite, configured in `travelcrm/settings.py` |
| PDF | WeasyPrint 70.0 |
| Pages | Django templates |
| Front end | Tabler 1.4.0, Bootstrap Icons, the Inter font, and Alpine.js, loaded from public CDNs in `core/templates/core/base.html` |

PostgreSQL is not configured in this repository.

## Project Structure

| Path | Purpose |
|---|---|
| `manage.py` | Command used to migrate the database and start the server |
| `travelcrm/` | Project settings, root URL list, and the WSGI/ASGI entry points |
| `core/` | The CRM application: models, forms, views, admin, and tests |
| `core/templates/core/` | HTML pages, including the quotation PDF template |
| `core/migrations/` | Database migrations already written for the CRM |
| `requirements.txt` | Python packages: Django and WeasyPrint |
| `.env.example` | Notes that this app does not need environment variables |
| `CLIENT_SETUP.md` | Short setup guide written for a non-technical reader |

Uploaded photos are stored in a local `media/` folder after someone adds them. That folder is ignored by Git.

## Requirements

- Python 3.12 or newer
- pip
- The packages in `requirements.txt`
- The native libraries WeasyPrint needs on Windows (`libgobject` and related GTK/Pango libraries)

The last item is not installed by `pip install -r requirements.txt`. On this Windows machine the application does not start until those libraries are present. Details are in [Current Status](#current-status).

## Local Installation

Commands below are for Windows PowerShell. Run them from the project folder, the folder that contains `manage.py`.

1. Clone the repository:

   ```powershell
   git clone https://github.com/sgtyash/travel_crm.git
   ```

2. Open the project folder:

   ```powershell
   cd travel_crm
   ```

3. Create a virtual environment:

   ```powershell
   python -m venv .venv
   ```

4. Activate it:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks the script, start commands with `.\.venv\Scripts\python` instead of `python`. That path was used successfully on this machine.

5. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

6. Environment variables: none are required. The application does not read a `.env` file. `.env.example` only records that fact. Do not put passwords or secret keys in the repository.

7. Apply database migrations:

   ```powershell
   python manage.py migrate
   ```

   This command creates `db.sqlite3`. On the current Windows setup it stops with a WeasyPrint library error before the database is created. See [Current Status](#current-status).

8. Create an admin user. This is required only for `/admin/`. The command asks you to choose a username and password. There is no shared default account.

   ```powershell
   python manage.py createsuperuser
   ```

9. Start the development server:

   ```powershell
   python manage.py runserver
   ```

10. Open the application at the address printed in the terminal. With no port added to the command, Django uses:

    [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Running the CRM

After `python manage.py runserver` is running, use these addresses:

| Page | Address |
|---|---|
| Home | http://127.0.0.1:8000/ |
| Customers | http://127.0.0.1:8000/customers/ |
| Enquiries | http://127.0.0.1:8000/enquiries/ |
| Quotations | http://127.0.0.1:8000/quotations/ |
| Django admin | http://127.0.0.1:8000/admin/ |

The navigation bar also links to Home, Customers, Enquiries, and Quotations.

Stop the server by selecting the terminal and pressing `Ctrl+C`.

The next time you want to open the CRM, you only need these two commands from the project folder:

```powershell
.\.venv\Scripts\Activate.ps1
python manage.py runserver
```

## How to use the CRM

Use the bar at the top of the page: **Home**, **Customers**, **Enquiries**, **Quotations**.

### Add a customer

1. Open **Customers**.
2. Choose **Add Customer**.
3. Enter the name, phone, email, and any notes.
4. Save. You return to that customer’s page and can change the details later.

### Add an enquiry

1. Open **Enquiries**.
2. Choose **Add Enquiry**.
3. Pick the customer, then enter the destination, start date, end date, number of adults, number of children, and travel type.
4. Save.

The enquiry list has a search box for a destination or customer name, and a filter for one customer.

### Create a quotation

1. Open **Quotations**.
2. Choose **Create Quotation**.
3. Fill in the five sections, then save:
   1. **Guest Details** — choose an existing customer, or switch to a new customer name. The arrival date is required. If you type the number of nights, the number of days updates with it. Choose Luxury or Luxury+, and type the package price.
   2. **Island Stays** — island, order, nights, hotel name, and room category. Use **Add Another Island** for another stay.
   3. **Ferry Legs** — departure island, arrival island, ferry operator, and class. Use **Add Another Ferry** for another trip.
   4. **Day-by-Day Plan** — day number, title, morning, afternoon, and evening. Use **Add Another Day** for the next day. Photos appear here after they are uploaded in the admin photo library.
   5. **Review & Save** — choose **Save Quotation**.
4. To change it later, open **Quotations** and choose **Open Quotation**.

You can remove an island stay, ferry leg, or day row inside that quotation. The customer and enquiry pages do not have a delete button.

### Download a PDF

1. Open a quotation that has already been saved.
2. Choose **Download PDF**.
3. The browser downloads a file named from the customer’s name.

The PDF is a brochure: cover, guest details, each day, hotels, ferries, activity rates, experiences, important information, inclusions, exclusions, payment terms, and a closing page. Agency text and photos come from Django admin. If those have not been filled in, those parts of the PDF are blank.

### Set the agency name, logo, and photos

1. Open http://127.0.0.1:8000/admin/ and sign in with the admin user you created.
2. From the CRM home page, **Agency settings** stores the agency name, logo, welcome and closing text, inclusions, exclusions, payment terms, and phone, email, and WhatsApp details. Only one agency record is allowed.
3. **Photo library** is where day photos and brochure images are uploaded.

## Login

The customer, enquiry, and quotation pages do not ask for a login.

Django admin at http://127.0.0.1:8000/admin/ does. Sign in with the username and password created by `python manage.py createsuperuser` on that computer. This repository does not include an admin account.

## Creating a quotation

The full click-by-click steps are in [Create a quotation](#create-a-quotation).

Saving a quotation creates an enquiry when the builder needs one. Enquiries can also be added on their own from **Enquiries**.

Hotel, transport, activity, and simple itinerary-day records exist in the database and in Django admin. The quotation screen itself uses island stays, ferry legs, and the day-by-day plan.

## PDF Generation

On a saved quotation, **Download PDF** calls `/quotations/<id>/pdf/`.

The view loads the quotation, day plans, island stays, ferry legs, activity rates, experiences, and agency settings. It fills `core/templates/core/quotation_pdf.html`, then WeasyPrint converts that HTML into a PDF download. The file name is based on the customer name.

The PDF template includes a cover, guest details, day pages, accommodation, ferries, an activity ratesheet, experiences, important information, inclusions and exclusions, payment terms, and a closing page. Agency wording and photos come from Django admin. If agency settings have not been saved, those sections are empty.

This download path is implemented and covered by a test in `core/tests.py`. It has not been confirmed on this Windows machine, because WeasyPrint cannot load its system libraries here. See the known issue below.

## Current Status

### Implemented

- Customer list, add, and edit
- Enquiry list, search, filter, add, and edit
- Quotation list and guided builder (guest details, island stays, ferry legs, day plan, package price)
- Photo library and single agency-settings record, edited in Django admin
- Activity rates and experiences, edited in Django admin and included in the PDF template
- PDF download code and an automated test for that download
- Django admin for the CRM models

### In progress

- Running the project on Windows. Python packages install. The server, migrations, and tests still stop while importing WeasyPrint.

### Not yet implemented

- Login on the CRM pages
- PostgreSQL
- Cloud deployment settings (allowed hosts, production static files, a production web server)
- A delete action for customers or enquiries on the CRM screens

### Known issues

`python manage.py migrate`, `python manage.py test`, and `python manage.py runserver` fail on this Windows computer before any page opens. `core/views.py` imports WeasyPrint when Django starts, and WeasyPrint cannot load `libgobject-2.0-0`. pip cannot install that library. WeasyPrint’s own install notes are here: [Installing WeasyPrint](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation).

Until that library load succeeds, the database file is not created and the site cannot be opened.

## Deployment

The application is intended to be deployed later to a cloud server so a client can use it in a browser. This repository is prepared for local development only. It does not yet contain deployment configuration, so no production deploy steps are listed here.
