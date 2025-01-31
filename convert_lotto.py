import xml.etree.ElementTree as ET
import csv
from datetime import datetime
from decimal import Decimal
import os

def convert_amount(amount):
    if amount:
        amount = abs(int(amount))
        return f"{amount / 100:.2f}".replace('.', ',')
    return None

def convert_date(date_str):
    if date_str:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%d.%m.%Y')
    return None

def entry(writer, root, game,formatted_date, number, xml_tag1, entries):
    for record in root.findall(game):
            row = {}
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

def entry_other_taxable(writer, root, game,formatted_date, number,xml_tag1, entries):
    for record in root.findall("other"):
            for r1 in record.findall("items"):
                for r2 in r1.findall(game):
                    row = {}
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
                                element = r2.find(xml_tag1)
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
                            element = r2.find(xml_tag1)
                            row[csv_field] = convert_amount(element.text if element is not None else None)
                        elif csv_field == 'belegdatum':
                            row[csv_field] = formatted_date
                        elif csv_field == 'extbelegnr':
                            invoice_number = root.find('invoiceNumber')
                            invoice_number_value = invoice_number.text if invoice_number is not None else None
                            row[csv_field] = invoice_number_value
                        else:
                            element = r2.find(xml_tag)
                            row[csv_field] = element.text if element is not None else None
                    writer.writerow(row)

def xml_to_csv(xml_file, csv_fields):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    invoice_date = root.find('invoiceDate')
    inv = invoice_date.text if invoice_date is not None else None
    number = root.find('yearWeek')
    number = number.text if number is not None else None
    csv_file = "Buchungen Lotto [" + inv + "].csv"
    formatted_date = convert_date(invoice_date.text if invoice_date is not None else None)

    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_fields.keys(), delimiter=';')
        writer.writeheader()

        ### DRAW GAME ###

        entry1 = ["2009", "300044", "0", "0", "1", "Umsatz Lotto", "ER"]
        entry(writer, root, "drawGame",formatted_date, number, "salesAmount", entry1)

        entry2 = ["300044", "4903", "0", "17", "2", "Provision Lotto", "ER"]
        entry(writer, root, "drawGame", formatted_date, number, "salesCommission", entry2)

        entry3 = ["300044", "2009", "0", "0", "2", "Gewinnauszahlungen Lotto", "ER"]
        entry(writer, root, "drawGame", formatted_date, number, "payoutAmount", entry3)

        entry4 = ["4903", "300044", "0", "17", "1", "Minderprovision Lotto", "ER"]
        entry(writer, root, "drawGame", formatted_date, number, "administrativeFee", entry4)

        entry5 = ["300044", "2009", "0", "17", "1", "GU Gratistipps Lotto", "ER"]
        entry(writer, root, "drawGame", formatted_date, number, "creditNote", entry5)

        entry6 = ["300044", "2009", "0", "0", "2", "GU Bonustipps Lotto", "ER"]
        entry(writer, root, "drawGame", formatted_date, number, "salesBonusBet", entry6)

        entry7 = ["2009", "300044", "0", "0", "1", "Anteilspauschale Lotto", "ER"]
        entry(writer, root, "drawGame", formatted_date, number, "gameCommunityServiceFee", entry7)

        entry8 = ["300044", "2010", "0", "0", "2", "Vorschuss neu Lotto", "ER"]
        entry(writer, root, "drawGame", formatted_date, number, "advanceNew", entry8)

        entry9 = ["2010", "300044", "0", "0", "1", "Vorschuss alt Lotto", "ER"]
        entry(writer, root, "drawGame", formatted_date, number, "advanceOld", entry9)

        ### INSTANT GAME ###

        entry10 = ["2008", "300044", "0", "0", "1", "Umsatz Lose", "ER"]
        entry(writer, root, "instantGame", formatted_date, number, "salesAmount", entry10)

        entry11 = ["300044", "4903", "0", "17", "2", "Verkaufsprovision Lose", "ER"]
        entry(writer, root, "instantGame", formatted_date, number, "salesCommission", entry11)

        entry12 = ["300044", "2008", "0", "0", "2", "Ausbezahlte Gewinne Lose", "ER"]
        entry(writer, root, "instantGame", formatted_date, number, "payoutAmount", entry12)

        entry13 = ["300044", "4903", "0", "17", "2", "Auszahlungsprovision Lose", "ER"]
        entry(writer, root, "instantGame", formatted_date, number, "payoutCommission", entry13)

        entry14 = ["300044", "2008", "0", "0", "2", "Rücklose Lose", "ER"]
        entry(writer, root, "instantGame", formatted_date, number, "unsoldTicketsAmount", entry14)

        entry15 = ["4903", "300044", "0", "17", "1", "Rücklosprovision Lose", "ER"]
        entry(writer, root, "instantGame", formatted_date, number, "unsoldTicketsCommission", entry15)

        ### EUROBON ###

        entry16 = ["2008", "300044", "0", "0", "1", "Umsatz Eurobon", "ER"]
        entry(writer, root, "eurobon", formatted_date, number, "salesAmount", entry16)

        entry17 = ["300044", "4903", "0", "17", "2", "Provision Eurobon", "ER"]
        entry(writer, root, "eurobon", formatted_date, number, "salesCommission", entry17)

        ### OTHER ###

        entry18 = ["7701", "300044", "20", "2", "1", "Kommunikationsentgelt Lotto netto", "ER"]
        entry_other_taxable(writer, root, "otherTaxableItem", formatted_date, number, "amountNet", entry18)

if __name__ == "__main__":

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

    print(f"Pfad in dem Dateien zu speichern sind und die Ausgabedateien erstellt werden:")
    print({os.getcwd()})
    print("--------------------------")

    xml_to_csv('abrechnung_lotto.xml', csv_fields)
