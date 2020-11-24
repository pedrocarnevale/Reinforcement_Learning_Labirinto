# Reinforcement_Learning_Labirinto:
Esse projeto tem como objetivo ensinar a máquina a chegar à saída do labirinto, utilizando recompensas e penalidades, ou seja, um **algoritmo de aprendizado por reforço**. O algoritmo utilizado foi o *Q-learning*, onde o agente decide qual ação tomar baseado numa tabela, cujos valores são construídos a partir de recompensas e penalidades. Quando o programa para de ser executado, é gerado um gráfico de linha para análise da evolução do módulo das recompensas ao longo dos episódios.

## Como executar:
- Primeiramente, faça download de todos os arquivos.py desse repositório.
- Além disso, é necessário instalar as bibliotecas *matplotlib*, *numpy* e *pygame*.
- Depois, é necessário executar o arquivo *GeraLabirinto.py*, onde será gerado um labirinto para o agente se locomover. Esse labirinto é gerado através do algoritmo **randomized depth-first search**.
- Após esse passo, basta executar o arquivo *RL_Labirinto.py*, e ver o agente aprendendo a achar a saída do labirinto.

## Alterando parâmetros:

 - No arquivo *GeraLabirinto.py*:
	 - **Comprimento e altura**: Definem o tamanho da tela da interface gráfica.
	 -  **NUM_LINHAS_LABIRINTO e NUM_COLUNAS_LABIRINTO**: Indicam o número de linhas e colunas do labirinto que será gerado.
	 - **TAMANHO_LADO_PAREDE**: Estabelece o tamanho da parede do labirinto.
	
- No arquivo *RL_Labirinto.py*:
	- **Comprimento e altura**: Definem o tamanho da tela da interface gráfica.
	-  **taxa_aprendizado**: Taxa na qual os valores da tabela do algoritmo *Q-learning* são alterados.
	- **desconto**: O quanto o agente leva em consideração as recompensas das ações futuras
	- **episódios**: Número máximo de episódios antes do programa parar de executar
	- **printar_freq**: Determina a cada quantos episódios a interface gráfica irá apresentar o deslocamento do agente.
	- **epsilon**: Define a probabilidade inicial do agente executar uma ação aleatória ou baseada nos valores da tabela do algoritmo.
	- **INICIO_DECAIMENTO_EPSILON e FIM_DECAIMENTO_EPSILON**: Indicam o conjunto de episódios nos quais o valor de epsilon será decrementado.

## Alterando recompensas e penalidades:
- Os valores das recompensas e penalidades dos agentes são definidos através de funções. Essas funções são empíricas, e tem como objetivo facilitar a aprendizagem do agente. Logo, os seus valores precisam ser testados até que seja atingido um desempenho satisfatório do agente. No arquivo *RL_Labirinto.py*, as funções e parâmetros que determinam as recompensas são as seguintes:

	-  **NAO_MOVER_PENALIDADE**: Se o agente não se movimentar em um momento, ele recebe esse valor para penalidade. O agente não se move se a ação escolhida pelo algoritmo fazer com que ele atinja uma parede.
	- **FINAL_TABULEIRO_RECOMPENSA**: Recompensa do agente ao chegar no objetivo. Deve ser um valor elevado para o agente aprender que essa é a principal meta dele.
	- **VISITA_VELHO_PENALIDADE**: Penalidade recebida pelo agente ao visitar um espaço já visitado anteriormente.
	- **VISITA_NOVO_RECOMPENSA**: Recompensa recebida pelo agente ao visitar um novo espaço, estimulando o agente a ir para novos lugares do labirinto.
	- **distancia_penalidade()**: Função que retorna a soma da diferença das coordenadas do agente e da saída do labirinto, que funciona como penalidade para estimular o agente a ficar por perto da saída do labirinto. 
 ## Observações:
 - Os arquivos *indiviuo.py* e *Labirinto.py* não precisam ser executados, pois eles apenas definem os atributos e métodos do agente e do labirinto, respectivamente. No entanto, eles devem estar no diretório dos demais arquivos para que o programa consiga ser executado.
