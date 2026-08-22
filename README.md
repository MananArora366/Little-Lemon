# Little Lemon

Backend for the Little Lemon restaurant — a Django web application with server-rendered
pages for customers and a REST API layer for programmatic access.

Built as the course project for the **Meta Back-End Developer** certificate
(*Django Web Framework*), extended with validation and test coverage beyond the
course requirements.

---

## Stack

| | |
|---|---|
| Python | 3.13 |
| Django | 6.1 |
| Django REST Framework | 3.18 |
| Database | SQLite (development) |

---

## Setup

```bash
git clone https://github.com/MananArora366/Little-Lemon.git
cd Little-Lemon

python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser   # optional, for /admin/
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

---

## Routes

### Web pages (server-rendered HTML)

| URL | View | Description |
|---|---|---|
| `/` | `index` | Landing page |
| `/web-menu/` | `web_menu_view` | Menu grid — in-stock items only, sorted by title |
| `/web-menu/<pk>/` | `web_menu_item_view` | Single item detail; returns 404 if the ID doesn't exist |
| `/web-book/` | `web_book_view` | Booking form (GET renders, POST saves and redirects) |
| `/admin/` | Django admin | Manage `Menu` and `Booking` records |

### REST API

| Method | Endpoint | Description |
|---|---|---|
| `GET`, `POST` | `/menu/` | List or create menu items |
| `GET`, `PUT`, `PATCH`, `DELETE` | `/menu/<pk>/` | Retrieve, update, or delete a menu item |
| `GET`, `POST` | `/restaurant/booking/tables/` | List or create bookings |
| `GET`, `PUT`, `PATCH`, `DELETE` | `/restaurant/booking/tables/<pk>/` | Retrieve, update, or delete a booking |
| | `/api-auth/` | DRF browsable-API login |

> API endpoints currently use `AllowAny`. Authentication and permissions are
> handled in the follow-up *APIs* course.

---

## Models

**`Menu`** — `title`, `price`, `inventory`

**`Booking`** — `name`, `no_of_guests`, `booking_date`

### Validation

Booking rules live as **validators on the model**, not on the form. This means the
same rules apply through every entry point — the web form, the REST API, the admin,
and direct ORM writes:

| Field | Rule |
|---|---|
| `no_of_guests` | Between 1 and 20 (`MinValueValidator` / `MaxValueValidator`) |
| `booking_date` | Cannot be in the past (custom `validate_not_in_past`) |

`BookingForm` deliberately does **not** re-implement these as `clean_<field>()`
methods — `ModelForm` already runs model validators during `full_clean()`, so
duplicating them would produce two competing error messages for one rule.

---

## Notable implementation details

**Post/Redirect/Get on the booking form.** A successful POST saves the booking,
sets a success message, and returns a `302` redirect rather than rendering the
page directly. Without this, pressing refresh after booking re-submits the form
and creates a duplicate reservation. Verified by `test_booking_post_redirects`
and confirmed against the dev server request log.

**Named URLs everywhere.** The `restaurant` app declares `app_name = 'restaurant'`,
and every template and redirect uses `{% url 'restaurant:...' %}` / `redirect('restaurant:...')`
instead of hardcoded paths. Tests use `reverse()` for the same reason.

**Template inheritance.** `base.html` holds the shared shell — nav, footer, global
styles, and the messages block. Pages extend it and inject page-specific CSS through
`{% block extra_css %}`, which is placed *after* the base stylesheet so page rules
can override base rules.

**Custom error pages.** `404.html` and `500.html` extend `base.html`.
These are only served when `DEBUG = False`; with `DEBUG = True` Django shows its
own debug traceback pages instead.

---

## Project structure

```
littlelemon/
├── littlelemon/            # project config
│   ├── settings.py
│   └── urls.py             # admin, app routes, DRF router, api-auth
├── restaurant/
│   ├── models.py           # Menu, Booking + validators
│   ├── forms.py            # BookingForm (ModelForm)
│   ├── serializers.py      # MenuSerializer, BookingSerializer
│   ├── views.py            # function views (web) + DRF class views (API)
│   ├── urls.py             # app_name = 'restaurant'
│   ├── admin.py
│   ├── tests.py
│   ├── migrations/
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── menu.html
│       ├── menu_item.html
│       ├── book.html
│       ├── 404.html
│       └── 500.html
├── manage.py
└── requirements.txt
```

---

## Tests

```bash
python manage.py test
```

Coverage includes model string representations and validators, web page rendering,
the empty-menu state, 404 handling for missing menu items, the PRG redirect,
form rejection of invalid guest counts and past dates, and API responses for
both valid and invalid booking payloads.

---

## Course progress

| Module | Topic | Status |
|---|---|---|
| 1 | Django project & app setup, URL routing | Complete |
| 2 | Views, URL mapping, error handling | Complete |
| 3 | Models, migrations, admin | Complete |
| 4 | Templates and template inheritance | Complete |
| 5 | Forms and `ModelForm` | Complete |

The Django REST Framework code in this repository goes beyond the *Django Web
Framework* course and belongs to the follow-up *APIs* course.
