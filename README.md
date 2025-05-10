# 📧 Email Checker

[![PyPI version](https://img.shields.io/pypi/v/email-checker-mv?color=darkgreen)](https://pypi.org/project/email-checker-mv/)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue)](https://www.python.org/)
[![Docker Image](https://img.shields.io/badge/docker-ready-blue)](https://hub.docker.com/)
[![MIT License](https://img.shields.io/badge/license-MIT-darkgreen.svg)](LICENSE)

**Email Checker** is a Python-based CLI and Dockerized tool for validating email addresses — individually or in batches. It detects disposable email domains (updated automatically from a public source), integrates with cron for scheduled tasks, and runs smoothly in local and containerized environments.

---

## 🚀 Features

* ✅ Validate a single email address from the CLI or Docker
* 📄 Batch check emails from CSV files (`/input/*.csv`)
* ὐ1 Update and store disposable domains for validation
* 🕒 Scheduled updates via cron (built-in)
* 🐳 Docker-ready for isolated use or integration
* 💻 Easy to install and use via `pip` or `make`

---

## 📦 Installation (CLI version)

```bash
  pip install email-checker-mv
```

### ὐ4 Uninstall

```bash
  pip uninstall email-checker-mv
```

---

## 🛠️ CLI Commands

| Command                           | Description                                    |
| --------------------------------- | ---------------------------------------------- |
| `check_email someone@example.com` | ✅ Check a single email                         |
| `check_batch`                     | 📄 Batch check CSV files in `input/` directory |
| `update_domains`                  | ὐ1 Update the list of disposable domains       |

Disposable domains are fetched from [Propaganistas/Laravel-Disposable-Email](https://github.com/Propaganistas/laravel-disposable-email).

---

## 🐳 Docker Usage

You can control Docker using either `make` or `manage.sh`.

### ▶️ `manage.sh` Script

> Before using it, ensure it’s executable:

```bash
  chmod +x manage.sh
```

| Command                                  | Description                                |
| ---------------------------------------- | ------------------------------------------ |
| `./manage.sh -start`                     | 🟢 Start the Docker container with build   |
| `./manage.sh -stop`                      | 🔵 Stop the running container              |
| `./manage.sh -destroy`                   | ⚠️ Remove containers, images, volumes      |
| `./manage.sh -logs`                      | 📄 Show cron job logs inside the container |
| `./manage.sh -batch`                     | 📬 Run batch check via Docker              |
| `./manage.sh -check someone@example.com` | ✅ Run single email check                   |
| `./manage.sh -update`                    | ὐ1 Update disposable domains inside Docker |
| `./manage.sh -help`                      | ℹ️ Show help message                       |

---

### ⚙️ `Makefile` Shortcuts

> Use `make help` to list all commands.

| Make Command                           | Description                                   |
| -------------------------------------- | --------------------------------------------- |
| `make start`                           | 🟢 Start the container                        |
| `make stop`                            | 🔵 Stop the container                         |
| `make destroy`                         | ⚠️ Remove everything related to the container |
| `make logs`                            | 📄 Follow cron job logs                       |
| `make batch`                           | 📬 Run batch email check inside Docker        |
| `make check email=someone@example.com` | ✅ Check a single email                        |
| `make update`                          | ὐ1 Update disposable domains                  |

---

## 📂 Cron Customization

You can edit the cron configuration directly inside the running container using:

```bash
  docker exec -it email_checker crontab -e
```

This allows advanced scheduling if needed.

---

## 📅 Input Files

* Batch checks read from `.csv` files placed in the `input/` folder.
* Results are stored in the `output/` folder by default.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🌐 Projects by the Author

### [intester.com](https://intester.com)

> **InTester** is a secure and transparent online knowledge assessment platform. It offers time-limited tests, anti-cheating measures, instant results with PDF certificates, and public test records — making it ideal for job seekers and recruiters alike.

### [dctsign.com](https://dctsign.com)

> **DCT Sign** is a blockchain-backed electronic signature platform that prioritizes privacy and data integrity. Users can securely sign documents without storing the original files, ensuring confidentiality and compliance with advanced e-signature standards.

---

*Thank you for using Email Checker! Contributions and feedback are welcome.*
