from types import MappingProxyType

TEMPLATE_PATHS = MappingProxyType({
    'VERIFY_ACCOUNT': 'templates/verify_account.html.jinja2',
})

EMAIL_SUBJECTS = MappingProxyType({
    'VERIFY_ACCOUNT': 'Verifica tu dirección de correo electrónico',
})

EMAIL_TEXT = MappingProxyType({
    'VERIFY_ACCOUNT': 'Bienvenido! Verifica tu dirección de correo electrónico',
})
