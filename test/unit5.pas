unit unit5;

interface
    type
        tclasse1 = class
            procedure maproc1();
            procedure maproc2(aparam1 : integer);
        private
            function mafunc1(aparam2 : string) : integer;
        protected
            function mafunc2(aparam2 : string) : integer;
        private
            function mafunc3(aparam2 : string) : integer;
        published
            function mafunc4(aparam2 : string) : integer;
        end;
implementation

end.
