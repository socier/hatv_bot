import sqlalchemy
import pandas as pd
import telegram

# TELEGRAM 관련 설정
TELEGRAM_TOKEN = '5489889627:AAGTTR95UBCkFw3oSIqTP9Ybto8dc1iyopk'   # hatv_bot
TELEGRAM_CHAT_ID = -1001533729786	# HATV 생산 채널
# TELEGRAM_CHAT_ID = 26288969 #JSLim

bot = telegram.Bot(token = TELEGRAM_TOKEN)

def send_telegram(msg, nopreveiw='true'):
	bot.sendMessage(chat_id = TELEGRAM_CHAT_ID, parse_mode='HTML', text=msg, disable_web_page_preview=nopreveiw)
	print (msg)

def prod_info():
	sql = 'exec mes..sp_bot_prod'
	df = pd.read_sql(sql, engine)

	if len (df.index) != 1:
		return

	sr = df.squeeze()
	work_dt = sr.work_dt
	shift = sr.work_shift
	bd = sr.scan_bd
	vc = sr.scan_vc
	ng = sr.scan_df
	ngr = ng / vc * 100
	tp = sr.scan_tp
	te = sr.scan_te
	bc = sr.scan_bc
	tpr = sr.roll_tp
	ter = sr.roll_te
	bcr = sr.roll_bc

	bds = sr.scan_bd_shift
	vcs = sr.scan_vc_shift
	ngs = sr.scan_df_shift
	ngsr = ngs / vcs * 100
	tps = sr.scan_tp_shift
	tes = sr.scan_te_shift
	bcs = sr.scan_bc_shift
	tprs = sr.roll_tp_shift
	ters = sr.roll_te_shift
	bcrs = sr.roll_bc_shift

	if bd < 1000:
		return

	msg = '----------------------------------\n'
	msg += f'{work_dt:%Y-%m-%d} Shift {shift}\n'
	msg += '----------------------------------\n'
	msg += f'BD : {bds:6,.0f} pcs\n'
	msg += f'VC : {vcs:6,.0f} pcs\n'
	msg += f'NG : {ngs:6,.0f} pcs    {ngsr:,.2f} % \n'
	if shift == 1:
		msg += f'TP : {tprs:6,.0f}  {tps:7,.0f} m\n'
	msg += f'EX : {ters:6,.0f} R   {tes:7,.0f} m\n'
	msg += f'BC : {bcrs:6,.0f} R   {bcs:7,.0f} m\n'

	if shift == 2:
		msg += '----------------------------------\n'
		msg += f'{work_dt:%Y-%m-%d} Total\n'
		msg += '----------------------------------\n'
		msg += f'BD : {bd:6,.0f} pcs\n'
		msg += f'VC : {vc:6,.0f} pcs\n'
		msg += f'NG : {ng:6,.0f} pcs    {ngr:,.2f} % \n'
		msg += f'TP : {tpr:6,.0f} R   {tp:7,.0f} m\n'
		msg += f'EX : {ter:6,.0f} R   {te:7,.0f} m\n'
		msg += f'BC : {bcr:6,.0f} R   {bc:7,.0f} m\n'

	msg += '----------------------------------\n'

	send_telegram(msg)



def defect_info():

	sql = 'exec mes..sp_bot_defect'
	df = pd.read_sql(sql, engine)

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
	engine = sqlalchemy.create_engine('mssql+pymssql://sa:ptha**345@10.12.11.219/pop')
	prod_info()
	defect_info()
