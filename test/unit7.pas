unit unit7;

interface
    type
        trecord1 = record
            procedure maproc1();
            procedure maproc2(aparam1 : integer);
            mavar1 : string;
        private
            function mafunc1(aparam2 : string) : integer;
        protected
            function mafunc2(aparam2 : string) : integer;
        public
            mavar2, mavar3 : integer;
            function mafunc3(aparam2 : string) : integer;

            property maprop1 : integer read mavar1 write mavar1 implements itest;
            property maprop2 : integer write mavar1;
            property maprop3 : integer read mavar1;
            property maprop4 : integer read mavar1 implements itest;
        published
            function mafunc4(aparam2 : string) : integer;
        private
            function mafunc5(aparam2 : string) : integer;
        end;
implementation

end.
