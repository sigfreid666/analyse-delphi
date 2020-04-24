from analyse_code.gestion_multiligne import gestion_multiligne


def test_ml1():
    lignes = ['premiere ligne\n',
              'deuxieme ligne\n']
    gl = gestion_multiligne(lignes)

    assert gl.data == 'premiere ligne deuxieme ligne '


def test_ml_commentaire():
    lignes = ['premiere ligne // avec un commentaire qui va bien\n',
              'deuxieme ligne\n']
    gl = gestion_multiligne(lignes)

    assert gl.data == 'premiere ligne  deuxieme ligne '


def test_ml_region():
    lignes = ['premiere ligne {$REGION}suite\n',
              'deuxieme ligne {$ENDREGION}\n']
    gl = gestion_multiligne(lignes)

    assert gl.data == 'premiere ligne  suite deuxieme ligne   '


def test_ml_parenthese():
    lignes = ['premiere ligne (* commentaire *)suite\n',
              'deuxieme ligne { re commentaire }\n']
    gl = gestion_multiligne(lignes)

    assert gl.data == 'premiere ligne suite deuxieme ligne  '


def test_ml_multiligne1():
    lignes = ['premiere ligne (* commentaire suite\n',
              'deuxieme ligne *)et la fin\n']
    gl = gestion_multiligne(lignes)

    assert gl.data == 'premiere ligne et la fin '


def test_ml_else():
    lignes = ['premiere ligne\n',
              '{$ELSE}\n',  
              'ligne qui doit etre supprime\n',
              '{$ENDIF}\n',
              'derniere ligne\n']
    gl = gestion_multiligne(lignes)

    assert gl.data == 'premiere ligne  derniere ligne '
