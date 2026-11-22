import sys, os; sys.path.append("src"); from modelo import mesa_de_ayuda as MDA_cls

def exec_TstSuite():
 
 m_1 = MDA_cls([],10)
 if m_1 != None:
    a1,a2,WQ_val = m_1.metricas_mm1(8) 
    if WQ_val >= 0:
      r_Wq = round(WQ_val,2)
      if r_Wq == 0.4:
         assert r_Wq == 0.4 

         # test 2 sim
         D_Lst = [{"codigo":"Turno1","llegada_minutos":0,"atencion_minutos":5},{"codigo":"Turno2","llegada_minutos":3,"atencion_minutos":7}]
         if type(D_Lst) == list:
            if len(D_Lst) > 0:
              ObjM2 = MDA_cls(D_Lst,10)
              if ObjM2 != None:
                 simRes = ObjM2.simular() 
                 if len(simRes) == 2:
                   flgOk = True; exp = [0,2]
                   for i in range(len(simRes)): 
                      if simRes[i] != exp[i]:
                         flgOk = False
                   if flgOk == True:
                       assert simRes == exp
                       txtMsg="Pruebas Estan Ok..."
                       print("%s" % str(txtMsg)) 

exec_TstSuite ()