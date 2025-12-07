import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from .peer import Peer
import threading

class TorrentGUI:
    def __init__(self, root):
        self.root = root
        self.peer = None
        self.setup_gui()
        self.initialize_peer()
        
    def setup_gui(self):
        self.root.title("Mini Torrent Client")
        self.root.geometry("800x600")
        
        # Set window icon
        try:
            self.root.iconbitmap("assets/icon.ico")
        except:
            pass
        
        # Create tabs
        self.tab_control = ttk.Notebook(self.root)
        
        # Download Tab
        self.download_tab = ttk.Frame(self.tab_control)
        self.setup_download_tab()
        
        # Upload Tab
        self.upload_tab = ttk.Frame(self.tab_control)
        self.setup_upload_tab()
        
        # Status Tab
        self.status_tab = ttk.Frame(self.tab_control)
        self.setup_status_tab()
        
        self.tab_control.add(self.download_tab, text='Downloads')
        self.tab_control.add(self.upload_tab, text='Uploads')
        self.tab_control.add(self.status_tab, text='Status')
        self.tab_control.pack(expand=1, fill="both")
        
    def setup_download_tab(self):
        # Torrent file selection
        ttk.Label(self.download_tab, text="Torrent File:").grid(row=0, column=0, padx=5, pady=5)
        self.torrent_path = tk.StringVar()
        ttk.Entry(self.download_tab, textvariable=self.torrent_path, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.download_tab, text="Browse", command=self.browse_torrent).grid(row=0, column=2, padx=5, pady=5)
        
        # Download button
        ttk.Button(self.download_tab, text="Start Download", command=self.start_download).grid(row=1, column=1, pady=10)
        
        # Download progress treeview
        self.download_tree = ttk.Treeview(self.download_tab, columns=('name', 'size', 'progress', 'speed', 'peers'), show='headings')
        self.download_tree.heading('name', text='File Name')
        self.download_tree.heading('size', text='Size')
        self.download_tree.heading('progress', text='Progress')
        self.download_tree.heading('speed', text='Speed')
        self.download_tree.heading('peers', text='Peers')
        self.download_tree.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')
        
        # Configure grid weights
        self.download_tab.grid_rowconfigure(2, weight=1)
        self.download_tab.grid_columnconfigure(1, weight=1)
        
    def setup_upload_tab(self):
        # File selection for sharing
        ttk.Label(self.upload_tab, text="File to Share:").grid(row=0, column=0, padx=5, pady=5)
        self.share_path = tk.StringVar()
        ttk.Entry(self.upload_tab, textvariable=self.share_path, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.upload_tab, text="Browse", command=self.browse_share_file).grid(row=0, column=2, padx=5, pady=5)
        
        # Tracker URL
        ttk.Label(self.upload_tab, text="Tracker URL:").grid(row=1, column=0, padx=5, pady=5)
        self.tracker_url = tk.StringVar(value="http://localhost:5000/announce")
        ttk.Entry(self.upload_tab, textvariable=self.tracker_url, width=50).grid(row=1, column=1, padx=5, pady=5)
        
        # Create torrent button
        ttk.Button(self.upload_tab, text="Create Torrent", command=self.create_torrent).grid(row=2, column=1, pady=10)
        
        # Shared files list
        self.upload_tree = ttk.Treeview(self.upload_tab, columns=('name', 'size', 'peers'), show='headings')
        self.upload_tree.heading('name', text='File Name')
        self.upload_tree.heading('size', text='Size')
        self.upload_tree.heading('peers', text='Peers')
        self.upload_tree.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')
        
        self.upload_tab.grid_rowconfigure(3, weight=1)
        self.upload_tab.grid_columnconfigure(1, weight=1)
        
    def setup_status_tab(self):
        # Peer ID display
        ttk.Label(self.status_tab, text="Peer ID:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.peer_id_label = ttk.Label(self.status_tab, text="")
        self.peer_id_label.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        
        # Port configuration
        ttk.Label(self.status_tab, text="Listening Port:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.port_entry = ttk.Entry(self.status_tab, width=10)
        self.port_entry.insert(0, "6881")
        self.port_entry.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        
        # Connection status
        ttk.Label(self.status_tab, text="Status:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.status_label = ttk.Label(self.status_tab, text="Not connected")
        self.status_label.grid(row=2, column=1, sticky='w', padx=5, pady=5)
        
        # Active connections
        ttk.Label(self.status_tab, text="Active Connections:").grid(row=3, column=0, sticky='nw', padx=5, pady=5)
        self.connections_tree = ttk.Treeview(self.status_tab, columns=('ip', 'port', 'up', 'down'), show='headings')
        self.connections_tree.heading('ip', text='IP Address')
        self.connections_tree.heading('port', text='Port')
        self.connections_tree.heading('up', text='Upload Speed')
        self.connections_tree.heading('down', text='Download Speed')
        self.connections_tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')
        
        self.status_tab.grid_rowconfigure(4, weight=1)
        self.status_tab.grid_columnconfigure(1, weight=1)
        
    def initialize_peer(self):
        port = int(self.port_entry.get())
        self.peer = Peer(port=port)
        self.peer_id_label.config(text=self.peer.peer_id)
        
        # Start peer server in background
        threading.Thread(target=self.peer.start_server, daemon=True).start()
        self.status_label.config(text="Running")
        
    def browse_torrent(self):
        filename = filedialog.askopenfilename(title="Select Torrent File", filetypes=[("Torrent files", "*.torrent")])
        if filename:
            self.torrent_path.set(filename)
            
    def browse_share_file(self):
        filename = filedialog.askopenfilename(title="Select File to Share")
        if filename:
            self.share_path.set(filename)
            
    def create_torrent(self):
        file_path = self.share_path.get()
        tracker_url = self.tracker_url.get()
        
        if not file_path:
            messagebox.showerror("Error", "Please select a file to share")
            return
            
        try:
            # Create torrent file (implement this in your peer.py)
            torrent_path = self.peer.create_torrent(file_path, tracker_url)
            messagebox.showinfo("Success", f"Torrent file created: {torrent_path}")
            
            # Add to shared files list
            self.upload_tree.insert('', 'end', values=(
                os.path.basename(file_path),
                f"{os.path.getsize(file_path)/1024/1024:.2f} MB",
                "0"
            ))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create torrent: {str(e)}")
            
    def start_download(self):
        torrent_file = self.torrent_path.get()
        if not torrent_file:
            messagebox.showerror("Error", "Please select a torrent file")
            return
            
        try:
            # Start download (implement in peer.py)
            self.peer.start_download(torrent_file)
            
            # Add to download list
            # You would get this info from parsing the torrent file
            self.download_tree.insert('', 'end', values=(
                "example.file",  # From torrent
                "100 MB",        # From torrent
                "0%",            # Progress
                "0 KB/s",        # Speed
                "0"              # Peers
            ))
            
            messagebox.showinfo("Started", "Download started")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start download: {str(e)}")

def run_gui():
    root = tk.Tk()
    app = TorrentGUI(root)
    root.mainloop()

if __name__ == '__main__':
    run_gui()