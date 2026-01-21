import sys
import os
import pypandoc
from pathlib import Path
from sqlalchemy import create_engine, text
from db_config import CONNECTION_STRING

def setup_database():
    """
    Connects to Postgres and creates the table if it doesn't exist.
    """
    try:
        engine = create_engine(CONNECTION_STRING)
        with engine.connect() as conn:
            # Create a table with an ID, Filename, and the HTML Content (Text)
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS parsed_documents (
                    id SERIAL PRIMARY KEY,
                    filename VARCHAR(255),
                    content TEXT, 
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.commit()
        print("[DB] Database connected and table verified.")
        return engine
    except Exception as e:
        print(f"[DB Error] Could not connect to database: {e}")
        sys.exit(1)

def convert_docx_to_html(file_path: Path, media_path: str):
    """
    Converts docx to HTML/MathML and extracts images.
    """
    print(f"--- Converting: {file_path.name} ---")
    
    # Ensure image directory exists
    if not os.path.exists(media_path):
        os.makedirs(media_path)
        print(f"[Info] Created directory: {media_path}")

    try:
        # Convert file
        # --extract-media: tells pandoc where to dump the images
        # --mathml: ensures mathematical formulas are preserved
        output_html = pypandoc.convert_file(
            str(file_path),
            'html',
            extra_args=['--mathml', '--standalone', f'--extract-media={media_path}']
        )
        
        # Simple verification checks
        if "<math" in output_html:
            print("[Check] MathML tags detected.")
        if "<img" in output_html:
            print("[Check] Image tags detected.")
            
        return output_html

    except OSError:
        print("[Error] Pandoc not found. Please install: sudo apt install pandoc")
        return None
    except RuntimeError as e:
        print(f"[Error] Conversion failed: {e}")
        return None

def save_to_db(engine, filename, content):
    """
    Inserts the processed HTML content into the PostgreSQL database.
    """
    try:
        with engine.connect() as conn:
            query = text("INSERT INTO parsed_documents (filename, content) VALUES (:fn, :ct)")
            conn.execute(query, {"fn": filename, "ct": content})
            conn.commit()
            print(f"[Success] '{filename}' stored in database.")
    except Exception as e:
        print(f"[DB Error] Failed to insert data: {e}")

if __name__ == "__main__":
    db_engine = setup_database()
    raw_input = input("Enter file path: ").strip()
    
    # Handle quotes if user drags and drops file in terminal
    raw_input = raw_input.replace("'", "").replace('"', "")
    file_path = Path(raw_input)

    if not file_path.exists():
        print(f"[Error] File not found: {file_path}")
        sys.exit(1)
    
    if file_path.suffix.lower() != ".docx":
        print("[Error] Input must be a .docx file.")
        sys.exit(1)

    # We use a folder named 'static_media' in the current directory, later we will manage this
    media_output_dir = "./static_media" 

    html_content = convert_docx_to_html(file_path, media_output_dir)
    if html_content:
        save_to_db(db_engine, file_path.name, html_content)
        # save in html for debugging 
        with open("debug_output.html", "w") as f:
            f.write(html_content)
            print("[Info] Debug copy saved to 'debug_output.html'")
