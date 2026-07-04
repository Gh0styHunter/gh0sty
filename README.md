# gh0sty Framework

🛡️ **Um Framework Profissional de Coleta de Informações, Inventário de Ativos e Auditoria de Segurança.**

[![Version](https://img.shields.io/badge/version-v1.0.0--beta-orange)](#)

[![Python Version](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue.svg)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

**gh0sty** é um framework de linha de comando de código aberto projetado para hackers éticos, DevOps e profissionais de segurança cibernética realizarem mapeamento de alvos autorizados, exploração de DNS e perfil de segurança de aplicações HTTP. Construído sobre os princípios de Clean Architecture, ele oferece alta modularidade, tipagem estática completa (`mypy`), execuções de pool de threads personalizadas e visualizações avançadas no console.

> [!IMPORTANT]
> **Aviso Legal:** Esta ferramenta é destinada apenas para auditorias de inventário autorizadas, análise de segurança e fins educacionais. O uso em alvos não autorizados é estritamente proibido e viola as leis de segurança cibernética.

---

## 🚀 Principais Recursos

* **Arquitetura Modular**: Comandos implementados como módulos individuais e desacoplados que compartilham utilitários principais em `gh0sty/modules/`.
* **Estética**: Saídas de linha de comando refinadas usando `Rich` para spinners, barras de progresso, tabelas e temas cyberpunk.
* **Inventário de Portas TCP**: Descoberta de hosts multi-threaded e varreduras de conexões de socket com rastreamento de progresso.
* **Perfilador Web**: Auditorias profundas verificando cabeçalhos HTTP, presença de cabeçalhos de segurança, atributos de segurança de cookies (flags Secure/HttpOnly), metadados de certificados TLS e caminhos de redirecionamento.
* **Mecanismo de Consulta DNS**: Resolve e registra registros padrão (`A`, `AAAA`, `MX`, `TXT`, `NS`, `SOA`, `CNAME`, `PTR`).
* **Compilador de Relatórios Elegante**: Converte sessões de varredura em JSON estruturado, CSV, Markdown limpo, PDF, XML, TXT ou uma interface HTML com tema escuro.
* **Qualidade de CI/CD**: Validações automatizadas usando verificações de tipagem do `pytest`, `black`, `ruff` e `mypy`.

---

## 🛠️ Visão Geral da Arquitetura

A base de código está organizada em camadas de componentes isoladas para garantir baixo acoplamento:
- `gh0sty/core/`: Gerenciamento de configurações, logs ricos no console, catalogação de exceções e loops de análise de linha de comando.
- `gh0sty/modules/`: Mapeamento de operações de alvo para subcomandos individuais.
- `gh0sty/utils/`: Resolvedores comuns, verificadores de socket e loops de execução de pool de threads concorrentes.
- `gh0sty/output/`: Alvos onde os relatórios de saída da varredura são salvos.
- `gh0sty/templates/`: Layouts base para relatórios HTML, Markdown e PDF.

---

## 📦 Instalação

Para instalar o **gh0sty** globalmente ou em seu ambiente atual:

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/Gh0styHunter/gh0sty.git
   cd gh0sty
   ```

2. **Configure um Ambiente Virtual**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # No Windows: .venv\Scripts\activate
   ```

3. **Instale as dependências padrão e de desenvolvimento**:
   ```bash
   pip install -e ".[dev]"
   ```

---

## ⚡ Início Rápido

Realize uma varredura básica de portas TCP em um host alvo autorizado:
```bash
gh0sty scan -t example.com -p 22,80,443 -f html -o gh0sty/output/html/inventory_report.html
```

Audite as configurações de SSL/TLS e cookies de uma aplicação web:
```bash
gh0sty web -t https://example.com -f md -o gh0sty/output/markdown/web_audit.md
```

Explore registros DNS para um domínio alvo:
```bash
gh0sty dns -t google.com
```

Leia as configurações globais:
```bash
gh0sty config --show
```

---

## 📂 Documentação

* Consulte [docs/usage.md](file:///c:/Users/Jackson%20F%20Bertoldo/Desktop/Projetos-Sec/gh0sty/docs/usage.md) para cobertura completa de comandos e flags da CLI.
* Consulte [docs/architecture.md](file:///c:/Users/Jackson%20F%20Bertoldo/Desktop/Projetos-Sec/gh0sty/docs/architecture.md) para esquemas arquiteturais principais.

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
