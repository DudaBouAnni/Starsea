# Starsea

API para gerenciamento de eventos musicais, conectando usuários, artistas, gêneros e organizadores. O projeto também possui integração com o Spotify para identificar usuários e importar informações de seus perfis.

O repositório contém o backend da aplicação e está em desenvolvimento.

## Tecnologias

- **Python** e **FastAPI** para a API HTTP.
- **SQLAlchemy** para acesso ao banco de dados e mapeamento das entidades.
- **Pydantic** para os schemas de entrada, saída e configuração.
- **MySQL**, utilizado pelo script de criação do banco.
- **Requests** para comunicação com o Spotify e o serviço de geolocalização.
- **python-dotenv** para carregar variáveis de ambiente.

## Funcionalidades

- Cadastro, listagem, atualização e exclusão de usuários, artistas, gêneros, organizadores e eventos.
- Associação de artistas a eventos e gêneros musicais.
- Associação de usuários a eventos e gêneros favoritos.
- Consulta de eventos de um artista ou organizador e de artistas de um gênero.
- Fluxo de login com Spotify e importação de nome, e-mail, imagem e país do perfil.
- Consulta opcional de cidade e estado por IP no login, sem substituir as coordenadas do dispositivo.
- Descoberta de shows próximos por coordenadas e raio de distância.
- Notificações na aplicação, com preferência de recebimento e marcação de leitura.
- Integração com Google Maps para consultar trajetos de carro, a pé, bicicleta e transporte público.
- Importação dos artistas de maior afinidade do Spotify e escolha manual de artistas favoritos.
- Recomendações e avisos que cruzam artistas ou gêneros do perfil musical, data do show e proximidade.

Parte das rotas apresenta falhas de implementação. Consulte as limitações ao final deste documento antes de utilizar a API.

## Estrutura do projeto

```text
app/
├── api/          # Rotas HTTP, dependências compartilhadas e registro de routers
├── core/         # Configurações da integração com Spotify
├── database/     # Conexão, base dos modelos e script SQL
├── exceptions/   # Exceções HTTP personalizadas
├── models/       # Modelos SQLAlchemy e tabelas associativas
├── schemas/      # Schemas Pydantic
├── services/     # Regras de negócio e integrações externas
└── main.py       # Inicialização da aplicação
```

O fluxo principal de uma requisição é: **rota → serviço → banco de dados**. Os schemas definem os formatos dos dados recebidos e das respostas que possuem um modelo declarado.

### Organização e padrões de código

- `app/api/dependencies.py` fornece a sessão do banco para as rotas e garante seu fechamento. Os módulos antigos continuam expondo `get_db` por importação para manter compatibilidade.
- `app/api/router.py` reúne os routers na ordem de registro da aplicação.
- `app/main.py` concentra a inicialização da API, o registro de rotas e o health check.
- As operações de localização, preferências e sincronização de notificações ficam em `app/services/nearby_service.py`; as rotas recebem os dados e delegam essas operações.
- A integração com o Google Maps separa a montagem de coordenadas, a interpretação das estimativas e a consulta ao provedor em funções menores.
- Os schemas utilizam `ConfigDict` do Pydantic 2 para a leitura de objetos do banco.
- `pyproject.toml` define os padrões de imports e formatação do Ruff e o diretório dos testes.

A organização preserva os arquivos existentes, os caminhos HTTP, os parâmetros e os schemas da API. As limitações funcionais anteriores continuam descritas ao final deste documento.

## Modelo de dados

| Entidade | Finalidade |
| --- | --- |
| Usuário | Armazena dados de perfil, identificação do Spotify e localização. |
| Evento | Armazena nome, descrição, data, local, link de ingressos e organizador. |
| Artista | Representa um artista participante de eventos. |
| Gênero | Representa um gênero musical associado a artistas e usuários. |
| Organizador | Representa o responsável por eventos. |
| Notificação | Guarda um aviso por usuário e evento, com distância e estado de leitura. |

Relacionamentos utilizados pelos modelos:

- Um organizador possui vários eventos; cada evento referencia um organizador.
- Eventos e artistas possuem relação de muitos para muitos.
- Artistas e gêneros possuem relação de muitos para muitos.
- Usuários e eventos possuem relação de muitos para muitos.
- Usuários e gêneros possuem relação de muitos para muitos.

Existe também uma tabela `organizer_event` no código, mas os relacionamentos dos modelos utilizam o campo `organizer_id` do evento.

## Configuração local

### Pré-requisitos

- Python 3.13, versão utilizada nos testes desta implementação.
- MySQL em execução e credenciais de acesso a um banco local.
- Aplicativo cadastrado no Spotify Developer Dashboard para configurar as credenciais OAuth.

As dependências estão em `requirements.txt`, com intervalos de versões. Os testes utilizam SQLite e simulam Google Maps e Spotify; a integração real com MySQL, Spotify e Google precisa ser validada com as credenciais do ambiente.

### 1. Acessar o projeto e criar um ambiente virtual

No PowerShell, dentro da pasta que contém o repositório:

```powershell
cd Starsea
python -m venv .venv
```

Os próximos comandos utilizam diretamente o Python do ambiente virtual, sem depender de sua ativação no terminal.

### 2. Instalar as dependências

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

O driver `pymysql` corresponde à URL de conexão apresentada abaixo.

### 3. Configurar as variáveis de ambiente

Copie `.env.example` para `.env` na raiz do repositório e preencha os valores:

```powershell
Copy-Item .env.example .env
```

```dotenv
DATABASE_URL=mysql+pymysql://usuario:senha@localhost:3306/starsea
SPOTIFY_CLIENT_ID=seu_client_id
SPOTIFY_CLIENT_SECRET=seu_client_secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8000/auth/callback
GOOGLE_MAPS_API_KEY=
```

Substitua os valores de exemplo pelas suas configurações. Caracteres especiais no usuário ou na senha precisam ser codificados para uso em uma URL de conexão.

A URI de redirecionamento deve corresponder à configurada no aplicativo do Spotify. Os campos de configuração do Spotify devem existir no `.env`; podem ficar vazios para testar outras rotas, mas `/auth/login` retornará 503 até que as credenciais sejam preenchidas.

O arquivo `.env` está listado no `.gitignore` e não deve ser incluído em commits.

### 4. Preparar o banco de dados

Execute o arquivo `app/database/schema.sql` em um cliente MySQL, como o MySQL Workbench. Ele cria o banco `starsea` e suas tabelas; o usuário utilizado na execução precisa ter as permissões correspondentes.

O script contém `CREATE DATABASE` e `CREATE TABLE` sem `IF NOT EXISTS`. Execute-o em um ambiente novo ou revise as instruções antes de aplicá-lo a um banco já existente.

A aplicação também chama `Base.metadata.create_all()` ao iniciar. Essa chamada cria tabelas ausentes, mas não atualiza tabelas existentes.

**Se o banco já existia antes da funcionalidade de proximidade**, faça um backup e execute a migração antes de iniciar a API:

```powershell
.\.venv\Scripts\python.exe -m app.database.migrate_nearby
```

A migração adiciona coordenadas, preferências e a tabela de notificações sem apagar os registros existentes. Pode ser executada novamente; não altera as colunas que já existem. No MySQL, alterações de estrutura podem ser confirmadas implicitamente, portanto não há rollback automático dessa migração. Não execute novamente o script de criação completo em um banco existente.

### 5. Iniciar a API

Na raiz do repositório:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Com a aplicação iniciada:

- API local: <http://127.0.0.1:8000>
- Documentação Swagger: <http://127.0.0.1:8000/docs>
- Documentação ReDoc: <http://127.0.0.1:8000/redoc>

A rota `GET /` retorna:

```json
{"status": "ok"}
```

## Rotas principais

| Prefixo | Responsabilidade |
| --- | --- |
| `/users` | Usuários, associação a eventos e gêneros favoritos. |
| `/artists` | Artistas, gêneros associados e consulta de eventos. |
| `/genres` | Gêneros musicais e consulta de artistas. |
| `/organizers` | Organizadores e consulta de seus eventos. |
| `/events` | Eventos e associação de artistas. |
| `/auth` | Integração de login com Spotify. |

Os recursos de cadastro utilizam `POST`, as consultas utilizam `GET`, as atualizações utilizam `PATCH` e as exclusões utilizam `DELETE`. Os caminhos, parâmetros e schemas completos podem ser consultados em `/docs` quando a API estiver em execução.

## Perfil musical e Spotify

### Configuração e autorização

Para um banco existente, execute a migração antes de iniciar a API. Ela também aplica a migração de proximidade, preservando os dados:

```powershell
.\.venv\Scripts\python.exe -m app.database.migrate_music
```

Configure `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET` e `SPOTIFY_REDIRECT_URI` no `.env`. Registre a URI exata de callback no aplicativo do Spotify. O segredo fica no servidor.

1. O navegador consulta `GET /auth/login` e mantém o cookie recebido.
2. A API retorna `login_url`, com as permissões `user-read-email`, `user-read-private` e **`user-top-read`**, além de um `state` aleatório.
3. A pessoa abre essa URL e autoriza o acesso na própria página do Spotify.
4. O Spotify redireciona para `/auth/callback` com `code` e `state`; o backend valida o cookie de autorização, com validade de dez minutos.
5. O backend consulta o perfil e até 50 artistas de maior afinidade no período `medium_term`, aproximadamente seis meses.
6. O backend cadastra ou atualiza o usuário, substitui seu snapshot de artistas do Spotify e reconcilia os avisos de shows próximos.

Use o mesmo host no início do fluxo e no callback, por exemplo `127.0.0.1`, para que o navegador envie o cookie. Não misture esse host com `localhost`. Usuários que já tinham autorizado o aplicativo precisam passar novamente pelo consentimento para conceder `user-top-read`.

A resposta do callback inclui `user` e `imported_artists`; não expõe senha local, código de autorização nem tokens. Tokens são usados somente nessa requisição e não são persistidos. **A importação ocorre ao autorizar o Spotify: não há atualização periódica nem monitoramento contínuo.** Para atualizar o perfil musical, repita o fluxo de autorização. As escolhas manuais são preservadas.

Os artistas vêm do endpoint oficial [Get User's Top Items](https://developer.spotify.com/documentation/web-api/reference/get-users-top-artists-and-tracks): trata-se de afinidade calculada pelo Spotify, sem contagem exata de reproduções. Aplicativos em desenvolvimento devem atender às [regras de acesso e cotas do Spotify](https://developer.spotify.com/documentation/web-api/concepts/quota-modes), incluindo a configuração de usuários autorizados e os requisitos de conta do proprietário.

Falhas, respostas inválidas e limites de consultas não apagam o perfil anterior. O callback agora trata a localização por IP como opcional; IPs privados e falhas de geolocalização não impedem a importação.

### Artistas e avisos personalizados

| Método e rota | Finalidade |
| --- | --- |
| `GET /users/1/music-profile` | Lista artistas, gêneros estimados, fontes, cobertura dos dados e data da última importação. |
| `PUT /users/1/music-profile/artists/2` | Seleciona manualmente o artista 2 do catálogo local. |
| `DELETE /users/1/music-profile/artists/2` | Remove somente a escolha manual desse artista. |
| `DELETE /users/1/music-profile/spotify` | Apaga as preferências importadas, preservando escolhas manuais. |
| `PUT /users/1/music-profile/genres/2` | Seleciona manualmente o gênero 2, sem alterar os dados importados. |
| `DELETE /users/1/music-profile/genres/2` | Remove somente a escolha manual do gênero. |
| `GET /users/1/recommended-events` | Lista shows próximos por artista ou gênero, com os motivos da recomendação. |

A busca de recomendações aceita `radius_km`, `offset` e `limit`, como a busca geral. Só considera eventos cadastrados no Starsea; o Spotify não é utilizado como fonte de agenda de shows.

A primeira importação do Spotify e a seleção manual ativam `personalized_notifications_only`. Para voltar a receber avisos gerais, envie `{"personalized_notifications_only": false}` em `PATCH /users/1/notification-preferences`. Reimportações preservam essa opção depois da primeira sincronização. Os usuários sem perfil musical mantêm o comportamento anterior de avisos gerais.

Com o filtro ativo, um aviso exige **artista ou gênero do perfil + evento de hoje em diante + coordenadas + distância dentro do raio**. Um perfil vazio não gera avisos personalizados. Mudanças nos artistas ou gêneros do catálogo também atualizam os avisos. `GET /nearby-events`, no caminho completo do usuário, continua mostrando a busca geral independentemente do gosto musical.

### Contrato da estimativa de gêneros

O importador utiliza o campo `genres` dos artistas quando o Spotify o disponibiliza. Campos ausentes, nulos ou vazios não impedem o uso dos artistas favoritos. Dados malformados interrompem a importação sem apagar o perfil anterior.

- Cada artista do ranking contribui com peso `1 / posição`, dividido igualmente entre seus gêneros distintos.
- O mesmo artista selecionado manualmente e importado conta uma única vez. Artistas somente manuais contribuem com peso 1.
- Uma escolha manual de gênero acrescenta peso 1 e é sempre elegível para recomendações.
- `affinity_percent` normaliza esses pesos; **não representa porcentagem de tempo ouvido ou reproduções**.
- Até cinco gêneros principais, além de todos os escolhidos manualmente, são usados no filtro. O campo `used_for_recommendations` indica quais foram selecionados.
- `genre_data_status` pode ser `available`, `partial`, `manual` ou `unavailable`. O frontend deve sinalizar cobertura parcial ou ausência de dados.
- `sources` distingue `spotify`, `artist_catalog` e `manual`. Quando o Spotify não fornece gêneros, os gêneros curados do artista no catálogo podem servir como alternativa, identificada por `artist_catalog`.

As tabelas `artist_spotify_genre` e `music_preference_genre` separam metadados do provedor dos gêneros manuais e preservam um snapshot por usuário. Uma nova importação de outro usuário não reescreve o histórico de afinidade já importado. Para instalações existentes, execute novamente `python -m app.database.migrate_music`; o comando cria essas tabelas de forma aditiva.

Em `/recommended-events`, `matched_artists`, `matched_genres` e `match_reasons` explicam a correspondência. Esses campos podem ser usados no frontend para exibir, por exemplo, “Porque você gosta de rock”. A busca continua limitada aos eventos cadastrados no Starsea e aos gêneros conhecidos dos artistas desses eventos.

Para identificar artistas, prefira preencher `spotify_id` no cadastro ou atualização do artista. A importação procura esse ID primeiro; só vincula um nome a um cadastro antigo quando existe uma única correspondência exata após normalização de caixa, espaços e Unicode. Nomes ambíguos não são associados automaticamente. Nesses casos, revise o catálogo e vincule o artista correto ao evento. As respostas do perfil incluem o link de origem do Spotify; ao exibir esses dados no frontend, siga as regras de atribuição do provedor.

Apagar as preferências do Spotify não revoga a autorização no provedor; a pessoa pode removê-la nas configurações da própria conta Spotify. O fluxo de importação ainda não cria uma sessão de acesso do Starsea: as rotas por `user_id` precisam de autenticação antes de exposição pública.

### YouTube Music

A API oficial do YouTube não disponibiliza o histórico de reprodução necessário para calcular os artistas mais ouvidos. Essa limitação está registrada na [documentação oficial](https://developers.google.com/youtube/v3/revision_history). Não há integração automática de histórico do YouTube Music nesta implementação, e não são solicitados cookies da conta Google.

Quem utiliza YouTube Music pode selecionar artistas manualmente pelos mesmos endpoints e receber os mesmos avisos de shows. Uma futura integração com playlists precisará de uma implementação própria e de confirmação dos artistas: playlist, canal e histórico de audição representam dados diferentes.

## Shows próximos e notificações

As coordenadas do usuário vêm do dispositivo, com a permissão de localização solicitada pelo futuro frontend, ou de um ponto escolhido manualmente. A localização aproximada por IP não é usada para decidir a proximidade. Não há rastreamento automático do dispositivo no backend.

### Registrar a localização do usuário

```http
PUT /users/1/location
Content-Type: application/json

{
  "latitude": -23.5505,
  "longitude": -46.6333
}
```

Para apagar a localização salva e os avisos associados, utilize `DELETE /users/1/location`.

### Informar o local do show

Envie `latitude` e `longitude` junto dos campos já exigidos em `POST /events/`. Exemplo:

```json
{
  "event_name": "Noite Starsea",
  "event_description": "Show de música ao vivo",
  "event_date": "2027-06-20",
  "event_location": "Praça da Sé, São Paulo",
  "ticket_link": "https://example.com/ingressos",
  "organizer_id": 1,
  "artists": [],
  "latitude": -23.5507,
  "longitude": -46.6336
}
```

O organizador deve existir. Ajuste a data para hoje ou uma data futura. As coordenadas são opcionais para manter a compatibilidade com os cadastros antigos, mas são necessárias para busca por proximidade e consulta de trajetos.

Também é possível atualizar as duas coordenadas com `PATCH /events/{event_id}`. Envie ambas como `null` para remover a localização. O texto de `event_location` não é convertido automaticamente em coordenadas; ao mudar o local, atualize também as coordenadas ou remova as antigas.

### Configurar os avisos

```http
PATCH /users/1/notification-preferences
Content-Type: application/json

{
  "notification_radius_km": 30,
  "nearby_notifications_enabled": true
}
```

O raio padrão é de **50 km**, com valores permitidos maiores que zero e até 1.000 km. Consulte as preferências em `GET /users/1/notification-preferences`.

### Consultar shows e avisos

| Método e rota | Resultado |
| --- | --- |
| `GET /users/1/nearby-events` | Shows de hoje em diante dentro do raio, ordenados por distância. |
| `GET /users/1/nearby-events?radius_km=20&limit=10&offset=0` | Busca com raio e paginação personalizados. |
| `GET /users/1/notifications` | Avisos ativos da aplicação. |
| `GET /users/1/notifications?unread_only=true` | Somente avisos ainda não lidos. |
| `PATCH /users/1/notifications/2/read` | Marca o aviso 2 como lido, desde que pertença ao usuário 1. |
| `POST /users/1/notifications/refresh` | Reconcilia os avisos, inclusive para shows importados diretamente no banco. |

As notificações são criadas automaticamente ao cadastrar ou editar um evento pela API e ao atualizar localização ou preferências. Há uma restrição de unicidade por usuário e evento para evitar duplicação. Uma atualização de distância ou de dados do show preserva o estado de leitura do aviso existente.

Shows fora do raio e sem coordenadas não geram avisos. Ao mudar a localização ou o raio, os avisos que deixam de ser elegíveis são removidos. Desativar os avisos limpa a caixa de notificações, mas permite continuar pesquisando shows manualmente. Shows de datas passadas deixam de aparecer nas consultas. As datas são avaliadas no fuso `America/Sao_Paulo` e os horários de criação das notificações são armazenados em UTC.

**A entrega é uma caixa de notificações no backend.** O frontend precisa consultar os endpoints para exibir um sino, contador ou banner; não há envio de push, e-mail ou WhatsApp, nem worker agendado. Pode consultar periodicamente `GET /notifications` usando o caminho completo do usuário; para importações externas, execute também o endpoint de refresh. O modelo atual possui apenas a data do evento, portanto não diferencia um show em andamento de outro que ocorrerá mais tarde no mesmo dia.

## Google Maps e meios de transporte

Para obter estimativas no backend:

1. Configure um projeto no Google Cloud com faturamento habilitado.
2. Ative a **Routes API**.
3. Crie uma chave, restrinja seu uso à Routes API e ao ambiente do servidor.
4. Preencha `GOOGLE_MAPS_API_KEY` no `.env` e reinicie a API.

Consulte a [configuração oficial da Routes API](https://developers.google.com/maps/documentation/routes/get-api-key). As chamadas estão sujeitas à cobrança e às cotas da sua conta. A chave é utilizada apenas no servidor e não é retornada nas respostas.

```http
GET /users/1/events/1/routes
```

A resposta contém quatro opções: `driving`, `walking`, `bicycling` e `transit`. Para cada uma, informa disponibilidade, distância do trajeto em quilômetros, duração estimada em minutos e um link para abrir o Google Maps.

Para escolher os meios de transporte e um limite de distância:

```http
GET /users/1/events/1/routes?modes=driving&modes=transit&max_distance_km=40
```

O campo `within_distance_limit` compara a distância do **trajeto** com esse limite, ou com o raio salvo do usuário quando o parâmetro não é enviado. Ele ajuda o frontend a indicar que uma rota está além da distância escolhida; não garante a viabilidade de uma viagem.

Diferenças importantes:

- `straight_line_distance_km` e as distâncias de busca/notificação são calculadas em linha reta, sem chamadas ao Google.
- `routes[].distance_km` e `duration_minutes` são estimativas da Routes API para o meio de transporte escolhido.
- As estimativas consideram **saída agora**, sem configuração de trânsito em tempo real; não são uma previsão para a data do show.
- A disponibilidade de trajetos e de transporte público depende da cobertura do Google na região.
- Cada consulta faz até uma chamada ao Google por meio de transporte distinto solicitado. As estimativas não são gravadas no banco.
- Sem chave, os links do Google Maps continuam disponíveis; as estimativas ficam nulas e o status é `maps_not_configured`. Os [links do Maps não exigem chave](https://developers.google.com/maps/documentation/urls/get-started).
- Quando não houver rota, o status será `no_route`. Falhas retornam `provider_timeout`, `provider_error` ou `invalid_provider_response`, sem inventar distância ou duração e sem impedir as demais opções de serem consultadas.

A integração utiliza o endpoint [Compute Routes](https://developers.google.com/maps/documentation/routes/compute_route_directions). O mapa e a navegação são abertos pelo link `maps_url`; este repositório não contém uma tela com mapa incorporado.

## Testes

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
```

Os testes usam bancos SQLite em memória, sem acessar seu banco configurado ou serviços externos. Cobrem proximidade, filtros, geração e leitura de avisos, preferências, exclusões, validação de coordenadas, migração repetível, integração de rotas simulada e falhas do provedor.

Para conferir a organização do código:

```powershell
.\.venv\Scripts\python.exe -m ruff check app tests
.\.venv\Scripts\python.exe -m ruff format --check app tests
```

Para aplicar a formatação ao editar arquivos, execute `ruff format app tests` pelo mesmo Python do ambiente virtual. As regras configuradas verificam imports e estilo; não substituem a revisão das regras de negócio.

## Estado atual e limitações

A leitura do código identificou os seguintes pontos pendentes:

- Algumas rotas retornam a própria função em vez de executá-la, ou chamam serviços sem os argumentos necessários.
- A consulta de eventos de um organizador referencia uma variável inexistente.
- A atualização de organizadores retorna dentro do laço de campos, limitando a atualização ao primeiro campo enviado.
- Há respostas de serviços incompatíveis com os schemas declarados em algumas rotas.
- As senhas do cadastro local são armazenadas sem hash e as rotas não possuem proteção de autenticação ou autorização.
- Não há frontend nem envio de notificações fora da aplicação.
- A busca de proximidade percorre os eventos futuros com coordenadas, e a criação/edição de shows avalia os usuários. Volumes maiores exigirão índices geoespaciais e processamento em fila.

As novas rotas seguem o padrão atual de identificação por `user_id` na URL. Antes de expor dados de localização ou notificações publicamente, implemente autenticação e vincule o usuário da rota à sessão autenticada. A verificação de pertencimento de uma notificação ao `user_id` não substitui essa autenticação.

Este README descreve a implementação encontrada no repositório. Os testes das novas funcionalidades não validam as rotas antigas nem substituem a validação com serviços reais.
