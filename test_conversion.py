import pypandoc
import os

def verify_conversion(file_path):
    print(f"--- Processing: {file_path} ---")
    
    # Define a folder to store extracted images
    media_dir = "./extracted_images"
    if not os.path.exists(media_dir):
        os.makedirs(media_dir)

    try:
        # Convert docx to html
        # --mathml: converts Word equations to standard MathML
        # --extract-media: saves images to the specified folder
        output_html = pypandoc.convert_file(
            file_path,
            'html',
            extra_args=['--mathml', f'--extract-media={media_dir}']
        )
        
        # 1. Check if MathML exists in the output
        if "<math" in output_html:
            print("\n[SUCCESS] Mathematical formulas detected (MathML tags found).")
        else:
            print("\n[WARNING] No MathML tags found. (Did the doc contain equations?)")

        # 2. Check for Images
        # We look into the folder we defined to see if files were created
        extracted_files = os.listdir(media_dir)
        if extracted_files:
            print(f"[SUCCESS] Images extracted to '{media_dir}':")
            for img in extracted_files:
                print(f" - {img}")
            
            # Verify the HTML links to these images
            if "<img" in output_html:
                print("[SUCCESS] Image tags found inside the HTML string.")
        else:
            print("\n[INFO] No images found in document.")

        # 3. Print a snippet of the text to terminal for visual check
        print("\n--- HTML Content Snippet (First 500 chars) ---")
        print(output_html[:500])
        print("...\n----------------------------------------------")
        
        return output_html

    except OSError:
        print("Error: Pandoc not found. Please run 'sudo apt install pandoc'")
    except RuntimeError as e:
        print(f"Conversion Error: {e}")

# --- Run the function ---
# Replace 'test.docx' with your actual file name
file_path = "/home/vishwajit/Workspace/unicode-parser/SHIFT-2 with format.docx" 
html = "./test.html"
doc_content = verify_conversion(file_path)
with open(html, 'w') as f:
    f.write(doc_content)
