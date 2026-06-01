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

########################

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
Abra o VSCode na pasta atual, abra o terminal do programa usando "CTRL+J" 
```bash
docker compose up
```

Na primeira vez o Docker irá:
- Baixar as imagens necessárias (Python 3.12, MySQL 8.0)
- Construir a imagem da aplicação (instalar dependências, etc.)
- Criar os containers `Clinica` (Django) e `clinica_db` (MySQL)
- Aguardar o MySQL ficar pronto
- Rodar as migrações automaticamente
- Iniciar o servidor de desenvolvimento do Django

### 3. Acesse o site

Abra o navegador e vá para:  
👉 **http://localhost:8000**

O servidor Django estará ouvindo na porta **8000** da sua máquina.

---

## 🛢️ Conectando ao banco de dados com MySQL Workbench

O banco de dados MySQL roda no container `clinica_db` e está mapeado para a porta **3307** do seu computador.  
Use os seguintes dados para configurar uma conexão no MySQL Workbench (ou qualquer outro cliente MySQL):

| Campo               | Valor               |
|---------------------|---------------------|
| **Connection name** | `Clinica`           |
| **Hostname**        | `localhost`         |
| **Port**            | `3307`              |
| **Username**        | `adminclinica`      |
| **Password**        | `admindjango`       |
| **Default Schema**  | `bd_clinica`        |

**Observação:**  
> O usuário `adminclinica` tem acesso total ao banco `bd_clinica`, que é o banco usado pela aplicação Django.  
> A senha de **root** (`senhaclinica`) existe apenas para administração do MySQL e não é necessária para acessar o banco da clínica.

### Configurando a conexão no Workbench

1. Clique no ícone **+** ao lado de "MySQL Connections".
2. Preencha os campos conforme a tabela acima.
3. Clique em **Test Connection** – deve aparecer "Successfully made the MySQL connection".
4. Clique em **OK** para salvar.

Agora você pode navegar pelas tabelas criadas pelo Django (`medicos`, `pacientes`, etc.).

---

## 🛑 Parando os containers

Para parar tudo, pressione `Ctrl+C` no terminal onde o `docker compose up` está rodando.  
Se quiser parar e remover os containers (mantendo os dados do banco):

```bash
docker compose down
```

Os dados do MySQL são armazenados em um volume Docker chamado `healing_mysql_data` e **não serão perdidos** ao parar ou remover os containers.  
Para apagar os dados de vez (começar do zero), remova também o volume:

```bash
docker compose down -v
```

---

## 📁 Estrutura de arquivos importante

```
.
├── docker-compose.yml      # Define os serviços (web + db)
├── Dockerfile              # Constrói a imagem da aplicação Django
├── entrypoint.sh           # Script que espera o MySQL e roda migrações
├── requirements.txt        # Dependências Python (Django, mysqlclient, etc.)
├── manage.py               # Utilitário do Django
└── healing/                # Projeto Django (settings, urls, etc.)
```

---

## 🔧 Solução de problemas comuns

### ❌ O container `Clinica` fica repetindo "MySQL ainda não está disponível..."
- Verifique se o container do MySQL (`clinica_db`) subiu corretamente.
- Confira se a senha no `docker-compose.yml` (healthcheck) está correta (`-padmindjango`).
- Tente aumentar o tempo de espera: no `entrypoint.sh`, mude `sleep 2` para `sleep 5`.

### ❌ A porta 3307 já está em uso
- Mude a porta do host no `docker-compose.yml` (ex: `"3308:3306"`). Depois use essa nova porta no Workbench.

### ❌ A porta 8000 já está em uso
- Altere o mapeamento para `"8001:8000"` no `docker-compose.yml` e acesse `localhost:8001`.

### ❌ Permissão negada ao rodar `docker compose`
- Execute os comandos com `sudo` ou adicione seu usuário ao grupo `docker`:
  ```bash
  sudo usermod -aG docker $USER
  ```
  (Reinicie a sessão para aplicar.)

---

## 👥 Uso em grupo / professor

Para que outra pessoa execute o projeto, basta:

1. Clonar o repositório
2. Ter o Docker instalado
3. Executar `docker compose up` na pasta raiz do projeto

Nenhuma configuração adicional de banco de dados ou dependências é necessária.

---

########################

## Autor
Gabryell Costa de Moura

### Contato
- Telefone: 63992274895
- Email: gabryellcostademoura1@gmail.com


