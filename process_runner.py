
import os
import subprocess
import sys
import ctypes

class ProcessRunner:
    @staticmethod
    def run_app(app_model, as_admin=False):
        """
        Runs the application.
        Strategies:
        1. Check extension. If .bat/.cmd, run directly.
        2. Detect venv in app directory.
        3. If venv, use venv/Scripts/python.exe.
        4. Else, use system python (sys.executable).
        
        It opens a NEW console window so the user can interact/see output.
        """
        
        target_dir = app_model.path
        entry_point = app_model.entry_point
        script_path = os.path.join(target_dir, entry_point)
        
        # Check for batch file
        ext = os.path.splitext(entry_point)[1].lower()
        if ext in [".bat", ".cmd"]:
            if as_admin:
                ProcessRunner.run_batch_as_admin(script_path, target_dir)
            else:
                ProcessRunner.run_batch(script_path, target_dir)
            return

        python_exe = ProcessRunner.detect_python(target_dir)

        if as_admin:
            ProcessRunner.run_as_admin(python_exe, script_path, target_dir)
        else:
            ProcessRunner.run_normal(python_exe, script_path, target_dir)

    @staticmethod
    def detect_python(app_dir):
        # Check common venv names
        venvs = ["venv", ".venv", "env"]
        for v in venvs:
            candidate = os.path.join(app_dir, v, "Scripts", "python.exe")
            if os.path.exists(candidate):
                return candidate
        
        # If running as compiled EXE (frozen), sys.executable is THIS EXE.
        # We must NOT use it to run scripts. Fallback to global "python".
        if getattr(sys, 'frozen', False):
            return "python"
            
        # Default to system python (development mode)
        return sys.executable

    @staticmethod
    def run_normal(interpreter, script, cwd):
        # RCA: Passing a list to subprocess on Windows with embedded quotes causes 
        # subprocess to escape them (e.g. \"path\"), which cmd.exe treats as a literal part of the filename.
        # FIX: We construct the full command string manually and pass it as a string to Popen.
        
        interpreter = os.path.normpath(interpreter)
        script = os.path.normpath(script)
        
        # Command Structure: cmd.exe /k "echo ... & echo ... & "interpreter" "script""
        # Added detailed logging so user knows WHICH python is running.
        
        command_to_run = (
            f'echo ------------------------------------------------ & '
            f'echo [ProcessRunner] Launching Application... & '
            f'echo [ProcessRunner] Interpreter: "{interpreter}" & '
            f'echo [ProcessRunner] Script:      "{script}" & '
            f'echo ------------------------------------------------ & '
            f'"{interpreter}" "{script}"'
        )
        
        full_cmd = f'cmd.exe /k "{command_to_run}"'
        
        try:
            subprocess.Popen(
                full_cmd, 
                cwd=cwd, 
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        except Exception as e:
            print(f"Error running app: {e}")

    @staticmethod
    def run_as_admin(interpreter, script, cwd):
        # Normalizing paths
        interpreter = os.path.normpath(interpreter)
        script = os.path.normpath(script)
        
        try:
            # Construct parameters for cmd.exe
            
            command_to_run = (
                f'echo ------------------------------------------------ & '
                f'echo [ProcessRunner] Launching Application (Admin)... & '
                f'echo [ProcessRunner] Interpreter: "{interpreter}" & '
                f'echo [ProcessRunner] Script:      "{script}" & '
                f'echo ------------------------------------------------ & '
                f'"{interpreter}" "{script}"'
            )
            
            params = f'/k "{command_to_run}"'
            
            ctypes.windll.shell32.ShellExecuteW(
                None, 
                "runas", 
                "cmd.exe", 
                params, 
                cwd, 
                1 # SW_SHOWNORMAL
            )
            
        except Exception as e:
            print(f"Error running as admin: {e}")

    @staticmethod
    def run_batch(script, cwd):
        script = os.path.normpath(script)
        
        command_to_run = (
            f'echo ------------------------------------------------ & '
            f'echo [ProcessRunner] Launching Batch File... & '
            f'echo [ProcessRunner] Script:      "{script}" & '
            f'echo ------------------------------------------------ & '
            f'"{script}"'
        )
        
        full_cmd = f'cmd.exe /k "{command_to_run}"'
        
        try:
            subprocess.Popen(
                full_cmd, 
                cwd=cwd, 
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        except Exception as e:
            print(f"Error running batch: {e}")

    @staticmethod
    def run_batch_as_admin(script, cwd):
        script = os.path.normpath(script)
        
        try:
            command_to_run = (
                f'echo ------------------------------------------------ & '
                f'echo [ProcessRunner] Launching Batch File (Admin)... & '
                f'echo [ProcessRunner] Script:      "{script}" & '
                f'echo ------------------------------------------------ & '
                f'"{script}"'
            )
            
            params = f'/k "{command_to_run}"'
            
            ctypes.windll.shell32.ShellExecuteW(
                None, 
                "runas", 
                "cmd.exe", 
                params, 
                cwd, 
                1 # SW_SHOWNORMAL
            )
            
        except Exception as e:
            print(f"Error running batch as admin: {e}")

    @staticmethod
    def open_directory(path):
        try:
            os.startfile(path)
        except Exception as e:
            print(f"Error opening directory: {e}")

    @staticmethod
    def open_in_editor(path):
        try:
            # Try opening the file directly (triggers default editor)
            os.startfile(path)
        except Exception as e:
            print(f"Error opening editor: {e}")
