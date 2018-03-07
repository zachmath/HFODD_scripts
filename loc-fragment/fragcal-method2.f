c---Langevin code with self-consistent mean-field-----10/01/12 
      implicit real*8 (a-h,o-z)
      dimension xx(36),yy(36),zz(60),den(36,36,60),dpro(36,36,60)
! 36 is the number of distinct x and y values, and 64 is the number of z values in the sample file
      dimension q(18),bb(18),b(50),c(50),d(50),qk(50),bbk(50)
      dimension zk(1001),valk(1001),q1(50),bb1(50),arg(1001),arg1(1001)
      dimension x1(1001),dent(1001,50),z1(1001),den1(1001,1001)
      dimension dens(1001,60),q2(60),bb2(60)  
      character(len=132) :: fichierIn, fichierOut
      Call Get_Command_Argument(1, fichierIn)
      Call Get_Command_Argument(2, fichierOut)
      open(7,file=fichierIn,status='old')
      open(5,file=fichierOut,status='unknown')

      n=36 ! Number of x, y values
      nn=18 ! I assume this is just n/2?
      nz=60 ! Number of z values
      nk=0 
      qk=0.0d0
      bbk=0.0d0
      denv=0.006d0
      q=0.0d0
      bb=0.0d0
      dent=0.0d0
      pi=4.0d0*datan(1.0d0)
c-------reading density-----------------------
      do iz=1,nz
       do iy=1,n
        do ix=1,n 
c-----change the position of dpro for neutron or proton-----
!-----The file is ordered: x, y, z, dneu, dpro, dtot (although this may be HFODD-version dependent, I'm afraid)
         read(7,*)xx(ix),yy(iy),zz(iz),dpro(ix,iy,iz),d1,den(ix,iy,iz)
        enddo
       enddo
      enddo
c----------------------------------------------------------
      do iz=nz,1,-1
       b=0.0d0
       c=0.0d0
       d=0.0d0
       do i=1,nn
        j=nn+1-i 
        q(i)=xx(j)
        bb(i)=den(j,j,iz)
        if(bb(i).lt.0.0001)bb(i)=0.0d0
       enddo
       
       vmin=1.0d0
       qm=maxval(q)
       if(qm.gt.denv)then
        call spline(q,bb,b,c,d,nn)
        do jj=1,100000
         xv=0.30d0+dfloat(jj-1)*0.0001d0
         call fspline(xv,val,q,bb,b,c,d,nn)
         vt=dabs(val-denv)
         if(vt.lt.vmin)then
          vmin=vt
          xmin=xv
         endif 
        enddo
        if(xmin.gt.0.5d0)then
         nk=nk+1
         qk(nk)=zz(iz)
         bbk(nk)=xmin
        endif 
       endif
      enddo 

      dz=(qk(nk)-qk(1))/1000
      do ii=1,1001
       z=qk(1)+dfloat(ii-1)*dz
       call inpolqd(z,val,qk,bbk,nk)
       zk(ii)=z
       valk(ii)=val
      enddo    
c----locating the maxima along z----------
      do i=2,1000
       if(valk(i)-valk(i-1).gt.0.0d0.and.valk(i)-valk(i+1).gt.0.0d0)
     1 then
        if(zk(i).lt.0.0d0)p1in=zk(i)
c---13.0 is used manually to avoid wrong maxima---this value may be
c---different for different inputs--------
        if(zk(i).gt.0.0d0.and.zk(i).lt.13.0d0)p2in=zk(i)
c        if(zk(i).gt.0.0d0)p2in=zk(i)
       endif
      enddo

      do i=nz,1,-1
       if(zz(i).gt.p1in)then
        i1in=i
        exit
       endif
      enddo
      do i=1,nz
       if(zz(i).lt.p2in)then
        i2in=i
        exit
       endif
      enddo

      write(5,*)'location of maxima'
! I think the order is something like "index1, index2, z1, z2"
      write(5,*)i1in,i2in,p1in,p2in
      nz1=nz-i1in+1
      nz2=i2in
      d1z=(p1in-zz(nz))/1000.0d0
      d2z=(zz(1)-p2in)/1000.0d0 
c################# CALCULATION FOR FRAG-1 ####################### 
c-----dent=density along x=y for each z, and x1=sqrt(x^2+y^2)---
      do iz=1,nz1
       izz=i1in+iz-1 
       q1=0.0d0
       bb1=0.0d0
       do i=1,nn+1
        j=nn+2-i 
        q1(i)=xx(j)
        bb1(i)=dpro(j,j,izz)
        if(bb1(i).lt.0.0001d0)bb1(i)=0.0d0
       enddo
       do j=1,1001
        x=0.0d0+dfloat(j-1)*0.01d0
        call inpolqd(x,val,q1,bb1,nn+1)
        if(val.lt.0.0001d0)val=0.0d0
        x1(j)=dsqrt(2.0d0)*x
        dent(j,iz)=val
       enddo
      enddo 
c----interpolation along z-----finally den1 is 1001X1001----
      do j=1,1001
       q1=0.0d0
       bb1=0.0d0
       do iz=1,nz1
        izz=nz-iz+1
        q1(iz)=zz(izz)
        bb1(iz)=dent(j,nz1-iz+1)
       enddo
       do i=1,1001
c---p1in is the starting z for FRAG-1------
        z=p1in-dfloat(i-1)*d1z
        call inpolqd(z,val,q1,bb1,nz1) 
        if(val.lt.0.0001d0)val=0.0d0
        z1(i)=0.0d0+dfloat(i-1)*d1z
        den1(j,i)=val
       enddo
      enddo
c----x1 and z integrations to get FRAG-1 n or p------
      do i=1,1001
       do j=1,1001
        arg(j)=2.0d0*pi*x1(j)*den1(j,i)
       enddo
       h=x1(2)-x1(1)
       nq=1001
       call simp(arg,h,nq,val)
       arg1(i)=val
      enddo 
      h=z1(2)-z1(1)
      call simp(arg1,h,nq,val1)
c--------Q20 for FRAG-1----------------------------
      do i=1,1001
       do j=1,1001
        arg(j)=2.0d0*pi*x1(j)*den1(j,i)*(2.0d0*z1(i)**2-x1(j)**2)
       enddo
       h=x1(2)-x1(1)
       nq=1001
       call simp(arg,h,nq,val)
       arg1(i)=val
      enddo 
      h=z1(2)-z1(1)
      call simp(arg1,h,nq,val2)

      write(5,*)'FRAG-1 n or p no.=',nint(2.0d0*val1),
     1          'Q20=',2.0d0*val2/val1
c###################### FRAG-2 ##############################
c-----dent=density along x=y for each z, and x1=sqrt(x^2+y^2)---
      dent=0.0d0
      do iz=1,nz2
       q1=0.0d0
       bb1=0.0d0
       do i=1,nn+1
        j=nn+2-i 
        q1(i)=xx(j)
        bb1(i)=dpro(j,j,iz)
        if(bb1(i).lt.0.0001d0)bb1(i)=0.0d0
       enddo
       do j=1,1001
        x=0.0d0+dfloat(j-1)*0.01d0
        call inpolqd(x,val,q1,bb1,nn+1)
        if(val.lt.0.0001d0)val=0.0d0
        x1(j)=dsqrt(2.0d0)*x
        dent(j,iz)=val
       enddo
      enddo 
c----interpolation along z-----finally den1 is 1001X1001----
      z1=0.0d0
      den1=0.0d0
      val=0.0d0
      do j=1,1001
       q1=0.0d0
       bb1=0.0d0
       do iz=1,nz2
        izz=nz2-iz+1
        q1(iz)=zz(izz)
        bb1(iz)=dent(j,izz)
       enddo
       do i=1,1001
c---p1in is the starting z for FRAG-2------
        z=p2in+dfloat(i-1)*d2z
        call inpolqd(z,val,q1,bb1,nz2)
        if(val.lt.0.0001d0)val=0.0d0
        z1(i)=0.0d0+dfloat(i-1)*d2z
        den1(j,i)=val
       enddo
      enddo
c----x1 and z integrations to get FRAG-2 n or p------
      do i=1,1001
       do j=1,1001
        arg(j)=2.0d0*pi*x1(j)*den1(j,i)
       enddo
       h=x1(2)-x1(1)
       nq=1001
       call simp(arg,h,nq,val)
       arg1(i)=val
      enddo 
      h=z1(2)-z1(1)
      call simp(arg1,h,nq,val1)
c--------Q20 for FRAG-2----------------------------
      do i=1,1001
       do j=1,1001
        arg(j)=2.0d0*pi*x1(j)*den1(j,i)*(2.0d0*z1(i)**2-x1(j)**2)
       enddo
       h=x1(2)-x1(1)
       nq=1001
       call simp(arg,h,nq,val)
       arg1(i)=val
      enddo 
      h=z1(2)-z1(1)
      call simp(arg1,h,nq,val2)

      write(5,*)'FRAG-2 n or p no.=',nint(2.0d0*val1),
     1          'Q20=',2.0d0*val2/val1

      stop
      end

c########################################################
      subroutine spline(x,y,b,c,d,n)
      implicit real*8 (a-h,o-z)
      dimension x(n),y(n),b(n),c(n),d(n)
      
      igap=n-1

      d(1)=x(2)-x(1)
      c(2)=(y(2)-y(1))/d(1)

      do i=2,igap
        d(i)=x(i+1)-x(i)
        b(i)=2.0*(d(i-1)+d(i))
        c(i+1)=(y(i+1)-y(i))/d(i)
        c(i)=c(i+1)-c(i)
      enddo

      b(1)=-d(1)
      b(n)=-d(n-1)
      c(1)=0.0d0
      c(n)=0.0d0
      if(n.ne.3)then
        c(1)=c(3)/(x(4)-x(2))-c(2)/(x(3)-x(1))
        c(n)=c(n-1)/(x(n)-x(n-2))-c(n-2)/(x(n-1)-x(n-3))
        c(1)=c(1)*d(1)**2/(x(4)-x(1))
        c(n)=-c(n)*d(n-1)**2/(x(n)-x(n-3))
      endif

      do i=2,n
        h=d(i-1)/b(i-1)
        b(i)=b(i)-h*d(i-1)
        c(i)=c(i)-h*c(i-1)
      enddo

      c(n)=c(n)/b(n)
      do j=1,igap
        i=n-j
        c(i)=(c(i)-d(i)*c(i+1))/b(i)
      enddo

      b(n)=(y(n)-y(igap))/d(igap)+d(igap)*(c(igap)+2.0*c(n))
      do i=1,igap
        b(i)=(y(i+1)-y(i))/d(i)-d(i)*(c(i+1)+2.0*c(i))
        d(i)=(c(i+1)-c(i))/d(i)
        c(i)=3.0*c(i)
      enddo
      c(n)=3.0*c(n)
      d(n)=d(n-1)
      return
      end 
c----------------------------------------------------------
      subroutine fspline(u,valu,x,y,b,c,d,n)
      implicit real*8 (a-h,o-z)
      dimension x(n),y(n),b(n),c(n),d(n)
 
      if(u.le.x(1))then
        valu=y(1)
        return
      endif
 
      if(u.ge.x(n))then
        valu=y(n)
        return
      endif

      i=1
      j=n+1
      do while(j.gt.i+1)
        k=(i+j)/2
        if(u.lt.x(k))then
          j=k
        else
          i=k
        endif
      enddo

      dx=u-x(i)
      valu=y(i)+dx*(b(i)+dx*(c(i)+dx*d(i)))

      return
      end 
c------------------------------------------------------------
      subroutine simp(g,h,m,valu)
c-----INTEGRATE FUNCTION g(z) using (m) equispaced points with step h
      implicit real*8 (a-h,o-z)
      dimension g(m)
      n=m-1
      sum1=0.d0
      sum2=0.d0
      do i=2,n,2
       sum1=sum1+g(i)
      enddo
      do j=3,n-1,2
       sum2=sum2+g(j)
      enddo
      valu=(h/3.d0)*(g(1)+4.d0*sum1+2.d0*sum2+g(n+1))
      return
      end subroutine  
c---------------------------------------------------------------
      subroutine inpolqd(u,valu,x,y,n)
      implicit real*8 (a-h,o-z)
      dimension x(n),y(n),b(n),c(n),d(n)
 
      if(u.le.x(1))then
        valu=y(1)
        return
      endif
 
      if(u.ge.x(n))then
        valu=y(n)
        return
      endif

            def=100.0
            do i=1,n
             if(abs(u-x(i)).lt.def)then
              ic=i
              def=abs(u-x(i))
             endif
            enddo
            if(ic.eq.1)then
             i0=1
             i1=2
             i2=3
            elseif(ic.eq.n)then
             i0=n-2
             i1=n-1
             i2=n
            else
             i0=ic-1
             i1=ic
             i2=ic+1 
            endif 
            al0=(u-x(i1))*(u-x(i2))/((x(i0)-x(i1))*(x(i0)-x(i2)))
            al1=(u-x(i0))*(u-x(i2))/((x(i1)-x(i0))*(x(i1)-x(i2)))
            al2=(u-x(i0))*(u-x(i1))/((x(i2)-x(i0))*(x(i2)-x(i1)))
            valu=y(i0)*al0+y(i1)*al1+y(i2)*al2 
 10         continue       
      return
      end 
   
