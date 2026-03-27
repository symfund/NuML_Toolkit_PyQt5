import sys
import os
import subprocess
from pathlib import Path

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QGridLayout, QLabel, QPushButton, QComboBox,
                             QFileDialog, QScrollArea)
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QProcess, pyqtSlot
from PyQt5.QtCore import QSettings, QStandardPaths

def get_settings_path():
    # Returns the 'AppData/Roaming' path for your app
    # Example: C:/Users/Name/AppData/Roaming/YourCompany/YourApp/settings.ini
    data_dir = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)

    # Ensure the directory exists
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    return os.path.join(data_dir, "settings.ini")

class ProjectCreatorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Define the ini file location in Roaming AppData
        ini_path = get_settings_path()
        self.settings = QSettings(ini_path, QSettings.IniFormat)

        self.setWindowTitle("TFLite Model Deploy / TFLite 模型部署")
        self.resize(1024, 800)

        # 1. Setup Font (Chinese Support)
        self.setup_chinese_font()

        # 2. Main Widget and Scroll Area
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Title Label
        title = QLabel("Project Setup / 工程设定")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        # Scrollable Content Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        grid = QGridLayout(scroll_content)
        grid.setSpacing(15)

        # --- UI ELEMENTS ---

        # 1. Project Directory
        grid.addWidget(QLabel("Output Directory / 输出目录"), 0, 0)
        self.btn_proj_dir = QPushButton("Select Folder")
        self.btn_proj_dir.clicked.connect(self.choose_project_directory)
        grid.addWidget(self.btn_proj_dir, 1, 0)

        # 2. Board Type
        grid.addWidget(QLabel("Board Type / 板子类型"), 2, 0)
        self.board_spinner = QComboBox()
        self.board_spinner.addItems(["NuMaker-M55M1", "NuGestureAI-M55M1"])
        grid.addWidget(self.board_spinner, 3, 0)

        # 3. Model File
        grid.addWidget(QLabel("Model File / 模型文件 (*.tflite):"), 4, 0)
        self.btn_model_file = QPushButton("Select .tflite File")
        self.btn_model_file.clicked.connect(self.choose_model_file)
        grid.addWidget(self.btn_model_file, 5, 0)

        # 4. Project Type
        grid.addWidget(QLabel("Project Type / 工程类型"), 6, 0)
        self.project_spinner = QComboBox()
        self.project_spinner.addItems(["make_gcc_arm", "uvision5_armc6"])
        grid.addWidget(self.project_spinner, 7, 0)

        # 5. Compiler Path
        grid.addWidget(QLabel("Compiler Path / 编译器"), 8, 0)
        self.btn_compiler = QPushButton("Select Compiler Path")
        self.btn_compiler.clicked.connect(self.choose_compiler_path)
        grid.addWidget(self.btn_compiler, 9, 0)

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        # Action Button
        self.btn_create = QPushButton("Generate Project / 生成工程")
        self.btn_create.setFixedHeight(60)
        self.btn_create.setStyleSheet("background-color: #3498db; color: white; font-weight: bold;")
        self.btn_create.clicked.connect(self.create_project)
        layout.addWidget(self.btn_create)

        # Load your saved values
        self.load_settings()

        self.process = QProcess(self)

        # Also connect the signals so you can see the output
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.process_finished)

    def setup_chinese_font(self):
        """Attempts to find and set a Windows Chinese font."""
        font_dir = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts')
        # Check for Microsoft YaHei (msyh.ttc)
        font_path = os.path.join(font_dir, 'msyh.ttc')
        if os.path.exists(font_path):
            font_id = QFontDatabase.addApplicationFont(font_path)
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.setFont(QFont(font_family, 10))

    def choose_project_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Project Directory")
        if directory:
            self.btn_proj_dir.setText(directory)

    def choose_model_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Model", "", "TFLite Files (*.tflite)")
        if file_path:
            self.btn_model_file.setText(file_path)

    def choose_compiler_path(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Compiler Toolchain", "", "EXE Files (*.exe)")
        if file_path:
            self.btn_compiler.setText(file_path)

    def create_project(self):
        print("--- Creating Project ---")
        print(f"Path: {self.btn_proj_dir.text()}")
        print(f"Board: {self.board_spinner.currentText()}")
        print(f"Model: {self.btn_model_file.text()}")
        print(f"Type: {self.project_spinner.currentText()}")
        print(f"Compiler: {self.btn_compiler.text()}")

        env_name = os.environ.get('CONDA_DEFAULT_ENV')
        env_path = os.environ.get('CONDA_PREFIX')
        script_dir = Path(__file__).resolve().parent
        working_dir = str(script_dir / "NuML_TFLM_Tool")

        #python_exe = str(Path(env_path) / "python.exe")

        # Use sys.executable instead of searching for CONDA_PREFIX
        python_exe = sys.executable

        # Construct arguments list (QProcess takes cmd and args separately)
        cmd = python_exe
        args = [
            "numl_tool.py",
            "deploy",
            "--output_path", self.btn_proj_dir.text(),
            "--board", self.board_spinner.currentText(),
            "--model_file", self.btn_model_file.text(),
            "--project_type", self.project_spinner.currentText(),
            "--ide_tool", self.btn_compiler.text()
        ]

        self.btn_create.setEnabled(False)
        self.btn_create.setStyleSheet("background-color: red; color: white;")
        self.btn_create.setText("CREATING / 创建中...")

        self.process.setWorkingDirectory(working_dir)
        self.process.start(cmd, args)
        
    @pyqtSlot()
    def handle_stdout(self):
        data = self.process.readAllStandardOutput().data().decode()
        print(data.strip())  # Or self.log_output.append(data)

    @pyqtSlot()
    def handle_stderr(self):
        data = self.process.readAllStandardError().data().decode()
        print(f"ERROR: {data.strip()}")

    def process_finished(self, exit_code, exit_status):
        self.btn_create.setEnabled(True)
        self.btn_create.setStyleSheet("background-color: green; color: white;")
        self.btn_create.setText("Generate Project / 生成工程")
        if exit_code == 0:
            print("Project created successfully!")
        else:
            print(f"Process failed with exit code {exit_code}")
        




        '''
        
        cmd = [
            python_exe,
            "numl_tool.py",
            "deploy",
            "--output_path", self.btn_proj_dir.text(),
            "--board", self.board_spinner.currentText(),
            "--model_file", self.btn_model_file.text(),
            "--project_type", self.project_spinner.currentText(),
            "--ide_tool", self.btn_compiler.text()
        ]
       
        try:
            self.proc = subprocess.Popen(cmd, cwd=working_dir)
        except OSError as e:
            # This catches "File Not Found" or permission errors
            print(f"Failed to start the process: {e}")
        except ValueError as e:
            # This catches invalid arguments passed to Popen
            print(f"Invalid arguments: {e}")

        # self.proc.wait()
        
        '''

    def load_settings(self):
        # Restore values; use a sensible default if the key doesn't exist
        proj_dir = self.settings.value("project_dir", "Select Folder")
        self.btn_proj_dir.setText(proj_dir)

        board = self.settings.value("board_type", "NuMaker-M55M1")
        index = self.board_spinner.findText(board)
        if index >= 0:
            self.board_spinner.setCurrentIndex(index)

        model = self.settings.value("model_file", "Select .tflite File")
        self.btn_model_file.setText(model)

        proj_type = self.settings.value("project_type", "Select Project Type")
        index = self.project_spinner.findText(proj_type)
        if index >= 0:
            self.project_spinner.setCurrentIndex(index)

        compiler = self.settings.value("compiler_file", "Select .exe File")
        self.btn_compiler.setText(compiler)

    def save_settings(self):
        # Save the text from buttons or values from combo boxes
        self.settings.setValue("project_dir", self.btn_proj_dir.text())
        self.settings.setValue("board_type", self.board_spinner.currentText())
        self.settings.setValue("model_file", self.btn_model_file.text())
        self.settings.setValue("project_type", self.project_spinner.currentText())
        self.settings.setValue("compiler_file", self.btn_compiler.text())

    # Tip: Trigger this in the closeEvent to ensure everything is saved on exit
    def closeEvent(self, event):
        self.save_settings()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setOrganizationName("Nuvoton")
    app.setOrganizationDomain("nuvoton.com")  # Optional, used on macOS
    app.setApplicationName("NumlQt5")

    window = ProjectCreatorApp()
    window.show()
    sys.exit(app.exec_())
