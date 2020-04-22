PROGRAM main1;

{$WEAKLINKRTTI ON}

//Customdpr
//Gendpr:InitGestionnaireMemoire,ClasseFinalisable,HooksTraduction,ApplicationIndex
//Gendpr:InstanceApplicationMonoposteEDT,Debug_ExpertDebogage

  USES
    unit1                         IN 'C:\Projets\Produits\DEV\unit1.pas',
    unit4                         IN 'C:\Projets\Produits\DEV\unit4_.pas';

{$R *.res}
{$R C:\Projets\Produits\DEV\Scolys\_Delphi\IconeBaseEdt.res}

BEGIN
  VAR LApplication : TApplicationIndex := CreerInstanceApplication ();
  IF Assigned (LApplication) THEN
    TRY
      LApplication.Execute ();
    FINALLY
      LApplication.Destroy ();
    END (* TRY ... FINALLY *);
END.