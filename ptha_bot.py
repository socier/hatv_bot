from this import d
import pymssql
import pandas as pd
import telegram

# TELEGRAM 관련 설정
TELEGRAM_TOKEN = '5700322476:AAGnGmckNe0jbBwhnNMt3apxsNpVyCL3lsY'   # ptha_bot
TELEGRAM_CHAT_ID = -1001809120134	# PTHA 영업 채널
#TELEGRAM_CHAT_ID = 26288969	# JSLim

bot = telegram.Bot(token = TELEGRAM_TOKEN)

def send_telegram(msg, nopreveiw='true'):
	bot.sendMessage(chat_id = TELEGRAM_CHAT_ID, parse_mode='HTML', text=msg, disable_web_page_preview=False)
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
	
	if run_status == 'Fail':
		emoji = '⛔⛔⛔'
	else:
		emoji = '😊'

	#msg  = '----------------------------------\n'
	msg = f'Order Transfer <b>{run_status}</b> {emoji}\n'
	#msg += '----------------------------------\n'

	#if run_status == 'Fail':
	#	msg += "<a href='https://s3.us-west-2.amazonaws.com/secure.notion-static.com/81e7cd92-3bd7-4915-8f0b-e81514f2b796/fail.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20220929%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20220929T080629Z&X-Amz-Expires=86400&X-Amz-Signature=9c7c1d64fed04def89334463c3d3804727a752c84d2bc82fe26353f85865ea4f&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22fail.png%22&x-id=GetObject'>Fail</a>"
	#else:
	#	msg += run_status

	msg += f' {run_date[0:4]}/{run_date[4:6]}/{run_date[6:8]} {run_time[0:2]}:{run_time[2:4]}:{run_time[4:6]}\n'
	#msg += '----------------------------------\n'

	send_telegram(msg)

if __name__ == '__main__':
	prod_info()

