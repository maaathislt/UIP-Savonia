import flet as ft

def main(page: ft.Page):
    page.title = "Expenses Tracker_LE TEXIER Mathis_s2520833"
    page.padding = 20

    # The different categories
    CATEGORIES = ["Food", "Transport", "Rent", "Tuition"]

    # Colors for each category
    COLORS = [
        ft.Colors.RED,
        ft.Colors.BLUE,
        ft.Colors.GREEN,
        ft.Colors.AMBER,
    ]

    # Here, we store the values of the expenses and we create a total
    expenses = []
    totals = {c: 0.0 for c in CATEGORIES}

    # We create a datatable to have the logs of teh data, it is composed of two columns, one for the category and one for the amount
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Category")),
            ft.DataColumn(ft.Text("Amount (€)")),
        ]
    )

    # Here, we create a pie chart with the colors that we created before, and the colors are assigned to the categories
    pie = ft.PieChart(
        sections=[
            ft.PieChartSection(
                value=0,
                title=f"{CATEGORIES[i]}: 0€",
                radius=55,
                color=COLORS[i]
            )
            for i in range(len(CATEGORIES))
        ],
        sections_space=4,
        center_space_radius=35,
    )

    # Everytime there is a new value, the pie gets updated
    def refresh_pie():
        for i, c in enumerate(CATEGORIES):
            pie.sections[i].value = totals[c]
            pie.sections[i].title = f"{c}: {totals[c]:.2f}€"
        page.update()

    # Here, we have the inputs, with the dropdown menu with the different categories
    category_dd = ft.Dropdown(
        options=[ft.dropdown.Option(c) for c in CATEGORIES],
        value=CATEGORIES[0],
        width=160,
        border_color=ft.Colors.WHITE
    )
    #Here, the amount that we want to add to the category
    amount_tf = ft.TextField(
        label="Amount (€)",
        width=160,
        border_color=ft.Colors.WHITE
    )

    # Snackbar helper
    def show_message(msg: str):
        page.snack_bar = ft.SnackBar(ft.Text(msg))
        page.snack_bar.open = True
        page.update()

    # Add Expense Handler
    def on_add(e):
        cat = category_dd.value
        amt_text = amount_tf.value.strip()
        amt = float(amt_text.replace(",", "."))

        if amt <= 0:
            show_message("Amount must be greater than 0.")
            return

        # Store expense
        expenses.append({"category": cat, "amount": amt})
        totals[cat] += amt

        # Add row to the table
        table.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(cat)),
                    ft.DataCell(ft.Text(f"{amt:.2f}")),
                ]
            )
        )

        # Update PieChart
        refresh_pie()

        # Reset field
        amount_tf.value = ""
        page.update()

    #The button that will be located on the left of the dropdown menu and the textfield for the amount
    add_btn = ft.ElevatedButton("Add Expense", on_click=on_add)

    # For the layout: We add the table and piechart side by side 
    page.add(
        ft.Text("Expense Tracker", size=24, weight="bold"),

        ft.Row([category_dd, amount_tf, add_btn], spacing=16),

        ft.Row(
            [
                ft.Column(
                    [
                        ft.Text("Expenses Table", size=18, weight="bold"),
                        table
                    ],
                    expand=True
                ),
                ft.Column(
                    [
                        ft.Text("Expenses Breakdown", size=18, weight="bold"),
                        pie
                    ],
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            ],
            spacing=30,
            expand=True
        )
    )

ft.app(target=main)