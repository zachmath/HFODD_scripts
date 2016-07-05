!-----------------------------------------------------------------------------!
! This file is part of the official HFODD v2.XX release and lists all options !
! available in HFODD (sequential data), together with their preset values     !
!-----------------------------------------------------------------------------!

                      ----  General data and iterations ---
NUCLIDE      IN_FIX  IZ_FIX
               86      66
FLOAT_NUC    XINFIX  XIZFIX
              -1.0    -1.0
PHASESPACE   NUMBSP  NUMBSP  NUMBSP  NUMBSP
               0       0       0       0
ITERATIONS   NOITER
              100
BROYDEN      IBROYD  N_ITER  ALPHAM  BROTRI
                0      7       0.8   1000.0
BROYDENMAT   NOIINP  MIXMAT
                4      0
ITERAT_EPS   EPSITE
              1.D-5
MAXANTIOSC   NULAST
               3
SLOW_DOWN    SLOWEV  SLOWOD
              0.5     0.5
SLOW_PAIR    SLOWPA
              0.5
SLOWLIPKIN   SLOWLI
              0.5
SLOWLIPMTD   SLOWLM  SLOWTP  SLOWRP
              0.5     0.5     0.5
PING-PONG    EPSPNG  NUPING
              0.0      10
CHAOTIC      NUCHAO
               10

                      --------  Specific features  --------
INSERT-HO    IPOTHO
               0
FINITETEMP   TEMP_T
              0.0
SHELLCORCT   IFSHEL
               0
SHELLPARAM   GSTRUN  GSTRUP  HOMFAC  NPOLYN
              1.2     1.2     4.5      6
HFBTHOISON   IF_THO  CBETHO
               0      0.0
MASSFRAGME   IFRAGM
               0
FRAGDENSIT   IDEALL  IDELOC  IDECON
               0       0       0
QPROTATION   MIN_QP  DELTAE  XLOCMX  V2_MIN  ITRMAX  NTHETA
               0       2.5    0.75    0.005    31      181
COLL_SPACE   L_COLL  M_COLL
               -2      0
                2      2
RENORMASS    IRENMA  DISTAX  DISTAY  DISTAZ
               0      0.0     0.0     0.0
TRANSLMASS   HBMRIN(1) HBMRIN(2) HBMRIN(3)
               1.0       1.0       1.0
RENORINERT   IRENIN  ROTATX  ROTATY  ROTATZ
               0      0.0     0.0     0.0
ROTATINERT   ROTRIN(0) ROTRIN(1) ROTRIN(2)
               1.0       1.0       1.0
GAUOVERAPP   IDOGOA
               1
ROTAT_CORR   KETA_R
               3
PROTNEUMIX   IPNMIX
               0
INI_INVERS   INIINV  INIKAR
               0       0
EULERANGLS   ALPAUX  BETAUX  GAMAUX  INIROT
              0.0     0.0     0.0      0
NILSSONPAR   NILDAT  CNILSN  DNILSN  CNILSP  DNILSP  HBANIX  HBANIY  HBANIZ
               0     -1.175  -0.247  -1.175  -0.352  11.170  11.170  6.280

                      -----------  Interaction  -----------
UNEDF-PROJ   IF_EDF
               0
SKYRME-SET   SKYRME
            SKM*
SKYRME-STD   ISTAND  KETA_J  KETA_W  KETACM  KETA_M
               1       1       0       0       0
HBAR2OVR2M   HBMINP
             20.73620941
EVE_SCA_TS       RHO     RHOD      LPR     TAU      SCU      DIV
               1.  1.   1.  1.   1.  1.   1.  1.   1.  1.   1.  1.
ODD_SCA_TS       SPI     SPID      LPS     CUR      KIS      ROT
               1.  1.   1.  1.   1.  1.   1.  1.   1.  1.   1.  1.
EVE_SCA_PM       RHO     RHOD      LPR     TAU      SCU      DIV
               1.  1.   1.  1.   1.  1.   1.  1.   1.  1.   1.  1.
ODD_SCA_PM       SPI     SPID      LPS     CUR      KIS      ROT
               1.  1.   1.  1.   1.  1.   1.  1.   1.  1.   1.  1.
EVE_ADD_TS       RHO     RHOD      LPR     TAU      SCU      DIV
               0.  0.   0.  0.   0.  0.   0.  0.   0.  0.   0.  0.
ODD_ADD_TS       SPI     SPID      LPS     CUR      KIS      ROT
               0.  0.   0.  0.   0.  0.   0.  0.   0.  0.   0.  0.
EVE_ADD_PM       RHO     RHOD      LPR     TAU      SCU      DIV
               0.  0.   0.  0.   0.  0.   0.  0.   0.  0.   0.  0.
ODD_ADD_PM       SPI     SPID      LPS     CUR      KIS      ROT
               0.  0.   0.  0.   0.  0.   0.  0.   0.  0.   0.  0.
SPIN_ORBIT   W0_INP  W0PINP
              120.0   120.0
LANDAU       LANODD  X0_LAN  X1_LAN  G0_LAN  G0PLAN  G1_LAN  G1PLAN
               0       0.0     0.0     0.0     0.0     0.0     0.0
LANDAU_SAT   HBMSAT  RHOSAT  EFFSAT
              -1.0    -1.0    -1.0
LAN4SCALED   LANSCA
               0
GOGNY        I_GOGA
               0
GOGNY_SET    GOGNAM
            D1S
REGUSKYRME   I_REGA
               0
REGUL_PAIR   IREGPA
               0
REGUORDER    N3LORD  REGWID
               1      1.0
REGUPARAMS   IREREG  N3LAUX  REGAUX
               0       0      1.0
REGUCOUPLI   IREREG  N3LAUX  REGAUX
               0       0      1.0
REGUL_TXYZ   IREREG  N3LAUX  REGAUX
               0       0      1.0
HYPERCONTR   IDOTHC
               0
YUKAWA       PIDUMM  I_YUKA
             0.7045    0
YUKAWATERM   PIDUMM  PNDUMM  YUKAGT  YUKAG0  YUKAG1  YUKAG2  IYUTYP  I_YUKA
             0.7045  4.7565   1.0     0.0     0.0     0.0       1      0
COULOMB      NUMCOU  NUMETA  FURMAX
               80      79     0.25
COULOMBPAR   ICOTYP  ICOUDI  ICOUEX
               7       1       1
COULOCHARG   E_EFFE
              1.0
3BODYDELTA   THRINP  ITHRIN
               0       0
4BODYDELTA   FOUINP  IFOUIN
               0       0
CHARBREAK2   T02CBR,X02CBR,I02CBR
               0.0    0.0    0
CHARBREAK3   T03CBR,X03CBR,I03CBR
               0.0    0.0    0

                      ----------    Pairing    ------------
PAIRING      IPAIRI
                0
HFB          IPAHFB
                0
CUTOFF       ECUTOF
              60.0
CUT_SPECTR   LIMQUA
                0
BCS          IPABCS
               -1
GOGNY_PAIR   IGOGPA
               0
HFBMEANFLD   IMFHFB
                0
PAIRNFORCE   PRHO_N  PRHODN  POWERN
            -200.00   0.0     1.0
PAIRPFORCE   PRHO_P  PRHODP  POWERP
            -200.00   0.0     1.0
PAIR_FORCE   PRHO_T  PRHODT  POWERT
               0.0    0.0     1.0
PAIRNINTER   PRHO_N  PRHOSN  POWERN
            -200.00   0.16    1.0
PAIRPINTER   PRHO_P  PRHOSP  POWERP
            -200.00   0.16    1.0
PAIR_INTER   PRHO_T  PRHOST  POWERT
               0.0    0.16    1.0
G_SCALING    FACTGN  FACTGP
               1.0     1.0
G_AUTOCALC   IAVRGG
                0
PAIR_MATRI   IDESTA  IDEMID  IDESTO  IDEDIS
                1       0       0       0
INI_DELTA    DELINI(0)  DELINI(1)
               1.0       1.0
FIXDELTA_N   DELFIN  IDEFIN
               1.0      0
FIXDELTA_P   DELFIP  IDEFIP
               1.0      0
INI_FERMI    FERINI(0) FERINI(1)
              -8.0      -8.0
FIXFERMI_N   FERFIN  IFEFIN
              -8.0      0
FIXFERMI_P   FERFIP  IFEFIP
              -8.0      0
ISO_FERMI    FERISO(1) FERISO(2) FERISO(3)
               0.0       0.0       0.0
FERMI_SCA    FERISO(0)
               0.0
ALMFERMI_N   FERALN  IFERAN
               0.0      0
ALMFERMI_P   FERALP  IFERAP
               0.0      0
FERMI_OFF    FE_OFF
               0.0
FERMI_RTP    FE_RAD  FE_THE  FE_PHI  FE_OFF
               0.0     0.0    0.0      0.0
LIPKIN       LIPKIN  LIPKIP
                0       0
NOBLOLIPKI   LIPNON  LIPNOP
                0       0
INI_LIPKIN   FE2INI(0)  FE2INI(1)
               0.1        0.1
FIXLAMB2_N   FE2FIN  IF2FIN
               0.1      0
FIXLAMB2_P   FE2FIP  IF2FIP
               0.1      0
LIPORDER     ILIPON  ILIPOP
                0       0
GAUGESHIFT   GAUSHI
             0.1232
GAUGEFRACT   MAXGAU
               1
                     -----------  Symmetries  -------------
SPHERICAL    ISPHER
               0
ROTATION     IROTAT
               1
TIMEREVERS   ITIREV
               0
SIMPLEXY     ISIMPY
               1
SIGNATUREY   ISIGNY
               1
PARITY       IPARTY
               -1
TSIMPLEX3D   ISIMTX  ISIMTY  ISIMTZ
               1       -1       1
TSIMPLEX_Y   ISIMTY
               -1
TSIMPLEXES   ISIMTX  ISIMTZ
               1       1
TIMEREPAIR   ITIREP
               0

                      -----------  q.p. blocking  ---------
BLOCKSIG_N  INSIGN  IPSIGN  ISSIGN  IDSIGN
               1       0       0       0
BLOCKSIG_P  INSIGP  IPSIGP  ISSIGP  IDSIGP
               1       0       0       0
BLOCKSIM_N  INSIMN  IRSIMN  IDSIMN
               1       0       0
BLOCKSIM_P  INSIMP  IRSIMP  IDSIMP
               1       0       0
BLOCKSIQ_N  INSIQN  IPSIQN  IDSIQN
               1       0       0
BLOCKSIQ_P  INSIQP  IPSIQP  IDSIQP
               1       0       0
BLOCKSIZ_N  INSIZN  IDSIZN
               1       0
BLOCKSIZ_P  INSIZP  IDSIZP
               1       0
BLOCKFIX_N  IFIBLN  INIBLN
               0       0
BLOCKFIX_P  IFIBLP  INIBLP
               0       0

                      -----  HF Vacuum Configurations  ----
VACUUMCONF  IVACUM
               0
VACSIG_NEU  KVASIG: PPSP, PPSM, PMSP, PMSM
                     21    21    22    22
VACSIG_PRO  KVASIG: PPSP, PPSM, PMSP, PMSM
                     16    16    17    17
VACSIG_NUC  KVAMIG: PPSP  PPSM  PMSP  PMSM
                     37    37    39    39
VACSIM_NEU  KVASIM: SP, SM
                    43  43
VACSIM_PRO  KVASIM: SP, SM
                    33  33
VACSIM_NUC  KVAMIM: SP, SM
                    76  76
VACPAR_NEU  KVASIQ: PP, PM
                    44  42
VACPAR_PRO  KVASIQ: PP, PM
                    32  34
VACPAR_NUC  KVAMPA: PP, PM
                    76  76

                      ----  HF Filling Configurations  ----
FILSIG_NEU   KPFILG: PPSP, PMSP, PPSM, PMSM  KHFILG: PPSP, PMSP, PPSM, PMSM  KOFILG: PPSP, PMSP, PPSM, PMSM
                      2     2     2     2             1     1     1     1             0     0     0     0
FILSIG_PRO   KPFILG: PPSP, PMSP, PPSM, PMSM  KHFILG: PPSP, PMSP, PPSM, PMSM  KOFILG: PPSP, PMSP, PPSM, PMSM
                      2     2     2     2             1     1     1     1             0     0     0     0
FILNON_NEU   KPFILZ(0) KHFILZ(0) KOFILZ(0)
               2          1        0
FILNON_PRO   KPFILZ(1) KHFILZ(1) KOFILZ(1)
               2          1        0

                      ----  HF Diabatic Configurations  ---
DIABATIC     ICHFLI  IPAFLI  ISIFLI  ISPFLI  ISHFLI  IFLIPI
               0       0       0       2       1       0
DIASIG_NEU   KPFLIG: PPSP, PMSP, PPSM, PMSM  KHFLIG: PPSP, PMSP, PPSM, PMSM  KOFLIG: PPSP, PMSP, PPSM, PMSM
                      2     2     2     2             1     1     1     1             0     0     0     0
DIASIG_PRO   KPFLIG: PPSP, PMSP, PPSM, PMSM  KHFLIG: PPSP, PMSP, PPSM, PMSM  KOFLIG: PPSP, PMSP, PPSM, PMSM
                      2     2     2     2             1     1     1     1             0     0     0     0
DIASIG_NUC   KPMLIG: PPSP, PMSP, PPSM, PMSM  KHMLIG: PPSP, PMSP, PPSM, PMSM  KOMLIG: PPSP, PMSP, PPSM, PMSM
                      2     2     2     2             1     1     1     1             0     0     0     0
DIASIM_NEU   KPFLIM: SP, SM  KHFLIM: SP, SM  KOFLIM: SP, SM
                      2   2           1   1           0   0
DIASIM_PRO   KPFLIM: SP, SM  KHFLIM: SP, SM  KOFLIM: SP, SM
                      2   2           1   1           0   0
DIASIM_NUC   KPMLIM: SP, SM  KHMLIM: SP, SM  KOMLIM: SP, SM
                      2   2           1   1           0   0
DIAPAR_NEU   KPFLIQ: PP, PM  KHFLIQ: PP, PM  KOFLIQ: PP, PM
                      2   2           1   1           0   0
DIAPAR_PRO   KPFLIQ: PP, PM  KHFLIQ: PP, PM  KOFLIQ: PP, PM
                      2   2           1   1           0   0
DIAPAR_NUC   KPMLIQ: PP, PM  KHMLIQ: PP, PM  KOMLIQ: PP, PM
                      2   2           1   1           0   0
DIANON_NEU   KPFLIZ(0) KHFLIZ(0) KOFLIZ(0)
                2         1         0
DIANON_PRO   KPFLIZ(1) KHFLIZ(1) KOFLIZ(1)
                2         1         0
DIANON_NUC   KPMLIZ  KHMLIZ  KOMLIZ
               2       1       0

                      -------  HF p.-h. Excitations  ------
PHSIGN_NEU   NUPAHO  KPPPSP  KPPPSM  KPPMSP  KPPMSM  KHPPSP  KHPPSM  KHPMSP  KHPMSM
               1       0       0       0       0       0       0       0       0
PHSIGN_PRO   NUPAHO  KPPPSP  KPPPSM  KPPMSP  KPPMSM  KHPPSP  KHPPSM  KHPMSP  KHPMSM
               1       0       0       0       0       0       0       0       0
PHSIGN_NUC   NUPAHO  LPPPSP  LPPPSM  LPPMSP  LPPMSM  LHPPSP  LHPPSM  LHPMSP  LHPMSM
               1       0       0       0       0       0       0       0       0
PHSIMP_NEU   NUPAHO  KPSIMP  KPSIMM  KHSIMP  KHSIMM
               1       0       0       0       0
PHSIMP_PRO   NUPAHO  KPSIMP  KPSIMM  KHSIMP  KHSIMM
               1       0       0       0       0
PHSIMP_NUC   NUPAHO  LPSIMP  LPSIMM  LHSIMP  LHSIMM
               1       0       0       0       0
PHPARI_NEU   NUPAHO  KPSIQP  KPSIQM  KHSIQP  KHSIQM
               1       0       0       0       0
PHPARI_PRO   NUPAHO  KPSIQP  KPSIQM  KHSIQP  KHSIQM
               1       0       0       0       0
PHPARI_NUC   NUPAHO  LPSIQP  LPSIQM  LHSIQP  LHSIQM
               1       0       0       0       0
PHNONE_NEU   NUPAHO(0) KPNONE(0) KHNONE(0)
               1       0       0
PHNONE_PRO   NUPAHO(1) KPNONE(1) KHNONE(1)
               1       0       0
PHNONE_NUC   NUPAHO  LPNONE  LHNONE
               1       0       0

                     ----  Parameters of the HO basis  ----
TWOBASIS     ITWOBA
               0
BASISAUTOM   IBASIS
               0
BASIS_SIZE   NOSCIL  NLIMIT  ENECUT
               10     286    800.0
HOMEGAZERO   FCHOM0
              1.2
FREQBASIS    HBARIX  HBARIY  HBARIZ  INPOME
              1.0     1.0     1.0      0
SURFAC_PAR   INNUMB  IZNUMB  R0PARM
               86      66     1.23
SURFAC_DEF   LAMBDA   MIU    ALPHAR
               -2      0      0.61
                4      0      0.10
OPTI-GAUSS   IOPTGS
               1
GAUSHERMIT   NXHERM  NYHERM  NZHERM
               18      18      32
EPS_HERMIT   EPSHER
             1.D-14

                     -------- Multipole moments  ----------
MAX_MULTIP   NMUCON  NMUCOU  NMUPRI
                4      4       4
RPA_CONSTR   IF_RPA
                0
MULTCONSTR   LAMBDA   MIU    STIFFQ  QASKED  IFLAGQ
                2      0      0.01   42.00     1
MULTLAGRAN   LAMBDA   MIU    QLINEA  IFLALQ
                2      0      0.00     0
MAX_SCHIFF   NSICON  NSIPRI
                0      0
SCHIFF_MOM   ISCHIF
                0
SCHICONSTR   LAMBDA   MIU    STIFFS  SASKED  IFLAGS
                2      0      1.00    0.00     0
SCHILAGRAN   LAMBDA   MIU    SLINEA  IFLALS
                2      0      0.00     0
MULTCONSCA   LAMBDA  STIFFG  GASKED  IFLAGG
                2     1.00    0.00     0
MAX_MAGNET   NMACON  NMAPRI
                0      0
TRANSITION   NMURED  NMARED  NSIRED
                2      1       0
NECK_CONST   IFNECK  Q0NECK  G_NECK
                0     1.0     0.0

                     --------  Angular Momentum  ----------
OMEGAY       OMEGAY
              0.50
OMISOY       OMISOY
              0.00
OMEGA_XYZ    OMEHAX  OMEHAY  OMEHAZ  ITILAX
              0.00    0.00    0.00      0
OMEGA_RTP    OMERAD  OMETHE  OMEPHI  ITILAX
              0.00    0.00    0.00      0
OMISO_XYZ    OMISOX  OMISOY  OMISOZ  ITISAX
              0.00    0.00    0.00      0
OMEGA_TURN   IMOVAX
                0
NORBCONSTR   NO_ORB
                0
SPINCONSTR   STIFFI  ASKEDI  IFLAGI
              0.00    0.00     0
SPICON_XYZ   STIFFI  ASKEDI  IFLAGI
              0.00    0.00     0
              0.00    0.00     0
              0.00    0.00     0
ISO_CONSTR   STIFFT  ASKEDT  IFLAGT
              0.00    0.00     0
              0.00    0.00     0
              0.00    0.00     0
SPINLAGRAN   DALSPI  IFLALI
               0.0      0
SPINLA_XYZ   DALSPI  IFLALI
              0.00     0
              0.00     0
              0.00     0
ISO_LAGRAN   DALISO  IFLALT
              0.00     0
              0.00     0
              0.00     0
ISOSP_CNST   DALISO  STIFFT  ASKEDT  JFLAGT
              0.00    0.00     0.00     0
              0.00    0.00     0.00     0
              0.00    0.00     0.00     0
SPICON_OME   STIFFA  ASKEDA  IFLAGA
              0.00     0.0     0

                      ----------  Projection  -------------
NUMBKERNEL   KFIKER
               0
CHECKERNEL   ICHKER
               1
PARAKERNEL   IPAKER  NUASTA  NUASTO  NUGSTA  NUGSTO
               0       1       1       1       1
PARA_ALL     IPAALL  NUBSTA  NUBSTO  NUTSTA  NUTSTO
               0       1       1       1       1
PARAKER_3D   IPAK3D  NATSTA  NATSTO  NGTSTA  NGTSTO
               0       1       1       1       1
PROJECTGCM   IPRROT  IPROMI  IPROMA  NUAKNO  NUBKNO  KPROJE  IFRWAV  ITOWAV  IWRWAV
               0       0       0       1       1        0      1       1       0
CUTOVERLAP   ICUTOV  CUTOVE  CUTOVF
               0     1.D-10   1.0
PROJ3D_ISO   IPRIS3  KSOSMI  KSOSMA  NATKNO  NBTKNO  KSOSTZ  EPSISO  ICSKIP  IFERME
               0       0       0       1       1       0     1.D-6     0       0
PROJECTISO   IPRISO  ISOSAD  NBTKNO  EPSISO  ICSKIP  IFERME  IIFEME  ITFEME  ISFEME
               0       0       1     1.D-6     0       0       0       2       1
FERMIMATEL   IFERME  IIFEME  ITFEME  ISFEME
               0       0       2       1
PARTNUMPRJ   IPNPRJ  NPPNPN  NPPNPP
               0       0       0

                     ------  Output-file  parameters  -----
ONE_LINE     I1LINE
               1
PRINT-ITER   IPRSTA  IPRMID  IPRSTO
               1       0       1
PRINT_MOME   IPRI_N  IPRI_P  IPRI_T
               1       1       1
EALLMINMAX   EMINAL  EMAXAL
              -50.0   20.0
EQUASI_MAX   EMAXQU
              +50.0
NILSSONLAB   NILXYZ
               3
PRINT_VIOL   IVIPRI
               0
TRANCUTPRI   QMUCUT  QMACUT  QSICUT
               0.0     0.0     0.0
PRINT_AMP    ISLPRI  ISUPRI  IENPRI  ISRPRI  IMIPRI  IKEPRI  IRMPRI
               0      999      1       1       1        0      0
PRINT_INTR   INTRIP
               1
PRINT_SYME   ISYMDE
               0
BOHR_BETAS   NEXBET  IPRIBE  IPRIBL
               4       0        1

                     ------------  I/O Flags  -------------
RECORDSAVE   IWRIRE
               1
FIELD_SAVE   IWRIFI
              -1
YUKAWASAVE   IWRIYU
              -1
GOGNYSAVE    IWRIGO
              -1
REGULSAVE    IWRIRO
              -1
LIPKINSAVE   IWRILI
               1
REVIEW       IREVIE
               2
COULOMSAVE   ICOULI  ICOULO
               0      0
SAVEKERNEL   ISAKER
               0
FIELD_OLD    IWRIOL
               0
WRITE_ISO    IWRISO
               0

                     ------------  I/O Files  -------------
RECORDFILE   FILREC
            HFODD.REC
REPLAYFILE   FILREP
            HFODD.REP
REP_FIELDS   FILFIP
            HFODD.FIC
REC_FIELDS   FILFIC
            HFODD.FIP
RECYUKFILE   FILYUC
            HFODD.YUK
REPYUKFILE   FILYUP
            HFODD.YUP
RECGOGFILE   FILGOC
            HFODD.GOC
REPGOGFILE   FILGOP
            HFODD.GOP
RECGPAFILE   FILGPC
            HFODD.GPA
REPGPAFILE   FILGPP
            HFODD.GPP
RECREGFILE   FILROC
            HFODD.ROC
REPREGFILE   FILROP
            HFODD.ROP
RECLIPFILE   FILLIC
            HFODD.LIC
REPLIPFILE   FILLIP
            HFODD.LIP
REVIEWFILE   FILREV
            HFODD.REV
WOODSAFILE   FILWOO
            HFODD.WFN
COULOMFILE   FILCOU
            HFODD.COU
KERNELFILE   FILKER
            HFODD.KER
ISOSPIFILE   FILISO
            HFODD.ISO
WAVEF_FILE   FILWAV
            HFODD.WAV

                     ------  Starting the iteration  ------
RESTART      ICONTI
               0
CONT_PAIRI   IPCONT
               0
CONTLIPKIN   ILCONT
               0
CONTFIELDS   IFCONT
               0
CONTAUGMEN   IACONT
               0
CONT_OMEGA   IOCONT
               0
CONTYUKAWA   IYCONT
               0
CONTGOGNY    IGCONT
               0
CONTGOGPAI   IGPCON
               0
CONTREGUL    IECONT
               0
CONTCMCORR   IMCONT
               0
CONTROTCOR   IRCONT
               0
CONTAUGSPI   ISCONT
               0
CONTAUGISO   ITCONT
               0
READ_WOODS   IREAWS
               0

                     ------------  Calculate  -------------
EXECUTE
                     ------------  Terminate  -------------
ALL_DONE
