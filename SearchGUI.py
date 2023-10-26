import tkinter as tk
import csv
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import os
import re
from reportlab.platypus import Image
import subprocess
import platform
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph


def generate_heading_text(search_id, search_day, search_month, search_year, day_limit, month_limit, year_limit):
    heading_text = "BRB Groups Attendance Report"
    #
    # if search_id:
    #     heading_text += f"Employee ID {search_id}"
    # else:
    #     date_range = []
    #     if search_day and search_month and search_year:
    #         start_date = f"{search_year}-{search_month}-{search_day}"
    #         date_range.append(start_date)
    #     if day_limit and month_limit and year_limit:
    #         end_date = f"{year_limit}-{month_limit}-{day_limit}"
    #         date_range.append(end_date)
    #
    #     if date_range:
    #         heading_text += "the Date " + " to ".join(date_range)
    #     else:
    #         heading_text += "All"

    return heading_text


def open_pdf(pdf_path):
    system = platform.system()
    if system == 'Windows':
        os.startfile(pdf_path)
    elif system == 'Linux':
        subprocess.run(['xdg-open', pdf_path])
    elif system == 'Darwin':  # macOS
        subprocess.run(['open', pdf_path])
    else:
        print(f'Unsupported platform: {system}')


rows = []
image_paths = []


def generate_pdf(rows):
    pdf_name = 'attendance_search_results.pdf'
    doc = SimpleDocTemplate(pdf_name, pagesize=landscape(letter))

    # Create table data
    table_data = [["ID", "Day", "Month", "Year", "Time"]] + rows
    table = Table(table_data)

    # Add table styles
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    # Generate heading text
    heading_text = generate_heading_text(search_id, search_day, search_month, search_year, day_limit, month_limit,
                                         year_limit)

    # Create the heading Paragraph
    heading_style = ParagraphStyle('Heading', fontSize=18, alignment=1, spaceAfter=20)
    heading = Paragraph(heading_text, heading_style)

    # Add the heading, table, and images to the elements list
    elements = [heading, table]

    # Add "Unrecognized Pictures" heading before images
    if image_paths:
        heading_style = ParagraphStyle('Heading', fontSize=18, alignment=1, spaceAfter=20, underline=True)
        heading = Paragraph("Unrecognized Faces", heading_style)
        elements.append(heading)

    # Add images to the PDF
    for img_path in image_paths:
        img = Image(img_path, width=200, height=100)
        img.hAlign = 'CENTER'
        elements.append(img)

    # Build the PDF
    doc.build(elements)

    open_pdf(pdf_name)

# Function to search for ID in attendance.csv and return matching rows
def search_id():
    global rows, image_paths, search_day, search_month, search_year, day_limit, month_limit, year_limit
    search_id = id_entry.get()
    search_day = day_entry.get()
    search_month = month_entry.get()
    search_year = year_entry.get()
    year_limit = year_limit_entry.get()
    month_limit = month_limit_entry.get()
    day_limit = day_limit_entry.get()

    with open('attendance.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header row
        rows = [row for row in reader if
                (not search_id or row[0] == search_id) and
                (not search_day or (search_day != '' and search_day.isdigit() and int(row[2]) >= int(search_day)) and
                 (not day_limit or (day_limit != '' and day_limit.isdigit() and int(row[2]) <= int(day_limit)))) and
                (not search_month or (
                        search_month != '' and search_month.isdigit() and int(row[3]) >= int(search_month))) and
                (not month_limit or (
                        month_limit != '' and month_limit.isdigit() and int(row[3]) <= int(month_limit))) and
                (not search_year or (
                        search_year != '' and search_year.isdigit() and int(row[4]) >= int(search_year))) and
                (not year_limit or (year_limit != '' and year_limit.isdigit() and int(row[4]) <= int(year_limit)))]

    # Find the matching image file paths
    image_folder = 'Unrecognized'
    pattern = re.compile(r'unrecognized_(\d{4})(\d{2})(\d{2})_(\d{6})\.png')
    image_paths = []

    for img_name in os.listdir(image_folder):
        match = pattern.match(img_name)
        if match:
            img_year, img_month, img_day, img_time = map(int, match.groups())
            if (
                    (not search_day or (search_day != '' and search_day.isdigit() and img_day >= int(search_day))) and
                    (not day_limit or (day_limit != '' and day_limit.isdigit() and img_day <= int(day_limit))) and
                    (not search_month or (
                            search_month != '' and search_month.isdigit() and img_month >= int(search_month))) and
                    (not month_limit or (
                            month_limit != '' and month_limit.isdigit() and img_month <= int(month_limit))) and
                    (not search_year or (
                            search_year != '' and search_year.isdigit() and img_year >= int(search_year))) and
                    (not year_limit or (year_limit != '' and year_limit.isdigit() and img_year <= int(year_limit)))
            ):
                image_paths.append(os.path.join(image_folder, img_name))
                print(os.path.join(image_folder, img_name))
    print(image_paths)
    result_text.delete('1.0', tk.END)  # Clear any previous search results
    result_text.insert(tk.END, "ID     Day Month Year Time" + '\n')
    if rows:
        for row in rows:
            result_text.insert(tk.END, ', '.join(row) + '\n')
    else:
        result_text.insert(tk.END, 'No matching rows found.')


# Create the GUI
root = tk.Tk()
root.title('Attendance Search')

# Add label and entry field for ID input
id_label = tk.Label(root, text='Enter ID:')
id_label.grid(row=0, column=0)
id_entry = tk.Entry(root)
id_entry.grid(row=0, column=1)

day_label = tk.Label(root, text='Enter Day:')
day_label.grid(row=1, column=0)
day_entry = tk.Entry(root)
day_entry.grid(row=1, column=1)

month_label = tk.Label(root, text='Enter Month:')
month_label.grid(row=2, column=0)
month_entry = tk.Entry(root)
month_entry.grid(row=2, column=1)

year_label = tk.Label(root, text='Enter Year:')
year_label.grid(row=3, column=0)
year_entry = tk.Entry(root)
year_entry.grid(row=3, column=1)

year_limit_label = tk.Label(root, text='Year Limit:')
year_limit_label.grid(row=3, column=2)
year_limit_entry = tk.Entry(root)
year_limit_entry.grid(row=3, column=3)

month_limit_label = tk.Label(root, text='Month Limit:')
month_limit_label.grid(row=2, column=2)
month_limit_entry = tk.Entry(root)
month_limit_entry.grid(row=2, column=3)

day_limit_label = tk.Label(root, text='Day Limit:')
day_limit_label.grid(row=1, column=2)
day_limit_entry = tk.Entry(root)
day_limit_entry.grid(row=1, column=3)

# Add button to initiate search
search_button = tk.Button(root, text='Search', command=search_id)
search_button.grid(row=4, column=2)

pdf_button = tk.Button(root, text='Export PDF', command=lambda: generate_pdf(rows))
pdf_button.grid(row=4, column=3)

# Add text box to display search results
result_text = tk.Text(root, height=10, width=50)
result_text.grid(row=5, column=0, columnspan=3)

root.mainloop()