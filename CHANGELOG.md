# Changelog

Todas as mudanças notáveis no framework **gh0sty** serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto segue o [Versionamento Semântico](https://semver.org/spec/v2.0.0.html) (Semantic Versioning).

## [1.0.0] - 2026-07-01

### Adicionado
- **Mecanismo Principal (Core)**: Estrutura de tempo de execução totalmente configurável que suporta níveis de log personalizados (console `Rich` + log em arquivo) e configurações locais personalizadas.
- **Módulo Scan**: Identificação de hosts, mapeamento de IPs e recursos de varredura concorrente de portas TCP (substitui `inventory`).
- **Módulo Web**: Parsing de cabeçalhos/banners HTTP, flags de auditoria de cookies, registro de histórico de redirecionamentos e parsing de certificados SSL/TLS (substitui `webinfo`).
- **Módulo DNS**: Resolução abrangente de registros A, AAAA, MX, TXT, NS, SOA, CNAME e PTR.
- **Módulo Report**: Converte resultados brutos de varredura em JSON, CSV, Markdown, PDF, XML, TXT e templates de relatório HTML com tema cyberpunk escuro.
- **Documentação**: README profissional, diretrizes de contribuição, fluxos de arquitetura e licenciamento.
- **Pipeline de CI/CD**: Verificações automáticas de lint (`Ruff`), formatação de código (`Black`), validação de tipagem estática (`Mypy`) e suíte de testes unitários (`PyTest`).
