# Log Fetcher Service

A REST API for fetching Unix log files with filtering and performance optimizations.

## Features
- Fetch logs from `/var/log`.
- Query logs by filename, number of entries, and keyword.
- Efficiently handles large files (>1GB).

## Requirements
- Python 3.8+
- Flask

## Setup
1. Clone the repository.
   ```bash
   git clone <repo_url>
   cd log-fetcher
