---

# 🌀 Mini Torrent Client

A lightweight BitTorrent-like client with a graphical user interface, built using *Python* and *Tkinter*.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-orange)

---

## 🎯 Features

- 📄 **File Sharing**: Create and share `.torrent` files
- 🔗 **Peer-to-Peer Downloading**: Download files from multiple peers
- 📡 **Tracker Support**: Built-in tracker server
- 🖥 **GUI Interface**: User-friendly graphical interface
- 💻 **Cross-Platform**: Works on **Windows**, **macOS**, and **Linux**

---

## 🚀 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/mini-torrent.git
cd mini-torrent
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## 📦 Requirements

- **Python 3.8+**
- **Required Python Packages:**
  - `bencodepy`
  - `requests`
  - `Flask` (for tracker server)

---

## ⚙ Usage

### 🎛 Running the Client GUI

```bash
python -m client.gui
```

### 📡 Running the Tracker Server

```bash
python -m tracker.server
```

### 🛠 Command-Line Options

| Option      | Description                                   | Default                        |
|------------|-----------------------------------------------|--------------------------------|
| `--port`   | Specify listening port                        | `6881`                         |
| `--tracker`| Specify tracker URL                          | `http://localhost:5000/announce` |

---

## 📂 Project Structure

```bash
mini-torrent/
├── client/               # Client application
│   ├── gui.py            # Main GUI interface
│   ├── peer.py           # Peer implementation
│   └── __init__.py
├── tracker/              # Tracker server
│   ├── server.py         # Tracker implementation
│   └── __init__.py
├── shared_files/         # Default shared files directory
├── downloads/            # Default download directory
├── docs/images/          # Directory for screenshots
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## 🖼 Screenshots

### 📌 Main Window
*(Add screenshot here: `/docs/images/main_window.png`)*

### 🔄 Creating Torrent
*(Add screenshot here: `/docs/images/create_torrent.png`)*

---

## 🛠 Troubleshooting

🔹 **Issue:** *Tracker server is not responding*
- Ensure the tracker server is running before starting the client.
- Check if the specified tracker URL is correct.

🔹 **Issue:** *Download is slow or stuck*
- Verify the number of available peers.
- Try restarting the client or tracker.

---

## 🤝 Contributing

Contributions are welcome! Follow these steps:

1️⃣ Fork the repository
2️⃣ Create a feature branch: `git checkout -b feature/your-feature`
3️⃣ Commit your changes: `git commit -am 'Add some feature'`
4️⃣ Push to the branch: `git push origin feature/your-feature`
5️⃣ Open a *Pull Request*

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](./LICENSE) file for details.

---

## 🔮 Future Work

- Implement peer choking/unchoking algorithm
- Add download speed limiting
- Support for multi-file torrents
- NAT traversal techniques
- Dark mode support

---

### 📝 Note:
This is an *educational project*. Use it responsibly and respect copyright laws.

---

