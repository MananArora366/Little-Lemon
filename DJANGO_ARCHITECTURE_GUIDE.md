# 🍋 Little Lemon Restaurant: Django Architecture & Interview Revision Guide

This guide is designed for quick review before technical interviews and systems design discussions. It compiles core Django architecture patterns, the MVT lifecycle, real-world bug fixes, and critical trade-offs implemented across the **Little Lemon** project.

---

## 🏛️ 1. Django MVT (Model-View-Template) Architecture

```
[ Client / Browser ]
        │  ▲
        │  │ (HTTP Request / Response)
        ▼  │
 [ URLconf (urls.py) ] ── (Path Converters: <int:pk>)
        │
        ▼
 [ View (views.py) ]
   ├── (Context Dictionary) ──► [ Template (DTL: base.html) ]
   │
   └── (QuerySet API: .filter(), .get()) ──► [ Model (models.py) ]
                                                   │
                                                   ▼
                                           [ Database (SQLite / MySQL) ]
```

### Key Distinctions for Interviews:
* **Django MVT vs Classic MVC**:
  * **Model**: Data access layer, schema definitions, and business invariants / validators.
  * **View (Django)** $\approx$ **Controller (MVC)**: Receives HTTP requests, executes business logic, calls ORM, prepares context, selects template.
  * **Template (Django)** $\approx$ **View (MVC)**: Presentation layer using Django Template Language (DTL).
  * **Framework (Django Engine)**: Acts as the master controller routing URLs and managing request/response middleware lifecycles.

---

## 🛡️ 2. Validation Architecture: "Single Source of Truth"

### ⚠️ The Trap: Form-level vs Model-level Validation
* **Form-level (`clean_<field>()`)**: Validates input *only* when data passes through a Django HTML Form.
* **The Vulnerability**: REST APIs (DRF `ModelSerializer`), Python scripts, `manage.py shell`, and admin bulk imports bypass `clean_<field>()` methods completely!
* **Architectural Solution**: Write field-level validators directly on the **Model**.

```python
# models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_not_in_past(value):
    """Universal validator: Form, DRF, Admin, and Python/Shell."""
    if value < timezone.now():
        raise ValidationError("Booking date cannot be in the past.")

class Booking(models.Model):
    name = models.CharField(max_length=255)
    no_of_guests = models.IntegerField(
        validators=[
            MinValueValidator(1, message="Must have at least 1 guest."),
            MaxValueValidator(20, message="Max capacity is 20 guests.")
        ]
    )
    booking_date = models.DateTimeField(validators=[validate_not_in_past])
```

### Validation Execution Matrix:
| Entry Point | Model Validators Enforced? | Mechanism |
|:---|:---:|:---|
| **Web `ModelForm`** | ✅ | Automatically triggered during `form.is_valid()` / `full_clean()` |
| **DRF `ModelSerializer`** | ✅ | Reads field validators from model automatically |
| **Django Admin** | ✅ | Triggered on admin form validation |
| **`booking.full_clean()`** | ✅ | Manually callable before `.save()` |
| **`objects.create()`** | ❌ (Raw save) | Bypasses validation unless `full_clean()` is invoked |

---

## 🔒 3. Security Pitfalls & Form/Serializer Hygiene

### ❌ Dangerous Smell: `fields = '__all__'`
```python
# BAD PRACTICE
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'  # Exposes any new internal or sensitive model field!
```

### ✅ Best Practice: Explicit Field Declarations
```python
# SECURE PRACTICE
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'no_of_guests', 'booking_date']
```

---

## 🔄 4. The Post/Redirect/Get (PRG) Pattern

### The Problem (F5 Duplicate Submission Bug):
Rendering a page directly on a POST request leaves the browser in a POST state. Hitting refresh (F5) re-posts the data and creates duplicate reservations or charges.

```
Without PRG:
Browser ── POST /book/ ──► Django saves DB ──► 200 OK (Render page)
User presses F5 ─────────► POST /book/ ──► DUPLICATE RESERVATION IN DB!

With PRG:
Browser ── POST /book/ ──► Django saves DB ──► 302 Found (Redirect to /book/)
Browser ── GET /book/  ──► Django ───────────► 200 OK (Clean page with message)
User presses F5 ─────────► GET /book/  ──► Idempotent safe reload!
```

### Implementation:
```python
# views.py
from django.shortcuts import render, redirect
from django.contrib import messages

def web_book_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your table has been reserved successfully!")
            return redirect('restaurant:web-book')  # 302 Redirect
    else:
        form = BookingForm()
    return render(request, 'book.html', {'form': form})
```

---

## ⚡ 5. QuerySet API & Lazy Evaluation

Django QuerySets are **lazy** — they do not hit the database until evaluated (iteration, slicing, `list()`, `len()`, or `repr()`).

```python
# 1. Chaining (No SQL executed yet)
qs = Menu.objects.filter(inventory__gt=0).order_by('title')

# 2. Inspecting the raw SQL query
print(qs.query)
# SELECT * FROM restaurant_menu WHERE inventory > 0 ORDER BY title ASC;

# 3. Single object lookup (Instant DB hit)
item = Menu.objects.get(pk=1)  # Raises DoesNotExist or MultipleObjectsReturned
# Or safer:
from django.shortcuts import get_object_or_404
item = get_object_or_404(Menu, pk=1)  # Raises Http404 on missing record
```

---

## 🧩 6. Template Inheritance & Partials

* **`base.html` (Master Template)**: Defines root HTML, stylesheets, messages container, and blocks:
  * `{% block extra_css %}{% endblock %}`
  * `{% block content %}{% endblock %}`
* **`{% include %}` (Composition)**: Embeds reusable snippets (e.g. `_header.html`, `_footer.html`).
* **`{% extends %}` (Inheritance)**: Child templates override specific blocks while retaining master branding and navigation.
* **`{% url 'namespace:name' %}`**: Decouples HTML templates from hardcoded URL paths.

---

## 🚀 7. Top 5 Django Interview Questions & Fast Answers

### Q1: What happens under the hood when a user visits a Django URL?
1. Request hits `WSGI` / `ASGI` server.
2. Django applies `MIDDLEWARE` pipeline (Security, Session, CSRF, Authentication).
3. `ROOT_URLCONF` resolves the path regex/converters into a view callable + kwargs.
4. View executes queries via Django ORM.
5. Response passes back through middleware to the client.

### Q2: What is the difference between `null=True` and `blank=True`?
* `null=True`: **Database-level** constraint. Column allows `NULL` values in SQL.
* `blank=True`: **Validation/Form-level** constraint. Field is optional in Django forms/admin.
* *Rule of thumb*: Avoid `null=True` on string-based fields (`CharField`, `TextField`) to prevent ambiguous `NULL` vs `""` empty states.

### Q3: How do you switch databases from SQLite to MySQL or PostgreSQL in Django?
Update the `DATABASES` dictionary in `settings.py` (specifying `ENGINE`, `NAME`, `USER`, `PASSWORD`, `HOST`, `PORT`), install the connector (e.g., `mysqlclient` or `psycopg2`), and run `python manage.py migrate`. Django ORM models and queries require **zero** code changes.

### Q4: Why should `get_object_or_404` be preferred over `.get()` in views?
Using `.get()` raises `Model.DoesNotExist` if the record is missing, causing a `500 Internal Server Error`. `get_object_or_404()` automatically catches `DoesNotExist` and returns a clean `404 Not Found` response.

### Q5: What is CSRF and how does Django protect forms?
CSRF (Cross-Site Request Forgery) tricks a logged-in user into executing unwanted actions. Django injects a secure, unique token via `{% csrf_token %}` into forms and verifies it in `CsrfViewMiddleware` on every POST/PUT/DELETE request.
