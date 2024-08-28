username = 'hzhou'
password = 'cognitiveati'
host = 'blissmotors.cqh3eh5shl0r.us-east-2.rds.amazonaws.com'
port = 5432

test_db = 'telle_ai_dev'
prod_db = 'bmcars_dev'

db_string = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(username, password, host, port, prod_db)

redis_host = '127.0.0.1'
redis_port = 6379

project_id = 'newagent-c47af'
# project_id = 'telle-ai-dev-rdgebu'
#
mail_settings = {
    "MAIL_SERVER": 'smtp.zoho.com',
    "MAIL_PORT": 587,
    "MAIL_USE_TLS": True,
    "MAIL_USE_SSL": False,
    "MAIL_USERNAME": 'noreply@telle.ai',
    "MAIL_PASSWORD": 'blissmotors'
}

# mail_settings = {
#     "MAIL_SERVER": 'smtp.gmail.com',
#     "MAIL_PORT": 587,
#     "MAIL_USE_TLS": True,
#     "MAIL_USE_SSL": False,
#     "MAIL_USERNAME": 'customercare@blissmotors.com',
#     "MAIL_PASSWORD": 'Blissmotors2018'
# }


ipinfo_access_token='362e2dc65c9e7a'
