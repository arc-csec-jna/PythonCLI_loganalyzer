# Log Analyzer (Python)

A CLI log analysis tool with Python that processes application logs through steaming file processing for minimal memory usage.

Dealing with:

Error metrics
First and last error events

Outputs:
Summary logs
Structured JSON reports

## Project Overview

This project demonstrates:

- Understanding of structured log formats
- CLI-based tool design using argparse
- Streaming file processing for large log handling
- Defensive parsing to handle malformed entries
- Structured report generation for downstream consumption

The analyzer is designed to simulate real-world log triage and backend debugging workflows.

## Why does this matter

Log analysis is critical in backend engineering and SRE workflows:

- Faster debugging in production systems
- Improved incident response and triage
- Foundational tooling for observability pipelines
- Error aggregation for trend analysis

This project models how backend systems process and analyze operational logs at scale.

## Features
- CLI-based log analysis
- Streaming file processing (no full file load into memory)
- Structured line parsing
- handling of malformed lines
- INFO / WARN / ERROR / UNKNOWN event counting
- Top-N error detection
- First and last error timestamp extraction
- Summary text report generation
- Structured JSON report export

## Example usage
CLI:

python log_analyzer.py src/data/sample/system.log --top 5 --json_dir reports

## Example output

Log Summary 
-------------------------
INFO:10
WARN:4
ERROR:5

Top 5 Errors:

1 x connection timeout after 5000ms
1 x connection timeout after 3000ms
1 x unhandled exception in request handler
1 x traceback (most recent call last)
1 x valueerror: invalid user input

## Design considerations

- Used streaming to handle large files
- Normalization of dynamic values for accurate aggregation
- Implementation of defensive parsing to avoid errors on malformed logs
- sorting performed using custom functions
- JSON export for API consumption

# Future improvements

- Normalizing dynami Values
- Structured log formats support
- Filtering based on timestamps
- Unit tests addition
- CI pipeline addition

## Project Structure
Python-pilot-project/
│
├── src/
│   └── log_analyzer.py
│
├── data/
│   └── samples/
│       └── system.log
│
├── reports/
│   └── sample_report.txt
│
├── README.md
├── requirements.txt
├── .gitignore
└── Dockerfile  (future development)


