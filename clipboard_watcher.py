import time
import os
import subprocess
import html


class ClipboardWatcher:
    def __init__(self):
        self.last_clipboard = ""
        self.file_counter = 1
        
    def get_next_filename(self):
        """Generate the next HTML filename with zero-padded number"""
        filename = f"{self.file_counter:02d}.html"
        self.file_counter += 1
        return filename
    
    def save_to_html(self, content):
        """Save clipboard content to HTML file"""
        filename = self.get_next_filename()
        
        # Escape HTML special characters
        escaped_content = html.escape(content)
        
        # Create HTML content
        html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clipboard Content - {filename}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            line-height: 1.6;
        }}
        .content {{
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}
        .timestamp {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <h1>Clipboard Content</h1>
    <div class="timestamp">Created: {time.strftime('%Y-%m-%d %H:%M:%S')}</div>
    <div class="content">{escaped_content}</div>
</body>
</html>"""
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Clipboard content saved to {filename}")
        except Exception as e:
            print(f"Error saving file {filename}: {e}")
    
    def clear_clipboard(self):
        """Clear the clipboard content"""
        try:
            # Clear clipboard using xclip
            subprocess.run(['xclip', '-selection', 'clipboard'], 
                          input='', text=True, timeout=1)
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            try:
                # Fallback to xsel
                subprocess.run(['xsel', '--clipboard', '--clear'], 
                              timeout=1)
            except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
                pass

    def get_clipboard_content(self):
        """Get current clipboard content using xclip for Linux/WSL"""
        try:
            # For WSL/Linux, use xclip or xsel
            result = subprocess.run(['xclip', '-o', '-selection', 'clipboard'], 
                                  capture_output=True, text=True, timeout=1)
            if result.returncode == 0:
                return result.stdout
            else:
                # Fallback to xsel if xclip fails
                result = subprocess.run(['xsel', '--clipboard', '--output'], 
                                      capture_output=True, text=True, timeout=1)
                if result.returncode == 0:
                    return result.stdout
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            pass
        return ""
    
    def watch_clipboard(self):
        """Main loop to watch clipboard changes"""
        print("Clipboard watcher started. Press Ctrl+C to stop.")
        print("Note: This requires xclip or xsel to be installed.")
        print("Install with: sudo apt-get install xclip")
        
        # Clear clipboard on startup
        print("Clearing clipboard...")
        self.clear_clipboard()
        
        print("Watching for clipboard changes...")
        
        try:
            while True:
                current_clipboard = self.get_clipboard_content()
                
                # Check if clipboard content has changed and is not empty
                if current_clipboard and current_clipboard != self.last_clipboard:
                    print(f"Clipboard changed: {current_clipboard[:50]}...")
                    self.save_to_html(current_clipboard)
                    self.last_clipboard = current_clipboard
                
                time.sleep(0.5)  # Check every 0.5 seconds
                
        except KeyboardInterrupt:
            print("\nClipboard watcher stopped.")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    watcher = ClipboardWatcher()
    watcher.watch_clipboard()