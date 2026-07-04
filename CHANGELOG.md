# Changelog

All notable changes to the **gh0sty** framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-07-01

### Added
- **Core Engine**: Fully configurable runtime structure supporting custom logging levels (`Rich` console + file log) and custom local settings.
- **Scan module**: Host identification, IP mapping, and concurrent TCP port scan capabilities (replaces `inventory`).
- **Web module**: HTTP banner/headers parsing, cookie audit flags, redirection history logging, and SSL/TLS peer certificate parsing (replaces `webinfo`).
- **DNS module**: Comprehensive A, AAAA, MX, TXT, NS, SOA, CNAME, and PTR record resolution.
- **Report module**: Convert raw JSON scanning results into CSV, Markdown, PDF, XML, TXT, and cyberpunk dark-themed HTML report templates.
- **Documentation**: Professional README, contributing guidelines, architecture flowmaps, and licensing.
- **CI/CD pipeline**: Automated lint checks (`Ruff`), format checks (`Black`), static typing validation (`Mypy`), and unit tests suite (`PyTest`).
