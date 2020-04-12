unit unit5;

interface
    type
        tclasse1 = class
        private
            procedure maproc1();
            procedure maproc2(aparam1 : integer);
            mavar1 : string;
            function mafunc1(aparam2 : string) : integer;
        public
            type
                tclasse2 = class
                    mavar4 : string;
                    public
                        function mafunc4(aparam2 : string) : integer;
                end;
            mavar2, mavar3 : integer;
            function mafunc3(aparam2 : string) : integer;
        end;
implementation

end.
