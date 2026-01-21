from pathlib import Path
import pypandoc
import sys

def process_doc(file_path: Path) -> str | None:
    """
    Converts a docx file to an HTML string with MathML for equations.
    """
    try:
        output = pypandoc.convert_file(
            str(file_path),
            'html',
            extra_args=['--mathml', '--standalone']
        )
        return output
    except OSError:
        print("Error: Pandoc not found. Please install Pandoc on your system.")
        return None


if __name__ == "__main__":
    file_path = Path(input("Enter file path: ").strip())
    print(f"Checking file {file_path}")

    if not file_path.exists():
        print("File doesn't exist, please cross-check the path!")
        sys.exit(1)

    if file_path.suffix.lower() != ".docx":
        print("Make sure you input a Word file with .docx extension!")
        sys.exit(1)

    content = process_doc(file_path)

    if content:
        print("Conversion successful!")
        print(content[:500])

