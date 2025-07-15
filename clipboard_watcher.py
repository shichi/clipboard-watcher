import time
import os
import subprocess
import html
import platform


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
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Clipboard content saved to {filename}")
        except Exception as e:
            print(f"Error saving file {filename}: {e}")
    
    def clear_clipboard(self):
        """Clear the clipboard content"""
        system = platform.system()
        try:
            if system == "Darwin":  # macOS
                subprocess.run(['pbcopy'], input='', text=True, timeout=1)
            elif system == "Windows": # Windows
                subprocess.run(['clip'], input=b'', timeout=1)
            else:  # Linux/WSL
                subprocess.run(['xclip', '-selection', 'clipboard'], 
                              input='', text=True, timeout=1)
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            try:
                if system == "Linux":
                    # Fallback to xsel for Linux
                    subprocess.run(['xsel', '--clipboard', '--clear'], 
                                  timeout=1)
            except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
                pass

    def get_clipboard_content(self):
        """Get current clipboard content"""
        system = platform.system()
        try:
            if system == "Darwin":  # macOS
                result = subprocess.run(['pbpaste'], 
                                      capture_output=True, text=True, timeout=1)
                if result.returncode == 0:
                    return result.stdout
            elif system == "Windows": # Windows
                result = subprocess.run(
                    ['powershell', '-command', 'Get-Clipboard'],
                    capture_output=True, text=True, timeout=1, shell=False
                )
                if result.returncode == 0:
                    return result.stdout.strip()
            else:  # Linux/WSL
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
        system = platform.system()
        if system == "Darwin":
            print("Note: This uses pbpaste/pbcopy for macOS clipboard access.")
        elif system == "Windows":
            print("Note: This uses PowerShell and clip for Windows clipboard access.")
        else:
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
                    print(current_clipboard)
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
