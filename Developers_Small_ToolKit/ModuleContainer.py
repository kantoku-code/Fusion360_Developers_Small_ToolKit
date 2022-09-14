import traceback
import adsk.core
import adsk.fusion
import sys
import pathlib
import importlib
import inspect
import collections
import json

# 呼び出しモジュールとして必要な関数名
REQUIRED_FUNCTIONS = (
    'run',
    'entry',
)

# 登録に必要なキー
ENTRY_KEYS = (
    'category',
    'name',
    'index',
    'icon',
    'tooltip',
)

# このフォルダーをパスに追加
THIS_DIR = pathlib.Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.append(str(THIS_DIR))

# コマンド用フォルダ
COMMANDS_DIR = THIS_DIR / 'commands'

# 終了時のremove呼び出し
_removeList =[]

class ModuleManager():
    def __init__(self) -> None:
        self.module_container = getExecutableModules()

    def __del__(self) -> None:
        self.callRemove()
        for con in self.module_container:
            del con['module']

    def getButtonInfo(self) -> str:

        def getInfo(info: dict):
            btnType = 'button'
            if 'btn_type' in info:
                btnType = info['btn_type']

            checkName = ''
            if 'check_name' in info:
                checkName = info['check_name']

            checkTooltip = ''
            if 'check_tooltip' in info:
                checkTooltip = info['check_tooltip']

            return {
                'name': info['name'],
                'id': info['id'],
                'icon': info['icon'],
                'tooltip': info['tooltip'],
                'btn_type': btnType,
                'check_name': checkName,
                'check_tooltip': checkTooltip,
            }

        # ***********
        categories = list(set(x['category'] for x in self.module_container))
        categories.sort()

        button_infos = {}
        for category in categories:
            pass
            infos = [con for con in self.module_container
                if con['category'] == category]

            infos.sort(key=lambda x: x['index'])

            btns = [getInfo(info) for info in infos]

            button_infos[category] = {
                'name' : category,
                'buttons' : btns,
            }

        return json.dumps(button_infos)

    def exec(self, id):
        for con in self.module_container:
            if con['id'] == id:
                con['module'].run({'IsApplicationStartup': True})
                break

    def changeValue(self, id, value):
        for con in self.module_container:
            if con['id'] == id:
                res = con['module'].changeValue(value)
                global _removeList
                if res:
                    _removeList.append(id)
                else:
                    _removeList.remove(id)
                break

    def changeSwitchCheckValue(self, id, sw_value, ch_value):
        for con in self.module_container:
            if con['id'] == id:
                res = con['module'].changeSwitchCheckValue(sw_value, ch_value)
                global _removeList
                if res:
                    _removeList.append(id)
                else:
                    _removeList.remove(id)
                break

    def callRemove(self):
        global _removeList
        for id in _removeList:
            for con in self.module_container:
                if con['id'] == id:
                    con['module'].removeEvent()

# https://note.nkmk.me/python-list-flatten/
def flatten(l):
    for el in l:
        if isinstance(el, collections.abc.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el


def getExecutableModules() -> list:

    # commandsフォルダ内の子フォルダ内のpyファイルの取得
    files = flatten([d.iterdir() for d in COMMANDS_DIR.iterdir() if d.is_dir()])
    pyFiles = [f for f in files if f.is_file() and f.suffix == '.py']

    # 必要な関数を持つモジュールの取得
    modules = []
    for file in pyFiles:

        # 各モジュールの親フォルダのパス追加
        path = str(file.parent)
        if path not in sys.path:
            sys.path.append(path)

        # モジュールとしてインポート
        module = importlib.import_module(file.stem)
        importlib.reload(module)

        # パス削除
        sys.path.remove(path)

        # モジュール内から関数名取得
        funcs = [func for func, _ in inspect.getmembers(module, inspect.isfunction)]

        # 関数名チェック
        if not all([funk in funcs for funk in REQUIRED_FUNCTIONS]):
            del module # モジュールの破棄
            continue

        # entryからdictチェック
        infos = module.entry()
        if not type(infos) is dict:
            del module # モジュールの破棄
            continue

        # キーのチェック
        if not all([key in infos for key in ENTRY_KEYS]):
            del module # モジュールの破棄
            continue

        # 実行可能なモジュール
        infos['module'] = module
        infos['id'] = len(modules)
        modules.append(infos)

    return modules