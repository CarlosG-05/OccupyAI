# 🎓📊 University Study Room Occupancy Tracker 🚀

Welcome to OccupyAI, the ultimate study room monitoring system!  
Track, manage, and visualize university study room occupancy with computer vision, FastAPI, Docker, and Supabase.

## ✨ Features

- 🕵️‍♂️ **Raspberry Pi Client:** Detects room occupancy and sends data to the server.
- ⚡ **FastAPI Server:** Receives, validates, and stores occupancy data.
- 🗄️ **Supabase Database:** Securely stores rooms, logs, and user accounts.
- 🐳 **Dockerized Deployment:** Easy setup and scaling with Docker Compose.
- 🔒 **Environment Security:** Secrets managed via `.env` (never committed!).
- 👥 **User Management:** Authenticated access for students and admins.

## 🛠️ Technologies

- 🐍 Python (Computer Vision, FastAPI)
- 🐳 Docker & Docker Compose
- 🦸 Supabase (PostgreSQL, Auth)
- 🧪 PowerShell/Python scripts for testing

## 🚦 Setup & Usage

1. 🏗️ Set up Supabase and create tables (`study_rooms`, `users`, etc.).
2. 📝 Fill in your `.env` file with Supabase credentials.
3. 🐳 Build and run the FastAPI server:
   ```sh
   docker compose up --build
   ```
4. 🤖 Use the Pi client or test scripts to send occupancy data.
5. 📊 View and manage data in Supabase.

## 🔐 Security

- 🚫 Never commit your `.env` or secrets!
- 🛡️ Enable Row Level Security (RLS) in Supabase for production.

## 🤝 Collaborators

- Carlos Guerrero — Electrial Engineering, UCSD
- Elijah Inamarga — Computer Science, SDSU
- Ruth Maggay — Bio Engineering, UCSD
- Gael Gallarzo
