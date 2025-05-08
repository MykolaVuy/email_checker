# 📧 Email Checker

[![PyPI version](https://img.shields.io/pypi/v/email-checker-mv)](https://pypi.org/project/email-checker-mv/)
[![Python Version](https://img.shields.io/badge/python-3.12+-blue)](https://www.python.org/)
[![Docker Image](https://img.shields.io/badge/docker-ready-blue)](https://hub.docker.com/)
[![MIT License](https://img.shields.io/badge/license-MIT-darkgreen.svg)](LICENSE)

**Email Checker** is a Python-based utility for validating email addresses in bulk or individually. It detects disposable email domains, supports scheduled checks via cron, and is available both as a standalone CLI tool and as a Dockerized service.

---

## 🚀 Features

- ✅ Validate a single email address from the CLI
- 📄 Batch validation from CSV files
- 🕒 Cron integration for scheduled checks
- 🐳 Dockerized for easy deployment
- 🔄 Automatic update of disposable domains list

---

### 📦 Installation (CLI Version)

Install the tool locally using `pip`:

```bash
  pip install email-checker-mv
```

###  Uninstall (CLI Version)

```bash
  pip uninstall email-checker
```

## 🛠️ CLI Commands

### Check a single email:

```bash
  check_email any.name@example.domain
```

### Batch check (from /input/*.csv):

```bash
  check_batch
```

### Update the list of disposable email domains:

```bash
  python3 src/app/utils/update_disposable_domains.py
```

## 🐳 Docker Usage

#### This project includes a manage.sh script to simplify Docker operations.

### Before first usage run:

```bash
  chmod +x manage.sh
```

### Start the service:

```bash
  ./manage.sh start
```

### Stop the service:

```bash
  ./manage.sh stop
``` 

### Destroy the container:

```bash
  ./manage.sh destroy
```

### Follow cron job logs:

```bash
  docker exec -it email_checker tail -f /var/log/cron.log
```

### Run batch check inside Docker:

```bash
  docker exec -it email_checker check_batch
```

### Run single email check inside Docker:

```bash
  docker exec -it email_checker check_email any.name@example.domain
```

#### 📋 Notes

- Input CSV files should be placed in the input/ directory.

- Disposable email domains are fetched from Propaganistas/Laravel-Disposable-Email.

- Cron jobs are preconfigured in the Docker image to run checks and update disposable domains.

#### 📄 License
- This project is licensed under the MIT License.
