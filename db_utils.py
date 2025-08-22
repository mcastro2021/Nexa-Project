#!/usr/bin/env python3
"""
Utilidades para la gestión de la base de datos del Nexa WhatsApp Bot
"""

import sqlite3
import argparse
from datetime import datetime, timedelta
import json
from typing import List, Dict, Any

class DatabaseManager:
    def __init__(self, db_path: str = 'nexa_bot.db'):
        self.db_path = db_path
    
    def get_connection(self):
        """Obtener conexión a la base de datos"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def backup_database(self, backup_path: str = None):
        """Crear backup de la base de datos"""
        if backup_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = f'backup_nexa_bot_{timestamp}.db'
        
        import shutil
        shutil.copy2(self.db_path, backup_path)
        print(f"Backup creado: {backup_path}")
        return backup_path
    
    def get_conversation_stats(self, days: int = 30) -> Dict[str, Any]:
        """Obtener estadísticas de conversaciones"""
        with self.get_connection() as conn:
            # Total de conversaciones
            total = conn.execute('SELECT COUNT(*) as count FROM conversations').fetchone()['count']
            
            # Conversaciones en los últimos N días
            date_limit = datetime.now() - timedelta(days=days)
            recent = conn.execute('''
                SELECT COUNT(*) as count FROM conversations 
                WHERE timestamp >= ?
            ''', (date_limit,)).fetchone()['count']
            
            # Conversaciones por día (últimos 7 días)
            daily_stats = conn.execute('''
                SELECT DATE(timestamp) as date, COUNT(*) as count 
                FROM conversations 
                WHERE timestamp >= DATE('now', '-7 days')
                GROUP BY DATE(timestamp)
                ORDER BY date DESC
            ''').fetchall()
            
            # Top palabras clave
            keywords = conn.execute('''
                SELECT message, COUNT(*) as count 
                FROM conversations 
                WHERE timestamp >= DATE('now', '-30 days')
                GROUP BY LOWER(message)
                ORDER BY count DESC
                LIMIT 10
            ''').fetchall()
            
            return {
                'total_conversations': total,
                'recent_conversations': recent,
                'daily_stats': [dict(row) for row in daily_stats],
                'top_keywords': [dict(row) for row in keywords]
            }
    
    def export_conversations(self, output_file: str = None, days: int = None):
        """Exportar conversaciones a JSON"""
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f'conversations_export_{timestamp}.json'
        
        with self.get_connection() as conn:
            query = 'SELECT * FROM conversations'
            params = []
            
            if days:
                date_limit = datetime.now() - timedelta(days=days)
                query += ' WHERE timestamp >= ?'
                params.append(date_limit)
            
            query += ' ORDER BY timestamp DESC'
            
            cursor = conn.execute(query, params)
            conversations = [dict(row) for row in cursor.fetchall()]
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(conversations, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"Conversaciones exportadas: {output_file}")
        return output_file
    
    def clean_old_conversations(self, days: int = 90):
        """Limpiar conversaciones antiguas"""
        with self.get_connection() as conn:
            date_limit = datetime.now() - timedelta(days=days)
            deleted = conn.execute('''
                DELETE FROM conversations 
                WHERE timestamp < ?
            ''', (date_limit,)).rowcount
            conn.commit()
        
        print(f"Eliminadas {deleted} conversaciones antiguas (más de {days} días)")
        return deleted
    
    def get_contact_list(self) -> List[Dict[str, Any]]:
        """Obtener lista de contactos únicos"""
        with self.get_connection() as conn:
            cursor = conn.execute('''
                SELECT DISTINCT phone_number, 
                       COUNT(*) as message_count,
                       MIN(timestamp) as first_message,
                       MAX(timestamp) as last_message
                FROM conversations 
                GROUP BY phone_number
                ORDER BY last_message DESC
            ''')
            return [dict(row) for row in cursor.fetchall()]
    
    def add_contact(self, phone_number: str, name: str = None):
        """Agregar contacto a la base de datos"""
        with self.get_connection() as conn:
            try:
                conn.execute('''
                    INSERT INTO contacts (phone_number, name)
                    VALUES (?, ?)
                ''', (phone_number, name))
                conn.commit()
                print(f"Contacto agregado: {phone_number}")
            except sqlite3.IntegrityError:
                print(f"El contacto {phone_number} ya existe")
    
    def get_conversation_history(self, phone_number: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Obtener historial de conversación de un número específico"""
        with self.get_connection() as conn:
            cursor = conn.execute('''
                SELECT * FROM conversations 
                WHERE phone_number = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (phone_number, limit))
            return [dict(row) for row in cursor.fetchall()]
    
    def search_conversations(self, search_term: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Buscar conversaciones por término"""
        with self.get_connection() as conn:
            cursor = conn.execute('''
                SELECT * FROM conversations 
                WHERE message LIKE ? OR response LIKE ?
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (f'%{search_term}%', f'%{search_term}%', limit))
            return [dict(row) for row in cursor.fetchall()]

def main():
    parser = argparse.ArgumentParser(description='Utilidades de base de datos para Nexa WhatsApp Bot')
    parser.add_argument('--db', default='nexa_bot.db', help='Ruta de la base de datos')
    
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')
    
    # Comando de estadísticas
    stats_parser = subparsers.add_parser('stats', help='Mostrar estadísticas')
    stats_parser.add_argument('--days', type=int, default=30, help='Días para estadísticas recientes')
    
    # Comando de backup
    backup_parser = subparsers.add_parser('backup', help='Crear backup de la base de datos')
    backup_parser.add_argument('--output', help='Ruta del archivo de backup')
    
    # Comando de exportación
    export_parser = subparsers.add_parser('export', help='Exportar conversaciones')
    export_parser.add_argument('--output', help='Archivo de salida')
    export_parser.add_argument('--days', type=int, help='Exportar solo conversaciones de los últimos N días')
    
    # Comando de limpieza
    clean_parser = subparsers.add_parser('clean', help='Limpiar conversaciones antiguas')
    clean_parser.add_argument('--days', type=int, default=90, help='Eliminar conversaciones más antiguas que N días')
    
    # Comando de contactos
    contacts_parser = subparsers.add_parser('contacts', help='Mostrar lista de contactos')
    
    # Comando de búsqueda
    search_parser = subparsers.add_parser('search', help='Buscar conversaciones')
    search_parser.add_argument('term', help='Término de búsqueda')
    search_parser.add_argument('--limit', type=int, default=100, help='Límite de resultados')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    db_manager = DatabaseManager(args.db)
    
    try:
        if args.command == 'stats':
            stats = db_manager.get_conversation_stats(args.days)
            print(f"\n📊 Estadísticas de conversaciones:")
            print(f"Total de conversaciones: {stats['total_conversations']}")
            print(f"Conversaciones recientes ({args.days} días): {stats['recent_conversations']}")
            
            print(f"\n📈 Conversaciones por día (últimos 7 días):")
            for day in stats['daily_stats']:
                print(f"  {day['date']}: {day['count']}")
            
            print(f"\n🔍 Palabras clave más usadas:")
            for keyword in stats['top_keywords'][:5]:
                print(f"  '{keyword['message']}': {keyword['count']} veces")
        
        elif args.command == 'backup':
            backup_path = db_manager.backup_database(args.output)
            print(f"✅ Backup completado: {backup_path}")
        
        elif args.command == 'export':
            export_path = db_manager.export_conversations(args.output, args.days)
            print(f"✅ Exportación completada: {export_path}")
        
        elif args.command == 'clean':
            deleted = db_manager.clean_old_conversations(args.days)
            print(f"✅ Limpieza completada: {deleted} conversaciones eliminadas")
        
        elif args.command == 'contacts':
            contacts = db_manager.get_contact_list()
            print(f"\n📞 Lista de contactos ({len(contacts)} contactos):")
            for contact in contacts:
                print(f"  {contact['phone_number']}: {contact['message_count']} mensajes")
        
        elif args.command == 'search':
            results = db_manager.search_conversations(args.term, args.limit)
            print(f"\n🔍 Resultados de búsqueda para '{args.term}' ({len(results)} resultados):")
            for result in results[:10]:  # Mostrar solo los primeros 10
                print(f"  {result['timestamp']} - {result['phone_number']}: {result['message'][:50]}...")
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    main()
