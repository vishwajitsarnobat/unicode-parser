```markdown
# Word to HTML/Unicode Converter (PostgreSQL)

This project allows you to convert complex Microsoft Word documents (`.docx`) into clean HTML Unicode strings and store them in a PostgreSQL database using Python.

**Key Features:**
* **Mathematical Formulae:** Converts Word Math (OMML) to standard **MathML** (web-ready equations).
* **Images:** Automatically extracts images from the Word document to a local folder and preserves the links in the HTML.
* **Multi-language Support:** Fully preserves Unicode characters (Hindi, Arabic, Chinese, etc.).
* **Database Storage:** Stores the processed content directly into a PostgreSQL table.

---

## Prerequisites

### 1. System Requirements (Linux/Ubuntu/Mint)
You must have **Pandoc** installed on your system. This is the engine used to parse the Word document structure.

```bash
sudo apt update
sudo apt install pandoc

```

### 2. Python Dependencies

Install the required Python libraries. You can use `pip` to install them directly:

```bash
pip install pypandoc sqlalchemy psycopg2-binary

```

* `pypandoc`: A wrapper for the system Pandoc tool.
* `sqlalchemy`: An ORM for safe and efficient database interactions.
* `psycopg2-binary`: The PostgreSQL adapter for Python.

---

## Configuration

### 1. Database Setup

Ensure you have a PostgreSQL database running. You can create a new database for this project via your terminal:

```sql
CREATE DATABASE doc_storage;

```

### 2. Project Configuration (`db_config.py`)

Open or create the `db_config.py` file in the root directory and update it with your actual PostgreSQL credentials:

```python
# db_config.py
DB_CONFIG = {
    "drivername": "postgresql",
    "username": "postgres",      # Your database username
    "password": "your_password", # Your database password
    "host": "localhost",
    "port": "5432",
    "database": "doc_storage"    # The name of the DB you created
}

# Connection String Constructor
CONNECTION_STRING = f"{DB_CONFIG['drivername']}://{DB_CONFIG['username']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

```

---

## Usage

1. **Place your Word document** inside the project folder or know its full path.
2. Run the main script:

```bash
python3 process_and_store.py

```

3. **Enter the file path** when prompted:

```text
Enter file path: /home/user/documents/math_paper.docx

```

### What happens next?

1. **Extraction:** Images are extracted to a `./static_media` folder created automatically.
2. **Conversion:** The document text is converted to HTML. Math becomes `<math>` tags; images become `<img src="...">` tags.
3. **Storage:** The script connects to the database. If the table `parsed_documents` does not exist, it creates it. It then inserts the filename and the converted HTML content.
4. **Verification:** A debug file (`debug_output.html`) is created locally so you can open it in a browser to visually verify the conversion.

---

## Project Structure

```text
.
├── db_config.py           # Database connection settings
├── process_and_store.py   # Main logic script (Conversion + DB Storage)
├── README.md              # Project documentation
├── static_media/          # (Auto-generated) Folder containing extracted images
└── debug_output.html      # (Auto-generated) Local preview of the last run

```

---

## Troubleshooting

* **Error: `Pandoc not found**`
* Ensure you ran `sudo apt install pandoc`.
* Verify installation by running `pandoc -v` in your terminal.


* **Error: `psycopg2` module not found**
* Ensure you installed the binary version: `pip install psycopg2-binary`.


* **Equations look like `x^2` instead of Math format**
* Check the HTML output source. It should contain `<math>` tags. If it contains simple text, the Word doc might not have used the native Equation Editor (OMML).



```

```
