!-----------------------------------------------------------------------------!
! This file is part of the official HFODD v2.73 release and lists all options !
! available in HFODD (parallel data), together with their preset values.      !
!-----------------------------------------------------------------------------!

             ------------  General data  --------------
CALCULMODE ! mpidef, mpibas
               1       0
CONSTR_DEF ! ifcons ! Turn constraints on
               1
ALL_FORCES ! numero  skyrme ! if numero <0, read next line
               1       SKM*

             ---------  Switch on batch mode  ---------
BATCH_MODE ! ibatch, nbatch
               0       1
BATCH_SPEC ! lambda,  miu,  read_next
               3       0       0

             -------------  Nucleus grid  -------------
ALL_NUCLEI ! izstrt, izstep, nstepz, instrt, instep, nstepn
               66       2      1       86      2       1
REALNUCLEI ! xzstrt, xzstep, nstepz, xnstrt, xnstep, nstepn
              66.0     2.0     1      86.0    2.0      1

             ---------  Multipole constraints  --------
MULTICONST ! lambda, miu, qBegin, qFin, numberQ
               2     0     10.0    10.0    4
MULTIRESTA ! lambda, miu, qBegin, qFin, numberQ
               2     0     10.0    10.0    4
OPTIM_GRID ! if_opt ! reset all multipoles to center on restart values
               0

             -------------  Basis grid  ---------------
BASIS-FREQ ! o_mini, o_step, noffre
              8.0     0.1      1
BASIS-NSHL ! n_mini, n_step, nofshl
               8       2       1
BASIS-NSTA ! nsmini, nsstep, nofsta
              165      2       1
BASIS-DEFS ! b20min, b20stp, nofb20
              0.0     0.1      1
END_DATA
