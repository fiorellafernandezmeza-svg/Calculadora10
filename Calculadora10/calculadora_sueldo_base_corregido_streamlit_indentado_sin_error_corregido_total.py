1| 
2| import streamlit as st
3| from datetime import datetime, timedelta
4| import calendar
5| from datetime import date
6| 
7| # --- 🔹 Feriados oficiales Perú 2026 ---
8| FERIADOS_PERU_2026 = [
9|     "2026-01-01",  # Año Nuevo
10|     "2026-04-02",  # Jueves Santo
11|     "2026-04-03",  # Viernes Santo
12|     "2026-05-01",  # Día del Trabajo
13|     "2026-06-07",  # Nuevo
14|     "2026-06-29",  # Nuevo
15|     "2026-07-23",  # Independencia del Perú
16|     "2026-07-28",  # Independencia del Perú
17|     "2026-07-29",  # Fiestas Patrias
18|     "2026-08-06",  # Nuevo
19|     "2026-08-30",  # Santa Rosa de Lima
20|     "2026-10-08",  # Combate de Angamos
21|     "2026-11-01",  # Todos los Santos
22|     "2026-12-08",  # Inmaculada Concepción
23|     "2026-12-09",  # Batalla de Ayacucho
24|     "2026-12-25",  # Navidad
25| ]
26| 
27| def es_feriado(fecha):
28|     """Verifica si una fecha es feriado en Perú."""
29|     return fecha.strftime("%Y-%m-%d") in FERIADOS_PERU_2026
30| 
31| # Datos de AFP combinados
32| afp_dict = {
33|     "HABITAT FLUJO": 0.1284,
34|     "INTEGRA FLUJO": 0.1292,
35|     "PRIMA FLUJO": 0.1297,
36|     "PROFUTURO FLUJO": 0.1306,
37|     "AFP MIXTA": 0.1137,
38|     "ONP": 0.13,
39| }
40| 
41| # Función para calcular horas trabajadas descontando 45 minutos de refrigerio
42| def calcular_horas_trabajadas(hora_ingreso, hora_salida):
43|     if hora_salida < hora_ingreso:
44|         hora_salida += timedelta(days=1)
45|     horas_trabajadas = (hora_salida - hora_ingreso).total_seconds() / 3600 - 0.75
46|     return max(horas_trabajadas, 0)
47| 
48| # Función para calcular tarifas
49| def calcular_tarifas(sueldo_base, asignacion_familiar, dias_mes, afp_descuento, tipo_trabajador, turno):
50|     if tipo_trabajador == "Obrero" and turno == "Día":
51|         tipo_trabajador = "Empleado"
52|     if turno == "Noche - Rotativo":
53|         sueldo_base = max(sueldo_base, 1525.50)
54|     
55| def calcular_tarifas(sueldo_base, asignacion_familiar, dias_mes, afp_descuento, tipo_trabajador, turno):
56| # Ajustes especiales por tipo de trabajador y turno
57|     if tipo_trabajador == "Obrero" and turno == "Día":
58|         tipo_trabajador = "Empleado"
59|     if turno == "Noche - Rotativo":
60|         sueldo_base = max(sueldo_base, 1525.50)
61|     
62|     # --- 1️⃣ Cálculo de tarifa ordinaria (igual que antes) ---
63|     base_diaria_ordinaria = (sueldo_base + asignacion_familiar) / dias_mes
64|     tarifa_hora = (base_diaria_ordinaria / 8) * (1 - afp_descuento)
65| 
66|     # --- 2️⃣ Cálculo de base para horas extra (siempre sobre 30 días) ---
67|     base_diaria_extra = (sueldo_base + asignacion_familiar) / 30
68|     tarifa_base_extra = (base_diaria_extra / 8) * (1 - afp_descuento)
69| 
70|     # --- 3️⃣ Cálculo de tarifas de horas extra ---
71|     if turno == "Noche - Rotativo":
72|         extra_25 = tarifa_base_extra * (1.25 if tipo_trabajador == "Empleado" else 1.40)
73|         extra_35 = tarifa_base_extra * (1.35 if tipo_trabajador == "Empleado" else 1.50)
74|     else:
75|         extra_25 = tarifa_base_extra * 1.25
76|         extra_35 = tarifa_base_extra * 1.35
77| 
78|     return tarifa_hora, extra_25, extra_35
79| 
80|     if turno == "Noche - Rotativo":
81|         extra_25 = tarifa_hora * (1.25 if tipo_trabajador == "Empleado" else 1.40)
82|         extra_35 = tarifa_hora * (1.35 if tipo_trabajador == "Empleado" else 1.50)
83|     else:
84|         extra_25 = tarifa_hora * 1.25
85|         extra_35 = tarifa_hora * 1.35
86|     return tarifa_hora, extra_25, extra_35
87| 
88| # Función para calcular netos
89| def calcular_netos(horas, tarifa_hora, tarifa_25, tarifa_35):
90|     h_ordinarias = min(horas, 8)
91|     h_extra_25 = min(max(horas - 8, 0), 2)
92|     h_extra_35 = max(horas - 10, 0)
93|     neto_ordinario = h_ordinarias * tarifa_hora
94|     neto_25 = h_extra_25 * tarifa_25
95|     neto_35 = h_extra_35 * tarifa_35
96|     total = neto_ordinario + neto_25 + neto_35
97|     return neto_ordinario, neto_25, neto_35, total
98| 
99| # Interfaz de usuario
100| st.title("Calculadora de Sueldo")
101| 
102| st.warning("""
103| ⚠️ **Importante:**  
104| El cálculo mostrado es solo una guía. 
105| **Incluye únicamente el descuento de AFP u ONP.** No considera otros descuentos. 
106| """)
107| 
108| tipo_trabajador = st.selectbox("Tipo de trabajador", ["Empleado", "Obrero"])
109| turno = st.selectbox("Turno", ["Día", "Rotativo"])
110| sueldo_base = st.number_input("Sueldo base", min_value=0.0)
111| asignacion_familiar = st.number_input("Asignación familiar", min_value=0.0)
112| dias_mes = st.number_input("Días del mes", min_value=1, max_value=31, value=30)
113| afp = st.selectbox("Tipo de AFP", list(afp_dict.keys()))
114| afp_descuento = afp_dict[afp]
115| 
116| # --- 💼 Cálculo directo para Empleado ---
117| if tipo_trabajador == "Empleado":
118|     st.markdown("### 👔 Cálculo de Pago Mensual - Empleado")
119| 
120|     # Ingreso bruto (básico + asignación familiar si aplica)
121|     ingreso_bruto = sueldo_base + asignacion_familiar
122|     st.write(f"**Ingreso bruto mensual:** S/ {ingreso_bruto:.2f}")
123| 
124|     # Tipo de aporte: AFP u ONP
125|     tipo_aporte = "AFP" if afp != "ONP" else "ONP"
126|     porcentaje_descuento = afp_descuento  # Usa el descuento seleccionado del combo
127| 
128|     # Cálculo del descuento previsional
129|     descuento = ingreso_bruto * porcentaje_descuento
130|     st.write(f"**Descuento {tipo_aporte}:** S/ {descuento:.2f}")
131| 
132|     # Pago neto
133|     pago_neto = ingreso_bruto - descuento
134|     st.success(f"💰 **Pago neto del mes:** S/ {pago_neto:.2f}")
135| 
136|     # Información adicional
137|     st.markdown("""
138|     > 🔹 Este cálculo considera una jornada completa de 8 horas diarias.  
139|     > 🔹 No incluye descuentos de 5ta categoría, préstamos, aportes de comedor ni otros.  
140|     > 🔹 Solo se aplica el descuento de AFP u ONP según el tipo seleccionado.
141|     """)
142| # --- 🧱 Si no es empleado, se ejecuta la parte de obreros (turnos y cálculo por día) ---
143| elif tipo_trabajador == "Obrero":
144| 
145|     if turno == "Día":
146|         st.subheader("Turno Día")
147|         col1, col2, col3 = st.columns(3)
148|         with col1:
149|             hora_ingreso_dia = st.time_input("Hora de ingreso (Día - Rotativo)", value=datetime.strptime("08:00", "%H:%M").time())
150|         with col2:
151|             hora_salida_dia = st.time_input("Hora de salida (Día - Rotativo)", value=datetime.strptime("17:00", "%H:%M").time())
152|         with col3:
153|             horas_dia = calcular_horas_trabajadas(
154|                 datetime.combine(datetime.today(), hora_ingreso_dia),
155|                 datetime.combine(datetime.today(), hora_salida_dia)
156|             )
157|             st.metric("Horas trabajadas (Día)", f"{horas_dia:.2f}")
158| 
159|         tarifa_dia, extra25_dia, extra35_dia = calcular_tarifas(
160|             sueldo_base, asignacion_familiar, dias_mes, afp_descuento, tipo_trabajador, "Día"
161|         )
162|         neto_dia, neto25_dia, neto35_dia, total_dia = calcular_netos(
163|             horas_dia, tarifa_dia, extra25_dia, extra35_dia
164|         )
165|         st.write(f"Tarifa hora ordinaria: S/ {tarifa_dia:.2f}")
166|         _ = f"Tarifa hora extra 25%: S/ {extra25_dia:.2f}"
167|         _ = f"Tarifa hora extra 35%: S/ {extra35_dia:.2f}"
168|         st.success(f"Neto por 8 horas: S/ {neto_dia:.2f}")
169|         _ = f"Neto por horas extra 25%: S/ {neto25_dia:.2f}"
170|         _ = f"Neto por horas extra 35%: S/ {neto35_dia:.2f}"
171|         st.success(f"Total turno día: S/ {total_dia:.2f}")
172| 
173|         # --- 📆 Nueva sección de información de pago para turno Día ---
174|         st.markdown("### 🗓️ Información de pago")
175|         tipo_pago = st.selectbox("Tipo de pago", ["Semanal", "Quincenal"])
176|         mes_pago = st.selectbox("Mes de pago", [calendar.month_name[i] for i in range(1, 13)])
177| 
178|         # Función auxiliar para nombre del día
179|         def nombre_dia(fecha):
180|             dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
181|             return dias[fecha.weekday()]
182| 
183|         year = 2026
184|         mes_num = list(calendar.month_name).index(mes_pago)
185|         dias_mes = calendar.monthrange(year, mes_num)[1]
186| 
187|         # --- 🔹 Cálculo semanal ---
188|         if tipo_pago == "Semanal":
189|             st.markdown("### 📅 Cuadro semanal (Turno Día)")
190|             pagos = []
191|             pago_semana = 0
192|             dias_semana = []
193| 
194|             for dia in range(1, dias_mes + 1):
195|                 fecha = date(year, mes_num, dia)
196|                 nombre = nombre_dia(fecha)
197| 
198|                 # Determinar pago diario
199|                 if es_feriado(fecha) or nombre == "domingo":
200|                     pago = neto_dia  # Pago por 8 horas turno día
201|                     feriado_flag = "🟥" if es_feriado(fecha) else ""
202|                 else:
203|                     pago = total_dia
204|                     feriado_flag = ""
205| 
206|                 pagos.append(pago)
207|                 dias_semana.append((dia, nombre, pago, feriado_flag))
208|                 pago_semana += pago
209| 
210|                 # Cierre de semana (viernes o fin de mes)
211|                 if nombre == "viernes" or dia == dias_mes:
212|                     st.markdown(f"**Semana que termina el viernes {dia:02d} de {mes_pago}:**")
213|                     for d, n, p, f in dias_semana:
214|                         st.write(f"{d:02d} | {n.capitalize()} {f} | S/ {p:.2f}")
215|                     st.success(f"**Total semana ({dias_semana[0][0]:02d}–{dia:02d}): S/ {pago_semana:.2f}**")
216| 
217|                     pago_semana = 0
218|                     dias_semana = []
219| 
220|             total_mes = sum(pagos)
221|             st.markdown("---")
222|             st.success(f"💰 **Total mensual ({mes_pago}): S/ {total_mes:.2f}**")
223| 
224|         # --- 🔹 Cálculo quincenal ---
225|         elif tipo_pago == "Quincenal":
226|             st.markdown("### 📅 Cuadro quincenal (Turno Día)")
227|             pagos = []
228|             st.write("**Día | Nombre | Pago diario**")
229| 
230|             # Primera quincena
231|             for dia in range(1, 16):
232|                 fecha = date(year, mes_num, dia)
233|                 nombre = nombre_dia(fecha)
234| 
235|                 if es_feriado(fecha) or nombre == "domingo":
236|                     pago = neto_dia
237|                     feriado_flag = "🟥" if es_feriado(fecha) else ""
238|                 else:
239|                     pago = total_dia
240|                     feriado_flag = ""
241| 
242|                 pagos.append(pago)
243|                 st.write(f"{dia:02d} | {nombre.capitalize()} {feriado_flag} | S/ {pago:.2f}")
244| 
245|             total_q1 = sum(pagos)
246|             st.success(f"**Total primera quincena: S/ {total_q1:.2f}**")
247| 
248|             # Segunda quincena
249|             pagos2 = []
250|             st.write("---")
251|             st.write("**Segunda quincena**")
252| 
253|             for dia in range(16, dias_mes + 1):
254|                 fecha = date(year, mes_num, dia)
255|                 nombre = nombre_dia(fecha)
256| 
257|                 if es_feriado(fecha) or nombre == "domingo":
258|                     pago = neto_dia
259|                     feriado_flag = "🟥" if es_feriado(fecha) else ""
260|                 else:
261|                     pago = total_dia
262|                     feriado_flag = ""
263| 
264|                 pagos2.append(pago)
265|                 st.write(f"{dia:02d} | {nombre.capitalize()} {feriado_flag} | S/ {pago:.2f}")
266| 
267|             total_q2 = sum(pagos2)
268|             st.success(f"**Total segunda quincena: S/ {total_q2:.2f}**")
269| 
270|             total_mes = total_q1 + total_q2
271|             st.markdown("---")
272|             st.success(f"💰 **Total mensual ({mes_pago}): S/ {total_mes:.2f}**")
273| 
274|     elif turno == "Rotativo":
275|         col_dia, col_noche = st.columns(2)
276| 
277|         with col_dia:
278|             st.subheader("Turno Día (Rotativo)")
279|             c1, c2, c3 = st.columns(3)
280|             with c1:
281|                 hora_ingreso_dia = st.time_input("Hora de ingreso", key="ingreso_dia", value=datetime.strptime("08:00", "%H:%M").time())
282|             with c2:
283|                 hora_salida_dia = st.time_input("Hora de salida", key="salida_dia", value=datetime.strptime("17:00", "%H:%M").time())
284|             with c3:
285|                 horas_dia = calcular_horas_trabajadas(
286|                     datetime.combine(datetime.today(), hora_ingreso_dia),
287|                     datetime.combine(datetime.today(), hora_salida_dia)
288|                 )
289|                 st.metric("Horas trabajadas (Día)", f"{horas_dia:.2f}")
290|             tarifa_dia, extra25_dia, extra35_dia = calcular_tarifas(
291|                 sueldo_base, asignacion_familiar, dias_mes, afp_descuento, tipo_trabajador, "Día"
292|             )
293|             neto_dia, neto25_dia, neto35_dia, total_dia = calcular_netos(
294|                 horas_dia, tarifa_dia, extra25_dia, extra35_dia
295|             )
296|             st.write(f"Tarifa hora ordinaria: S/ {tarifa_dia:.2f}")
297|             _ = f"Tarifa hora extra 25%: S/ {extra25_dia:.2f}"
298|             _ = f"Tarifa hora extra 35%: S/ {extra35_dia:.2f}"
299|             st.success(f"Neto por 8 horas: S/ {neto_dia:.2f}")
300|             _ = f"Neto por horas extra 35%: S/ {neto35_dia:.2f}"
301|             _ = f"Neto por horas extra 35%: S/ {extra35_dia:.2f}"
302|             st.success(f"Total turno día: S/ {total_dia:.2f}")
303| 
304|         with col_noche:
305|             st.subheader("Turno Noche (Rotativo)")
306|             c1, c2, c3 = st.columns(3)
307|             with c1:
308|                 hora_ingreso_noche = st.time_input("Hora de ingreso", key="ingreso_noche", value=datetime.strptime("22:00", "%H:%M").time())
309|             with c2:
310|                 hora_salida_noche = st.time_input("Hora de salida", key="salida_noche", value=datetime.strptime("07:00", "%H:%M").time())
311|             with c3:
312|                 horas_noche = calcular_horas_trabajadas(
313|                     datetime.combine(datetime.today(), hora_ingreso_noche),
314|                     datetime.combine(datetime.today(), hora_salida_noche)
315|                 )
316|                 st.metric("Horas trabajadas (Noche)", f"{horas_noche:.2f}")
317|             tarifa_noche, extra25_noche, extra35_noche = calcular_tarifas(
318|                 sueldo_base, asignacion_familiar, dias_mes, afp_descuento, tipo_trabajador, "Noche - Rotativo"
319|             )
320|             neto_noche, neto25_noche, neto35_noche, total_noche = calcular_netos(
321|                 horas_noche, tarifa_noche, extra25_noche, extra35_noche
322|             )
323|             st.write(f"Tarifa hora ordinaria: S/ {tarifa_noche:.2f}")
324|             _ = f"Tarifa hora extra 25%: S/ {extra25_noche:.2f}"
325|             _ = f"Tarifa hora extra 35%: S/ {extra35_noche:.2f}"
326|             st.success(f"Neto por 8 horas: S/ {neto_noche:.2f}")
327|             _ = f"Neto por horas extra 25%: S/ {neto25_noche:.2f}"
328|             _ = f"Neto por horas extra 35%: S/ {neto35_noche:.2f}"
329|             st.success(f"Total turno noche: S/ {total_noche:.2f}")
330| 
331|         # Nuevas opciones de pago
332|         st.markdown("### 🗓️ Información de pago")
333|         tipo_pago = st.selectbox("Tipo de pago", ["Semanal", "Quincenal"])
334|         turno_inicio_pago = st.selectbox("Turno del primer día de pago", ["Día", "Noche"])
335|         mes_pago = st.selectbox("Mes de pago", [calendar.month_name[i] for i in range(1, 13)])
336| 
337|         # Función para obtener nombre del día
338|         def nombre_dia(fecha):
339|             dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
340|             return dias[fecha.weekday()]
341| 
342|         # Mostrar cuadro según selección
343|         
344|         if tipo_pago == "Semanal":
345|             st.markdown("### 📅 Calculo semanal (mes completo)")
346|             year = 2026
347|             mes_num = list(calendar.month_name).index(mes_pago)
348|             dias_mes = calendar.monthrange(year, mes_num)[1]
349|             
350|             pagos = []
351|             turno_semana = turno_inicio_pago
352|             pago_semana = 0
353|             dias_semana = []
354|             
355|             st.write("**Día | Nombre | Turno | Pago diario**")
356|             
357|             for dia in range(1, dias_mes + 1):
358|                 fecha = date(year, mes_num, dia)
359|                 nombre = nombre_dia(fecha)
360| 
361|                 # 🔁 Cambio de turno cada lunes (excepto el primer día)
362|                 if nombre == "lunes" and dia != 1:
363|                     turno_semana = "Noche" if turno_semana == "Día" else "Día"
364| 
365|                 # 💰 Cálculo del pago diario
366|                 if es_feriado(fecha):
367|                     pago = neto_dia  # feriado se paga como día neto (8 horas turno día)
368|                     feriado_flag = "🟥"
369|                 else:
370|                     if nombre == "domingo":
371|                         pago = neto_dia if turno_semana == "Día" else neto_noche
372|                         feriado_flag = ""
373|                     else:
374|                         pago = total_dia if turno_semana == "Día" else total_noche
375|                         feriado_flag = ""
376| 
377|                 pagos.append(pago)
378|                 dias_semana.append((dia, nombre, turno_semana, pago, feriado_flag))
379|                 pago_semana += pago
380| 
381|                 # 📅 Cierre semanal cada viernes o fin de mes
382|                 if nombre == "viernes" or dia == dias_mes:
383|                  
384|                     st.markdown(f"**Semana que termina el viernes {dia:02d} de {mes_pago}:**")
385|                     for d, n, t, p, f in dias_semana:
386|                         st.write(f"{d:02d} | {n.capitalize()} | {t} | {f} S/ {p:.2f}")
387|                     st.success(f"**Total semana ({dias_semana[0][0]:02d}–{dia:02d}): S/ {pago_semana:.2f}**")
388| 
389|                     pago_semana = 0
390|                     dias_semana = []
391| 
392|             total_mes = sum(pagos)
393|             st.markdown("---")
394|             st.success(f"💰 **Total mensual ({mes_pago}): S/ {total_mes:.2f}**")
395| 
396|         elif tipo_pago == "Quincenal":
397|             st.markdown("### 📅 Cálculo quincenal (mes completo)")
398| 
399|             year = 2026
400|             mes_num = list(calendar.month_name).index(mes_pago)
401|             dias_en_mes = calendar.monthrange(year, mes_num)[1]
402| 
403|             pagos = []
404|             st.write("**Día | Nombre | Pago diario**")
405|             turno_semana = turno_inicio_pago
406| 
407|             total_quincena_1 = 0
408|             total_quincena_2 = 0
409| 
410|             for dia in range(1, dias_en_mes + 1):
411|                 fecha = date(year, mes_num, dia)
412|                 nombre = nombre_dia(fecha)
413| 
414|                 # 🔁 Cambio de turno cada lunes (excepto el primer día)
415|                 if nombre == "lunes" and dia != 1:
416|                     turno_semana = "Noche" if turno_semana == "Día" else "Día"
417| 
418|                 # 💰 Feriado: pago fijo día
419|                 if es_feriado(fecha):
420|                     pago = neto_dia
421|                     feriado_flag = "🟥"
422|                 else:
423|                     # Domingo paga neto según turno actual
424|                     if nombre == "domingo":
425|                         pago = neto_dia if turno_semana == "Día" else neto_noche
426|                         feriado_flag = ""
427|                     else:
428|                         pago = total_dia if turno_semana == "Día" else total_noche
429|                         feriado_flag = ""
430| 
431|                 pagos.append(pago)
432|                 st.write(f"{dia:02d} | {nombre.capitalize()} {feriado_flag} | S/ {pago:.2f}")
433| 
434|                 # 🔹 Suma automática al final de cada quincena
435|                 if dia == 15:
436|                     total_quincena_1 = sum(pagos)
437|                     st.success(f"**🟦 Total primera quincena: S/ {total_quincena_1:.2f}**")
438|                     st.markdown("---")
439| 
440|                 if dia == dias_en_mes:
441|                     total_quincena_2 = sum(pagos[15:])  # del 16 en adelante
442|                     st.success(f"**🟩 Total segunda quincena: S/ {total_quincena_2:.2f}**")
443|                     st.markdown("---")
444| 
445|             # 🔸 Total general del mes
446|             total_mes = total_quincena_1 + total_quincena_2
447|             st.info(f"💰 **Total mes completo: S/ {total_mes:.2f}**")
448| 
449|             # Información adicional
450|             st.markdown("""
451|             > 🔹 Este cálculo considera una jornada con horas extras, segun el horario seleccionado.  
452|             > 🔹 No incluye descuentos de 5ta categoría, préstamos, aportes de comedor ni otros.  
453|             > 🔹 Solo se aplica el descuento de AFP u ONP según el tipo seleccionado.
454|             """)
455| 
456|             
