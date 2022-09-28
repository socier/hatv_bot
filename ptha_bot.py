from this import d
import pymssql
import pandas as pd
import telegram

# TELEGRAM 관련 설정
TELEGRAM_TOKEN = '5700322476:AAGnGmckNe0jbBwhnNMt3apxsNpVyCL3lsY'   # ptha_bot
TELEGRAM_CHAT_ID = -1001809120134	# PTHA 영업 채널

bot = telegram.Bot(token = TELEGRAM_TOKEN)

def send_telegram(msg, nopreveiw='true'):
	bot.sendMessage(chat_id = TELEGRAM_CHAT_ID, parse_mode='HTML', text=msg, disable_web_page_preview=nopreveiw)
	print (msg)

def read_sql(sql):
	conn = pymssql.connect('10.11.12.200', 'sa', 'wms!2010', 'sap')
	df = pd.read_sql(sql, conn)
	return df

def prod_info():
	sql = "exec sap.dbo.USP_IT_MESSAGE 'SP_BOHLE_TRANSFER_ORDER'"

	df = read_sql(sql)

	if len (df.index) != 1:
		return

	run_status = df.run_status[0]
	run_date = str(df.run_date[0])
	run_time = str(df.run_time[0])
	
	msg  = '----------------------------------\n'
	msg += 'Order Transfer Status\n'
	msg += '----------------------------------\n'
	msg += f'{run_status} {run_date[0:4]}/{run_date[4:6]}/{run_date[6:8]} {run_time[0:2]}:{run_time[2:4]}:{run_time[4:6]}\n'

	msg += '----------------------------------\n'

	send_telegram(msg)

if __name__ == '__main__':
	prod_info()

