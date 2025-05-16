# 📧 Email Checker

[![PyPI version](https://img.shields.io/pypi/v/email-checker-mv?color=darkgreen)](https://pypi.org/project/email-checker-mv/)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue)](https://www.python.org/)
[![Docker Image](https://img.shields.io/badge/docker-ready-blue)](https://hub.docker.com/)
[![MIT License](https://img.shields.io/badge/license-MIT-darkgreen.svg)](https://raw.githubusercontent.com/MykolaVuy/email_checker/refs/heads/main/LICENSE)
[![GitHub Repo](https://img.shields.io/badge/source-GitHub-black?logo=github)](https://github.com/MykolaVuy/email_checker)

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

## 📂 Source Code

The complete source code is available on [GitHub](https://github.com/your-username/email-checker).  
Feel free to explore, contribute, or fork the project.

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

| Command                              | Description                                     |
|--------------------------------------|-------------------------------------------------|
| `check_email someone@example.com`    | ✅ Check a single email (default output)         |
| `check_email someone@example.com -S` | ✅ Check a single email (short output)           |
| `check_email someone@example.com -F` | ✅ Check a single email (full output)            |
| `check_batch`                        | 📄 Batch check `.csv` files in the `input/` dir |
| `update_domains`                     | 🔄 Update the list of disposable domains        |

Disposable domains are fetched from [Propaganistas/Laravel-Disposable-Email](https://github.com/Propaganistas/laravel-disposable-email).

#### 📄 CSV Format for `check_batch`

The `check_batch` command processes a CSV file located in the `input/` directory and expects the following format:

- **Delimiter**: Must be a **comma (`,`)**
- **Headers**: Required columns are:
  - `email` – the email address to validate
  - `status` – must be one of the supported values below

Only rows with the appropriate `status` values will be processed. All others will be skipped.

#### 🏷️ Supported `status` Values for `check_batch`

| Status       | Description                                                   |
|--------------|---------------------------------------------------------------|
| `check`      | Check email with default verbosity                            |
| `check S`    | Check email with **short** response                           |
| `check F`    | Check email with **full** response                            |
| `undefined`  | Alias for `check`, treated the same as `check`               |
| `undefined S`| Alias for `check S`, runs with **short** verbosity            |
| `undefined F`| Alias for `check F`, runs with **full** verbosity             |

#### ✅ Example input file (`input/emails.csv`)

```csv
email,status
user1@example.com,check
user2@example.com,undefined
user3@example.com,check S
user4@example.com,undefined F
```


### 📤 Output

The output format is consistent across both `check_email` (CLI) and `check_batch` (CSV):

- When using **CLI**, results are printed to the terminal.
- When using **batch**, results are written to the `status` column in the CSV file.

You can safely rerun the same CSV file — already processed rows (anything except `check`, `check S`, `check F`, etc.) will be skipped.

#### 📋 Possible values

| Result Format                             | Meaning                                         |
| ----------------------------------------- | ------------------------------------------------|
| `valid`                                   | 📥 Address exists and accepts emails            |
| `invalid\|format`                         | ❌ Invalid email format (regex check failed)    |
| `invalid\|non-ascii`                      | ❌ Email contains non-ASCII characters          |
| `invalid\|disposable`                     | 🗑️ Disposable/temporary email address           |
| `invalid\|mx`                             | 📡 No MX record found for the domain            |
| `invalid\|smtp no-code: <msg>`         	 | 🚫 SMTP connection was closed without a response|
| `invalid\|smtp <cat_short> <code>`        | ⚙️ Default output: short type and SMTP code     |
| `invalid\|smtp <cat>\|<code>\|<msg_short>` | 🧾 Short output: verbose type and short message |
| `invalid\|smtp <cat>\|<code>\|<msg>`      | 📜 Full output: verbose type and full message   |

> 📝 These formats apply both in CLI and in .csv batch processing.

#### 📦 SMTP Response Type Codes

| Code | Meaning                                                                    |
| ---- | -------------------------------------------------------------------------- |
| `HB / hard-bounce`    | ❌ **Hard bounce** – Address does not exist               |
| `SB / soft-bounce`    | ⚠️ **Soft bounce** – Temporary delivery issue             |
| `PE / protocol-error` | 🧩 **Protocol error** – SMTP syntax or protocol failure   |
| `UN / unknown`        | ❓ **Unknown** – Unclassified or unknown SMTP response    |
| `NC / no-code`        | 🔌 **No code** – Connection closed unexpectedly (no code) |

> 📎 Note: `check_batch` rewrites the result to the "status" column in the output CSV file for each email.

---

## 🐳 Docker Usage

You can control Docker using either `make` or `manage.sh`.

### ▶️ `manage.sh` Script

> Before using it, ensure it’s executable:

```bash
  chmod +x manage.sh
```

| Command                                     | Description                             |
| ------------------------------------------- | --------------------------------------- |
| `./manage.sh -start`                        | 🟢 Start the container with build       |
| `./manage.sh -stop`                         | 🛑 Stop the container                   |
| `./manage.sh -destroy`                      | ⚠️ Remove container, images, volumes    |
| `./manage.sh -logs`                         | 📄 Tail cron logs                       |
| `./manage.sh -batch`                        | 📬 Run batch email check                |
| `./manage.sh -check someone@example.com`    | ✅ Run single email check                |
| `./manage.sh -check someone@example.com -S` | ✅ Run single email check (short output) |
| `./manage.sh -check someone@example.com -F` | ✅ Run single email check (full output)  |
| `./manage.sh -update`                       | 🔄 Update list of disposable domains    |
| `./manage.sh -help`                         | ℹ️ Show this help message               |


### ⚙️ `Makefile` Shortcuts

> Use `make help` to list all commands.

| Command                                     | Description                             |
| ------------------------------------------- | --------------------------------------- |
| `./manage.sh -start`                        | 🟢 Start the container with build       |
| `./manage.sh -stop`                         | 🛑 Stop the container                   |
| `./manage.sh -destroy`                      | ⚠️ Remove container, images, volumes    |
| `./manage.sh -logs`                         | 📄 Tail cron logs                       |
| `./manage.sh -batch`                        | 📬 Run batch email check                |
| `./manage.sh -check someone@example.com`    | ✅ Run single email check                |
| `./manage.sh -check someone@example.com -S` | ✅ Run single email check (short output) |
| `./manage.sh -check someone@example.com -F` | ✅ Run single email check (full output)  |
| `./manage.sh -update`                       | 🔄 Update list of disposable domains    |
| `./manage.sh -help`                         | ℹ️ Show this help message               |


### 📂 Cron Customization

You can edit the cron configuration directly inside the running container using:

```bash
  docker exec -it email_checker crontab -e
```

This allows advanced scheduling if needed.

---

## 📄 License

This project is licensed under the [MIT License](https://raw.githubusercontent.com/MykolaVuy/email_checker/refs/heads/main/LICENSE).

---

## 🌐 Projects by the Author

### [intester.com](https://intester.com)

> **InTester** is a secure and transparent online knowledge assessment platform. It offers time-limited tests, anti-cheating measures, instant results with PDF certificates, and public test records — making it ideal for job seekers and recruiters alike.

### [dctsign.com](https://dctsign.com)

> **DCT Sign** is a blockchain-backed electronic signature platform that prioritizes privacy and data integrity. Users can securely sign documents without storing the original files, ensuring confidentiality and compliance with advanced e-signature standards.

---

*Thank you for using Email Checker! Contributions and feedback are welcome.*
