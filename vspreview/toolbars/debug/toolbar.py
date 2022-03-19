from __future__ import annotations

from typing import Mapping, Any

from PyQt5.QtWidgets import QLineEdit, QHBoxLayout, QPushButton

from ...utils import debug, set_qobject_names
from ...core import AbstractMainWindow, AbstractToolbar, try_load

from .settings import DebugSettings


class DebugToolbar(AbstractToolbar):
    _storable_attrs = ('settings',)

    __slots__ = (
        *_storable_attrs, 'test_button',
        'exec_lineedit', 'exec_button',
        'test_button', 'toggle_button'
    )

    def __init__(self, main: AbstractMainWindow) -> None:
        super().__init__(main, 'Debug', DebugSettings())

        self.setup_ui()

        self.test_button.clicked.connect(self.test_button_clicked)
        self.exec_button.clicked.connect(self.exec_button_clicked)
        self.exec_lineedit.editingFinished.connect(self.exec_button_clicked)

        if self.main.DEBUG_TOOLBAR_BUTTONS_PRINT_STATE:
            self.filter = debug.EventFilter(main)
            self.main.toolbars.main.widget.installEventFilter(self.filter)
            for toolbar in self.main.toolbars:
                toolbar.widget.installEventFilter(self.filter)

        set_qobject_names(self)

    def setup_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setObjectName('DebugToolbar.setup_ui.layout')
        layout.setContentsMargins(0, 0, 0, 0)

        self.test_button = QPushButton(self)
        self.test_button.setText('Test')
        layout.addWidget(self.test_button)

        self.break_button = QPushButton(self)
        self.break_button.setText('Break')
        layout.addWidget(self.break_button)

        self.exec_lineedit = QLineEdit(self)
        self.exec_lineedit.setPlaceholderText(
            'Python statement in context of DebugToolbar.exec_button_clicked()'
        )
        layout.addWidget(self.exec_lineedit)

        self.exec_button = QPushButton(self)
        self.exec_button.setText('Exec')
        layout.addWidget(self.exec_button)

        layout.addStretch()

        self.toggle_button.setVisible(False)

    def test_button_clicked(self, checked: bool | None = None) -> None:
        from vspreview.utils import vs_clear_cache
        vs_clear_cache()

    def exec_button_clicked(self, checked: bool | None = None) -> None:
        try:
            exec(self.exec_lineedit.text())
        except Exception as e:
            print(e)

    def break_button_clicked(self, checked: bool | None = None) -> None:
        breakpoint()

    def __getstate__(self) -> Mapping[str, Any]:
        return {
            attr_name: getattr(self, attr_name)
            for attr_name in self._storable_attrs
        }

    def __setstate__(self, state: Mapping[str, Any]) -> None:
        try_load(state, 'settings', DebugSettings, self.settings)