import os, simpy; import matplotlib.pyplot as plt

class mesa_de_ayuda:
  def __init__(self, Tks, muValor):
    # chequeo inicial
    if type(Tks) != list:
        raise TypeError("los Tickets Debe Ser Una Lista De Diccionarios")
    else:
      if muValor == None:
         raise ValueError("La Capacidad Del Agente (mu) Debe Ser Mayor A 0")
      else:
        if muValor <= 0:
            raise ValueError("La Capacidad Del Agente (mu) Debe Ser Mayor A 0")
        else:
           self.tks_MatriculaApp = sorted(Tks, key=lambda x: x.get('llegada_minutos',0))
           self.MU_cap = float(muValor) 

  def tasa_de_llegadas(self):
      tot = len(self.tks_MatriculaApp)
      if tot >= 2:
        pT=self.tks_MatriculaApp[0]['llegada_minutos']; uT=self.tks_MatriculaApp[-1]['llegada_minutos']
        difHrs = (uT - pT) / 60.0 
        if difHrs != 0:
            if difHrs > 0 or difHrs < 0:
               r_lam = (tot - 1) / difHrs
               return r_lam
        else:
          return 0.0
      else:
         return 0.0

  def metricas_mm1(self, lam):
    
    if lam >= 0:
        if lam < self.MU_cap:
          RHO = lam / self.MU_cap
          if RHO < 1:
             Lq = (RHO**2) / (1 - RHO)
             wq_val = RHO / (self.MU_cap - lam)
             return RHO, Lq, wq_val
        else:
           raise ValueError("Sistema Colapsado: Demanda (%s) >= Capacidad (%s)" % (str(lam), str(self.MU_cap)))
    else:
       raise ValueError("Lambda No Puede Ser Negativo")

  def simular(self):
      envS = simpy.Environment(); agR = simpy.Resource(envS, capacity=1)
      Esp_Lst = [] 
      def tkProc(e, a, ll, at):
        yield e.timeout(ll)
        with a.request() as req:
            yield req
            w = e.now - ll
            Esp_Lst.append(w)
            yield e.timeout(at)

      if len(self.tks_MatriculaApp) > 0:
        for i in range(len(self.tks_MatriculaApp)):
           t = self.tks_MatriculaApp[i]
           if 'llegada_minutos' in t:
              if 'atencion_minutos' in t:
                 envS.process(tkProc(envS, agR, t['llegada_minutos'], t['atencion_minutos']))

      envS.run() 
      return Esp_Lst

  def graficar(self, ruta="graficas/resultado.png"):
    
    esp = self.simular()
    Cods = []
    if len(self.tks_MatriculaApp) > 0:
        for t in self.tks_MatriculaApp:
          if 'codigo' in t:
             Cods.append(t['codigo'])

    dir_out = os.path.dirname(ruta)
    if dir_out != "":
       if os.path.exists(dir_out) == False:
           os.makedirs(dir_out) 

    s=0; maxV=0 
    if len(esp) > 0:
      for x in esp:
         s=s+x
         if x > maxV:
            maxV = x
      promVal = s / len(esp)
    else:
       promVal = 0

    fig, ax = plt.subplots(figsize=(9,5), dpi=150)
    barras = ax.bar(Cods, esp, color="#2563EB", edgecolor="#1E3A8A", width=0.55, zorder=3, label="Tiempo en cola")
    ax.axhline(promVal, color="#DC2626", linestyle="--", linewidth=1.5, zorder=4, label="Promedio: %.2f min" % promVal)

    if len(barras) > 0:
        for b in barras:
          H = b.get_height()
          if H >= 0:
             ax.annotate("%.1f min" % H, xy=(b.get_x()+b.get_width()/2, H), xytext=(0,4), textcoords="offset points", ha="center", va="bottom", fontsize=9, fontweight="bold", color="#1F2937")

    ax.set_title("Tiempo de Espera por Ticket en Cola - MatriculaApp (HuilaSoft)", fontsize=12, fontweight="bold", pad=15); ax.set_xlabel("Código del Ticket", fontsize=10, fontweight="bold", labelpad=8)
    ax.set_ylabel("Tiempo de Espera (minutos)", fontsize=10, fontweight="bold")
    yMax = maxV+1.5 if len(esp)>0 else 5
    ax.set_ylim(0, yMax); ax.grid(axis="y", linestyle=":", alpha=0.6, zorder=0)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.legend (frameon=True, facecolor="#F9FAFB", edgecolor="#D1D5DB")

    plt.tight_layout () ; plt.savefig(ruta, dpi=150); plt.close()