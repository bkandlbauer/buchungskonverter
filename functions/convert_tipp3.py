import xml.etree.ElementTree as ET
import csv
from datetime import datetime
from decimal import Decimal
from io import StringIO


csv_fields = {
        'satzart': None,
        'konto': None,        
        'gkonto': None,
        'belegnr': None,
        'belegdatum': None,
        'prozent': None,
        'steuercode': None,
        'buchcode': None,
        'betrag': None,      
        'steuer': None,
        'skonto': None,
        'text': None,
        'buchsymbol': None,
        'extbelegnr': None,
    }

def convert_amount(amount):
    """Convert the amount from integer (e.g., -6700) to a string in the format "-67,00"."""
    if amount:
        amount = abs(int(amount))
        return f"{amount / 100:.2f}".replace('.', ',')
    return None

def convert_amount2(amount):
    """Convert the amount from integer (e.g., -6700) to a string in the format "-67,00"."""
    if amount:
        amount = abs(int(amount)) * 1.2
        return f"{amount / 100:.2f}".replace('.', ',')
    return None

def convert_date(date_str):
    """Convert the date from 'YYYY-MM-DD' to 'DD.MM.YYYY'."""
    if date_str:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%d.%m.%Y')
    return None

def entry(writer, root, formatted_date, number, xml_tag1, entries):
    for record in root.findall('drawGame'):
            row = {}
            calc_tax = 0
            for csv_field, xml_tag in csv_fields.items():
                if csv_field == 'konto':
                    row[csv_field] = entries[0]
                elif csv_field == 'satzart':
                    row[csv_field] = '0'
                elif csv_field == 'gkonto':
                    row[csv_field] = entries[1]
                elif csv_field == 'belegnr':
                    row[csv_field] = number
                elif csv_field == 'prozent':
                    row[csv_field] = entries[2]
                elif csv_field == 'steuercode':
                    row[csv_field] = entries[3]
                elif csv_field == 'buchcode':
                    row[csv_field] = entries[4]
                elif csv_field == 'steuer':
                    if(entries[2] != "0"):
                        element = record.find(xml_tag1)
                        amount = convert_amount(element.text if element is not None else None)
                        convert_amount_decimal_format = amount.replace(',', '.')
                        calc_tax = Decimal(convert_amount_decimal_format) * Decimal('0.2')
                        tax = f"{calc_tax:.2f}".replace('.', ',')
                        row[csv_field] = tax
                    else:
                        row[csv_field] = '0'
                elif csv_field == 'skonto':
                    row[csv_field] = '0'
                elif csv_field == 'text':
                    row[csv_field] = entries[5]
                elif csv_field == 'buchsymbol':
                    row[csv_field] = entries[6]
                elif csv_field == 'betrag':
                    element = record.find(xml_tag1)
                    if(xml_tag1 == "salesCommission" ):
                        row[csv_field] = convert_amount2(element.text if element is not None else None)
                    elif(xml_tag1 == "affiliateCommission" ):
                        row[csv_field] = convert_amount2(element.text if element is not None else None)
                    else:
                        row[csv_field] = convert_amount(element.text if element is not None else None)
                elif csv_field == 'belegdatum':
                    row[csv_field] = formatted_date
                elif csv_field == 'extbelegnr':
                    invoice_number = root.find('invoiceNumber')
                    invoice_number_value = invoice_number.text if invoice_number is not None else None
                    row[csv_field] = invoice_number_value
                else:
                    element = record.find(xml_tag)
                    row[csv_field] = element.text if element is not None else None
            writer.writerow(row)

def xml_to_csv_tipp3(xml_file):
    root = ET.fromstring(xml_file)

    invoice_date = root.find('invoiceDate')
    number = root.find('yearWeek')
    number = number.text if number is not None else None
    formatted_date = convert_date(invoice_date.text if invoice_date is not None else None)

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=csv_fields.keys(), delimiter=';')
    writer.writeheader()

    entry1 = ["2007", "300043", "0", "0", "1", "Umsatz Tipp 3", "ER"]
    entry(writer, root, formatted_date, number, "salesAmount", entry1)

    entry2 = ["300043", "4902", "20", "1", "2", "Umsatzprovision Tipp 3", "ER"]
    entry(writer, root, formatted_date, number, "salesCommission", entry2)

    entry3 = ["300043", "2007", "0", "0", "2", "Gewinnauszahlung Tipp 3", "ER"]
    entry(writer, root, formatted_date, number, "payoutAmount", entry3)

    entry4 = ["4902", "300043", "20", "1", "1", "Minderprovision Tipp 3", "ER"]
    entry(writer, root, formatted_date, number, "administrativeFee", entry4)

    entry6 = ["300043", "4902", "20", "1", "2", "Partnerprogramm Provision Tipp 3", "ER"]
    entry(writer, root, formatted_date, number, "affiliateCommission", entry6)

    entry7 = ["300043", "2007", "0", "0", "2", "Promotion-Guthaben Tipp 3", "ER"]
    entry(writer, root, formatted_date, number, "voucherSales", entry7)

    return output.getvalue()
