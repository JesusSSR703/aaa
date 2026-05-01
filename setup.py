#!/usr/bin/env python3
"""
Los profetas — Setup Rápido
Script para configurar rápidamente todo el sistema
"""

import os
import sys
import subprocess

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_step(text):
    print(f"\n✓ {text}")

def print_error(text):
    print(f"\n✗ {text}")

def main():
    print_header("Los profetas — Setup Inicial")
    
    # Paso 1: Verificar Python
    print_step("Verificando Python...")
    if sys.version_info < (3, 7):
        print_error("Se requiere Python 3.7 o superior")
        return False
    print(f"  Python {sys.version.split()[0]} detectado ✓")
    
    # Paso 2: Instalar dependencias
    print_header("Instalando Dependencias")
    try:
        print("  Instalando Flask y flask-cors...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"])
        print_step("Dependencias instaladas")
    except subprocess.CalledProcessError:
        print_error("No se pudieron instalar las dependencias")
        return False
    
    # Paso 3: Crear base de datos
    print_header("Inicializando Base de Datos")
    try:
        print("  Ejecutando seed.py...")
        subprocess.check_call([sys.executable, "seed.py"])
        print_step("Base de datos creada")
    except subprocess.CalledProcessError:
        print_error("Error al crear la base de datos")
        return False
    
    # Paso 4: Verificar archivos
    print_header("Verificando Archivos")
    archivos_requeridos = ['base.py', 'seed.py', 'api.py', 'losprofetas.db']
    todos_presentes = True
    for archivo in archivos_requeridos:
        if os.path.exists(archivo):
            print(f"  ✓ {archivo}")
        else:
            print(f"  ✗ {archivo} (faltante)")
            todos_presentes = False
    
    if not todos_presentes:
        print_error("Algunos archivos están faltando")
        return False
    
    # Paso 5: Resumen
    print_header("✅ Setup Completado Exitosamente!")
    print("""
┌─────────────────────────────────────────────────────┐
│ Próximos pasos:                                     │
│                                                     │
│ 1. Inicia el servidor API:                         │
│    python api.py                                   │
│                                                    │
│ 2. Abre http://localhost:5000 en tu navegador     │
│                                                    │
│ 3. Abre index.html para ver la interfaz web       │
│                                                    │
│ 📚 Documentación: Revisa DATABASE.md               │
│                                                    │
└─────────────────────────────────────────────────────┘
    """)
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
