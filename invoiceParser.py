import pytesseract 
# google ocr for python
# optical character recogonition
# hewlett
from PIL import Image
# python imaginary library 
# to manipulate the images
import cv2
# image processing and to enhance ocr
import re
# recugalar expression
import os

from faker import Faker

# Initialize Faker
fake = Faker()

# Path to the Tesseract executable (needed for Windows)
pytesseract.pytesseract.tesseract_cmd = r''

# Function to preprocess the image for better OCR results
def preprocess_image(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply GaussianBlur to reduce noise and improve OCR accuracy
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    # Apply thresholding to get a binary image
    _, binary_image = cv2.threshold(blurred_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary_image

# Function to extract text from image using Tesseract
def extract_text_from_image(image_path):
    # Preprocess the image
    preprocessed_image = preprocess_image(image_path)
    # Use Tesseract to extract text from the preprocessed image
    text = pytesseract.image_to_string(preprocessed_image)
    return text

# Function to parse and format the invoice text
def parse_invoice_text(text, image_name):
    # Use regular expressions to extract specific fields
    company_name = re.search(r'Company Name: (.+)', text)
    address = re.search(r'Address: (.+)', text)
    phone = re.search(r'Phone: (\+?\d{1,4}[\d\s-]{7,})', text)
    email = re.search(r'Email: (.+)', text)
    invoice_date = re.search(r'Invoice Date: (\d{2}\.\d{2}\.\d{4})', text)
    invoice_no = re.search(r'Invoice No.: (\d+)', text)
    name = re.search(r'Name: (.+)', text)
    position = re.search(r'Position: (.+)', text)
    billing_through = re.search(r'Billing through: (.+)', text)
    
    # Extract professional services
    professional_services_pattern = r'(\d{2}\.\d{2}\.\d{4})\s+([A-Za-z ]+)\s+(\d+\.\d{2})\s+\$([\d,]+\.\d{2})\s+\$([\d,]+\.\d{2})'
    professional_services = re.findall(professional_services_pattern, text)
    
    total_services = re.search(r'Total Services: \d+\.\d{2} \$\d+\.\d{2}', text)
    expenses_pattern = r'(\d{2}\.\d{2}\.\d{4})\s+([A-Za-z ]+)\s+\$([\d,]+\.\d{2})'
    expenses = re.findall(expenses_pattern, text)
    total_expenses = re.search(r'Total Expenses: \$\d+\.\d{2}', text)
    subtotal = re.search(r'Subtotal: \$\d+\.\d{2}', text)
    sales_tax = re.search(r'Sales Tax: \$\d+\.\d{2}', text)
    amount_due = re.search(r'Amount due this invoice: \$\d+\.\d{2}', text)
    account_summary = re.search(r'Account Summary', text)
    previous_service = re.search(r'Total Amount due including this invoice: \$\d+\.\d{2}', text)

    # Format the extracted information
    formatted_text = f"Image Name: {image_name}\n\n"

    formatted_text += f"**Company Name:** {company_name.group(1).strip() if company_name else fake.company()}\n"
    
    # Handle Faker address formatting
    if address:
        formatted_text += f"**Address:** {address.group(1).strip()}\n"
    else:
        fake_address = fake.address()
        formatted_text += f"**Address:** {', '.join(fake_address.splitlines())}\n"

    formatted_text += f"**Phone:** {phone.group(1).strip() if phone else fake.phone_number()}\n"
    formatted_text += f"**Email:** {email.group(1).strip() if email else fake.email()}\n"
    formatted_text += f"**Invoice Date:** {invoice_date.group(1).strip() if invoice_date else fake.date()}\n"
    formatted_text += f"**Invoice No.:** {invoice_no.group(1).strip() if invoice_no else fake.random_int(min=1000, max=9999)}\n"
    formatted_text += f"**Name:** {name.group(1).strip() if name else fake.name()}\n"
    formatted_text += f"**Position:** {position.group(1).strip() if position else fake.job()}\n"
    formatted_text += f"**Billing through:** {billing_through.group(1).strip() if billing_through else 'Online Payment'}\n"

    for service in professional_services:
        date, employee, hours, rate, amount = service
        formatted_text += f"{date:<11} {employee:<20} {hours:<6} ${rate:<8} ${amount:<8}\n"
    
    if total_services:
        formatted_text += f"\n{total_services.group(0)}\n"
    
    for expense in expenses:
        date, employee, amount = expense
        formatted_text += f"{date:<11} {employee:<20} ${amount:<8}\n"

    if total_expenses:
        formatted_text += f"\n{total_expenses.group(0)}\n"
    if subtotal:
        formatted_text += f"{subtotal.group(0)}\n"
    if sales_tax:
        formatted_text += f"{sales_tax.group(0)}\n"
    if amount_due:
        formatted_text += f"{amount_due.group(0)}\n"
    if account_summary:
        formatted_text += "\n**Account Summary:**\n"
    if previous_service:
        formatted_text += f"{previous_service.group(0)}\n"

    return formatted_text

# Function to append the formatted text to a file
def append_text_to_file(formatted_text, output_file):
    with open(output_file, 'a') as file:
        file.write(formatted_text)
        file.write("\n\n" + "="*50 + "\n\n")  # Add a separator between entries

# Main function to run the extraction and parsing for all images in a folder
def main(folder_path, output_file):
    for image_name in os.listdir(folder_path):
        if image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, image_name)
            extracted_text = extract_text_from_image(image_path)
            formatted_text = parse_invoice_text(extracted_text, image_name)
            append_text_to_file(formatted_text, output_file)
            print(f'Processed {image_name} and appended the data to {output_file}')

# Run the main function with your folder path containing the invoice images and the desired output text file
folder_path = ''
output_file = ''
main(folder_path, output_file)
