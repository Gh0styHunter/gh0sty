# Contribuindo para o gh0sty

Obrigado por demonstrar interesse em melhorar o framework **gh0sty**! Agradecemos todas as contribuições, incluindo correções de bugs, novos módulos, verificações de segurança, atualizações de documentação e pull requests.

## Código de Conduta

Por favor, comporte-se profissionalmente e trate todos os colaboradores com respeito. Este projeto foi desenvolvido apenas para fins éticos e de auditoria de alvos autorizada.

## Configuração do Ambiente de Desenvolvimento

Para configurar seu ambiente de desenvolvimento:

1. Clone este repositório:
   ```bash
   git clone https://github.com/Gh0styHunter/gh0sty.git
   cd gh0sty
   ```

2. Configure o ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # No Windows: .venv\Scripts\activate
   ```

3. Instale as dependências de desenvolvimento:
   ```bash
   pip install -e ".[dev]"
   ```

## Diretrizes de Desenvolvimento

Antes de abrir um pull request, certifique-se de que seu código respeita nossas diretrizes de qualidade:

- **Type Hints (Dicas de Tipo)**: Todas as funções e classes devem ser estaticamente tipadas.
- **Docstrings**: Use docstrings no estilo Google da PEP 257.
- **Formatação**: Formate seu código usando `black` (limite de linha: 100):
  ```bash
  black .
  ```
- **Linting**: Mantenha o código livre de avisos usando `ruff`:
  ```bash
  ruff check .
  ```
- **Análise Estática**: Verifique a correção da tipagem com `mypy`:
  ```bash
  mypy gh0sty tests
  ```
- **Testes**: Garanta que todos os testes passem:
  ```bash
  pytest
  ```

Obrigado por manter o **gh0sty** limpo, seguro e profissional!
