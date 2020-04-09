unit unit3;

interface

    uses
        uses1,
        // avec des commentaires
        uses2;

    PROCEDURE Proc1(AParam1 : Integer);
    FUNCTION Func1(AParam1 : Integer) : Integer;
    PROCEDURE Proc2();
    FUNCTION Func2() : String;
    PROCEDURE Proc3;
    FUNCTION Func3 : Integer;
    PROCEDURE Proc4(AParam1, AParam2 : Integer);
    FUNCTION Func4(AParam1, AParam2 : Integer) : Boolean;
    PROCEDURE Proc5(CONST AParam1, AParam2 : Integer);
    FUNCTION Func5(CONST AParam1, AParam2 : Integer) : Double;
    PROCEDURE Proc6(VAR AParam1, AParam2 : Integer);
    FUNCTION Func6(VAR AParam1, AParam2 : Integer) : Integer;
    PROCEDURE Proc7(OUT AParam1, AParam2 : Integer);
    FUNCTION Func7(OUT AParam1, AParam2 : Integer) : String;
    PROCEDURE Proc8(OUT AParam1, AParam2 : Integer); OVERLOAD;
    FUNCTION Func8(OUT AParam1, AParam2 : Integer) : Integer; OVERLOAD;
    PROCEDURE Proc8(AParam3 : String; OUT AParam1, AParam2 : Integer); OVERLOAD;

implementation

    uses
        uses3,
        // avec des commentaires
        uses4,
        uses5;

end.

