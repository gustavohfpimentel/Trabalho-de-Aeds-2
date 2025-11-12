# Trabalho Prático 01: Manipulação e Organização de Arquivos de Dados

## Disciplina: Algoritmos e Estruturas de Dados II (AEDS II)
**Instituição:** Universidade Federal de Ouro Preto (UFOP)
**Autor:** Gustavo Henrique F. Pimentel
**Matrícula:** 22.1.8039

---

## 🎯 Objetivo do Projeto

Este trabalho prático tem como objetivo simular e avaliar o impacto de diferentes estratégias de organização de registros em arquivos binários (`.DAT`), considerando as restrições de armazenamento em blocos de tamanho fixo.

O projeto implementa e compara três abordagens principais:
1.  **Registros de Tamanho Fixo**
2.  **Registros de Tamanho Variável Contíguo** (Sem espalhamento)
3.  **Registros de Tamanho Variável Espalhado** (Com fragmentação entre blocos)

## 📁 Estrutura do Repositório

| Arquivo | Descrição |
| :--- | :--- |
| `trabalho_aeds.py` | Código-fonte principal da simulação em Python. |
| `alunos_fixo.dat` | Arquivo de dados gerado com a estratégia de **Tamanho Fixo**. |
| `alunos_var_contiguo.dat` | Arquivo de dados gerado com a estratégia de **Tamanho Variável Contíguo**. |
| `alunos_var_espalhado.dat` | Arquivo de dados gerado com a estratégia de **Tamanho Variável Espalhado**. |
| `relatorio_abnt_final_v4.pdf` | Relatório descritivo da solução e análise comparativa, formatado nas normas ABNT. |

## ⚙️ Como Executar o Projeto

O projeto foi desenvolvido em Python. Para executá-lo, siga os passos abaixo:

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/gustavohfpimentel/Trabalho-de-Aeds-2.git
    cd Trabalho-de-Aeds-2
    ```

2.  **Execute o script principal:**
    ```bash
    python3 trabalho_aeds.py
    ```

O programa solicitará a entrada de parâmetros (como o tamanho do bloco e o número de registros) e gerará os arquivos `.DAT` e as estatísticas de ocupação.

---

## 📊 Resultados e Análise

A análise detalhada dos resultados, incluindo a eficiência de armazenamento e o *trade-off* entre as estratégias, pode ser encontrada no arquivo **`relatorio_abnt_final_v4.pdf`**.

| Estratégia de Armazenamento | Blocos Usados | Eficiência Total | Tipo de Desperdício Principal |
| :--- | :--- | :--- | :--- |
| Tamanho Fixo | 34 | 95,93% | Interno (*Padding*) |
| Variável (Contíguo) | 23 | 87,38% | Externo (Fim dos blocos) |
| Variável (Espalhado) | 20 | 99,04% | Mínimo |

## 📧 Contato

**Gustavo Henrique F. Pimentel**
Matrícula: 22.1.8039
Universidade Federal de Ouro Preto (UFOP)
