# App Manager

A generic application manager for launching and managing Python scripts and batch files.

## Features
-   **Dashboard**: A clean, modern interface to view your apps.
-   **Batch Support**: Launch `.bat` and `.cmd` files directly.
-   **Management**: Add, remove, and configure entry points for your apps.
-   **Installer**: Easy-to-use setup script included.

## Installation
Download the latest release from the [Releases](https://github.com/yourusername/app-manager/releases) page.

## Building from Source
1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install customtkinter pyinstaller winshell pywin32
    ```
3.  Run the build tool:
    ```bash
    python build_tool.py
    ```
4.  The installer will be generated in `dist/AppManager_Setup.exe`.
