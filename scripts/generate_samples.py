"""
Sample Invoice Generator
Creates sample invoice images for testing
"""

from PIL import Image, ImageDraw, ImageFont
import os


def create_sample_invoice(filename="test_invoice.png", output_dir="test_files"):
    """Create a sample invoice image"""

    # Create directory
    os.makedirs(output_dir, exist_ok=True)

    # Create image
    width, height = 800, 1000
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    # Try to use a default font
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
        font_medium = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Draw invoice content
    y_pos = 50

    # Header
    draw.text((300, y_pos), "INVOICE", fill='black', font=font_large)
    y_pos += 80

    # Company name
    draw.text((50, y_pos), "ABC Pvt Ltd", fill='black', font=font_medium)
    y_pos += 40
    draw.text((50, y_pos), "123 Business Street", fill='black', font=font_small)
    y_pos += 30
    draw.text((50, y_pos), "City, State 12345", fill='black', font=font_small)
    y_pos += 60

    # Invoice details
    draw.text((50, y_pos), "Invoice No: INV-2025-001", fill='black', font=font_medium)
    y_pos += 40
    draw.text((50, y_pos), "Date: 25/10/2025", fill='black', font=font_medium)
    y_pos += 60

    # Line items header
    draw.line([(50, y_pos), (750, y_pos)], fill='black', width=2)
    y_pos += 10
    draw.text((50, y_pos), "Description", fill='black', font=font_medium)
    draw.text((500, y_pos), "Amount", fill='black', font=font_medium)
    y_pos += 40
    draw.line([(50, y_pos), (750, y_pos)], fill='black', width=1)
    y_pos += 20

    # Line items
    items = [
        ("Product A", "5,000.00"),
        ("Product B", "3,500.00"),
        ("Service Fee", "1,500.00"),
    ]

    for desc, amount in items:
        draw.text((50, y_pos), desc, fill='black', font=font_small)
        draw.text((500, y_pos), f"₹ {amount}", fill='black', font=font_small)
        y_pos += 35

    # Total
    y_pos += 20
    draw.line([(400, y_pos), (750, y_pos)], fill='black', width=2)
    y_pos += 20
    draw.text((400, y_pos), "TOTAL:", fill='black', font=font_medium)
    draw.text((500, y_pos), "₹ 10,000.00", fill='black', font=font_medium)

    # Save
    filepath = os.path.join(output_dir, filename)
    img.save(filepath)
    print(f"✅ Created: {filepath}")

    return filepath


def create_sample_po(filename="test_po.png", output_dir="test_files"):
    """Create a sample purchase order image"""

    # Create directory
    os.makedirs(output_dir, exist_ok=True)

    # Create image
    width, height = 800, 1000
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    # Try to use a default font
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
        font_medium = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Draw PO content
    y_pos = 50

    # Header
    draw.text((250, y_pos), "PURCHASE ORDER", fill='black', font=font_large)
    y_pos += 80

    # Company name (slightly different)
    draw.text((50, y_pos), "ABC Private Limited", fill='black', font=font_medium)
    y_pos += 40
    draw.text((50, y_pos), "123 Business Street", fill='black', font=font_small)
    y_pos += 30
    draw.text((50, y_pos), "City, State 12345", fill='black', font=font_small)
    y_pos += 60

    # PO details
    draw.text((50, y_pos), "PO No: PO-2025-001", fill='black', font=font_medium)
    y_pos += 40
    draw.text((50, y_pos), "Date: 25/10/2025", fill='black', font=font_medium)
    y_pos += 60

    # Line items header
    draw.line([(50, y_pos), (750, y_pos)], fill='black', width=2)
    y_pos += 10
    draw.text((50, y_pos), "Description", fill='black', font=font_medium)
    draw.text((500, y_pos), "Amount", fill='black', font=font_medium)
    y_pos += 40
    draw.line([(50, y_pos), (750, y_pos)], fill='black', width=1)
    y_pos += 20

    # Line items (slightly different amount for testing)
    items = [
        ("Product A", "5,000.00"),
        ("Product B", "3,450.00"),  # Different from invoice
        ("Service Fee", "1,500.00"),
    ]

    for desc, amount in items:
        draw.text((50, y_pos), desc, fill='black', font=font_small)
        draw.text((500, y_pos), f"₹ {amount}", fill='black', font=font_small)
        y_pos += 35

    # Total
    y_pos += 20
    draw.line([(400, y_pos), (750, y_pos)], fill='black', width=2)
    y_pos += 20
    draw.text((400, y_pos), "TOTAL:", fill='black', font=font_medium)
    draw.text((500, y_pos), "₹ 9,950.00", fill='black', font=font_medium)

    # Save
    filepath = os.path.join(output_dir, filename)
    img.save(filepath)
    print(f"✅ Created: {filepath}")

    return filepath


def create_matched_samples():
    """Create matching invoice and PO for testing"""

    # Create invoice
    width, height = 800, 1000
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
        font_medium = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()

    y_pos = 50
    draw.text((300, y_pos), "INVOICE", fill='black', font=font_large)
    y_pos += 80
    draw.text((50, y_pos), "XYZ Corporation", fill='black', font=font_medium)
    y_pos += 80
    draw.text((50, y_pos), "Invoice No: INV-100", fill='black', font=font_medium)
    y_pos += 40
    draw.text((50, y_pos), "Date: 26/10/2025", fill='black', font=font_medium)
    y_pos += 80
    draw.text((400, y_pos), "TOTAL:", fill='black', font=font_medium)
    draw.text((500, y_pos), "₹ 5,000.00", fill='black', font=font_medium)

    os.makedirs("test_files", exist_ok=True)
    img.save("test_files/matched_invoice.png")
    print("✅ Created: test_files/matched_invoice.png")

    # Create matching PO
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    y_pos = 50
    draw.text((250, y_pos), "PURCHASE ORDER", fill='black', font=font_large)
    y_pos += 80
    draw.text((50, y_pos), "XYZ Corporation", fill='black', font=font_medium)
    y_pos += 80
    draw.text((50, y_pos), "PO No: PO-100", fill='black', font=font_medium)
    y_pos += 40
    draw.text((50, y_pos), "Date: 26/10/2025", fill='black', font=font_medium)
    y_pos += 80
    draw.text((400, y_pos), "TOTAL:", fill='black', font=font_medium)
    draw.text((500, y_pos), "₹ 5,000.00", fill='black', font=font_medium)

    img.save("test_files/matched_po.png")
    print("✅ Created: test_files/matched_po.png")


if __name__ == "__main__":
    print("🎨 Generating sample test files...\n")

    # Create mismatched samples
    create_sample_invoice()
    create_sample_po()

    print()

    # Create matched samples
    create_matched_samples()

    print("\n✅ All sample files created in 'test_files/' directory")
    print("\nYou can now test with:")
    print("  - test_invoice.png + test_po.png (should show MISMATCH)")
    print("  - matched_invoice.png + matched_po.png (should show MATCHED)")

