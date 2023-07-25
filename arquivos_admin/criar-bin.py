import os
import polib
import gettext

# Lista de idiomas suportados
languages = ["en_US", "es_ES", "pt_BR"]

# Diretório onde estão os arquivos .po
po_dir = os.path.join(os.path.dirname(__file__), "locale")

# Diretório onde serão gerados os arquivos .mo
mo_dir = os.path.join(os.path.dirname(__file__), "locale")

# Verifica se o diretório de destino para os arquivos .mo existe
if not os.path.exists(mo_dir):
    os.makedirs(mo_dir)

# Função para gerar o arquivo .mo para um idioma específico
def generate_mo_file(lang):
    po_file_path = os.path.join(po_dir, lang, "LC_MESSAGES", "lampodoro.po")
    mo_file_path = os.path.join(mo_dir, lang, "LC_MESSAGES", "lampodoro.mo")

    po = polib.pofile(po_file_path)
    po.save_as_mofile(mo_file_path)

# Gera os arquivos .mo para cada idioma suportado
for lang in languages:
    generate_mo_file(lang)

# Configuração de internacionalização para o idioma padrão (en_US)
locale_dir = mo_dir
lang = gettext.translation("lampodoro", localedir=locale_dir, languages=["en_US"])
lang.install()

# Configuração de internacionalização para o idioma padrão (es_ES)
locale_dir = mo_dir
lang = gettext.translation("lampodoro", localedir=locale_dir, languages=["es_ES"])
lang.install()

# Configuração de internacionalização para o idioma padrão (pt_BR)
locale_dir = mo_dir
lang = gettext.translation("lampodoro", localedir=locale_dir, languages=["pt_BR"])
lang.install()

print('Arquivos .mo Criados com Sucesso!!')