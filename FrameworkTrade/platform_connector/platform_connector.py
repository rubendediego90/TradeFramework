import MetaTrader5 as mt5
import os
from dotenv import load_dotenv, find_dotenv
from utils.utils import Utils

class PlatformConnector():
    
    def __init__(self, symbol_list : list):
        # Buscar valores
        load_dotenv(find_dotenv())
        
        # Inicializacion de la plataforma
        self._initialize_platform()
        
        # TODO ver si podemos operas (restricciones ftmo)
        # Fines de semana
        # Calcular noticias
        # Perdidas en el dia
        
        
        #Esta activado el trading algoritmico
        self._check_algo_trading_enabled()
        
        #Añadimos los simbolos 
        self._add_symbols_to_marketwatch(symbol_list)
        
        #Informacion por consola
        self._print_account_info()
        
        
    def disconnect() -> None:
        # Desconexcion de mt5 
        mt5.shutdown()
    
    def _initialize_platform(self) -> None:
        init = mt5.initialize(
            path=os.getenv("MT5_PATH"),
            login=int(os.getenv("MT5_LOGIN")),
            password=os.getenv("MT5_PASSWORD"),
            server=os.getenv("MT5_SERVER"),
            timeout=int(os.getenv("MT5_TIMEOUT")),
            portable=eval(os.getenv("MT5_PORTABLE"))
        )
        
        if init:
            current_account_info = mt5.account_info()
            print("------------------------------------------------------------------")
            print(f"Login: {mt5.account_info().login} \tserver: {mt5.account_info().server}")
        else:
            print("failed to connect at account #{}, error code: {}".format(os.getenv("MT5_LOGIN"), mt5.last_error()))
            
    def _check_algo_trading_enabled(self) -> None:
        # comprobar que el trading algoritmico esta activado
        if not mt5.terminal_info().trade_allowed:
            raise Exception("El trading algorítmico está desactivado")
        
    #TODO mensaje telegram añadir en cada operacion si es real o no
    def _is_real_account(self) -> None:
        #Comprueba el tipo de cuenta
        account_info = mt5.account_info().trade_mode
        
        if account_info == mt5.ACCOUNT_TRADE_MODE_DEMO:
            print("Cuenta tipo demo")
            
        elif account_info == mt5.ACCOUNT_TRADE_MODE_REAL:
            print("Cuenta tipo demo")
                
    def _add_symbols_to_marketwatch(self, symbols: list) -> None:
        
        # 1) Comprobamos si el símbolo ya está visible en el MW
        # 2) Si no lo está, lo añadiremos

        for symbol in symbols:
            if mt5.symbol_info(symbol) is None:
                print(f"{Utils.dateprint()} - No se ha podido añadir el símbolo {symbol} al MarketWatch: {mt5.last_error()}")
                continue
            
            if not mt5.symbol_info(symbol).visible:
                if not mt5.symbol_select(symbol, True):
                    print(f"No se ha podido añadir el símbolo {symbol} al MarketWatch: {mt5.last_error()}")
                else:
                    print(f"Símbolo {symbol} se ha añadido con éxito al MarketWatch!")
            else:
                print(f"El símbolo {symbol} ya estaba en el MarketWatch.")
    
    def _print_account_info(self) -> None:
        # Recuperar un objeto de tipo AccountInfo
        account_info = mt5.account_info()._asdict()

        print(f"+------------ Información de la cuenta ------------")
        print(f"| - ID de cuenta: {account_info['login']}")
        print(f"| - Nombre trader: {account_info['name']}")
        print(f"| - Broker: {account_info['company']}")
        print(f"| - Servidor: {account_info['server']}")
        print(f"| - Apalancamiento: {account_info['leverage']}")
        print(f"| - Divisa de la cuenta: {account_info['currency']}")
        print(f"| - Balance de la cuenta: {account_info['balance']}")
        print(f"+--------------------------------------------------")
