import sys
import requests
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                              QTableWidget, QTableWidgetItem, QMessageBox, 
                              QComboBox, QGroupBox, QLineEdit, QTabWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

API_BASE_URL = 'http://localhost:8000/api'


class ChemicalVisualizerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.session = requests.Session()
        self.current_dataset = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Chemical Equipment Visualizer - Desktop')
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Title
        title = QLabel('🧪 Chemical Equipment Visualizer')
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('color: #667eea; padding: 10px;')
        main_layout.addWidget(title)
        
        # Auth section
        auth_group = QGroupBox('Authentication')
        auth_layout = QHBoxLayout()
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Username')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.login_btn = QPushButton('Login')
        self.login_btn.clicked.connect(self.handle_login)
        self.logout_btn = QPushButton('Logout')
        self.logout_btn.clicked.connect(self.handle_logout)
        self.logout_btn.setEnabled(False)
        
        self.auth_status_label = QLabel('Not logged in')
        
        auth_layout.addWidget(QLabel('Username:'))
        auth_layout.addWidget(self.username_input)
        auth_layout.addWidget(QLabel('Password:'))
        auth_layout.addWidget(self.password_input)
        auth_layout.addWidget(self.login_btn)
        auth_layout.addWidget(self.logout_btn)
        auth_layout.addWidget(self.auth_status_label)
        auth_layout.addStretch()
        
        auth_group.setLayout(auth_layout)
        main_layout.addWidget(auth_group)
        
        # Upload section
        upload_group = QGroupBox('Upload CSV Data')
        upload_layout = QHBoxLayout()
        
        self.file_label = QLabel('No file selected')
        self.select_file_btn = QPushButton('Select CSV File')
        self.select_file_btn.clicked.connect(self.select_file)
        
        self.upload_btn = QPushButton('Upload & Analyze')
        self.upload_btn.clicked.connect(self.upload_file)
        self.upload_btn.setEnabled(False)
        
        upload_layout.addWidget(self.file_label)
        upload_layout.addWidget(self.select_file_btn)
        upload_layout.addWidget(self.upload_btn)
        upload_layout.addStretch()
        
        upload_group.setLayout(upload_layout)
        main_layout.addWidget(upload_group)
        
        # Dataset selection
        dataset_group = QGroupBox('Recent Datasets')
        dataset_layout = QHBoxLayout()
        
        dataset_layout.addWidget(QLabel('Select Dataset:'))
        self.dataset_combo = QComboBox()
        self.dataset_combo.currentIndexChanged.connect(self.on_dataset_selected)
        dataset_layout.addWidget(self.dataset_combo)
        
        self.refresh_btn = QPushButton('Refresh List')
        self.refresh_btn.clicked.connect(self.load_datasets)
        dataset_layout.addWidget(self.refresh_btn)
        
        self.download_pdf_btn = QPushButton('Download PDF Report')
        self.download_pdf_btn.clicked.connect(self.download_pdf)
        self.download_pdf_btn.setEnabled(False)
        dataset_layout.addWidget(self.download_pdf_btn)
        
        dataset_layout.addStretch()
        
        dataset_group.setLayout(dataset_layout)
        main_layout.addWidget(dataset_group)
        
        # Tabs for data and charts
        self.tabs = QTabWidget()
        
        # Summary tab
        summary_tab = QWidget()
        summary_layout = QVBoxLayout()
        self.summary_label = QLabel('No data loaded')
        self.summary_label.setWordWrap(True)
        self.summary_label.setStyleSheet('padding: 15px; background: #f0f0f0; border-radius: 5px;')
        summary_layout.addWidget(self.summary_label)
        summary_tab.setLayout(summary_layout)
        
        # Data table tab
        table_tab = QWidget()
        table_layout = QVBoxLayout()
        self.data_table = QTableWidget()
        table_layout.addWidget(self.data_table)
        table_tab.setLayout(table_layout)
        
        # Charts tab
        charts_tab = QWidget()
        charts_layout = QVBoxLayout()
        
        self.figure = Figure(figsize=(10, 6))
        self.canvas = FigureCanvas(self.figure)
        charts_layout.addWidget(self.canvas)
        
        charts_tab.setLayout(charts_layout)
        
        self.tabs.addTab(summary_tab, 'Summary')
        self.tabs.addTab(table_tab, 'Data Table')
        self.tabs.addTab(charts_tab, 'Charts')
        
        main_layout.addWidget(self.tabs)
        
        # Status bar
        self.statusBar().showMessage('Ready')
        
        # Load initial data
        self.load_datasets()
        
        # Apply stylesheet
        self.apply_styles()
    
    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }
            QGroupBox {
                background: white;
                border-radius: 8px;
                padding: 15px;
                margin: 5px;
                font-weight: bold;
            }
            QPushButton {
                background: #667eea;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #5568d3;
            }
            QPushButton:disabled {
                background: #cccccc;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
            }
            QComboBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 5px;
            }
            QTableWidget {
                background: white;
                border-radius: 5px;
            }
        """)
    
    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter username and password')
            return
        
        try:
            response = self.session.post(f'{API_BASE_URL}/auth/login/', 
                                        json={'username': username, 'password': password})
            if response.status_code == 200:
                data = response.json()
                self.auth_status_label.setText(f"Logged in as: {data['user']['username']}")
                self.login_btn.setEnabled(False)
                self.logout_btn.setEnabled(True)
                QMessageBox.information(self, 'Success', 'Login successful!')
            else:
                QMessageBox.warning(self, 'Error', response.json().get('error', 'Login failed'))
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Login error: {str(e)}')
    
    def handle_logout(self):
        try:
            self.session.post(f'{API_BASE_URL}/auth/logout/')
            self.auth_status_label.setText('Not logged in')
            self.login_btn.setEnabled(True)
            self.logout_btn.setEnabled(False)
            self.username_input.clear()
            self.password_input.clear()
            QMessageBox.information(self, 'Success', 'Logged out successfully')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Logout error: {str(e)}')
    
    def select_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Select CSV File', '', 'CSV Files (*.csv)')
        if filename:
            self.selected_file = filename
            self.file_label.setText(filename.split('/')[-1])
            self.upload_btn.setEnabled(True)
    
    def upload_file(self):
        if not hasattr(self, 'selected_file'):
            QMessageBox.warning(self, 'Error', 'No file selected')
            return
        
        try:
            with open(self.selected_file, 'rb') as f:
                files = {'file': f}
                response = self.session.post(f'{API_BASE_URL}/datasets/upload/', files=files)
            
            if response.status_code == 201:
                QMessageBox.information(self, 'Success', 'File uploaded successfully!')
                self.load_datasets()
                self.file_label.setText('No file selected')
                self.upload_btn.setEnabled(False)
            else:
                QMessageBox.warning(self, 'Error', response.json().get('error', 'Upload failed'))
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Upload error: {str(e)}')
    
    def load_datasets(self):
        try:
            response = self.session.get(f'{API_BASE_URL}/datasets/')
            if response.status_code == 200:
                datasets = response.json()
                self.dataset_combo.clear()
                for dataset in datasets:
                    self.dataset_combo.addItem(
                        f"{dataset['filename']} - {dataset['uploaded_at'][:10]}",
                        dataset['id']
                    )
                self.statusBar().showMessage(f'Loaded {len(datasets)} datasets')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load datasets: {str(e)}')
    
    def on_dataset_selected(self, index):
        if index >= 0:
            dataset_id = self.dataset_combo.currentData()
            if dataset_id:
                self.load_dataset_details(dataset_id)
                self.download_pdf_btn.setEnabled(True)
    
    def load_dataset_details(self, dataset_id):
        try:
            response = self.session.get(f'{API_BASE_URL}/datasets/{dataset_id}/')
            if response.status_code == 200:
                self.current_dataset = response.json()
                self.display_summary()
                self.display_table()
                self.display_charts()
                self.statusBar().showMessage('Dataset loaded successfully')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load dataset: {str(e)}')
    
    def display_summary(self):
        if not self.current_dataset:
            return
        
        summary = self.current_dataset['summary']
        summary_text = f"""
        <h2 style='color: #667eea;'>Dataset Summary</h2>
        <p><b>Filename:</b> {self.current_dataset['filename']}</p>
        <p><b>Total Equipment:</b> {summary.get('total_count', 0)}</p>
        <hr>
        <h3>Average Values</h3>
        <p><b>Flowrate:</b> {summary.get('avg_flowrate', 0):.2f}</p>
        <p><b>Pressure:</b> {summary.get('avg_pressure', 0):.2f}</p>
        <p><b>Temperature:</b> {summary.get('avg_temperature', 0):.2f}</p>
        <hr>
        <h3>Equipment Types Distribution</h3>
        """
        
        for eq_type, count in summary.get('equipment_types', {}).items():
            summary_text += f"<p><b>{eq_type}:</b> {count}</p>"
        
        self.summary_label.setText(summary_text)
    
    def display_table(self):
        if not self.current_dataset or 'equipment' not in self.current_dataset:
            return
        
        equipment = self.current_dataset['equipment']
        
        self.data_table.setRowCount(len(equipment))
        self.data_table.setColumnCount(5)
        self.data_table.setHorizontalHeaderLabels(['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'])
        
        for i, eq in enumerate(equipment):
            self.data_table.setItem(i, 0, QTableWidgetItem(eq['equipment_name']))
            self.data_table.setItem(i, 1, QTableWidgetItem(eq['equipment_type']))
            self.data_table.setItem(i, 2, QTableWidgetItem(str(eq['flowrate'])))
            self.data_table.setItem(i, 3, QTableWidgetItem(str(eq['pressure'])))
            self.data_table.setItem(i, 4, QTableWidgetItem(str(eq['temperature'])))
        
        self.data_table.resizeColumnsToContents()
    
    def display_charts(self):
        if not self.current_dataset:
            return
        
        summary = self.current_dataset['summary']
        
        self.figure.clear()
        
        # Create 2 subplots
        ax1 = self.figure.add_subplot(121)
        ax2 = self.figure.add_subplot(122)
        
        # Bar chart for averages
        labels = ['Flowrate', 'Pressure', 'Temperature']
        values = [
            summary.get('avg_flowrate', 0),
            summary.get('avg_pressure', 0),
            summary.get('avg_temperature', 0)
        ]
        colors = ['#54a0ff', '#ee5a6f', '#feca57']
        
        ax1.bar(labels, values, color=colors, alpha=0.7)
        ax1.set_title('Average Parameter Values', fontweight='bold')
        ax1.set_ylabel('Value')
        ax1.grid(axis='y', alpha=0.3)
        
        # Pie chart for equipment types
        types = list(summary.get('equipment_types', {}).keys())
        counts = list(summary.get('equipment_types', {}).values())
        
        ax2.pie(counts, labels=types, autopct='%1.1f%%', startangle=90)
        ax2.set_title('Equipment Type Distribution', fontweight='bold')
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def download_pdf(self):
        if not self.current_dataset:
            QMessageBox.warning(self, 'Error', 'No dataset selected')
            return
        
        dataset_id = self.current_dataset['id']
        
        try:
            response = self.session.get(f'{API_BASE_URL}/datasets/{dataset_id}/generate_pdf/', stream=True)
            
            if response.status_code == 200:
                filename, _ = QFileDialog.getSaveFileName(self, 'Save PDF Report', 
                                                         f'report_{dataset_id}.pdf', 
                                                         'PDF Files (*.pdf)')
                if filename:
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    QMessageBox.information(self, 'Success', f'PDF saved to {filename}')
            else:
                QMessageBox.warning(self, 'Error', 'Failed to generate PDF')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'PDF download error: {str(e)}')


def main():
    app = QApplication(sys.argv)
    window = ChemicalVisualizerApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
