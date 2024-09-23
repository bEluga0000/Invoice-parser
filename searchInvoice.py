import re

# Function to search for an invoice based on user input
def search_invoices(text_file, search_field, search_value):
    # Read the entire content of the text file
    with open(text_file, 'r') as file:
        content = file.read()

    # Prepare the search pattern
    search_pattern = re.compile(rf"\*\*{re.escape(search_field)}:\*\* {re.escape(search_value)}", re.IGNORECASE)

    # Find all invoice blocks
    invoice_blocks = content.split("==================================================")

    # Initialize a flag to check if any matching invoice is found
    found = False

    for block in invoice_blocks:
        if search_pattern.search(block):
            print(f"Found an invoice matching {search_field} = {search_value}:\n")
            print(block.strip())
            print("==================================================")
            found = True

    if not found:
        print(f"No invoices found with {search_field} = {search_value}.")

# Main function
def main():
    # User input for field and value
    search_field = input("Enter the field to search (e.g., 'Company Name', 'Invoice No.', etc.): ").strip()
    search_value = input(f"Enter the value for '{search_field}': ").strip()

    # Path to the text file
    text_file = ''

    # Search for the invoice
    search_invoices(text_file, search_field, search_value)

# Run the main function
if __name__ == "__main__":
    main()
