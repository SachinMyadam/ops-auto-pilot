# 🚀 Ops Auto-Pilot: The Autonomous AI DevOps Engineer

> **"As a solo developer, I didn't have a team to review my code. So, I built one."**

![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-blue)
![AI Model](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-orange)
![Orchestration](https://img.shields.io/badge/Orchestration-Motia-purple)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)

## 💡 The Problem
Developing alone is hard. Without a second pair of eyes, simple bugs (like missing colons or logic errors) slip into production. Context switching between coding, testing, and debugging kills momentum.

## 🤖 The Solution
**Ops Auto-Pilot** is an intelligent, autonomous agent that lives inside the CI/CD pipeline. It acts as a Senior Engineer that never sleeps.
* **Watches** every code push automatically.
* **Analyzes** syntax and logic using Google's **Gemini 2.5 Flash**.
* **Fixes** bugs instantly and explains the solution.
* **Alerts** me in real-time via Discord.

---

## 🏗️ Architecture & Workflow

We utilized a hybrid architecture using **Motia** for orchestration and observability, and **GitHub Actions** for execution.

<img width="1440" height="787" alt="Screenshot 2025-12-18 at 4 35 22 PM" src="https://github.com/user-attachments/assets/991b03b5-e72d-445d-983f-a2be6aa1863a" />


1.  **Trigger:** Developer pushes code to GitHub.
2.  **Orchestration (Motia):** A webhook sends the event payload to **Motia**, which traces the request and visualizes the event flow (`GitHubWebhook` → `AIAnalyzer`).
3.  **Execution (GitHub Actions):** The pipeline spins up a runner and launches the Python Agent.
4.  **Intelligence (Gemini 2.5):** The agent reads the diff and queries Gemini 2.5 Flash to find bugs.
5.  **Notification (Discord):** The agent formats the fix and pings the Discord channel immediately.

---

## 🛠️ Tech Stack

* **Orchestration & Observability:** [Motia](https://motia.com) (Visualizing event flows and tracing webhooks).
* **CI/CD Automation:** GitHub Actions.
* **AI Intelligence:** Google Gemini 2.5 Flash (via Google GenAI SDK).
* **Alerting:** Discord Bot API.
* **Language:** Python 3.10+.

---

## ⚡ How It Works (Demo)

1.  **The Mistake:** I push a file `bad_code.py` with a syntax error (e.g., missing colon).
2.  **The Trigger:** `git push origin main` automatically wakes up the agent.
3.  **The Fix:** Within 30 seconds, my Discord server pings:
    > 🚨 **AI Code Review Alert**
    > "The bug in your code is a missing colon in the for loop statement."

---

## 🚀 Setup & Installation

### 1. Environment Variables
To replicate this pipeline, you need the following secrets in GitHub Actions:
* `GOOGLE_API_KEY`: For Gemini AI.
* `DISCORD_TOKEN`: For the Bot notification.

### 2. GitHub Workflow
The automation is defined in `.github/workflows/deploy.yml`, which triggers on every `push` event.

### 3. Motia Integration
Configure a Webhook in GitHub Settings pointing to your Motia Ingress URL to enable visual tracing.

---

## 🏆 Future Improvements
* **Auto-Merge:** Allow the AI to automatically merge the PR if the fix is simple.
* **Jira Integration:** Create tickets automatically for complex bugs.
