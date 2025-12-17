# 🤖 Ops Auto-Pilot: Self-Healing DevOps Agent

An autonomous event-driven agent that monitors CI/CD pipelines, diagnoses build failures using **Google Gemini 1.5**, and proposes fixes instantly. Built with **Motia**, **Python**, and **Redis**.

## 🚀 How It Works
1.  **Listener:** A Webhook Step receives `workflow_job` failure events from GitHub.
2.  **Analysis:** The event is passed to an AI Agent Step.
3.  **Diagnosis:** **Google Gemini 1.5 Flash** analyzes the error logs to determine the root cause (e.g., "Out of Memory", "DB Auth Fail").
4.  **Action:** The agent outputs a structured JSON remediation plan.

## 🛠️ Tech Stack
* **Framework:** Motia (Event-Driven Architecture)
* **AI Model:** Google Gemini 1.5 Flash (via `google-generativeai`)
* **State Store:** Redis
* **Language:** Python 3.13

## ⚡️ Quick Start

### 1. Prerequisites
* Node.js & Python 3.13
* Redis (locally running)
* Google Gemini API Key

### 2. Installation
```bash
npm install
./python_modules/bin/pip install -r requirements.txt
./python_modules/bin/pip install -U google-generativeai
// Testing AI Bot
