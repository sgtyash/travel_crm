# Setting up the Travel Agency CRM

This guide is for someone who wants to open the CRM on a Windows computer. You do not need to change the program. You only need to download it and start it.

## What this project is

Travel Agency CRM is a website that runs on your computer. It is for keeping customers, travel enquiries, and trip quotations. A saved quotation can be downloaded as a PDF.

The pages for customers, enquiries, and quotations do not ask you to log in. A separate admin page does.

## A problem you should know about first

On Windows, this project does not currently start.

The PDF tool (WeasyPrint) needs extra Windows software that is not included in the download. Without it, the setup commands stop with an error about a missing library named `libgobject-2.0-0`. When that happens:

- the database is not created
- the website does not open
- there is nothing to log in to yet

Installing the normal Python packages is not enough to fix this. Ask the developer before spending time on the steps below. The steps are still the correct ones to use after that library problem is fixed.

## What needs to be installed

1. **Git**, so you can download the project.
2. **Python 3.12 or newer**, including pip. Python 3.13 has been used with this project.
3. The extra Windows libraries that WeasyPrint needs. They are not installed by the steps in this guide.

## How to download the project

1. Open PowerShell.
2. Go to the folder where you want the project. For example, your user folder:

   ```powershell
   cd $HOME
   ```

3. Download the project:

   ```powershell
   git clone https://github.com/sgtyash/travel_crm.git
   ```

4. A new folder named `travel_crm` will appear.

## How to open the project

In PowerShell:

```powershell
cd travel_crm
```

You are in the right folder when you can see a file named `manage.py`.

## How to start the CRM

Run these commands one at a time. Wait for each one to finish.

Create a private Python folder for this project:

```powershell
python -m venv .venv
```

Turn that folder on:

```powershell
.\.venv\Scripts\Activate.ps1
```

If Windows refuses to run that file, you can still continue. Put `.\.venv\Scripts\python` in front of the later commands instead of `python`.

Install the project’s Python packages:

```powershell
python -m pip install -r requirements.txt
```

You do not need to create a `.env` file. This project does not use one.

Create the local database:

```powershell
python manage.py migrate
```

Create your own admin login. The command will ask you for a username, email, and password. Choose a password you will remember. Do not use a password written in an email or chat.

```powershell
python manage.py createsuperuser
```

Start the website:

```powershell
python manage.py runserver
```

Leave this PowerShell window open while you use the CRM. When it is running, the window stays busy on purpose.

## How to open it in a browser

Open a browser and go to:

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

Other useful pages:

| Page | Address |
|---|---|
| Customers | http://127.0.0.1:8000/customers/ |
| Enquiries | http://127.0.0.1:8000/enquiries/ |
| Quotations | http://127.0.0.1:8000/quotations/ |
| Admin | http://127.0.0.1:8000/admin/ |

## How to use the CRM

After the site is open, use the links at the top of the page.

### Add a customer

1. Click **Customers**.
2. Click **Add Customer**.
3. Type the name, phone, email, and any notes.
4. Save.

### Add an enquiry

1. Click **Enquiries**.
2. Click **Add Enquiry**.
3. Choose the customer.
4. Type the destination, travel dates, number of adults, number of children, and the type of trip.
5. Save.

You can search the enquiry list by destination or customer name.

### Create a quotation

1. Click **Quotations**.
2. Click **Create Quotation**.
3. Work through the page from top to bottom:
   - Guest details, including the arrival date and the package price
   - Island stays, including the hotel name and room
   - Ferry trips between islands
   - A plan for each day: morning, afternoon, and evening
4. Click **Save Quotation** at the bottom of the page. Use **Add Another Island**, **Add Another Ferry**, or **Add Another Day** when the trip has more than one of those.
5. To change it later, go back to **Quotations** and click **Open Quotation**.

### Download the PDF

1. Open a quotation you have already saved.
2. Click **Download PDF**.
3. Your browser saves the brochure.

The agency name, logo, and extra brochure text are added from the **Admin** page. If you have not filled those in, the PDF still downloads, with those sections left blank.

### Add the agency logo and photos

1. Open http://127.0.0.1:8000/admin/.
2. Sign in with the admin username and password you created.
3. Open **Agency settings** for the agency name, logo, and brochure text.
4. Open **Photo library** to upload pictures used on the quotation.

## How to log in

Customers, enquiries, and quotations open without a login.

The admin page asks for the username and password you typed during `createsuperuser`. There is no ready-made username or password in this project.

## How to stop the CRM

Click the PowerShell window where the server is running, then press `Ctrl+C`.

You can start it again later from the project folder:

```powershell
.\.venv\Scripts\Activate.ps1
python manage.py runserver
```

## If an error occurs

- **`libgobject-2.0-0` or WeasyPrint** — this is the known Windows problem. The CRM will not open until those libraries are installed. Send the developer a screenshot of the error. Do not keep retrying the same command.
- **`python` is not recognized** — Python is not installed, or it was not added to PATH. Install Python 3.12 or newer and try again.
- **Activate.ps1 cannot be loaded** — use `.\.venv\Scripts\python` instead of `python` for the remaining commands.
- **Address will not open in the browser** — check that the PowerShell window still shows the server running, and that you used `http://127.0.0.1:8000/`.
- **Admin login fails** — the CRM pages do not use that login. For `/admin/`, use the username and password from `createsuperuser` on this same computer.

More detail for a developer is in `README.md`.
