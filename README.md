# Autonumber Django Application

Django implementation of the Autonumber service.

This is a reimplementation of the Autonumber service from the Ruby on Rails app.

## Installation Options

There are two ways to install this application:

* [uv](https://github.com/astral-sh/uv) (for the recommended installation)
* pyenv, which will manages the shims for `pip` and `python`

---

## Installation

First, get the code by cloning the repository:

```zsh
git clone https://github.com/umd-lib/autonumber-django.git
cd autonumber-django
```

With uv you can install python like so:

```zsh
uv python install 3.14.0
```

With pyenv you use

```zsh
pyenv install 3.14.0
```

### Option 1: Using `uv` (Recommended)

1. **Create a virtual environment:**

    ```zsh
    uv venv
    ```

2. **Install the dependencies:**

    ```zsh
    uv sync --extra dev
    ```

### Option 2: Using pyenv

This uses the standard tools built into Python.

1. **Create a virtual environment:**

    ```zsh
    python -m venv .venv --prompt autonumber
    ```

2. **Activate the environment:**

    ```zsh
    source .venv/bin/activate
    ```

3. **Install the project and its dependencies:**

    ```zsh
    pip install -e ".[dev]"
    ```

---

## Running the Application

Once you have installed the project using either method, you need to set up the database and run the server.

### Option 1: Using `uv` (Recommended)

1. **Run the database migrations:**

    ```zsh
    uv run src/manage.py migrate
    ```

2. **(Optional) Create a superuser:**
    This allows you to log into the Django admin interface at `/admin/`.

    ```zsh
    uv run src/manage.py createsuperuser
    ```

3. **Run the development server:**

    ```zsh
    uv run src/manage.py runserver
    ```

4. Visit **`http://127.0.0.1:8000`** in your web browser.

### Option 2: Using pyenv

1. **Run the database migrations:**

    ```zsh
    python src/manage.py migrate
    ```

2. **(Optional) Create a superuser:**
    This allows you to log into the Django admin interface at `/admin/`.

    ```zsh
    python src/manage.py createsuperuser
    ```

3. **Run the development server:**

    ```zsh
    python src/manage.py runserver
    ```

4. Visit [http://localhost:8000](http://localhost:8000) in your web browser.

---

## Running Tests

This project uses `pytest` and `pytest-django`.

1. **Run the test suite:**
    With uv

    ```zsh
    uv run pytest
    ```

    With pyenv

    ```zsh
    pytest
    ```

    **NOTE** With pyenv you may need to `source .venv/bin/activate` again after installing the optional
    dependencies, so that the pytest shim gets properly updated in your terminal session.
