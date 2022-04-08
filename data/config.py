from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
IP = env.str("ip")
emailLogin = env.str('emailLogin')
emailPassword = env.str('emailPassword')
defaultEmail = env.str('defaultEmail')
defaultDirectory = env.str('defaultDirectory')
smtpServer = env.str('smtpServer')
smtpPort = env.int('smtpPort')