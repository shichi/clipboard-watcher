# Clipboard Watcher

A Python utility that monitors clipboard changes and automatically saves the content to sequentially numbered HTML files.

## Features

- **Real-time clipboard monitoring**: Watches for clipboard changes every 0.5 seconds
- **Automatic HTML export**: Saves clipboard content to styled HTML files
- **Sequential file naming**: Creates files as `01.html`, `02.html`, `03.html`, etc.
- **Clipboard clearing**: Clears clipboard on startup to avoid capturing pre-existing content
- **Cross-platform support**: Works on Linux/WSL environments
- **Styled HTML output**: Generated HTML files include timestamps and clean formatting

## Requirements

- Python 3.x
- `xclip` or `xsel` (for clipboard access on Linux/WSL)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/your-username/clipboard-watcher.git
cd clipboard-watcher
```

2. Install required system dependencies:
```bash
# Ubuntu/Debian
sudo apt-get install xclip

# Alternative: xsel
sudo apt-get install xsel
```

## Usage

Run the clipboard watcher:
```bash
python3 clipboard_watcher.py
```

The program will:
1. Clear the current clipboard content
2. Start monitoring for new clipboard changes
3. Save each new clipboard content to a numbered HTML file
4. Display status messages in the terminal

To stop the program, press `Ctrl+C`.

## Output Format

Each HTML file contains:
- A clean, responsive layout
- Timestamp of when the content was captured
- Properly escaped HTML content
- Professional styling with good readability

Example output file (`01.html`):
```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>Clipboard Content - 01.html</title>
    <!-- Styled CSS included -->
</head>
<body>
    <h1>Clipboard Content</h1>
    <div class="timestamp">Created: 2025-07-14 10:30:45</div>
    <div class="content">Your clipboard content here...</div>
</body>
</html>
```

## How It Works

1. **Startup**: Clears existing clipboard content to ensure only new copies are captured
2. **Monitoring**: Continuously checks clipboard content every 0.5 seconds
3. **Change Detection**: Compares current clipboard with previous state
4. **File Creation**: When changes are detected, creates a new HTML file with incremented number
5. **Content Processing**: Escapes HTML special characters and applies formatting

## Configuration

The monitoring interval and file naming can be customized by modifying the source code:

- **Check interval**: Change `time.sleep(0.5)` in the `watch_clipboard()` method
- **File naming**: Modify the `get_next_filename()` method for different naming schemes

## Troubleshooting

**"No module named 'tkinter'"**: This program uses `xclip`/`xsel` instead of tkinter for better Linux/WSL compatibility.

**Clipboard not detected**: Ensure `xclip` or `xsel` is installed:
```bash
which xclip
# or
which xsel
```

**Permission issues**: Make sure the script has execution permissions:
```bash
chmod +x clipboard_watcher.py
```

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.