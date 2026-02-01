# App Manager

I built this tool to organize my growing collection of Python scripts and batch files. It's a simple, clean dashboard that lets you manage and launch your local apps without digging through folders every time.

## What it does
-   **All in one place**: Scans your projects folder and shows everything in a nice grid.
-   **Runs anything**: Works with Python scripts (`.py`) and Windows Batch files (`.bat`/`.cmd`).
-   **Customizable**: You can add specific apps manually or change which file launching them.
-   **Dark Mode**: It just looks better.

## How to use it
You can download the latest installer from the [Releases page](https://github.com/who4/App-Manager/releases).

Just run the setup file, point it to where you keep your projects, and you're good to go.

## Development
If you want to run it from source or modify it, here is how I build it:

1.  Clone the repo:
    ```bash
    git clone https://github.com/who4/App-Manager.git
    ```
2.  Install the requirements:
    ```bash
    pip install customtkinter pyinstaller winshell pywin32
    ```
3.  Run the build script:
    ```bash
    python build_tool.py
    ```

The installer will pop out in the `dist` folder.
