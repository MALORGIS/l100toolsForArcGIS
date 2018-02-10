# -*- coding: UTF-8 -*-

#ロケールの確認と_の適用

import os
import locale

#set locale
loctext = locale.setlocale(locale.LC_ALL, "")

import gettext

domain = 'l100tools'
localedir = os.path.join(os.path.dirname(
              os.path.dirname(__file__)), 'locale')

if (loctext.lower().find('japan') > -1):
  t = gettext.translation(domain, localedir, ['ja'], fallback=True)
  t.install()
else:
  gettext.NullTranslations().install()
