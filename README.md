# 🔒 Webcam Spyware Security

A powerful and user-friendly desktop application designed to protect your privacy by giving you complete control over your webcam. This tool helps prevent unauthorized access to your webcam by malicious spyware and provides comprehensive logging of all webcam-related activities.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

## 🌟 Features

### Core Functionality
- **🎥 Webcam Control**: Enable or disable your webcam with a single click
- **📊 Status Monitor**: Real-time webcam status checking
- **🔐 Password Protection**: Secure authentication for sensitive operations
- **📝 Activity Logging**: Comprehensive HTML-based activity logs with timestamps
- **🚨 Intruder Detection**: Automatically records video when wrong password is entered

### Security Features
- **Password-Protected Actions**: All webcam control actions require authentication
- **Intruder Video Capture**: Records 10-second video on unauthorized access attempts
- **Activity Tracking**: All actions are logged with timestamps for security auditing
- **Customizable Credentials**: Change username and password on the fly

### User Experience
- **Modern Dark Theme**: Sleek, eye-friendly interface with cyan accents
- **Real-time Feedback**: Live activity log displayed in the application
- **Comprehensive Logs**: Beautiful HTML logs with color-coded entries
- **Easy Navigation**: Intuitive button-based interface

## 📋 Prerequisites

Before running this application, ensure you have the following installed:

- **Python 3.7 or higher**
- **Windows Operating System** (required for PowerShell webcam control commands)
- **Administrator privileges** (for webcam control operations)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/adithya984/webcam-spyware-security.git
cd webcam-spyware-security
```

### 2. Install Required Dependencies
```bash
pip install -r requirements.txt
```

Required packages:
- `tkinter` (usually comes with Python)
- `Pillow` (PIL) - for image handling
- `opencv-python` (cv2) - for video capture
- `requests` - for downloading project info

### 3. Run the Application
```bash
python webcam_spyware_detector.py
```

## 🎮 Usage

### Default Credentials
- **Username**: `admin`
- **Password**: `admin`

> ⚠️ **Important**: Change the default password immediately after first launch for security!

### Available Actions

#### 🔓 Unprotected Actions (No Password Required)
- **Project Info**: View project documentation (downloads from GitHub if not available locally)
- **Check Status**: View current webcam status (OK/Error/Unknown)
- **Change Password**: Update your authentication credentials
- **Clear Logs**: Clear all activity logs
- **Exit**: Close the application

#### 🔒 Protected Actions (Password Required)
- **Disable Camera**: Completely disable your webcam at the system level
- **Enable Camera**: Re-enable your webcam
- **View Logs**: Open the HTML activity log in your default browser

### Activity Logs

The application maintains two types of logs:

1. **In-App Log**: Displayed in the application window with real-time updates
2. **HTML Log** (`logs.html`): Persistent, color-coded log file that can be opened in any web browser

Log entries are color-coded:
- 🟢 **Green**: Camera enabled or successful actions
- 🔴 **Red**: Camera disabled or blocked actions
- ⚫ **Gray**: Informational messages

## 🛡️ Security Features Explained

### Intruder Detection
When an incorrect password is entered, the application:
1. Logs the failed attempt with timestamp
2. Activates the webcam (if available)
3. Records a 10-second video
4. Saves the video to your Desktop with timestamp: `intruder_YYYYMMDD_HHMMSS.avi`

This helps you identify who attempted unauthorized access to your webcam controls.

### PowerShell Integration
The application uses Windows PowerShell commands to control webcam devices at the system level:
- `Get-PnpDevice -Class Camera | Disable-PnpDevice` - Disables webcam
- `Get-PnpDevice -Class Camera | Enable-PnpDevice` - Enables webcam
- `Get-PnpDevice -Class Camera | Select-Object Status` - Checks webcam status

## 📁 Project Structure

```
webcam-spyware-security/
│
├── webcam_spyware_detector.py    # Main application file
├── logs.html                      # Activity log (generated at runtime)
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── images.png                     # Optional header image
├── logo.png                       # Optional logo image
└── project info.pdf              # Project documentation (auto-downloaded)
```

## 🎨 Customization

### Change Application Theme
Edit the color constants in `webcam_spyware_detector.py`:
```python
# Line 257-258: Header colors
fg="#03dac6"  # Cyan accent color
bg="black"    # Background color

# Line 272-273: Button styles
bg="#03dac6"  # Button background
fg="black"    # Button text
```

### Add Custom Logo
Place your logo image in the project directory:
- `images.png` - Header image (150x150px recommended)
- `logo.png` - Logo below Project Info button (120x120px recommended)

## ⚙️ Configuration

You can modify these settings in `webcam_spyware_detector.py`:

```python
# Line 20-22: File paths and credentials
HTML_LOG_FILE = "logs.html"
USERNAME = "admin"
PASSWORD = "admin"

# Line 23: Project info URL
PROJECT_INFO_URL = "https://github.com/adithya984/supraja-intern/raw/main/project%20%20info.pdf"
```

## 🐛 Troubleshooting

### "Camera is Unknown" Status
- Ensure you're running the application with Administrator privileges
- Check if Windows recognizes your webcam in Device Manager

### Commands Not Working
- Right-click the application and select "Run as Administrator"
- Verify PowerShell execution policy allows scripts to run

### Intruder Video Not Recording
- Ensure your webcam is enabled and functioning
- Check that OpenCV can access your camera (driver issues)
- Verify you have write permissions to the Desktop folder

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Adithya Yana Mala Manda**
- GitHub: [@adithya984](https://github.com/adithya984)
- Repository: [webcam-spyware-security](https://github.com/adithya984/webcam-spyware-security)

## 🙏 Acknowledgments

- Built as an internship project
- Uses Windows PowerShell for system-level webcam control
- UI inspiration from modern security applications

## ⚠️ Disclaimer

This tool is designed for legitimate privacy protection purposes. Users are responsible for ensuring they comply with all applicable laws and regulations when using this software. The developers are not responsible for any misuse of this application.

---

**Stay Safe! Protect Your Privacy! 🔒**
