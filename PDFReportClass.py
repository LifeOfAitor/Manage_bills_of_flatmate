import os
import webbrowser
from datetime import datetime
from fpdf import FPDF


class PdfReport:
    def __init__(self, filename):
        self.filename = filename

    def generate(self, flatmate1, flatmate2):
        # Individual expenses for each one
        individual_flatmate1 = flatmate1.total_individual_expenses()
        individual_flatmate2 = flatmate2.total_individual_expenses()

        # Common expenses total
        common_flatmate1 = flatmate1.total_common_expenses()
        common_flatmate2 = flatmate2.total_common_expenses()

        # Round common expenses
        common_total_each = (common_flatmate1 + common_flatmate2) / 2

        # Calculate the total expense without rounding
        total1 = individual_flatmate1 + common_total_each
        total2 = individual_flatmate2 + common_total_each

        # Determine who owes whom and by how much
        if common_flatmate1 > common_flatmate2:
            owes = flatmate2.name
            owed = flatmate1.name
            amount = round((common_flatmate1 - common_flatmate2) / 2, 2)
        else:
            owes = flatmate1.name
            owed = flatmate2.name
            amount = round((common_flatmate2 - common_flatmate1) / 2, 2)

        pdf = FPDF(orientation="P", unit="pt", format="a4")
        pdf.add_page()

        # Title and total expenses
        pdf.set_font(family="Times", style="B", size=20)
        pdf.cell(w=0, h=60,
                 txt=f"Gastos para {flatmate1.name} e {flatmate2.name}".upper(),
                 border=0, align="C", ln=1)

        pdf.set_font(family="Times", size=12)
        pdf.cell(w=0, h=15,
                 txt=f"Gastos totales de {flatmate1.name}: {total1:.2f}",
                 border=0, ln=1, align="L")
        pdf.cell(w=0, h=15,
                 txt=f"Gastos totales de {flatmate2.name}: {total2:.2f}",
                 border=0, ln=1, align="L")

        # Individual expenses section
        pdf.set_font(family="Times", style="B", size=14)
        pdf.cell(w=0, h=25, txt="Gastos de cada uno:", border=0, ln=1,
                 align="L")

        for flatmate in [flatmate1, flatmate2]:
            pdf.set_font(family="Times", style="B", size=12)
            pdf.cell(w=0, h=20, txt=f"Gastos de {flatmate.name}:", border=0,
                     ln=1, align="L")
            pdf.set_font(family="Times", size=12)
            for expense in flatmate.expenses:
                type_of_expense = "Común" if expense['is_common'] else "Personal"
                pdf.cell(w=200, h=15,
                         txt=f"{expense['description']} ({type_of_expense})",
                         border=0, align="L")
                pdf.cell(w=100, h=15, txt=f"{expense['amount']:.2f}", border=0,
                         ln=1, align="R")
            pdf.cell(w=0, h=15,
                     txt=f"Total gastos personales de {flatmate.name}: {flatmate.total_individual_expenses():.2f}",
                     border=0, ln=1, align="L")

        # Common expenses section
        pdf.set_font(family="Times", style="B", size=14)
        pdf.cell(w=0, h=25, txt="Gastos comunes", border=0, ln=1, align="L")
        pdf.set_font(family="Times", size=12)
        for expense in flatmate1.expenses + flatmate2.expenses:
            if expense['is_common']:
                pdf.cell(w=200, h=15, txt=f"{expense['description']}", border=0,
                         align="L")
                pdf.cell(w=100, h=15, txt=f"{expense['amount']:.2f}", border=0,
                         ln=1, align="R")

        # Settlement section
        pdf.set_font(family="Times", style="B", size=14)
        pdf.cell(w=0, h=25, txt="Resumen:", border=0, ln=1, align="L")
        pdf.set_font(family="Times", size=12)
        pdf.cell(w=0, h=15,
                 txt=f"{owes} debe a {owed} {amount:.2f}",
                 border=0, ln=1, align="L")

        # Output PDF using a relative path
        output_folder = os.path.join(os.getcwd(), "cuentas_mensuales_alquiler")
        os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

        pdf_path = os.path.join(output_folder, self.filename)
        pdf.output(pdf_path)
        webbrowser.open("file://" + os.path.realpath(pdf_path))
