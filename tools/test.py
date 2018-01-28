# -*- coding:utf-8 -*-
import gettext
#import translationstring
import os
import locale

loctext = locale.setlocale(locale.LC_ALL, "")

domain = 'l100tools'
localedir = os.path.join(os.path.dirname(
              os.path.dirname(__file__)), 'locale')

if (loctext.lower().find('japan') > -1):
  t = gettext.translation(domain, localedir, ['ja'], fallback=True)
  t.install()
else:
  gettext.NullTranslations().install()

#translator = translationstring.Translator()

print(_("Feature Vertices To Points"))
