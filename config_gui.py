# config_gui.py
from __future__ import annotations

from typing import Any, Dict, Optional, Callable

from aqt import mw
from aqt.qt import *
from aqt.utils import tooltip, showWarning


AddonConfig = Dict[str, Any]

DEFAULT_CONFIG: AddonConfig = {
    "01_provider": "gemini",
    "01_openai_api_key": "",
    "01_openai_model": "gpt-4o-mini",
    "01_gemini_api_key": "",
    "01_gemini_model": "gemini-2.5-flash-lite",

    "02_question_field": "Front",
    "02_answer_field": "Back",
    "02_explanation_field": "Explanation",

    "03_language": "en",
    "03_domain": "general",  
    "03_audience": "general",
    "03_explanation_style": "definition_and_mechanism",
    "03_target_length_chars": 260,

    "04_on_existing_behavior": "append",
    "04_append_separator": "\n<hr>\n",
    "04_skip_if_exists": False,  # legacy (GUIでは同期だけする)

    "05_max_notes_per_run": 50,
    "05_review_shortcut": "Ctrl+Shift+L",
}


def _merged_config(addon_id: str) -> AddonConfig:
    cfg = mw.addonManager.getConfig(addon_id) or {}
    merged = dict(DEFAULT_CONFIG)
    merged.update(cfg)
    return merged


class ExplainerConfigDialog(QDialog):
    def __init__(
        self,
        addon_id: str,
        parent: Optional[QWidget] = None,
        on_apply: Optional[Callable[[], None]] = None,
    ) -> None:
        super().__init__(parent or mw)
        self.addon_id = addon_id
        self.on_apply = on_apply

        self.setWindowTitle("AI Card Explainer — Settings")
        self.setMinimumWidth(720)

        self.cfg = _merged_config(addon_id)

        self._build_ui()
        self._load_to_ui(self.cfg)

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)

        self.tabs = QTabWidget(self)
        root.addWidget(self.tabs)

        # --- Tab: Provider ---
        tab_provider = QWidget(self)
        self.tabs.addTab(tab_provider, "Provider")
        lay_p = QVBoxLayout(tab_provider)

        form_p = QFormLayout()
        lay_p.addLayout(form_p)

        self.provider = QComboBox()
        self.provider.addItem("OpenAI", "openai")
        self.provider.addItem("Gemini", "gemini")
        form_p.addRow("Provider", self.provider)

        # OpenAI
        openai_box = QGroupBox("OpenAI")
        lay_p.addWidget(openai_box)
        openai_form = QFormLayout(openai_box)

        self.openai_key = QLineEdit()
        self.openai_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.openai_key.setPlaceholderText("If empty: use env OPENAI_API_KEY")
        self.openai_key.setMinimumWidth(520)

        self.openai_model = QLineEdit()
        self.openai_model.setPlaceholderText("e.g. gpt-4o-mini")
        self.openai_model.setMinimumWidth(520)

        openai_form.addRow("API key", self.openai_key)
        openai_form.addRow("Model", self.openai_model)

        # Gemini
        gemini_box = QGroupBox("Gemini")
        lay_p.addWidget(gemini_box)
        gemini_form = QFormLayout(gemini_box)

        self.gemini_key = QLineEdit()
        self.gemini_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.gemini_key.setPlaceholderText("If empty: use env GEMINI_API_KEY")
        self.gemini_key.setMinimumWidth(520)

        self.gemini_model = QLineEdit()
        self.gemini_model.setPlaceholderText("e.g. gemini-2.5-flash-lite")
        self.gemini_model.setMinimumWidth(520)

        gemini_form.addRow("API key", self.gemini_key)
        gemini_form.addRow("Model", self.gemini_model)

        # --- Tab: Fields ---
        tab_fields = QWidget(self)
        self.tabs.addTab(tab_fields, "Fields")
        form_f = QFormLayout(tab_fields)

        self.q_field = QLineEdit()
        self.a_field = QLineEdit()
        self.e_field = QLineEdit()
        for w in (self.q_field, self.a_field, self.e_field):
            w.setMinimumWidth(520)

        form_f.addRow("Question field", self.q_field)
        form_f.addRow("Answer field", self.a_field)
        form_f.addRow("Explanation field", self.e_field)

        # --- Tab: Output ---
        tab_out = QWidget(self)
        self.tabs.addTab(tab_out, "Output")
        form_o = QFormLayout(tab_out)

        self.domain = QComboBox()
        self.domain.addItem("Medical (medicine / biology / nursing)", "medical")
        self.domain.addItem("General (non-medical topics)", "general")
        form_o.addRow("Mode", self.domain)

        self.language = QComboBox()

        # Common
        self.language.addItem("Japanese (ja)", "ja")
        self.language.addItem("English (en)", "en")

        # Europe
        self.language.addItem("German (de)", "de")
        self.language.addItem("French (fr)", "fr")
        self.language.addItem("Spanish (es)", "es")
        self.language.addItem("Italian (it)", "it")
        self.language.addItem("Portuguese (pt)", "pt")
        self.language.addItem("Russian (ru)", "ru")

        # Asia / Others
        self.language.addItem("Chinese (zh)", "zh")
        self.language.addItem("Korean (ko)", "ko")
        self.language.addItem("Arabic (ar)", "ar")

        form_o.addRow("Language", self.language)

        self.style = QComboBox()
        self.style.addItem("Definition only", "definition_only")
        self.style.addItem("Definition + Mechanism", "definition_and_mechanism")
        self.style.addItem("Full", "full")
        form_o.addRow("Style", self.style)

        self.target_len = QSpinBox()
        self.target_len.setRange(80, 800)
        form_o.addRow("Target length (chars)", self.target_len)

        # --- Tab: Behavior / Batch ---
        tab_b = QWidget(self)
        self.tabs.addTab(tab_b, "Behavior")
        lay_b = QVBoxLayout(tab_b)

        form_b = QFormLayout()
        lay_b.addLayout(form_b)

        self.on_exists = QComboBox()
        self.on_exists.addItem("Skip (do nothing)", "skip")
        self.on_exists.addItem("Overwrite", "overwrite")
        self.on_exists.addItem("Append", "append")
        form_b.addRow("When explanation exists", self.on_exists)

        self.append_sep = QTextEdit()
        self.append_sep.setMinimumHeight(80)
        self.append_sep.setPlaceholderText("Separator used when Append is selected.")
        form_b.addRow("Append separator", self.append_sep)

        self.max_notes = QSpinBox()
        self.max_notes.setRange(1, 5000)
        form_b.addRow("Max notes per run", self.max_notes)

        self.shortcut = QKeySequenceEdit()
        form_b.addRow("Review shortcut", self.shortcut)

        # live UI tweaks
        self.on_exists.currentIndexChanged.connect(self._sync_append_enabled)

        # Buttons
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Apply
            | QDialogButtonBox.StandardButton.RestoreDefaults
        )
        root.addWidget(self.buttons)

        self.buttons.accepted.connect(self._on_ok)
        self.buttons.rejected.connect(self.reject)
        self.buttons.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self._on_apply)
        self.buttons.button(QDialogButtonBox.StandardButton.RestoreDefaults).clicked.connect(self._on_defaults)

    def _sync_append_enabled(self) -> None:
        is_append = (self.on_exists.currentData() == "append")
        self.append_sep.setEnabled(is_append)

    def _load_to_ui(self, cfg: AddonConfig) -> None:
        # Provider
        self._set_combo_by_data(self.provider, cfg.get("01_provider", "openai"))
        self.openai_key.setText(str(cfg.get("01_openai_api_key", "")) or "")
        self.openai_model.setText(str(cfg.get("01_openai_model", DEFAULT_CONFIG["01_openai_model"])) or "")
        self.gemini_key.setText(str(cfg.get("01_gemini_api_key", "")) or "")
        self.gemini_model.setText(str(cfg.get("01_gemini_model", DEFAULT_CONFIG["01_gemini_model"])) or "")

        # Fields
        self.q_field.setText(str(cfg.get("02_question_field", "Front")) or "Front")
        self.a_field.setText(str(cfg.get("02_answer_field", "Back")) or "Back")
        self.e_field.setText(str(cfg.get("02_explanation_field", "Explanation")) or "Explanation")

        # Output
        # new key preferred; fallback to legacy key
        dom = cfg.get("03_domain", None) or cfg.get("03_audience", "general")
        self._set_combo_by_data(self.domain, dom)

        self._set_combo_by_data(self.language, cfg.get("03_language", "ja"))
        self._set_combo_by_data(self.style, cfg.get("03_explanation_style", "definition_and_mechanism"))
        self.target_len.setValue(int(cfg.get("03_target_length_chars", 260) or 260))

        # Behavior
        self._set_combo_by_data(self.on_exists, cfg.get("04_on_existing_behavior", "skip"))
        self.append_sep.setPlainText(str(cfg.get("04_append_separator", "\n<hr>\n")))

        self.max_notes.setValue(int(cfg.get("05_max_notes_per_run", 50) or 50))

        seq = QKeySequence(str(cfg.get("05_review_shortcut", "Ctrl+Shift+L") or "Ctrl+Shift+L"))
        self.shortcut.setKeySequence(seq)

        self._sync_append_enabled()

    def _collect_from_ui(self) -> AddonConfig:
        cfg: AddonConfig = dict(self.cfg)

        cfg["01_provider"] = self.provider.currentData()

        cfg["01_openai_api_key"] = self.openai_key.text().strip()
        cfg["01_openai_model"] = self.openai_model.text().strip() or DEFAULT_CONFIG["01_openai_model"]

        cfg["01_gemini_api_key"] = self.gemini_key.text().strip()
        cfg["01_gemini_model"] = self.gemini_model.text().strip() or DEFAULT_CONFIG["01_gemini_model"]

        cfg["02_question_field"] = self.q_field.text().strip() or "Front"
        cfg["02_answer_field"] = self.a_field.text().strip() or "Back"
        cfg["02_explanation_field"] = self.e_field.text().strip() or "Explanation"

        cfg["03_language"] = self.language.currentData()
        cfg["03_domain"] = self.domain.currentData()
        # legacy sync (safe if user downgrades to an older add-on build)
        cfg["03_audience"] = cfg["03_domain"]
        cfg["03_explanation_style"] = self.style.currentData()
        cfg["03_target_length_chars"] = int(self.target_len.value())

        cfg["04_on_existing_behavior"] = self.on_exists.currentData()
        cfg["04_append_separator"] = self.append_sep.toPlainText()

        # legacy key: GUI側で “同期だけ” して矛盾を減らす
        cfg["04_skip_if_exists"] = (cfg["04_on_existing_behavior"] == "skip")

        cfg["05_max_notes_per_run"] = int(self.max_notes.value())

        ks = self.shortcut.keySequence()
        cfg["05_review_shortcut"] = ks.toString() or DEFAULT_CONFIG["05_review_shortcut"]

        return cfg

    def _write_config(self, cfg: AddonConfig) -> None:
        mw.addonManager.writeConfig(self.addon_id, cfg)
        self.cfg = cfg

        if self.on_apply:
            try:
                self.on_apply()
            except Exception:
                # 反映失敗しても保存自体は成功させる
                pass

    def _on_apply(self) -> None:
        cfg = self._collect_from_ui()
        self._write_config(cfg)
        tooltip("Settings saved.")

    def _on_ok(self) -> None:
        self._on_apply()
        self.accept()

    def _on_defaults(self) -> None:
        self.cfg = dict(DEFAULT_CONFIG)
        self._load_to_ui(self.cfg)
        tooltip("Defaults loaded (not saved yet).")

    @staticmethod
    def _set_combo_by_data(cb: QComboBox, data: Any) -> None:
        for i in range(cb.count()):
            if cb.itemData(i) == data:
                cb.setCurrentIndex(i)
                return
        cb.setCurrentIndex(0)


def open_config_gui(addon_id: str, parent: Optional[QWidget] = None, on_apply: Optional[Callable[[], None]] = None) -> None:
    try:
        dlg = ExplainerConfigDialog(addon_id=addon_id, parent=parent or mw, on_apply=on_apply)
        dlg.exec()
    except Exception as e:
        showWarning(f"Failed to open settings dialog:\n{e}")
