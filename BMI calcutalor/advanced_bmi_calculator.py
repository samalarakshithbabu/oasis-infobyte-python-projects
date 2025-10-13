import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTk
import datetime

class HealthDataManager:
    def __init__(self, db_file="health_tracker.db"):
        self.database = db_file
        self.setup_storage()
    
    def setup_storage(self):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS health_data (
                record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL,
                body_weight REAL NOT NULL,
                body_height REAL NOT NULL,
                bmi_value REAL NOT NULL,
                health_status TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        connection.commit()
        connection.close()
    
    def store_measurement(self, user, weight, height, bmi, status):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO health_data (user_name, body_weight, body_height, bmi_value, health_status, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user, weight, height, bmi, status, current_time))
        connection.commit()
        connection.close()
    
    def fetch_user_data(self, username):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute('''
            SELECT * FROM health_data WHERE user_name = ? ORDER BY timestamp
        ''', (username,))
        data = cursor.fetchall()
        connection.close()
        return data
    
    def get_user_list(self):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute('SELECT DISTINCT user_name FROM health_data ORDER BY user_name')
        user_list = [row[0] for row in cursor.fetchall()]
        connection.close()
        return user_list

class BodyMassIndexProcessor:
    @staticmethod
    def compute_bmi(mass, height_m):
        return mass / (height_m * height_m)
    
    @staticmethod
    def determine_category(bmi_score):
        if bmi_score < 18.5:
            return "Underweight"
        elif bmi_score < 25:
            return "Healthy Weight"
        elif bmi_score < 30:
            return "Overweight"
        elif bmi_score < 35:
            return "Obese Class 1"
        elif bmi_score < 40:
            return "Obese Class 2"
        else:
            return "Obese Class 3"
    
    @staticmethod
    def provide_guidance(health_category):
        recommendations = {
            "Underweight": "Focus on nutrient-dense foods and strength training exercises.",
            "Healthy Weight": "Continue your balanced lifestyle with regular physical activity.",
            "Overweight": "Incorporate cardio exercises and monitor portion sizes.",
            "Obese Class 1": "Seek professional guidance for sustainable weight management.",
            "Obese Class 2": "Consider medical supervision for comprehensive health planning.",
            "Obese Class 3": "Urgent medical consultation recommended for optimal health outcomes."
        }
        return recommendations.get(health_category, "Consult healthcare professionals for personalized advice.")

class HealthTrackerInterface:
    def __init__(self, main_window):
        self.window = main_window
        self.window.title("Personal Health & BMI Tracker")
        self.window.geometry("850x650")
        self.window.configure(bg='#e8f4f8')
        
        self.data_manager = HealthDataManager()
        self.bmi_processor = BodyMassIndexProcessor()
        
        self.build_interface()
    
    def build_interface(self):
        self.tab_container = ttk.Notebook(self.window)
        self.tab_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        self.build_calculator_section()
        self.build_records_section()
        self.build_visualization_section()
    
    def build_calculator_section(self):
        calculator_tab = ttk.Frame(self.tab_container)
        self.tab_container.add(calculator_tab, text="Health Calculator")
        
        header = tk.Label(calculator_tab, text="BMI Health Calculator", 
                         font=('Segoe UI', 22, 'bold'), bg='#e8f4f8', fg='#2c3e50')
        header.pack(pady=25)
        
        form_container = ttk.Frame(calculator_tab)
        form_container.pack(pady=25)
        
        ttk.Label(form_container, text="Full Name:", font=('Segoe UI', 11)).grid(row=0, column=0, sticky='w', padx=8, pady=8)
        self.user_name = tk.StringVar()
        ttk.Entry(form_container, textvariable=self.user_name, width=25, font=('Segoe UI', 10)).grid(row=0, column=1, padx=8, pady=8)
        
        ttk.Label(form_container, text="Body Weight (kg):", font=('Segoe UI', 11)).grid(row=1, column=0, sticky='w', padx=8, pady=8)
        self.body_weight = tk.StringVar()
        ttk.Entry(form_container, textvariable=self.body_weight, width=25, font=('Segoe UI', 10)).grid(row=1, column=1, padx=8, pady=8)
        
        ttk.Label(form_container, text="Height (meters):", font=('Segoe UI', 11)).grid(row=2, column=0, sticky='w', padx=8, pady=8)
        self.body_height = tk.StringVar()
        ttk.Entry(form_container, textvariable=self.body_height, width=25, font=('Segoe UI', 10)).grid(row=2, column=1, padx=8, pady=8)
        
        process_btn = tk.Button(calculator_tab, text="Process Health Data", 
                               command=self.process_health_calculation, 
                               bg='#3498db', fg='white', font=('Segoe UI', 13, 'bold'),
                               relief='flat', padx=20, pady=8)
        process_btn.pack(pady=25)
        
        self.output_container = ttk.Frame(calculator_tab)
        self.output_container.pack(pady=25)
        
        self.health_result = tk.Label(self.output_container, text="", 
                                     font=('Segoe UI', 15, 'bold'), bg='#e8f4f8', fg='#27ae60')
        self.health_result.pack()
        
        self.guidance_text = tk.Label(self.output_container, text="", 
                                     font=('Segoe UI', 11), bg='#e8f4f8', fg='#34495e', wraplength=450)
        self.guidance_text.pack(pady=15)
    
    def build_records_section(self):
        records_tab = ttk.Frame(self.tab_container)
        self.tab_container.add(records_tab, text="Health Records")
        
        selection_panel = ttk.Frame(records_tab)
        selection_panel.pack(pady=15)
        
        ttk.Label(selection_panel, text="Choose User:", font=('Segoe UI', 12)).pack(side='left', padx=8)
        self.selected_user = tk.StringVar()
        self.user_selector = ttk.Combobox(selection_panel, textvariable=self.selected_user, width=25, font=('Segoe UI', 10))
        self.user_selector.pack(side='left', padx=8)
        
        load_btn = tk.Button(selection_panel, text="Display Records", 
                            command=self.display_user_records, bg='#e74c3c', fg='white',
                            font=('Segoe UI', 11), relief='flat')
        load_btn.pack(side='left', padx=8)
        
        self.records_display = ttk.Treeview(records_tab, 
                                           columns=('Timestamp', 'Weight', 'Height', 'BMI', 'Status'),
                                           show='headings')
        
        for column in self.records_display['columns']:
            self.records_display.heading(column, text=column)
            self.records_display.column(column, width=140)
        
        self.records_display.pack(fill='both', expand=True, padx=15, pady=15)
        
        records_scroll = ttk.Scrollbar(records_tab, orient='vertical', command=self.records_display.yview)
        self.records_display.configure(yscrollcommand=records_scroll.set)
        records_scroll.pack(side='right', fill='y')
    
    def build_visualization_section(self):
        viz_tab = ttk.Frame(self.tab_container)
        self.tab_container.add(viz_tab, text="Health Analytics")
        
        controls_panel = ttk.Frame(viz_tab)
        controls_panel.pack(pady=15)
        
        ttk.Label(controls_panel, text="Select User:", font=('Segoe UI', 12)).pack(side='left', padx=8)
        self.viz_user_selection = tk.StringVar()
        self.viz_user_combo = ttk.Combobox(controls_panel, textvariable=self.viz_user_selection, width=25, font=('Segoe UI', 10))
        self.viz_user_combo.pack(side='left', padx=8)
        
        create_chart_btn = tk.Button(controls_panel, text="Create Visualization", 
                                    command=self.create_health_chart, bg='#9b59b6', fg='white',
                                    font=('Segoe UI', 11), relief='flat')
        create_chart_btn.pack(side='left', padx=8)
        
        self.visualization_area = ttk.Frame(viz_tab)
        self.visualization_area.pack(fill='both', expand=True, padx=15, pady=15)
    
    def verify_user_input(self):
        try:
            username = self.user_name.get().strip()
            if not username:
                raise ValueError("Please enter your full name")
            
            weight_kg = float(self.body_weight.get())
            if weight_kg <= 0 or weight_kg > 600:
                raise ValueError("Weight must be between 1 and 600 kg")
            
            height_m = float(self.body_height.get())
            if height_m <= 0 or height_m > 2.5:
                raise ValueError("Height must be between 0.1 and 2.5 meters")
            
            return username, weight_kg, height_m
        except ValueError as error:
            messagebox.showerror("Data Validation Error", str(error))
            return None, None, None
    
    def process_health_calculation(self):
        username, weight_kg, height_m = self.verify_user_input()
        if username is None:
            return
        
        bmi_score = self.bmi_processor.compute_bmi(weight_kg, height_m)
        health_status = self.bmi_processor.determine_category(bmi_score)
        health_guidance = self.bmi_processor.provide_guidance(health_status)
        
        self.health_result.config(text=f"BMI Score: {bmi_score:.2f} | Status: {health_status}")
        self.guidance_text.config(text=health_guidance)
        
        self.data_manager.store_measurement(username, weight_kg, height_m, bmi_score, health_status)
        
        self.refresh_user_selections()
        
        messagebox.showinfo("Processing Complete", "Health data calculated and stored successfully!")
    
    def refresh_user_selections(self):
        available_users = self.data_manager.get_user_list()
        self.user_selector['values'] = available_users
        self.viz_user_combo['values'] = available_users
    
    def display_user_records(self):
        selected_user = self.selected_user.get()
        if not selected_user:
            messagebox.showwarning("Selection Required", "Please choose a user from the dropdown")
            return
        
        for item in self.records_display.get_children():
            self.records_display.delete(item)
        
        user_data = self.data_manager.fetch_user_data(selected_user)
        for entry in user_data:
            self.records_display.insert('', 'end', values=(
                entry[6], entry[2], entry[3], f"{entry[4]:.2f}", entry[5]
            ))
    
    def create_health_chart(self):
        chart_user = self.viz_user_selection.get()
        if not chart_user:
            messagebox.showwarning("User Selection Required", "Please select a user for visualization")
            return
        
        health_records = self.data_manager.fetch_user_data(chart_user)
        if not health_records:
            messagebox.showinfo("No Data Found", "No health records available for the selected user")
            return
        
        for widget in self.visualization_area.winfo_children():
            widget.destroy()
        
        time_points = [datetime.datetime.strptime(record[6], "%Y-%m-%d %H:%M:%S") for record in health_records]
        bmi_values = [record[4] for record in health_records]
        
        figure, axis = plt.subplots(figsize=(11, 7))
        axis.plot(time_points, bmi_values, marker='s', linewidth=3, markersize=8, color='#e74c3c')
        axis.set_title(f'Health Progress Tracking - {chart_user}', fontsize=18, fontweight='bold', color='#2c3e50')
        axis.set_xlabel('Timeline', fontsize=14, color='#34495e')
        axis.set_ylabel('BMI Index', fontsize=14, color='#34495e')
        axis.grid(True, alpha=0.4, linestyle='--')
        
        axis.axhspan(0, 18.5, alpha=0.15, color='lightblue', label='Underweight Zone')
        axis.axhspan(18.5, 25, alpha=0.15, color='lightgreen', label='Healthy Zone')
        axis.axhspan(25, 30, alpha=0.15, color='orange', label='Overweight Zone')
        axis.axhspan(30, 50, alpha=0.15, color='lightcoral', label='Obesity Zone')
        
        axis.legend(loc='upper right')
        plt.xticks(rotation=50)
        plt.tight_layout()
        
        chart_canvas = FigureCanvasTk(figure, self.visualization_area)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def launch_application(self):
        self.refresh_user_selections()
        self.window.mainloop()

def initialize_health_tracker():
    application_window = tk.Tk()
    health_app = HealthTrackerInterface(application_window)
    health_app.launch_application()

if __name__ == "__main__":
    initialize_health_tracker()