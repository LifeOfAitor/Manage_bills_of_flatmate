import FreeSimpleGUI as sg
from datetime import datetime
from FlatmateClass import Flatmate
from PDFReportClass import PdfReport
import locale

# Constants for keys to avoid typos and ensure consistency
KEY_FLATMATE_DROPDOWN = "flatmate"
KEY_DESCRIPTION_INPUT = "description"
KEY_AMOUNT_INPUT = "amount"
KEY_IS_COMMON_CHECKBOX = "is_common"
KEY_CONFIRM_LABEL = "confirm_label"
KEY_GENERATE_REPORT = "generate_report"
KEY_EXIT = "exit"

class ExpenseApp:
    def __init__(self, flatmate1, flatmate2):
        self.flatmates = {flatmate1.name: flatmate1, flatmate2.name: flatmate2}

        # Set the light theme for the GUI
        sg.theme("LightGreen")

        # spanish for date time
        locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
        self.current_date = datetime.now()

        # Define the components of the GUI
        text_title = sg.Text(f"CUENTAS {self.current_date.strftime('%B').upper()} {self.current_date.year}", justification="c",
                             size=(30, 1))

        # Replace Combo with Radio Buttons
        radio_flatmate1 = sg.Radio(flatmate1.name, "FLATMATE", key=f"{flatmate1.name}_radio", default=True)
        radio_flatmate2 = sg.Radio(flatmate2.name, "FLATMATE", key=f"{flatmate2.name}_radio")

        text_expense = (sg.Text("Gasto:"), sg.InputText(key=KEY_DESCRIPTION_INPUT, size=(10, 1)))
        text_price = (sg.Text("Coste:"), sg.InputText(key=KEY_AMOUNT_INPUT, size=(10, 1)))
        shared = sg.Checkbox("Gasto común", key=KEY_IS_COMMON_CHECKBOX)

        # Add elements to layout
        layout = [
            [text_title],
            [radio_flatmate1, radio_flatmate2],
            [text_expense],
            [text_price],
            [shared],
            [sg.Button("Añadir"),
             sg.Button("Generar PDF", key=KEY_GENERATE_REPORT),
             sg.Button("Salir", key=KEY_EXIT)],
            [sg.Text("", key=KEY_CONFIRM_LABEL, size=(40, 1), text_color="green", justification="center")]
        ]

        # Create the window
        self.window = sg.Window("Expense Tracker", layout,
                                element_justification='c',
                                resizable=True, finalize=True,
                                font=("Calibri", 25))

        # Main event loop for the application
        self.run()

    def run(self):
        while True:
            event, values = self.window.read()

            # If the window is closed or the "Exit" button is pressed, break the loop
            if event in (sg.WIN_CLOSED, KEY_EXIT):
                break

            # Add Expense button pressed
            if event == "Añadir":
                self.add_expense(values)

            # Generate Report button pressed
            elif event == KEY_GENERATE_REPORT:
                self.generate_report()

        # Close the window when the loop ends
        self.window.close()

    def add_expense(self, values):
        # Determine selected flatmate based on radio button selection
        selected_flatmate = self.flatmates[values[f"{list(self.flatmates.keys())[0]}_radio"] and list(self.flatmates.keys())[0] or list(self.flatmates.keys())[1]]
        description = values[KEY_DESCRIPTION_INPUT]
        is_common = values[KEY_IS_COMMON_CHECKBOX]

        # Input validation
        if not description:
            self.window[KEY_CONFIRM_LABEL].update("Introduce un valor válido", text_color="red")
            return

        try:
            amount = float(values[KEY_AMOUNT_INPUT])
        except ValueError:
            self.window[KEY_CONFIRM_LABEL].update("Introduce la cantidad correctamente", text_color="red")
            return

        # Add expense to the selected flatmate
        selected_flatmate.add_expense(description, amount, is_common)
        self.window[KEY_CONFIRM_LABEL].update(f"{description} añadido para {selected_flatmate.name} ({amount:.2f})", text_color="green")

        # Clear inputs
        self.window[KEY_DESCRIPTION_INPUT].update("")
        self.window[KEY_AMOUNT_INPUT].update("")
        self.window[KEY_IS_COMMON_CHECKBOX].update(False)

    def generate_report(self):
        month_year = f"{self.current_date.strftime('%B')}_{self.current_date.year}"
        filename = f"{month_year}_report.pdf"
        pdf_report = PdfReport(filename)
        pdf_report.generate(*self.flatmates.values())
        self.window[KEY_CONFIRM_LABEL].update(f"{filename} generado correctamente", text_color="green")

if __name__ == "__main__":
    aitor = Flatmate("Flatmate1")
    irene = Flatmate("Flatmate2")
    app = ExpenseApp(aitor, irene)
