PyQt5 Version NuML Toolkit
===
### TensorFlow Lite Model Deployment Tool for NuMaker M55M1 Running Within Miniforge3 Conda Environment (numl_toolkit)
![Screenshot of PyQt5 version NuML Toolkit.](/assets/images/numl_toolkit_pyqt5.png)

## Create Conda environment 'numl_toolkit'
1. Go to https://conda-forge.org/miniforge/ to fetch and install the latest Miniforge for Windows.
2. Clone this repository into D:\Projects\NuML_Toolkit_PyQt5
   ```
   git clone https://github.com/symfund/NuML_Toolkit_PyQt5.git D:\Projects\NuML_Toolkit_PyQt5
   ```
3. Open Miniforge Prompt
   ```
   (base) C:\Users\Arthur>
   ```
4. Change path to D:\Projects\NuML_Toolkit_PyQt5
   ```
   (base) C:\Users\Arthur>cd D:\Projects\NuML_Toolkit_PyQt5
   (base) C:\Users\Arthurs>d:
   (base) D:\Projects\NuML_Toolkit_PyQt5
   ```
5. Create the conda environment 'numl_toolkit' from the YAML file
   ```
   conda env create -f conda/environment.yml
   ```
6. Activate the conda environment 'numl_toolkit'
   ```
   conda activate numl_toolkit
   ```
7. Install Python packages through PIP
   ```
   pip install -r requirements.txt
   ```
8. Change directory to 'NuML_TFLM_Tool'
   ```
   cd NuML_TFLM_Tool
   ```
9. Run the Python script file 'setup_progendef.py'
   ```
   python setup_progendef.py
   ```

## Run PyQt5 version NuML Toolkit within Miniforge Prompt
1. Open Miniforge Prompt
   ```
   (base) C:\Users\Arthur>
   ```
2. Activate the 'numl_toolkit' conda environment
   ```
   conda activate numl_toolkit
   ```
3. Change directory to 'D:\Projects\NuML_Toolkit_PyQt5'
   ```
   (base) C:\Users\Arthur>cd D:\Projects\NuML_Toolkit_PyQt5
   (base) C:\Users\Arthurs>d:
   (base) D:\Projects\NuML_Toolkit_PyQt5
   ```
4. Run PyQt5 version NuML Toolkit
   ```
   pythonw numl_toolkit_pyqt5
   ```

## Run PyQt5 version NuML Toolkit without opening Miniforge Prompt
There are two primary ways to launch a PyQt5 Numl_Toolkit application: Verbose (Console) Launch and Silent (Windowed) Launch.
1. Verbose (Console) Launch: The application opens with an attached console or terminal window. This terminal displays real-time logs, print() statements, and error tracebacks alongside the GUI.
Double click the following batch file to verbose launch
```
verbose_launch_numl_toolkit_pyqt5.bat
```
3. Silent (Windowed) Launch: The application opens only the GUI window, suppressing the console entirely.
Double click the following VBScript file to silent launch
```
silent_launch_numl_toolkit_pyqt5.vbs
```
