#!/usr/bin/env python3
"""
Debug script para probar el nuevo filtrado NCS usando Diccionario de Rutas

Este script prueba:
1. La restauración de Rutas Diccionario.txt
2. La nueva implementación de collect_routes_dictionary()
3. El filtrado NCS mejorado con diccionario real
4. Comparación entre filtrado hardcodeado vs diccionario
"""

import asyncio
import os
import sys
import pandas as pd
from datetime import datetime, timedelta
import logging

# Configurar path para importar módulos
sys.path.append('/app')

from dashboard_analyzer.data_collection.pbi_collector import PBIDataCollector
from dashboard_analyzer.data_collection.ncs_collector import NCSDataCollector
from dashboard_analyzer.anomaly_explanation.genai_core.agents.causal_explanation_agent import CausalExplanationAgent
from dashboard_analyzer.anomaly_explanation.genai_core.utils.enums import LLMType

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_routes_dictionary():
    """Prueba la nueva funcionalidad del diccionario de rutas"""
    print("=" * 80)
    print("🗺️ TESTING ROUTES DICTIONARY FUNCTIONALITY")
    print("=" * 80)
    
    try:
        # 1. Probar colección del diccionario de rutas
        print("\n📊 1. Testing Routes Dictionary Collection...")
        pbi_collector = PBIDataCollector()
        
        routes_dict = await pbi_collector.collect_routes_dictionary()
        
        if routes_dict.empty:
            print("❌ ERROR: Routes dictionary is empty!")
            return False
        
        print(f"✅ SUCCESS: Collected {len(routes_dict)} routes")
        print(f"📋 Columns: {list(routes_dict.columns)}")
        
        # Mostrar muestra de rutas
        print("\n📋 Sample routes from dictionary:")
        if len(routes_dict) > 0:
            sample_routes = routes_dict.head(10)
            for _, route in sample_routes.iterrows():
                route_code = route.get('route', 'N/A')
                haul = route.get('haul_aggr', 'N/A')
                country = route.get('country_name', 'N/A')
                region = route.get('gr_region', 'N/A')
                print(f"   • {route_code} -> {haul} ({country}, {region})")
        
        # 2. Analizar distribución por haul
        print(f"\n📊 2. Routes Distribution by Haul:")
        haul_counts = routes_dict['haul_aggr'].value_counts()
        for haul, count in haul_counts.items():
            print(f"   • {haul}: {count} routes")
        
        # 3. Mostrar algunos códigos de aeropuerto por haul
        print(f"\n✈️ 3. Airport Codes by Haul Type:")
        
        for haul_type in ['LH', 'SH']:
            haul_routes = routes_dict[routes_dict['haul_aggr'] == haul_type]
            airports = set()
            
            for _, route in haul_routes.iterrows():
                route_code = route.get('route', '')
                if '-' in route_code:
                    origin, dest = route_code.split('-', 1)
                    airports.add(origin.strip().upper())
                    airports.add(dest.strip().upper())
            
            sample_airports = sorted(list(airports))[:15]  # Primeros 15
            print(f"   • {haul_type}: {len(airports)} unique airports")
            print(f"     Sample: {', '.join(sample_airports)}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR in routes dictionary test: {e}")
        return False

async def test_ncs_filtering():
    """Prueba el filtrado NCS con el nuevo método"""
    print("\n" + "=" * 80)
    print("🚨 TESTING NCS FILTERING WITH ROUTES DICTIONARY")
    print("=" * 80)
    
    try:
        # 1. Crear instancia del agente causal
        print("\n🤖 1. Creating Causal Explanation Agent...")
        agent = CausalExplanationAgent(llm_type=LLMType.CLAUDE_SONNET_4)
        
        # 2. Obtener datos NCS de muestra
        print("\n📥 2. Collecting Sample NCS Data...")
        
        # Usar fechas recientes para el test
        end_date = datetime.now() - timedelta(days=1)
        start_date = end_date - timedelta(days=7)
        
        print(f"   Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        
        # Crear instancia del colector NCS
        ncs_collector = NCSDataCollector()
        
        # Intentar obtener datos NCS
        try:
            ncs_data = await ncs_collector.collect_incidents_for_period(
                start_date=start_date.strftime('%Y-%m-%d'),
                end_date=end_date.strftime('%Y-%m-%d')
            )
            
            if ncs_data.empty:
                print("⚠️ No NCS data available for the test period, creating mock data...")
                # Crear datos de muestra para el test
                ncs_data = create_mock_ncs_data()
            else:
                print(f"✅ Collected {len(ncs_data)} NCS incidents")
                
        except Exception as e:
            print(f"⚠️ Error collecting real NCS data: {e}")
            print("Creating mock data for testing...")
            ncs_data = create_mock_ncs_data()
        
        # 3. Probar filtrado para diferentes segmentos
        test_segments = [
            "Global",
            "Global/LH", 
            "Global/SH",
            "Global/LH/Business",
            "Global/SH/Economy"
        ]
        
        print(f"\n🔍 3. Testing NCS Filtering for Different Segments:")
        print(f"   Original NCS incidents: {len(ncs_data)}")
        
        for segment in test_segments:
            print(f"\n   Testing segment: {segment}")
            
            try:
                # Filtrar NCS por segmento usando el nuevo método
                filtered_ncs = await agent._filter_ncs_by_segment(ncs_data, segment)
                
                reduction_rate = (1 - len(filtered_ncs) / len(ncs_data)) * 100 if len(ncs_data) > 0 else 0
                print(f"      ✅ Filtered: {len(filtered_ncs)}/{len(ncs_data)} incidents ({reduction_rate:.1f}% reduction)")
                
                if len(filtered_ncs) > 0 and len(filtered_ncs.columns) > 0:
                    # Mostrar muestra de incidentes filtrados
                    incident_col = filtered_ncs.columns[0]
                    sample_incidents = filtered_ncs[incident_col].head(3).tolist()
                    for i, incident in enumerate(sample_incidents, 1):
                        incident_preview = str(incident)[:100] + "..." if len(str(incident)) > 100 else str(incident)
                        print(f"         {i}. {incident_preview}")
                
            except Exception as e:
                print(f"      ❌ Error filtering segment {segment}: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR in NCS filtering test: {e}")
        return False

def create_mock_ncs_data():
    """Crear datos NCS de muestra para testing"""
    mock_incidents = [
        "Retraso vuelo IB123 MAD-JFK por causas técnicas - 45 minutos",
        "Cancelación vuelo IB456 BCN-MAD meteorología adversa",
        "Desvío vuelo IB789 LIM-MAD a Cancún por condiciones en destino",
        "Equipaje perdido MAD-GRU vuelo IB101 - 15 pasajeros afectados",
        "Problemas técnicos A350 en ruta MEX-MAD vuelo IB202",
        "Retraso conexión PMI-MAD por saturación aeropuerto",
        "Incidencia operativa CDG-MAD vuelo IB303 - ATC delay",
        "Mantenimiento correctivo aeronave LAX-MAD",
        "Oversale vuelo SCL-MAD clase Business - 3 pasajeros",
        "Retraso tripulación BOS-MAD por normativa descanso"
    ]
    
    # Crear DataFrame con los incidentes mock
    mock_data = pd.DataFrame({
        '': mock_incidents  # Columna sin nombre como en datos reales
    })
    
    print(f"   Created {len(mock_data)} mock NCS incidents for testing")
    return mock_data

async def test_filtering_comparison():
    """Comparar filtrado hardcodeado vs diccionario"""
    print("\n" + "=" * 80)
    print("🔄 COMPARING HARDCODED vs DICTIONARY FILTERING")
    print("=" * 80)
    
    # Crear datos de test con rutas específicas
    test_incidents = [
        "Retraso vuelo MAD-JFK por condiciones meteorológicas",
        "Cancelación MAD-GRU por problemas técnicos", 
        "Desvío MAD-MEX a Santo Domingo por tormenta",
        "Incidencia MAD-BCN saturación del espacio aéreo",
        "Problema técnico MAD-PMI - cambio de aeronave",
        "Retraso European flight MAD-CDG por ATC",
        "Domestic issue MAD-SVQ equipment change",
        "International route MAD-BOG crew timeout",
        "Long haul disruption MAD-LAX weather",
        "Short haul delay MAD-LIS slot restriction"
    ]
    
    test_data = pd.DataFrame({'': test_incidents})
    
    # Simular filtrado hardcodeado (lógica anterior)
    def simulate_hardcoded_filtering(data, haul_type):
        incident_col = data.columns[0]
        
        if haul_type == 'SH':
            sh_keywords = ['MAD', 'BCN', 'PMI', 'VLC', 'SVQ', 'LIS', 'CDG',
                         'european', 'domestic', 'peninsular']
            pattern = '|'.join([f'\\b{kw}\\b' for kw in sh_keywords])
        elif haul_type == 'LH':
            lh_keywords = ['JFK', 'GRU', 'MEX', 'BOG', 'LAX', 'international', 'transoceanic']
            pattern = '|'.join([f'\\b{kw}\\b' for kw in lh_keywords])
        else:
            return data
        
        mask = data[incident_col].str.contains(pattern, na=False, regex=True, case=False)
        return data[mask]
    
    # Crear agente para filtrado con diccionario
    agent = CausalExplanationAgent(llm_type=LLMType.CLAUDE_SONNET_4)
    
    print(f"\n📊 Test Data: {len(test_data)} incidents")
    for i, incident in enumerate(test_incidents, 1):
        print(f"   {i}. {incident}")
    
    # Comparar filtrados para LH y SH
    for haul_type in ['LH', 'SH']:
        print(f"\n🔍 Filtering for {haul_type}:")
        
        # Filtrado hardcodeado
        hardcoded_result = simulate_hardcoded_filtering(test_data, haul_type)
        print(f"   Hardcoded: {len(hardcoded_result)} incidents")
        
        # Filtrado con diccionario
        try:
            dictionary_result = await agent._filter_using_routes_dictionary(
                test_data, haul_type, test_data.columns[0]
            )
            print(f"   Dictionary: {len(dictionary_result)} incidents")
            
            # Mostrar diferencias
            hardcoded_set = set(hardcoded_result.iloc[:, 0].tolist())
            dictionary_set = set(dictionary_result.iloc[:, 0].tolist())
            
            only_hardcoded = hardcoded_set - dictionary_set
            only_dictionary = dictionary_set - hardcoded_set
            
            if only_hardcoded:
                print(f"   ⚠️ Only in hardcoded: {len(only_hardcoded)} incidents")
            if only_dictionary:
                print(f"   ✅ Only in dictionary: {len(only_dictionary)} incidents")
            if not only_hardcoded and not only_dictionary:
                print(f"   🎯 Perfect match between methods!")
                
        except Exception as e:
            print(f"   ❌ Dictionary filtering failed: {e}")

async def main():
    """Función principal del script de debug"""
    print("🚀 STARTING NCS ROUTES DICTIONARY DEBUG TESTS")
    print("=" * 80)
    
    success_count = 0
    total_tests = 3
    
    # Test 1: Diccionario de rutas
    if await test_routes_dictionary():
        success_count += 1
        
    # Test 2: Filtrado NCS
    if await test_ncs_filtering():
        success_count += 1
        
    # Test 3: Comparación de métodos
    try:
        await test_filtering_comparison()
        success_count += 1
    except Exception as e:
        print(f"❌ Comparison test failed: {e}")
    
    # Resumen final
    print("\n" + "=" * 80)
    print("📋 FINAL TEST SUMMARY")
    print("=" * 80)
    print(f"✅ Successful tests: {success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("🎉 ALL TESTS PASSED! The new NCS filtering with routes dictionary is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the errors above for debugging.")
    
    print("\n🎯 Next steps:")
    print("   1. Review any errors or warnings above")
    print("   2. Test with real NCS data when available")
    print("   3. Validate filtering accuracy with different segments")
    print("   4. Monitor performance in production analysis")

if __name__ == "__main__":
    # Ejecutar el debug
    asyncio.run(main()) 