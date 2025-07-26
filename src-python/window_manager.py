import sys
import webview
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
        host: str = localhost
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

    def create_window(self, on_closed: Optional[callable] = None) -> webview.Window:
        if self._is_created:
            raise RuntimeError(f"A janela '{self.title}' já foi criada.")

        self.window = webview.create_window(
            title=self.title,
            url=self.url,
            width=self.width,
            height=self.height,
            on_closed=on_closed
        )
        self._is_created = True
        return self.window

    def close_window(self):
        if self.window and self._is_created:
            webview.destroy_window(self.window)
            self._is_created = False

    def is_created(self) -> bool:
        return self._is_created


class SupervisorioWindow(BaseWindow):
    def __init__(self, port: int):
        super().__init__(
            title="Supervisório",
            route="/",
            port=port,
            width=1400,
            height=900
        )


class AdminWindow(BaseWindow):
    def __init__(self, port: int):
        super().__init__(
            title="Painel de Administrador",
            route="/admin",
            port=port,
            width=1200,
            height=800
        )


class WindowManager:
    def __init__(self, port: int, host: str = localhost):
        self.port = port
        self.host = host
        self.windows: Dict[str, BaseWindow] = {}

    def create_window(
        self,
        key: str,
        window_cls: Type[BaseWindow],
        on_closed: Optional[callable] = None
    ) -> webview.Window:
        if key in self.windows and self.windows[key].is_created():
            raise RuntimeError(f"A janela '{key}' já está aberta.")

        if window_cls is AdminWindow:
            if any(isinstance(w, AdminWindow) and w.is_created() for w in self.windows.values()):
                raise RuntimeError("A janela de administrador já está aberta.")

        window = window_cls(port=self.port)
        self.windows[key] = window
        return window.create_window(on_closed=on_closed)

    def close_window(self, key: str):
        if key in self.windows and self.windows[key].is_created():
            self.windows[key].close_window()
            del self.windows[key]

    def list_open_windows(self) -> List[str]:
        return [key for key, win in self.windows.items() if win.is_created()]
