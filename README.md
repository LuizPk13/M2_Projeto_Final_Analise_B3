# 📈 Análise de Performance de Ações da B3 (2021–2023)

**Linha temática:** Linha 2 — Performance de Mercado de Ações (B3)

---

## 1. Contexto e Perguntas de Negócio

1. Qual a rentabilidade comparativa (Base 100) de cada ativo de 2021 a 2023?
2. Quais ativos tiveram a melhor relação retorno × risco (Sharpe empírico)?
3. Como se distribuem os retornos diários (dispersão, assimetria e caudas)?
4. Qual o drawdown máximo de cada ativo e qual foi o mais resiliente?
5. Como os preços se comportaram frente às médias móveis SMA 21 e SMA 50?

---

## 2. Fonte de Dados

- **Fonte:** Yahoo Finance via [`yfinance`](https://github.com/ranaroussi/yfinance) (dados públicos, sem dados pessoais)
- **Período:** 04/01/2021 a 28/12/2023, cotação diária (745 pregões por ativo)
- **Ativos:** WEGE3, EMBJ3, VALE3, GGBR4, KLBN11, PETR4, PRIO3, EGIE3, ITUB4, BBDC4, ABEV3, RENT3
- **Observação:** a EMBR3 do enunciado passou a negociar como **EMBJ3** desde 03/11/2025; o histórico foi obtido pelo código novo.

---

## 3. Pipeline de Dados

```
yfinance → extracao.py → cotacoes_brutas.csv → tratamento.py → cotacoes_limpas.csv
         → metricas.py → cotacoes_metricas.csv → Supabase → app.py
```

Cada etapa foi investigada em notebook (`notebooks/`) e consolidada em script (`src/`).

- **Extração:** 8.940 linhas (12 ativos × 745 pregões), com preço ajustado por proventos (`Adj Close`).
- **Tratamento:** colunas renomeadas para português, data convertida para `datetime`, preços arredondados para 2 casas. Não foram encontrados nulos, duplicados ou preços inválidos; o script mantém essas verificações de forma defensiva para futuras extrações. 3 registros com volume zero foram mantidos (ver Limitações).
- **Métricas:** setor, volume financeiro, retorno diário, Base 100, retorno acumulado, drawdown e médias móveis, calculados por ativo em ordem cronológica.

---

## 4. Dicionário de Dados (`cotacoes_metricas.csv`)

| Coluna | Tipo | Descrição / Cálculo |
|---|---|---|
| `data` | datetime | Data do pregão |
| `nome_acao` | str | Código do ativo na B3 |
| `setor` | str | Setor econômico (classificação da B3, simplificada) |
| `abertura`, `maxima`, `minima`, `fechamento` | float | Preços do dia em R$ (2 casas) |
| `fechamento_ajustado` | float | Fechamento ajustado por dividendos e desdobramentos |
| `volume` | int | Quantidade de ações negociadas |
| `volume_financeiro` | float | `volume × fechamento` (R$, aproximado) |
| `retorno_diario` | float | Variação % do preço ajustado frente ao pregão anterior |
| `base_100` | float | Preço ajustado ÷ primeiro preço × 100 |
| `retorno_acumulado` | float | `base_100 / 100 − 1` |
| `drawdown` | float | Queda % em relação ao maior preço já atingido |
| `sma_21`, `sma_50` | float | Médias móveis simples de 21 e 50 pregões |

**Por ativo:** volatilidade anualizada = desvio padrão do retorno diário × √252; Sharpe empírico = retorno acumulado ÷ volatilidade anualizada.

---

## 5. Tecnologias

**Python** (pandas, numpy) para ETL · **yfinance** para extração · **Plotly** para gráficos interativos · **Streamlit** para o Data App · **Supabase/PostgreSQL** com SQLAlchemy para o banco · **Jupyter** para investigação · **Git/GitHub** (GitFlow) e **Trello** (Kanban) para gestão.

---

## 6. Principais Resultados

| Ativo | Setor | Retorno acumulado | Volatilidade anual | Drawdown máx. | Sharpe empírico |
|---|---|---:|---:|---:|---:|
| PETR4 | Petróleo e Energia | 228,69% | 39,42% | −39,10% | 5,80 |
| PRIO3 | Petróleo e Energia | 208,32% | 46,78% | −34,32% | 4,45 |
| EMBJ3 | Bens Industriais | 167,50% | 46,82% | −58,27% | 3,58 |
| EGIE3 | Petróleo e Energia | 25,35% | 18,76% | −17,65% | 1,35 |
| GGBR4 | Materiais Básicos | 30,79% | 35,56% | −33,93% | 0,87 |
| ITUB4 | Financeiro | 24,02% | 28,83% | −35,87% | 0,83 |
| VALE3 | Materiais Básicos | 18,11% | 33,90% | −41,34% | 0,53 |
| WEGE3 | Bens Industriais | 3,51% | 32,83% | −49,51% | 0,11 |
| ABEV3 | Consumo | 2,57% | 25,46% | −31,42% | 0,10 |
| RENT3 | Consumo | −0,25% | 36,89% | −38,40% | −0,01 |
| KLBN11 | Materiais Básicos | −0,80% | 26,62% | −39,30% | −0,03 |
| BBDC4 | Financeiro | −6,93% | 31,38% | −46,05% | −0,22 |

---

## 7. Limitações

- O painel descreve o comportamento dos preços; **correlação não implica causalidade**.
- **Sharpe empírico simplificado:** usa retorno de 3 anos e não desconta a taxa livre de risco (CDI/Selic). Serve apenas para comparar os ativos entre si.
- **Volume zero:** 3 registros (0,03% da base) com volume zero e preços idênticos, indicando falha da fonte. Foram mantidos por terem preço ajustado válido.
- **Preço ajustado e volume financeiro** seguem a metodologia do Yahoo Finance e uma aproximação pelo fechamento, respectivamente.
- Resultados restritos a 12 ativos e 3 anos; **rentabilidade passada não garante rentabilidade futura**.

---

## 8. Aplicação Profissional

---

## 9. Data App

🔗 [PREENCHER: link do Streamlit Cloud]

[PREENCHER: screenshots e guia rápido das abas e filtros]

---

## 10. Como Executar

```bash
git clone https://github.com/LuizPk13/M2_Projeto_Final_Analise_B3.git
cd M2_Projeto_Final_Analise_B3
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt

# Opcional: refazer o pipeline
python src/extracao.py && python src/tratamento.py && python src/metricas.py

# Credenciais: copie .streamlit/secrets.toml.example para secrets.toml e preencha
streamlit run app.py
```

Sem o `secrets.toml`, o app usa o CSV de `data/processed/` como contingência.

---

## 11. Estrutura de Pastas

```
.streamlit/        tema e modelo de credenciais
data/              arquivos brutos e processados
data/processed/    bases limpa e com métricas
data/raw/          base bruta
notebooks/         investigação do tratamento e das métricas
src/               scripts do pipeline
```

---

## 12. Gestão Ágil e Links

- 📋 **Trello:** · [Trello](https://trello.com/b/nUl2gxb3/projeto-analise-b3)
- 🚀 **App:** [PREENCHER]
- 🎥 **Vídeo:** [PREENCHER]

[PREENCHER: print do quadro Trello]

Versionamento em GitFlow: `main`, `develop` e uma `feature/*` por tarefa, integradas via Pull Request.

---

## 13. Autoria e Referências

**Luiz Fernando de Jesus Silva Homem** · [GitHub](https://github.com/LuizPk13)
Projeto Final — Módulo 2: Visualização de Dados e BI — SESISENAI/SC · LAB365 · Prof. Savio Ricardo Garcia

- [pandas](https://pandas.pydata.org/docs/) · [yfinance](https://github.com/ranaroussi/yfinance) · [Streamlit](https://docs.streamlit.io/) · [Plotly](https://plotly.com/python/plotly-express/) · [Supabase](https://supabase.com/docs)
- [Mudança de ticker da Embraer para EMBJ3 — Análise de Ações](https://www.analisedeacoes.com/noticias/embraer-embr3-mudara-de-ticker-na-b3-e-na-nyse-a-partir-de-3-de-novembro/)
- Assistente de IA (Claude, Anthropic) utilizado como apoio para orientação técnica e revisão de código.