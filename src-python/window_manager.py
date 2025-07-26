import sys
import webview
import threading
import time
import queue
from typing import Optional, Dict, List, Type
from abc import ABC

localhost = "127.0.0.1"

class BaseWindow(ABC):
    def __init__(
        self,
        title: str,
        route: str,
        port: int,
        width: int = 1200,
        height: int = 800,
        host: str = localhost,
        auto_open: bool = True
    ):
        self.title = title
        self.route = route
        self.port = port
        self.host = host
        self.width = width
        self.height = height
        self.url = f"http://{self.host}:{self.port}{self.route}"
        self.window: Optional[webview.Window] = None
        self._is_created = False
        
        if auto_open:
            self.create_window()

    def create_window(self, on_closed: Optional[callable] = None) -> webview.Window:
        if self._is_created:
            raise RuntimeError(f"A janela '{self.title}' já foi criada.")

        self.window = webview.create_window(
            title=self.title,
            url=self.url,
            width=self.width,
            height=self.height
        )
        self._is_created = True
        return self.window

    def _on_window_closed(self):
        self._is_created = False

    def close_window(self):
        if self.window and self._is_created:
            self._is_created = False

    def is_created(self) -> bool:
        return self._is_created


class SupervisorioWindow(BaseWindow):
    def __init__(self, port: int, auto_open: bool = True):
        super().__init__(
            title="Supervisório",
            route="/",
            port=port,
            width=1400,
            height=900,
            auto_open=auto_open
        )


class AdminWindow(BaseWindow):
    def __init__(self, port: int, window_manager=None, auto_open: bool = True):
        self.window_manager = window_manager
        super().__init__(
            title="Painel de Administrador",
            route="/admin",
            port=port,
            width=1200,
            height=800,
            auto_open=auto_open
        )
    
    def _on_window_closed(self):
        # janela de admin fechada, encerra o programa
        super()._on_window_closed()
        print("Janela de admin fechada. Encerrando aplicação...")
        if self.window_manager:
            self.window_manager.shutdown()
        else:
            sys.exit(0)


class WindowManager:
    def __init__(self, port: int, host: str = localhost):
        self.port = port
        self.host = host
        self.windows: Dict[str, BaseWindow] = {}
        self._running = True
        self._webview_started = False

    def open_supervisorio(self, key: str = "supervisorio") -> SupervisorioWindow:
        # abre uma janela do supervisório
        if key in self.windows and self.windows[key].is_created():
            raise RuntimeError(f"A janela '{key}' já está aberta.")
        
        window = SupervisorioWindow(port=self.port)
        self.windows[key] = window
        return window

    def open_admin(self, key: str = "admin") -> AdminWindow:
        # abre uma janela de administrador
        if key in self.windows and self.windows[key].is_created():
            raise RuntimeError(f"A janela '{key}' já está aberta.")

        # verifica se já existe uma janela de admin aberta
        if any(isinstance(w, AdminWindow) and w.is_created() for w in self.windows.values()):
            raise RuntimeError("A janela de administrador já está aberta.")
        
        window = AdminWindow(port=self.port, window_manager=self)
        self.windows[key] = window
        return window

    def close_window(self, key: str):
        # fecha uma janela específica
        if key in self.windows and self.windows[key].is_created():
            self.windows[key].close_window()
            del self.windows[key]

    def close_all_windows(self):
        # fecha todas as janelas abertas
        for key in list(self.windows.keys()):
            if self.windows[key].is_created():
                self.windows[key].close_window()
        self.windows.clear()

    def list_open_windows(self) -> List[str]:
        # lista as janelas abertas
        return [key for key, win in self.windows.items() if win.is_created()]

    def shutdown(self):
        # encerra a aplicação
        self._running = False
        self.close_all_windows()
        print("Encerrando aplicação...")
        sys.exit(0)

    def is_running(self) -> bool:
        # verifica se o gerenciador ainda está em execução
        return self._running

    def start_webview(self):
        # inicia o loop principal do webview (deve ser chamado na thread principal)
        if not self._webview_started:
            self._webview_started = True
            print("Iniciando interface gráfica...")
            webview.start(debug=False)
            # quando webview.start() termina, todas as janelas foram fechadas
            self._on_all_windows_closed()

    def _on_all_windows_closed(self):
        # callback quando todas as janelas são fechadas
        print("Todas as janelas foram fechadas.")
        self._running = False

    def wait_for_windows(self):
        # aguarda até que todas as janelas sejam fechadas
        try:
            # inicia o webview na thread principal
            self.start_webview()
        except KeyboardInterrupt:
            print("Interrompido pelo usuário...")
            self.shutdown()
