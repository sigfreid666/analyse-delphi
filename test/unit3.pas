unit unit3;

interface

    uses
        uses1,
        // avec des commentaires
        uses2;

    PROCEDURE Proc1(AParam1 : Integer);
    PROCEDURE Proc2();
    PROCEDURE Proc3;
    PROCEDURE Proc4(AParam1, AParam2 : Integer);
    PROCEDURE Proc5(CONST AParam1, AParam2 : Integer);
    PROCEDURE Proc6(VAR AParam1, AParam2 : Integer);
    PROCEDURE Proc7(OUT AParam1, AParam2 : Integer);
    PROCEDURE Proc8(OUT AParam1, AParam2 : Integer); OVERLOAD;
    PROCEDURE Proc8(AParam3 : String; OUT AParam1, AParam2 : Integer); OVERLOAD;

implementation

    uses
        uses3,
        // avec des commentaires
        uses4,
        uses5;

end.

