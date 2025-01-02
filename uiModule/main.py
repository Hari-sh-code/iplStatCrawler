import tkinter as tk
from tkinter import ttk, messagebox
from data_management.list_categories import list_categories
from data_management.load_category_data import load_category_data
from data_management.validate_excel_files import validate_excel_files
from player.collect_player_stats import collect_player_stats
from player.suggest_player_names import suggest_player_names


class StatsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Player Stats")
        self.geometry("800x600")

        # Variables for categories, year, etc.
        self.selected_year = None
        self.excel_file = None
        self.categories = []
        self.selected_categories = []
        self.row_counts = {}
        self.collected_stats = []

        # Initialize the UI
        self.create_year_selection()

    def clear_frame(self):
        """Clears the current frame (removes all widgets)."""
        for widget in self.winfo_children():
            widget.destroy()

    def add_back_button(self, callback):
        """Adds a back button to the UI."""
        back_button = tk.Button(self, text="Back", command=lambda: self.go_back(callback))
        back_button.pack(pady=10)

    def go_back(self, callback):
        """Navigates back to the previous screen."""
        self.clear_frame()
        callback()

    def go_back_to_main(self):
        """Navigates back to the main screen (year selection)."""
        self.clear_frame()
        self.create_year_selection()

    def create_year_selection(self):
        """Creates the UI for year selection."""
        self.clear_frame()
        tk.Label(self, text="Select Year:").pack(pady=10)

        base_path = '../scrapeModule/statsData'
        years = validate_excel_files(base_path, range(2008, 2024 + 1))

        if not years:
            messagebox.showerror("Error", "No Excel files found for the specified years.")
            self.destroy()
            return

        self.years = years
        year_var = tk.StringVar(self)
        year_menu = ttk.Combobox(self, textvariable=year_var, values=list(years.keys()))
        year_menu.pack(pady=10)

        tk.Button(self, text="Submit", command=lambda: self.load_categories(year_var.get())).pack(pady=10)
        self.add_back_button(self.go_back_to_main)  # Add back button to go back to the main screen

    def load_categories(self, selected_year):
        """Loads categories for the selected year."""
        self.selected_year = selected_year
        self.excel_file = self.years[int(selected_year)]
        self.categories = list_categories(self.excel_file)

        if not self.categories:
            messagebox.showerror("Error", "No categories found in the file.")
            self.destroy()
            return

        self.create_category_selection()

    def create_category_selection(self):
        """Creates the UI for selecting categories."""
        self.clear_frame()
        tk.Label(self, text="Select Categories:").pack(pady=10)

        self.selected_categories = []
        for category in self.categories:
            var = tk.BooleanVar()
            tk.Checkbutton(self, text=category, variable=var).pack(anchor=tk.W)
            self.selected_categories.append((category, var))

        tk.Button(self, text="Submit", command=self.process_categories).pack(pady=10)
        self.add_back_button(self.go_back_to_main)

    def process_categories(self):
        """Processes the selected categories."""
        self.selected_categories = [cat for cat, var in self.selected_categories if var.get()]

        if not self.selected_categories:
            messagebox.showerror("Error", "No categories selected.")
            return

        self.create_display_options()

    def create_display_options(self):
        """Creates the UI for selecting display options."""
        self.clear_frame()
        self.display_option = tk.StringVar(self)

        options = ["Row count", "Display all category", "Search player", "Exit"]
        tk.Label(self, text="How would you like to display the data?").pack(pady=10)
        display_menu = ttk.Combobox(self, textvariable=self.display_option, values=options)
        display_menu.pack(pady=10)

        tk.Button(self, text="Submit", command=self.handle_display_option).pack(pady=10)
        self.add_back_button(self.go_back_to_main)

    def handle_display_option(self):
        """Handles the selected display option."""
        option = self.display_option.get()
        if option == "Row count":
            self.handle_row_count()
        elif option == "Display all category":
            self.handle_display_all()
        elif option == "Search player":
            self.handle_search_player()
        elif option == "Exit":
            self.destroy()

    def handle_row_count(self):
        """Handles displaying row count results."""
        self.clear_frame()
        self.row_counts = {}

        for selected_category in self.selected_categories:
            tk.Label(self, text=f"Select row count for category '{selected_category}' (Max. 60)").pack(pady=10)

            row_count_var = tk.IntVar(value=5)
            row_count_spinbox = tk.Spinbox(self, from_=1, to=60, textvariable=row_count_var)
            row_count_spinbox.pack(pady=10)

            self.row_counts[selected_category] = row_count_var

        tk.Button(self, text="Submit", command=self.display_row_count_results).pack(pady=10)
        self.add_back_button(self.go_back_to_main)

    def display_row_count_results(self):
        """Displays the top players based on the selected row count."""
        self.clear_frame()
        for selected_category in self.selected_categories:
            row_count = self.row_counts[selected_category].get()
            df = load_category_data(self.excel_file, selected_category)
            top_players = df.head(row_count)

            tk.Label(self, text=f"Top {row_count} players in category '{selected_category}':").pack(pady=10)
            text_box = tk.Text(self, height=10, width=150)
            text_box.pack(pady=50)
            text_box.insert(tk.END, top_players.to_string(index=False))

        self.add_back_button(self.create_display_options)

    def handle_display_all(self):
        """Handles displaying all data for the selected categories."""
        self.clear_frame()
        for selected_category in self.selected_categories:
            df = load_category_data(self.excel_file, selected_category)
            text_box = tk.Text(self, height=10, width=150)
            text_box.pack(pady=10)
            text_box.insert(tk.END, df.to_string(index=False))

        self.add_back_button(self.create_display_options)

    def handle_search_player(self):
        """Handles searching for a player."""
        self.clear_frame()
        tk.Label(self, text="Enter the player's name:").pack(pady=10)
        player_name_var = tk.StringVar()
        player_entry = tk.Entry(self, textvariable=player_name_var)
        player_entry.pack(pady=10)

        tk.Button(self, text="Submit", command=lambda: self.search_player(player_name_var.get())).pack(pady=10)
        self.add_back_button(self.create_display_options)

    def search_player(self, player_name):
        """Searches for player names matching the input."""
        self.clear_frame()
        all_suggestions = set()
        for selected_category in self.selected_categories:
            df = load_category_data(self.excel_file, selected_category)
            suggestions = suggest_player_names(df, player_name)
            all_suggestions.update(suggestions)

        if all_suggestions:
            selected_suggestion = tk.StringVar(self)
            suggestion_menu = ttk.Combobox(self, textvariable=selected_suggestion, values=list(all_suggestions))
            suggestion_menu.pack(pady=10)
            tk.Button(self, text="Submit", command=lambda: self.display_player_stats(selected_suggestion.get())).pack(pady=10)
        else:
            messagebox.showinfo("No Suggestions", f"No suggestions found for player '{player_name}'.")

    def display_player_stats(self, player_name):
        """Displays stats for the selected player."""
        self.clear_frame()
        for selected_category in self.selected_categories:
            row_count = self.row_counts.get(selected_category, 5)  # Use stored row count or default to 5
            df = load_category_data(self.excel_file, selected_category)
            player_stats = collect_player_stats(df, player_name, row_count)

            if player_stats is not None:
                tk.Label(self, text=f"Stats for player '{player_name}' in category '{selected_category}':").pack(pady=10)
                text_box = tk.Text(self, height=10, width=150)
                text_box.pack(pady=10)
                text_box.insert(tk.END, player_stats.to_string(index=False))
            else:
                messagebox.showinfo("No Stats",
                                    f"No stats found for player '{player_name}' in category '{selected_category}'.")

        self.add_back_button(self.handle_search_player)


if __name__ == "__main__":
    app = StatsApp()
    app.mainloop()
