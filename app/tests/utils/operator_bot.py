from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.schemas.operator_bot import OperatorBot, OperatorBotCreate, OperatorBotUpdate
from app.tests.utils.utils import (
    random_int_range, random_float_range,
    random_lower_string)


def create_random_operator_bot():
    user_id = random_int_range(1000, 2000)
    binance_api_key = random_lower_string()
    binance_api_secret = random_lower_string()
    binance_config_base_currency = "BTC"
    binance_config_quote_currency = "EUR"
    binance_config_granularity = "15m"
    binance_config_live = False
    binance_config_verbose = True
    binance_config_graphs = False
    binance_config_buymaxsize = 0.0004
    binance_config_sellupperpcnt = 10
    binance_config_selllowerpcnt = -10
    binance_config_disablebullonly = False
    binance_config_disablebuynearhigh = False
    binance_config_disablebuymacd = False
    binance_config_disablebuyema = False
    binance_config_disablebuyobv = False
    binance_config_disablebuyelderray = False
    binance_config_disablefailsafefibonaccilow = False
    binance_config_disablefailsafelowerpcnt = False
    binance_config_disableprofitbankupperpcnt = False
    binance_config_disableprofitbankfibonaccihigh = False
    binance_config_disableprofitbankreversal = False
    logger_filelog = True
    logger_logfile = "pycryptobot.log"
    logger_fileloglevel = "DEBUG"
    logger_consolelog = True
    logger_consoleloglevel = "INFO"
    telegram_client_id = random_lower_string()
    telegram_token = random_lower_string()
    bot_name_expected = f'{user_id}-{binance_config_base_currency}{binance_config_quote_currency}'

    cryptobot_config_in = OperatorBotCreate(
        user_id=user_id,
        binance_api_key=binance_api_key,
        binance_api_secret=binance_api_secret,
        binance_config_base_currency=binance_config_base_currency,
        binance_config_quote_currency=binance_config_quote_currency,
        binance_config_granularity=binance_config_granularity,
        binance_config_live=binance_config_live,
        binance_config_verbose=binance_config_verbose,
        binance_config_graphs=binance_config_graphs,
        binance_config_buymaxsize=binance_config_buymaxsize,
        binance_config_sellupperpcnt=binance_config_sellupperpcnt,
        binance_config_selllowerpcnt=binance_config_selllowerpcnt,
        binance_config_disablebullonly=binance_config_disablebullonly,
        binance_config_disablebuynearhigh=binance_config_disablebuynearhigh,
        binance_config_disablebuymacd=binance_config_disablebuymacd,
        binance_config_disablebuyema=binance_config_disablebuyema,
        binance_config_disablebuyobv=binance_config_disablebuyobv,
        binance_config_disablebuyelderray=binance_config_disablebuyelderray,
        binance_config_disablefailsafefibonaccilow=binance_config_disablefailsafefibonaccilow,
        binance_config_disablefailsafelowerpcnt=binance_config_disablefailsafelowerpcnt,
        binance_config_disableprofitbankupperpcnt=binance_config_disableprofitbankupperpcnt,
        binance_config_disableprofitbankfibonaccihigh=binance_config_disableprofitbankfibonaccihigh,
        binance_config_disableprofitbankreversal=binance_config_disableprofitbankreversal,
        logger_filelog=logger_filelog, logger_logfile=logger_logfile, logger_fileloglevel=logger_fileloglevel,
        logger_consolelog=logger_consolelog, logger_consoleloglevel=logger_consoleloglevel,
        telegram_client_id=telegram_client_id,
        telegram_token=telegram_token,
    )

    operator_bot__bot_name, operator_bot = crud.operator_bot.create_bot(obj_in=cryptobot_config_in)
    
    return operator_bot__bot_name, operator_bot

