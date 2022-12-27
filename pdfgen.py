import os
import csv
import pdfkit
import webbrowser
import money
from item import Item
from datetime import datetime
from typing import Iterable
from dotenv import load_dotenv

CHROME_PATH = 'usr/bin/google-chrome'


class PDFGenerator:

    def __init__(self) -> None:
        load_dotenv()
        pass

    def arm_row(self, item: Item) -> str:
        row = ""
        row += '<tr>'
        row += '    <td style="text-align: center;">{}</td>'.format(item.quantity)
        row += '    <td> {} </td>'.format(item.detail)
        row += '    <td style="text-align: right;">$ {} </td>'.format(money.convert(item.price))
        row += '    <td style="text-align: center;"> {} </td>'.format(str(money.convert(item.aliquot)) + " %" if item.aliquot > 0 else "-")
        row += '    <td style="text-align: right;">$ {} </td>'.format(money.convert(item.total))
        row += '</tr>'

        return row

    def gen_budget(self, items: Iterable[Item]):
        customer = input("Cliente: ")

        template_path = './templates/budget.html'
        html_output_path = './outputs/html/budget.html'
        title = 'Presupuesto {} {}'.format(customer, datetime.now().strftime('%Y-%m-%d'))
        output_path = './outputs/prints/' + title.replace(' ', '-') + '.pdf'

        with open(template_path) as template:

            filedata = template.read()

            rows = ""
            subtotal = 0
            total = 0
            tribute = 0
            for item in items:
                total += item.total
                subtotal += item.price
                tribute += item.tribute
                rows += self.arm_row(item)

            filedata = filedata.replace('[[LOGO]]', os.getenv('LOGO'))
            filedata = filedata.replace('[[PHONE]]', os.getenv('PHONE'))
            filedata = filedata.replace('[[EMAIL]]', os.getenv('EMAIL'))
            filedata = filedata.replace('[[DATE]]', datetime.now().strftime('%d/%m/%Y'))
            filedata = filedata.replace('[[TITLE]]', title)
            filedata = filedata.replace('[[CUSTOMER]]', customer)
            filedata = filedata.replace('[[ITEMS]]', rows)
            filedata = filedata.replace('[[SUBTOTAL]]', '$ {}'.format(money.convert(subtotal)))
            filedata = filedata.replace('[[TRIBUTE]]', '$ {}'.format(money.convert(tribute))if tribute > 0 else ' - ')
            filedata = filedata.replace('[[TOTAL]]', '$ {}'.format(money.convert(total)))

            with open(html_output_path, 'w') as file:
                file.write(filedata)

            options = {'enable-local-file-access': None}
            pdfkit.from_file(html_output_path, output_path, options=options)
            webbrowser.get(using='google-chrome').open_new(output_path)

    def read_csv(self,):
        with open("./items.csv", 'r') as file:

            items = []
            csvreader = csv.reader(file)

            for row in csvreader:
                quantity = int(row[0])
                detail = row[1].strip()
                price = float(row[2])
                aliquot = float(row[3]) if len(row) > 3 else None
                items.append(Item(quantity, detail, price, aliquot))

            self.gen_budget(items)
