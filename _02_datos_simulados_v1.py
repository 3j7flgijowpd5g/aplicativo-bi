import pandas as pd
import numpy as np
import random
import faker

# Instanciar generador de datos falsos
fake = faker.Faker()

# Crear un conjunto de datos simulados explícitamente
np.random.seed(42)
random.seed(42)

data = {
    "Orden": [i + 1 for i in range(200)],
    "DNI": [str(fake.unique.random_int(min=10000000, max=99999999)) for _ in range(200)],
    "Apellido_Paterno": [fake.last_name() for _ in range(200)],
    "Apellido_Materno": [fake.last_name() for _ in range(200)],
    "Nombres": [fake.first_name() for _ in range(200)],
    "Edad": [random.randint(18, 80) for _ in range(200)],
    "Direccion": [fake.address() for _ in range(200)],
    "Celular": [f"+51 9{random.randint(10000000, 99999999)}" for _ in range(200)],
    "Correo": [fake.email() for _ in range(200)],
    "Ingreso_Anual": [random.randint(10000, 50000) for _ in range(200)],
    "Genero": [random.choice(["Masculino", "Femenino"]) for _ in range(200)],
    "Estado_Civil": [random.choice(["Soltero", "Casado", "Viudo", "Divorciado"]) for _ in range(200)],
    "Nivel_Educativo": [random.choice(["Primaria", "Secundaria", "Técnico", "Universitario"]) for _ in range(200)],
    "Ocupacion": [fake.job() for _ in range(200)],
    "Fecha_Nacimiento": [fake.date_of_birth(minimum_age=18, maximum_age=80) for _ in range(200)],
    "Nacionalidad": [fake.country() for _ in range(200)],
    "Provincia": [fake.state() for _ in range(200)],
    "Distrito": [fake.city() for _ in range(200)],
    "Centro_Medico": [random.choice(["Hospital Central", "Clínica Salud", "Centro Médico Familiar"]) for _ in range(200)],
    "Tipo_Seguro": [random.choice(["Privado", "Público", "Mixto"]) for _ in range(200)],
    "Fecha_Registro": [fake.date_this_decade() for _ in range(200)],
    "Historial_Medico": [random.choice(["Diabetes", "Hipertensión", "Cardiopatía", "Ninguno"]) for _ in range(200)],
    "Medicamentos_Recetados": [random.randint(0, 5) for _ in range(200)],
    "Citas_Anuales": [random.randint(1, 10) for _ in range(200)],
    "Peso": [round(random.uniform(50.0, 100.0), 1) for _ in range(200)],
    "Altura": [round(random.uniform(1.5, 2.0), 2) for _ in range(200)],
    "IMC": [round(random.uniform(18.5, 40.0), 1) for _ in range(200)],
    "Presion_Arterial": [f"{random.randint(90, 140)}/{random.randint(60, 90)}" for _ in range(200)],
    "Frecuencia_Cardiaca": [random.randint(60, 100) for _ in range(200)],
    "Frecuencia_Respiratoria": [random.randint(12, 20) for _ in range(200)],
    "Temperatura": [round(random.uniform(36.0, 39.0), 1) for _ in range(200)],
    "Grupo_Sanguineo": [random.choice(["A", "B", "AB", "O"]) for _ in range(200)],
    "Factor_RH": [random.choice(["+", "-"]) for _ in range(200)],
    "Alergias": [random.choice(["Ninguna", "Polen", "Medicamentos", "Alimentos"]) for _ in range(200)],
    "Cirugias": [random.randint(0, 3) for _ in range(200)],
    "Vacunas_Al_Dia": [random.choice(["Sí", "No"]) for _ in range(200)],
    "Pruebas_Laboratorio": [random.randint(0, 10) for _ in range(200)],
    "Ultima_Visita": [fake.date_this_year() for _ in range(200)],
    "Dias_Hospitalizacion": [random.randint(0, 15) for _ in range(200)],
    "Horas_Ejercicio_Semanal": [random.randint(0, 10) for _ in range(200)],
    "Consumo_Alcohol": [random.choice(["Ninguno", "Ocasional", "Frecuente"]) for _ in range(200)],
    "Tabaquismo": [random.choice(["Sí", "No"]) for _ in range(200)],
    "Dieta_Saludable": [random.choice(["Sí", "No"]) for _ in range(200)],
    "Nivel_Estres": [random.randint(1, 10) for _ in range(200)],
    "Nivel_Satisfaccion": [random.randint(1, 10) for _ in range(200)],
    "Costo_Citas_Anuales": [random.randint(200, 2000) for _ in range(200)],
    "Costo_Tratamiento": [random.randint(1000, 10000) for _ in range(200)],
    "Costo_Medicamentos": [random.randint(100, 5000) for _ in range(200)],
    "Satisfaccion_Servicio": [random.randint(1, 5) for _ in range(200)],
}

# Crear un DataFrame
df_realistic_explicit = pd.DataFrame(data)

# Guardar el DataFrame en un archivo CSV
df_realistic_explicit.to_csv("_00_aplic_v2_Ejemplo_Data_Realista_53_Columnas.csv", index=False)

print("Archivo 'Ejemplo_Data_Realista_53_Columnas.csv' creado con éxito.")