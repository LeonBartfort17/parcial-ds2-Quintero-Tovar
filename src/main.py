from pymongo import *; from modelo import mesa_de_ayuda as mda

def Protocolo_Datos_Mesa():
    #
    cli=MongoClient("mongodb://localhost:27017/")
    if cli != None:
      BaseDatos = cli["MatriculaApp"]
      if BaseDatos is not None:
          tk_lst=list(BaseDatos.tickets.find()) 
          if len(tk_lst) != 0:
             ag=BaseDatos.agentes.find_one({"en_turno":True})
             if ag!=None:
                if "ticket_hora" in ag:
                   muVal = ag["ticket_hora"] 
                   objetosM = mda(tk_lst,muVal)
                   L = objM.tasa_de_llegadas()
                   if L>=0:
                       r,Lq,Wq=objM.metricas_mm1(L)
                       Esp_Sim = objM.simular() 
                       aux1,aux2,wq_9_5 = objM.metricas_mm1(9.5)

                       s=0; c=0 
                       for e in Esp_Sim:
                         s+=e; c+=1
                       if c>0:
                           avgE=s/c
                           print("Lambda: %s" % str(round(L,2)))
                           print("Wq teorico (min): %s" % str(round(Wq*60,2)))
                           print("Espera simulada (min): %s" % str(round(avgE,2)))
                           print("Wq con 9.5 (min): %s" % str(round(wq_9_5*60,2)))
                           objetosM.graficar() 
Protocolo_Datos_Mesa()