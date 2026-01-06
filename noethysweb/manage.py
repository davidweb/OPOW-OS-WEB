#!/usr/bin/env python
#  Copyright (c) 2019-2021 Ivan LUCAS.
#  Noethysweb, application de gestion multi-activités.
#  Distribué sous licence GNU GPL.

import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'noethysweb.settings')

    # Compatibility shim: provide legacy translation API names removed in newer Django
    # (e.g. ugettext_lazy -> gettext_lazy) so third-party packages importing the
    # old names keep working.
    try:
        import importlib
        trans = importlib.import_module("django.utils.translation")
        aliases = [
            ("ugettext", "gettext"),
            ("ugettext_lazy", "gettext_lazy"),
            ("ungettext", "ngettext"),
            ("ungettext_lazy", "ngettext_lazy"),
        ]
        for old_name, new_name in aliases:
            if not hasattr(trans, old_name) and hasattr(trans, new_name):
                setattr(trans, old_name, getattr(trans, new_name))
    except Exception:
        # If importing django.utils.translation fails here, let the normal error flow occur later.
        pass

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
