#!/usr/bin/env python3
"""
Los profetas — Validación y Diagnóstico del Sistema
Verifica que todo esté correctamente configurado
"""

import os
import sys
import sqlite3
from pathlib import Path

def print_header(text):
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")

def check_file(filename):
    exists = os.path.exists(filename)
    status = "✓" if exists else "✗"
    print(f"  {status} {filename}")
    return exists

def check_import(module_name):
    try:
        __import__(module_name)
        print(f"  ✓ {module_name}")
        return True
    except ImportError:
        print(f"  ✗ {module_name} (no instalado)")
        return False

def main():
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║       Los profetas — Validación del Sistema                              ║
║                                                                           ║
║       Verifica que todos los componentes estén configurados               ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """)
    
    all_ok = True
    
    # ==================== ARCHIVOS ====================
    print_header("📁 Archivos Requeridos")
    
    required_files = [
        'base.py',
        'api.py',
        'dashboard.py',
        'seed.py',
        'setup.py',
        'INICIAR_TODO.py',
        'requirements.txt',
        'LEEME_PRIMERO.md',
        'COMPLETO_v2.0.md',
        'DATABASE.md',
    ]
    
    for f in required_files:
        if not check_file(f):
            all_ok = False
    
    # ==================== BASE DE DATOS ====================
    print_header("🗄️  Base de Datos")
    
    db_file = 'losprofetas.db'
    if os.path.exists(db_file):
        print(f"  ✓ {db_file} existe")
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            
            # Verificar tablas
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' ORDER BY name
            """)
            tables = cursor.fetchall()
            
            print(f"\n  Tablas encontradas: {len(tables)}")
            expected_tables = [
                'usuarios', 'nfts', 'comentarios', 'transacciones',
                'ofertas', 'favoritos', 'notificaciones', 'configuracion'
            ]
            
            for table in expected_tables:
                found = any(t[0] == table for t in tables)
                status = "✓" if found else "✗"
                print(f"    {status} {table}")
                if not found:
                    all_ok = False
            
            # Contar registros
            cursor.execute("SELECT COUNT(*) FROM usuarios")
            usuarios = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM nfts")
            nfts = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM transacciones")
            transacciones = cursor.fetchone()[0]
            
            print(f"\n  Datos iniciales:")
            print(f"    • Usuarios: {usuarios}")
            print(f"    • NFTs: {nfts}")
            print(f"    • Transacciones: {transacciones}")
            
            conn.close()
        except Exception as e:
            print(f"  ✗ Error al verificar BD: {e}")
            all_ok = False
    else:
        print(f"  ✗ {db_file} no existe (ejecuta seed.py)")
        all_ok = False
    
    # ==================== DEPENDENCIAS ====================
    print_header("📦 Dependencias Python")
    
    dependencies = [
        'flask',
        'flask_cors',
        'sqlite3',
        'numpy',
        'sklearn',
        'pandas',
        'scipy',
    ]
    
    missing = []
    for dep in dependencies:
        if dep == 'sklearn':
            if not check_import('sklearn'):
                missing.append('scikit-learn')
        elif dep == 'sqlite3':
            if not check_import('sqlite3'):
                missing.append('sqlite3')
        else:
            if not check_import(dep):
                missing.append(dep)
    
    if missing:
        print(f"\n  ⚠️  Dependencias faltantes: {', '.join(missing)}")
        print(f"\n  Instala con: pip install -r requirements.txt")
        all_ok = False
    
    # ==================== INTEGRIDAD DE CÓDIGO ====================
    print_header("📝 Integridad de Código")
    
    # Verificar base.py
    try:
        from base import DatabaseNFT
        print("  ✓ base.py importa correctamente")
        
        # Verificar métodos
        db = DatabaseNFT(':memory:')
        methods = [
            'crear_usuario', 'obtener_usuario',
            'crear_nft', 'obtener_nft',
            'obtener_recomendaciones', 'predecir_precio_nft',
            'detectar_anomalias', 'busqueda_inteligente',
            'analisis_usuario_detallado', 'generar_insights'
        ]
        
        missing_methods = []
        for method in methods:
            if not hasattr(db, method):
                missing_methods.append(method)
        
        if missing_methods:
            print(f"  ✗ Métodos faltantes: {', '.join(missing_methods)}")
            all_ok = False
        else:
            print(f"  ✓ Todos los métodos ML/IA disponibles ({len(methods)})")
        
        db.cerrar()
    except Exception as e:
        print(f"  ✗ Error en base.py: {e}")
        all_ok = False
    
    # ==================== PUERTOS ====================
    print_header("🌐 Puertos")
    
    print("  Puertos requeridos:")
    print("    • 5000 (API REST)")
    print("    • 5001 (Dashboard)")
    print("\n  ⚠️  Verifica que estén disponibles antes de iniciar")
    
    # ==================== RESUMEN ====================
    print_header("📊 Resumen de Validación")
    
    if all_ok:
        print("""
✅ ¡SISTEMA COMPLETO Y LISTO!

Puedes ejecutar:
  • python INICIAR_TODO.py          (Opción fácil)
  • python seed.py && python api.py (Opción manual)

Abre en tu navegador:
  • http://localhost:5001 (Dashboard)
  • http://localhost:5000/api/health (API status)
        """)
    else:
        print("""
⚠️  HAY PROBLEMAS A RESOLVER

Acciones sugeridas:
  1. Instala dependencias: pip install -r requirements.txt
  2. Carga datos de prueba: python seed.py
  3. Verifica que no falten archivos
  4. Intenta nuevamente: python validacion.py
        """)
    
    print("\nPara más información, consulta LEEME_PRIMERO.md\n")
    
    return 0 if all_ok else 1

if __name__ == '__main__':
    sys.exit(main())
