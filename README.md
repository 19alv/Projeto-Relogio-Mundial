#  Horário Mundial

Consultor de horários mundiais em Python, via terminal. Mostra a hora atual de países de todos os continentes e exibe uma saudação (**Bom dia**, **Boa tarde** ou **Boa noite**) de acordo com o horário.

## Funcionalidades

- Saudação inicial conforme o horário local;
- Consulta de horários por continente e país;
- Todos os continentes, com os principais países de cada um;
- Adição de novos países ao continente correto;
- Países adicionados ficam salvos e aparecem nas próximas consultas;
- Busca de fusos horários por parte do nome (ex.: `kolkata`, `tokyo`).

## Como usar

1. Baixe o arquivo `horario_mundial_v2.py` deste repositório (clique em **Code > Download ZIP** e extraia a pasta, ou abra o arquivo e use o botão de download).
2. Abra o terminal na pasta onde o arquivo foi salvo.
3. Execute o programa:

```bash
python horario_mundial_v2.py
```

Exemplo de saída:

```
Boa tarde! Bem-vindo ao
consultor de horários mundiais.
Seu horário local: 29/10/2026 15:15

===== MENU =====
  1 - Consultar por continente/país
  2 - Ver todos os países
  3 - Adicionar um país
  0 - Sair
```

```
Japão
  30/10/2026 03:15 - Boa noite lá
```

## Adicionando um país

1. Escolha a opção **3** no menu
2. Selecione o continente
3. Digite o nome do país (ou país/cidade)
4. Informe o fuso horário no formato IANA (ex.: `Asia/Kolkata`) ou digite parte do nome para buscar

O país é salvo no arquivo `paises_personalizados.json`, criado automaticamente na pasta do script, e passa a aparecer como opção no continente escolhido.

## Regras da saudação

| Horário         | Saudação  |
|-----------------|-----------|
| 05h00 às 11h59  | Bom dia   |
| 12h00 às 17h59  | Boa tarde |
| 18h00 às 04h59  | Boa noite |

## Tecnologias

- Python
- `datetime` e `zoneinfo` (biblioteca padrão)
- `json` para persistência dos países adicionados

## Observação

Em compiladores online, os arquivos criados costumam ser apagados ao fim da sessão, então os países adicionados podem não ser mantidos. Rodando localmente, o arquivo `paises_personalizados.json` é preservado.
