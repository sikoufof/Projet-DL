import re

def translate(text):
    """Translate the given text to Parseltongue.

    :param str text: The text to translate.

    :returns: the translated text.
    :rtype: str
    """
    return re.sub(r"[\w\d]", "s", text)

"""<Courte explication de ce que fait la fonction (une ou deux lignes max)
suivie d'un saut de ligne>.

<Explications plus longues si besoin... On peut faire plusieurs paragraphes
et utiliser tout le formatage reStructuredText proposé par Sphinx !>.

:param <TYPE> <NOM>: <Description du paramètre>.
:param <NOM>: <Description d'un autre paramètre. Ici on ne précise pas le type, c'est optionnel>.

:returns: <Description de ce qui est retourné (si la fonction retourne quelque chose)>.
:rtype: <Type de ce qui est retourné>

:raises <Exception>: <Description de l'exception>.

"""
