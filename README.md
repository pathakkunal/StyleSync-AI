---
title: MerchFlow AI
emoji: 👟
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# MerchFlow AI - Open Source E-Commerce Agent

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Made%20with-Python-blue.svg)

## About
MerchFlow AI is a **Multi-Agent System built in Pure Python (No LangChain)** that automates product listing generation using Enterprise-Grade Computer Vision. It leverages advanced visual analysis to streamline e-commerce workflows.

## Architecture
The system operates through a coordinated pipeline:
1.  **Input Image** → Raw processing
2.  **Visual Analyst (Gemini 1.5)** → Extracts visual features and metadata
3.  **Manager Agent** → Orchestrates data flow and decision making
4.  **n8n Webhook (Self-Hosted)** → Triggers downstream automation and integration

## Open Source Notice
This project is open source under the MIT License. Feel free to fork and contribute.

## Setup
To run this project, you need to configure the following Environment Variables:

*   `GOOGLE_API_KEY`: Your Google Gemini API Key.
*   `N8N_WEBHOOK_URL`: The URL for your self-hosted n8n webhook connector.
