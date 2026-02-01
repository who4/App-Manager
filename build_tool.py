import PyInstaller.__main__
import shutil
import os

def clean():
    print("Cleaning up...")
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist", ignore_errors=True)
    if os.path.exists("AppManager.spec"):
        os.remove("AppManager.spec")
    if os.path.exists("AppManager_Setup.spec"):
        os.remove("AppManager_Setup.spec")

def build_app_manager():
    print("Building App Manager (Core)...")
    # Build the main app as a directory (onedir)
    # We hide the console for the main app
    PyInstaller.__main__.run([
        'main.py',
        '--name=AppManager',
        '--noconsole',
        '--onedir',
        '--noconfirm',
        '--icon=assets/app_icon.ico',
        '--add-data=assets/app_icon.ico;assets',
        '--exclude-module=pythoncom',
        '--exclude-module=pywin32',
    ])

def build_installer():
    print("Building App Manager Installer...")
    
    # Check if AppManager build exists
    app_dist_path = os.path.abspath("dist/AppManager")
    if not os.path.exists(app_dist_path):
        print("Error: AppManager build not found!")
        return

    # Build the setup script as a single executable (onefile)
    # It must include the AppManager build as data
    # format for add-data is "source;dest" on Windows
    add_data_arg = f'{app_dist_path};AppManager_Bin'

    PyInstaller.__main__.run([
        'setup_script.py',
        '--name=AppManager_Setup_v2',
        '--onefile',
        '--noconsole',  # GUI Installer
        '--noconfirm',
        '--icon=assets/app_icon.ico',
        f'--add-data={add_data_arg}',
        # Exclude problematic modules
        '--exclude-module=pythoncom',
        '--exclude-module=pywin32',
        '--hidden-import=customtkinter',
    ])

if __name__ == "__main__":
    clean()
    build_app_manager()
    build_installer()
    print("Build Complete! Installer should be in dist/AppManager_Setup.exe")
