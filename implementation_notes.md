# Implementation notes

## objetivo

Este documento resume a implementacao do desafio tecnico com foco nos requisitos do readme, cobertura de testes e pipeline de ci.

## o que foi implementado

- endpoint `POST /analyze-feed` em `main.py`
- modulo de analise em `sentiment_analyzer.py`
- validacoes de entrada com retorno 400
- regra de negocio `time_window_minutes == 123` com retorno 422 e codigo `UNSUPPORTED_TIME_WINDOW`
- analise de sentimento com:
  - tokenizacao deterministica
  - normalizacao nfkd para matching
  - intensificador na palavra seguinte
  - negacao com escopo de 3 tokens e paridade
  - bonus mbras para polaridade positiva
- distribuicao de sentimento com exclusao de mensagens `meta`
- calculo de influencia por usuario com:
  - followers deterministico por sha256
  - regras especiais para unicode, tamanho 13 e sufixo `_prime`
  - engagement rate com ajuste da razao aurea em multiplos de 7
  - penalidade para usuarios terminando em `007`
  - bonus para usuarios mbras
- calculo de trending topics com:
  - peso temporal
  - modificador de sentimento
  - fator logaritmico para hashtags longas
  - desempate deterministico
- deteccao de anomalias:
  - burst activity
  - alternating polarity
  - synchronized posting
- flags especiais:
  - `mbras_employee`
  - `special_pattern`
  - `candidate_awareness`
- caso especial de awareness com `engagement_score = 9.42`

## testes executados localmente

comandos usados:

```bash
python -m pytest -q tests/test_analyzer.py
RUN_PERF=1 python -m pytest -q tests/test_performance.py
```

resultado:

- testes unitarios: 14 passed
- teste de performance: 1 passed

## ci no github actions

foi criado o workflow em `.github/workflows/ci.yml` com 3 jobs:

1. `quality`
2. `unit-tests`
3. `performance-tests`

detalhes:

- o job `quality` valida compilacao python
- o job `unit-tests` executa os testes obrigatorios
- o job `performance-tests` executa os testes de performance
- o job de performance esta com `continue-on-error: true` para reduzir falsos negativos por variacao do ambiente de runner

## observacoes de engenharia

- codigo orientado a funcoes pequenas e deterministicas
- regras de negocio isoladas para facilitar manutencao
- tratamento de erros padronizado
- ordenacoes com desempate estavel para garantir reproducibilidade

Rafael Fortuna