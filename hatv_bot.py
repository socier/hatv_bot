import pymssql
import pandas
import telegram

# TELEGRAM 관련 설정
TELEGRAM_TOKEN = '5489889627:AAGTTR95UBCkFw3oSIqTP9Ybto8dc1iyopk'   # hatv_bot
TELEGRAM_CHAT_ID = -1001533729786	# HATV 생산 채널
# TELEGRAM_CHAT_ID = 26288969 #JSLim

bot = telegram.Bot(token = TELEGRAM_TOKEN)

def send_telegram(msg, nopreveiw='true'):
	bot.sendMessage(chat_id = TELEGRAM_CHAT_ID, parse_mode='HTML', text=msg, disable_web_page_preview=nopreveiw)
	print (msg)

def read_sql(sql):
	conn = pymssql.connect('10.12.11.219', 'sa', 'ptha**345', 'mes')
	df = pandas.read_sql(sql, conn)
	return df

def prod_info():
	sql = 'exec mes..sp_bot_prod'

	df = read_sql(sql)

	if len (df.index) != 1:
		return

	work_dt = df.work_dt[0]
	shift = df.work_shift[0]
	bd = df.scan_bd[0]
	vc = df.scan_vc[0]
	ng = df.scan_df[0]
	ngr = ng / vc * 100

	bds = df.scan_bd_shift[0]
	vcs = df.scan_vc_shift[0]
	ngs = df.scan_df_shift[0]
	ngsr = ngs / vcs * 100

	if bd < 1000:
		return

	msg = '----------------------------------\n'
	msg += f'{work_dt:%Y-%m-%d} Shift {shift}\n'
	msg += '----------------------------------\n'
	msg += f'BD : {bds:,.0f}  VC : {vcs:,.0f}\nNG : {ngs:,.0f}  {ngr:.2f}% \n'

	if shift == 2:
		msg += '----------------------------------\n'
		msg += f'{work_dt:%Y-%m-%d} Total\n'
		msg += '----------------------------------\n'
		msg += f'BD : {bd:,.0f}  VC : {vc:,.0f}\nNG : {ng:,.0f}  {ngsr:.2f}% \n'

	msg += '----------------------------------\n'

	send_telegram(msg)



def defect_info():

	sql = 'exec mes..sp_bot_defect'
	df = read_sql(sql)

	if len (df.index) < 1:
		return

	msg  = '----------------------------------\n'
	msg += 'TOP 5 DEFECT\n'
	msg += '----------------------------------\n'

	for index, row in df.head(5).iterrows():
		msg += f'[{index + 1} : {row.qty:,.0f}] {row.u_etrto} {row.u_pattern}\n    {row.u_group3}\n'

	msg += '----------------------------------\n'
	send_telegram(msg)


if __name__ == '__main__':
	prod_info()
	defect_info()
