unit unit1;

interface

    uses
        premier,
        deuxieme;

    function myfunc(AParam1 : integer) : string;
    procedure myproc(AParam1 : integer);
    type
        tclass1 = class
        end;

implementation

    uses
        troisieme,
        quatrieme;

end.

