# You Translate
CRUD para trabalho de Linguagem de Programação

# Informações de Login

Admin
email: admin@youtranslate.com
senha: admin123

User
email: user@youtranslate.com
senha: user123

# Introdução

O “You Translate” é uma ferramenta onde o usuário poderá traduzir palavras de maneira rápida e prática, além de conhecer seu significado e aplicação. Os idiomas utilizados para essa aplicação são o inglês e português, assim o usuário terá acesso às informações da palavra desejada em ambas as línguas.

# Metodologia
Para o desenvolvimento desse projeto serão utilizados: Python para back end, SqLite 3 para banco de dados e Tkinter para a interface gráfica.

O You translate conta com duas classes de usuários e suas respectiva permissões:

Permissões          Administrador      Comum
Add conteúdo            sim             não
Editar conteúdo         sim             não
Visualizar conteúdo     sim             sim
Deletar conteúdo        sim             não


Para o cadastro desses usuário serão necessários os seguinte parâmetros:
id - int
email - str (primary key)
senha - str
adm - bool (se TRUE, indica que o usuário é administrador. Se FALSE, indica que é um usuário comum.)


Para o cadastro do conteúdo do app, serão necessários os seguintes parâmetros:

id - int
pt-word - str (primary key)
pt-meaning - str
eng-word - str
eng-meaning - str

Caso o usuário logado seja um administrador, a tela irá mostrar as opções de ações como adicionar nova palavra, editar uma palavra já cadastrada, deletar ou visualizar todo conteúdo. Ao contrário do administrador, o usuário comum terá somente acesso ao tradutor, ou seja, ele insere a palavra que deseja traduzir e terá como resposta a sua tradução e significado.


exemplo de CRUD com banco de dados
https://dev.to/driuzim/criando-um-crud-simples-com-python-opl

exemplo de CRUD com banco de dados e tela com Tkinter
https://www.youtube.com/watch?app=desktop&v=7N25wyyJ7pc&ab_channel=UsandoPython

from tabulate import tabulate ---> evita o uso de for para mostrar listas no vscode
