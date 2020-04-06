unit unit2;

interface

    uses
        uses1,
        // avec des commentaires
        uses2;

    type

        Classe1 = CLASS
            private
                fargument1 : integer;
                fargument2 : string;
            public
                fargument3 : cardinal;
        END;

        Classe2 = CLASS (Classe1)
            private
                fargument4 : integer;
                fargument5 : string;
            public
                fargument6 : cardinal;
        END;

        Record1 = record
            param1 : integer;
            param2 : string;
        end;

        Interface1 = interface
            procedure maprocedure(aparam1 : integer);
        end;

        TArrayBlabla = ARRAY OF Integer;
        TProcPB = PROCEDURE (AParam : Integer) OF OBJECT;
        TProcFB = FUNCTION (AParam : Integer) OF OBJECT;
        TProcP = PROCEDURE (AParam : Integer);
        TProcF = FUNCTION (AParam : Integer);
        TProcPBSP = PROCEDURE () OF OBJECT;
        TProcFBSP = FUNCTION () OF OBJECT;
        TProcPSP = PROCEDURE ();
        TProcFSP = FUNCTION ();

implementation

    uses
        uses3,
        // avec des commentaires
        uses4,
        uses5;

end.

