# Projeto desenvolvido durante o curso PYSTACK WEEK 10

Este projeto foi desenvolvido como parte do curso PYSTACK WEEK 10, oferecido gratuitamente pela [Pythonando](https://pythonando.com.br/).

O curso tem como objetivo ensinar gratuitamente aos participantes a linguagem de programação Python juntamente com o framework Django. Os participantes aprendem sobre essas tecnologias, incluindo suas aplicações e como se inserir no mercado de trabalho como desenvolvedor web back-end. O curso também aborda a criação de portfólios no GitHub e fornece certificados de conclusão.

## Tema do Projeto: Site para Consultório Médico

Este projeto tem como tema um site para um consultório médico, com áreas de cadastro para pacientes e médicos. O objetivo é permitir que os médicos cadastrem suas agendas de atendimento, que serão visíveis para os pacientes que desejam marcar uma consulta.

### Recursos Principais:
- **Agendas de Atendimento para Médicos:** Os médicos podem criar e gerenciar suas agendas de horários disponíveis para consultas.
- **Marcação de Consultas:** Os pacientes podem solicitar consultas com os médicos, e estes podem aceitá-las. 
- **Videochamadas:** Os médicos podem adicionar links para videochamadas (por exemplo, Google Meet) para as consultas agendadas.
- **Histórico de Consultas:** Consultas confirmadas ficam salvas no histórico do paciente e do médico, permitindo acesso a receitas e documentos enviados durante o atendimento.
- **Análise de Desempenho para Médicos:** Os médicos têm acesso a um gráfico que mostra horas trabalhadas, dias trabalhados e ganhos financeiros em um determinado período de tempo.


## 📦 Pré‑requisitos

Você precisa ter instalado:

- [Git](https://git-scm.com/)  
- [Docker](https://docs.docker.com/engine/install/) (a engine, não apenas o Docker Desktop)  
- [Docker Compose v2](https://docs.docker.com/compose/install/) (plugin `docker compose`, sem hífen)

No Ubuntu, você pode instalar tudo com:
```bash
sudo apt update
sudo apt install git docker.io docker-compose-v2
sudo systemctl start docker
sudo usermod -aG docker $USER   # para não precisar de sudo nos comandos docker
```
**Depois faça logout/login ou reinicie a sessão** para a permissão de grupo funcionar.

---

## 🚀 Como rodar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/Byell00123/Clinica_Online.git
cd Clinica_Online/src/healing
```

### 2. Execute o Docker Compose
Abra o VSCode na pasta atual(`Clinica_Online/src/healing`), depois abra o terminal do VSCode usando "CTRL+J".
```bash
docker compose up
```

Na primeira execução, o Docker irá:
- Baixar as imagens do Python 3.12 e MySQL 8.0
- Construir a imagem da aplicação (instalar dependências Python, etc.)
- Criar os containers `Clinica` (Django) e `clinica_db` (MySQL)
- Aguardar o MySQL ficar pronto
- Aplicar as migrações automaticamente
- Iniciar o servidor Django

Para **rodar em segundo plano** (liberar o terminal), adicione a flag `-d`:
```bash
docker compose up -d
```

Com os containers em segundo plano, você pode usar outros comandos livremente (veja a seção abaixo).

#### Comandos do Django sem ambiente virtual
Antes, você precisava ativar o `venv` para rodar `python manage.py ...`.  
Agora, com Docker, os comandos são executados **dentro do container**. A estrutura básica é:

```bash
docker compose exec web python manage.py <comando>
```

Exemplos:

| Ação | Comando |
|------|---------|
| Criar superusuário | `docker compose exec web python manage.py createsuperuser` |
| Acessar o shell do Django | `docker compose exec web python manage.py shell` |
| Criar novas migrações | `docker compose exec web python manage.py makemigrations` |
| Aplicar migrações | `docker compose exec web python manage.py migrate` |
| Coletar arquivos estáticos | `docker compose exec web python manage.py collectstatic` |

> **Atenção:** O container `Clinica` precisa estar rodando. Se usou `up` sem `-d`, abra outro terminal para esses comandos.

#### Por que isso funciona?
- Todas as dependências (Django, mysqlclient, etc.) já estão instaladas na imagem do container.
- O comando `docker compose exec` executa o que você deseja dentro do container em funcionamento.
- As variáveis de ambiente (como `DB_HOST`) já estão definidas, então o Django conecta ao MySQL sem configuração extra.

#### E se eu quiser rodar um comando antes de subir o container?
Para comandos que não dependem dos serviços (ex: `startapp`), use `docker compose run`:

```bash
docker compose run --rm web python manage.py startapp meu_app
```

A flag `--rm` remove o container temporário após a execução.

#### Tabela de equivalência (antes e depois do Docker)

| Antes (com venv ativo) | Agora (com Docker) |
|------------------------|---------------------|
| `python manage.py runserver` | Automático no `docker compose up` |
| `python manage.py migrate` | Já executado no `up`; manual: `docker compose exec web python manage.py migrate` |
| `python manage.py createsuperuser` | `docker compose exec web python manage.py createsuperuser` |
| `python manage.py shell` | `docker compose exec web python manage.py shell` |
| `python manage.py test` | `docker compose exec web python manage.py test` |

### 3. Acessar o site
Abra o navegador e vá para:  
👉 **http://localhost:8000**

O servidor de desenvolvimento do Django estará ouvindo na porta **8000** da sua máquina.

---

## 🛢️ Conectar ao banco de dados (MySQL Workbench)

O MySQL está rodando no container `clinica_db` e mapeado para a porta **3307** do seu computador.  
Utilize os seguintes dados de conexão:

| Campo | Valor |
|-------|-------|
| **Connection name** | `Clinica` |
| **Hostname** | `localhost` |
| **Port** | `3307` |
| **Username** | `adminclinica` |
| **Password** | `admindjango` |
| **Default Schema** | `bd_clinica` |

> ℹ️ O usuário `adminclinica` tem privilégios totais apenas sobre o banco `bd_clinica`. A senha de root (`senhaclinica`) não é necessária para acessar os dados da aplicação.

### Passos no Workbench
1. Clique no **+** ao lado de "MySQL Connections".
2. Preencha com os dados da tabela.
3. Clique em **Test Connection** – a mensagem "Successfully made the MySQL connection" deve aparecer.
4. Salve e conecte. Agora você pode explorar as tabelas (`medicos`, `pacientes`, etc.).

---

## 🛑 Parando os containers

- Se iniciou com `docker compose up` (primeiro plano), pressione **Ctrl+C** no terminal.
- Se usou `docker compose up -d` (segundo plano):

```bash
# Apenas pausar os containers (dados preservados)
docker compose stop

# Parar e remover os containers (dados do banco mantidos)
docker compose down
```

Os dados do MySQL ficam em um volume Docker (`healing_mysql_data`) e **sobrevivem** a remoções normais.  
Para apagar tudo e recomeçar do zero:

```bash
docker compose down -v
```

---

## 📁 Estrutura de arquivos importante

```
.
├── docker-compose.yml      # Define os serviços (web + db)
├── Dockerfile              # Constrói a imagem da aplicação Django
├── entrypoint.sh           # Script de inicialização (aguarda MySQL, migra e sobe o servidor)
├── requirements.txt        # Dependências Python (Django, mysqlclient, etc.)
├── manage.py               # Utilitário do Django
└── healing/                # Configurações do projeto (settings, urls, etc.)
```

---

## 🔧 Problemas comuns

### O container `Clinica` exibe "MySQL ainda não está disponível..." repetidamente
- Verifique se o container `clinica_db` está rodando com `docker ps`.
- Confirme se a senha no healthcheck do `docker-compose.yml` está correta (`-padmindjango`).
- Se necessário, aumente o tempo de espera editando `entrypoint.sh` (`sleep 2` → `sleep 5`).

### A porta 3307 já está em uso
Altere o mapeamento no `docker-compose.yml` (ex: `"3308:3306"`) e use a nova porta no Workbench.

### A porta 8000 está ocupada
Troque o mapeamento para `"8001:8000"` e acesse `localhost:8001`.

### Permissão negada ao usar `docker compose`
Execute com `sudo` ou adicione seu usuário ao grupo `docker`:
```bash
sudo usermod -aG docker $USER
```
Lembre-se de reiniciar a sessão.

---

## Autor
**Gabryell Costa de Moura**

📞 Telefone: (63) 99227-4895  
✉️ Email: gabryellcostademoura1@gmail.com