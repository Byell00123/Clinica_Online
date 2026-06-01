#!/bin/sh
set -e

echo "Aguardando o MySQL ficar pronto..."

# Garante um valor padrão para a porta (caso a variável não esteja definida)
DB_PORT_VAL=${DB_PORT:-3306}

# Loop até conseguir conectar ao MySQL
until python -c "import MySQLdb; MySQLdb.connect(host='${DB_HOST}', user='${DB_USER}', password='${DB_PASSWORD}', db='${DB_NAME}', port=${DB_PORT_VAL})" 2>/dev/null; do
    echo "MySQL ainda não está disponível - aguardando..."
    sleep 2
done

echo "MySQL pronto! Aplicando migrações..."
python manage.py migrate --noinput

echo "Iniciando o servidor Django..."
exec "$@"