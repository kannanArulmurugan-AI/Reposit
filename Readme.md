YouTube Downloader with yt-dlp and aria2c

This project is a Python-based GUI application to download YouTube videos using yt-dlp and aria2c. The downloader fetches video URLs, processes them in parallel, and shows download progress via a user-friendly interface. The project supports downloading multiple videos at once, and it can also fetch URLs from a Google Sheet.
Features

    Download YouTube videos using yt-dlp.
    Fast download speeds with the aria2c external downloader.
    Supports downloading multiple videos in parallel.
    Fetches video URLs from Google Sheets.
    Progress bar to display download progress.

Requirements

The following software and Python libraries are required to run the project:
Software

    Python 3.x: Make sure Python is installed.
    yt-dlp: A command-line YouTube downloader.
    aria2c: A lightweight multi-protocol & multi-source command-line download utility.
    Google Sheets API (optional): Used to fetch URLs from a Google Sheet.

Python Libraries

Install the following Python libraries:

    tkinter (for the graphical interface)
    yt-dlp (for downloading videos)
    subprocess (to run command-line processes)
    threading (for parallel processing)
    gspread (for Google Sheets API integration)
    oauth2client (for Google Sheets API authorization)

Installation and Setup
Step 1: Install yt-dlp and aria2c

To use yt-dlp with aria2c for faster downloads, install them using the following commands:

bash

sudo apt update
sudo apt install -y yt-dlp aria2

Step 2: Install Required Python Libraries

Make sure you have the required Python libraries installed. You can install them using pip:

bash

pip install gspread oauth2client

Step 3: Set Up Google Sheets API (Optional)

If you plan to use Google Sheets to fetch video URLs, follow these steps:

    Go to the Google Cloud Console.
    Create a project and enable the Google Sheets API and Google Drive API.
    Download your credentials.json file and place it in the project directory.
    Ensure your Google Sheet has URLs listed in the first column.

Step 4: Run the Application

Once everything is installed, you can run the downloader. Navigate to the project directory and run the Python script:

bash

python youtube_command.py

The GUI will open, allowing you to either manually enter YouTube URLs or fetch them from a Google Sheet (if configured).
How It Works

    Manual Input: Click the "Add URL" button and enter a YouTube URL.
    Google Sheets Integration: If the "From Google Sheet" checkbox is selected, the first two URLs from your sheet will be fetched and processed.
    The download progress will be shown in the progress bar.
    You can cancel any download using the "Cancel" button.

Example Command

For manual execution, the downloader uses this command format:

bash

yt-dlp -f best --external-downloader aria2c --external-downloader-args "-x 10 -s 10 -j 10 --max-tries=99 --retry-wait=5" <YouTube URL>

    -x: Number of connections per download.
    -s: Number of segments.
    -j: Number of parallel downloads.

Troubleshooting

    Missing Dependencies: Ensure all required software and Python libraries are installed.
    Google Sheets API Error: Make sure your credentials.json is correctly set up, and the API is enabled in your Google Cloud Console.
    Download Issues: Check your internet connection and ensure the YouTube URL is correct.

Feel free to modify the script to fit your needs!

Contributing

If you'd like to contribute to this project, please follow these steps:

    Fork the repository: Click the "Fork" button at the top-right of the repository page on GitHub to create your own copy of the project.
    Clone your fork: Clone your forked repository to your local machine.

    bash

git clone https://github.com/your-username/your-repo-name.git

Create a new branch: It's good practice to create a new branch for each feature or bug fix you want to work on.

bash

git checkout -b feature/new-feature

Make your changes: Implement your feature or fix the bug in your local environment.
Commit your changes: Once you've made your changes, commit them with a meaningful commit message.

bash

git commit -m "Add feature X"

Push to your fork: Push the changes to your forked repository.

bash

    git push origin feature/new-feature

    Create a Pull Request: Go to the original repository and create a pull request with a description of what you've changed.

License

This project is licensed under the MIT License. You are free to use, modify, and distribute the software, provided that you include a copy of the MIT License in any substantial portions of the project.
FAQ
1. Why is my download stuck at a certain percentage?

If your download is stuck for too long, it could be due to internet connection issues, or the YouTube video server might be having temporary issues. Try restarting the download by canceling and re-adding the URL.
2. Can I download multiple videos at once?

Yes! The script supports multiple simultaneous downloads. You can either enter URLs manually or fetch them in bulk from a Google Sheet. The tool will process them two at a time in parallel.
3. How do I set up the Google Sheets API for bulk downloads?

To set up Google Sheets API:

    Ensure you have your credentials.json file in the root directory of the project.
    Your Google Sheet should have the video URLs listed in the first column.
    Ensure you've enabled the necessary API services in your Google Cloud project (Google Sheets API, Google Drive API).

4. What is aria2c, and why do I need it?

aria2c is a command-line download utility that supports multiple connections and retries, significantly speeding up the download process compared to regular downloads. The script uses yt-dlp with aria2c to optimize downloads by allowing multiple simultaneous connections for each video file.
Known Issues

    File Permissions: Ensure your credentials.json file has the correct permissions so the script can access it.
    Connection Drops: If your internet connection drops, the script may pause. aria2c will retry the connection several times, but if it fails, you may need to restart the download.

Future Improvements

    Add support for additional video formats (e.g., MP4, WebM).
    Add the ability to specify download resolutions (e.g., 720p, 1080p).
    Improve error handling for network issues and YouTube throttling.

Additional Resources

    yt-dlp GitHub Repository
    aria2c Documentation
    Google Sheets API