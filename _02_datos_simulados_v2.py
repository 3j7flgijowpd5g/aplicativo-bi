import pandas as pd
import numpy as np
import random
import faker

# Instanciar generador de datos falsos
fake = faker.Faker()

# Configuración dinámica
NUM_ROWS = 500  # Número de filas a generar

# Semillas para reproducibilidad
np.random.seed(42)
random.seed(42)

# Generación de datos simulados
data = {
    "Orden": [i + 1 for i in range(NUM_ROWS)],
    "DNI": [str(fake.unique.random_int(min=10000000, max=99999999)) for _ in range(NUM_ROWS)],
    "Apellido_Paterno": [fake.last_name() for _ in range(NUM_ROWS)],
    "Apellido_Materno": [fake.last_name() for _ in range(NUM_ROWS)],
    "Nombres": [fake.first_name() for _ in range(NUM_ROWS)],
    "Edad": [random.randint(18, 80) for _ in range(NUM_ROWS)],
    "Direccion": [fake.address() for _ in range(NUM_ROWS)],
    "Celular": [f"+51 9{random.randint(10000000, 99999999)}" for _ in range(NUM_ROWS)],
    "Correo": [fake.email() for _ in range(NUM_ROWS)],
    "Ingreso_Anual": [random.randint(10000, 50000) for _ in range(NUM_ROWS)],
    "Genero": [random.choice(["Masculino", "Femenino"]) for _ in range(NUM_ROWS)],
    "Estado_Civil": [random.choice(["Soltero", "Casado", "Viudo", "Divorciado"]) for _ in range(NUM_ROWS)],
    "Nivel_Educativo": [random.choice(["Primaria", "Secundaria", "Técnico", "Universitario"]) for _ in range(NUM_ROWS)],
    "Ocupacion": [fake.job() for _ in range(NUM_ROWS)],
    "Fecha_Nacimiento": [fake.date_of_birth(minimum_age=18, maximum_age=80) for _ in range(NUM_ROWS)],
    "Nacionalidad": [fake.country() for _ in range(NUM_ROWS)],
    "Provincia": [fake.state() for _ in range(NUM_ROWS)],
    "Distrito": [fake.city() for _ in range(NUM_ROWS)],
    "Centro_Medico": [random.choice(["Hospital Central", "Clínica Salud", "Centro Médico Familiar"]) for _ in range(NUM_ROWS)],
    "Tipo_Seguro": [random.choice(["Privado", "Público", "Mixto"]) for _ in range(NUM_ROWS)],
    "Fecha_Registro": [fake.date_this_decade() for _ in range(NUM_ROWS)],
    "Historial_Medico": [random.choice(["Diabetes", "Hipertensión", "Cardiopatía", "Ninguno"]) for _ in range(NUM_ROWS)],
    "Medicamentos_Recetados": [random.randint(0, 5) for _ in range(NUM_ROWS)],
    "Citas_Anuales": [random.randint(1, 10) for _ in range(NUM_ROWS)],
    "Peso": [round(random.uniform(50.0, 100.0), 1) for _ in range(NUM_ROWS)],
    "Altura": [round(random.uniform(1.5, 2.0), 2) for _ in range(NUM_ROWS)],
    "IMC": [round(random.uniform(18.5, 40.0), 1) for _ in range(NUM_ROWS)],
    "Presion_Arterial": [f"{random.randint(90, 140)}/{random.randint(60, 90)}" for _ in range(NUM_ROWS)],
    "Frecuencia_Cardiaca": [random.randint(60, 100) for _ in range(NUM_ROWS)],
    "Frecuencia_Respiratoria": [random.randint(12, 20) for _ in range(NUM_ROWS)],
    "Temperatura": [round(random.uniform(36.0, 39.0), 1) for _ in range(NUM_ROWS)],
    "Grupo_Sanguineo": [random.choice(["A", "B", "AB", "O"]) for _ in range(NUM_ROWS)],
    "Factor_RH": [random.choice(["+", "-"]) for _ in range(NUM_ROWS)],
    "Alergias": [random.choice(["Ninguna", "Polen", "Medicamentos", "Alimentos"]) for _ in range(NUM_ROWS)],
    "Cirugias": [random.randint(0, 3) for _ in range(NUM_ROWS)],
    "Vacunas_Al_Dia": [random.choice(["Sí", "No"]) for _ in range(NUM_ROWS)],
    "Pruebas_Laboratorio": [random.randint(0, 10) for _ in range(NUM_ROWS)],
    "Ultima_Visita": [fake.date_this_year() for _ in range(NUM_ROWS)],
    "Dias_Hospitalizacion": [random.randint(0, 15) for _ in range(NUM_ROWS)],
    "Horas_Ejercicio_Semanal": [random.randint(0, 10) for _ in range(NUM_ROWS)],
    "Consumo_Alcohol": [random.choice(["Ninguno", "Ocasional", "Frecuente"]) for _ in range(NUM_ROWS)],
    "Tabaquismo": [random.choice(["Sí", "No"]) for _ in range(NUM_ROWS)],
    "Dieta_Saludable": [random.choice(["Sí", "No"]) for _ in range(NUM_ROWS)],
    "Nivel_Estres": [random.randint(1, 10) for _ in range(NUM_ROWS)],
    "Nivel_Satisfaccion": [random.randint(1, 10) for _ in range(NUM_ROWS)],
    "Costo_Citas_Anuales": [random.randint(200, 2000) for _ in range(NUM_ROWS)],
    "Costo_Tratamiento": [random.randint(1000, 10000) for _ in range(NUM_ROWS)],
    "Costo_Medicamentos": [random.randint(100, 5000) for _ in range(NUM_ROWS)],
    "Satisfaccion_Servicio": [random.randint(1, 5) for _ in range(NUM_ROWS)],
}

# Crear un DataFrame
df_simulated = pd.DataFrame(data)

# Guardar el DataFrame en un archivo CSV
output_file = "_00_aplic_v3_Ejemplo_Data_Realista_53_Columnas.csv"

df_simulated.to_csv(output_file, index=False)

print(f"Archivo '{output_file}' creado con éxito.")
