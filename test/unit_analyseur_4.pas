unit unit1;

interface

    uses
        premier,
        deuxieme;

    function myfunc(AParam1 : integer) : string;
    procedure myproc(AParam1 : integer);
    type
        tclass1 = class
            fparam1 : integer;
            fparam2 : string;
            function myfuncclass1(AParam2 : string) : string;
        end;

implementation

    uses
        troisieme,
        quatrieme;

end.

