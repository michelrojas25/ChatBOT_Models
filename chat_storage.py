import sqlite3
from datetime import datetime
import threading

class AlmacenamientoChat:
    def __init__(self):
        # Usar un thread local para manejar las conexiones
        self.thread_local = threading.local()
        
    def get_connection(self):
        # Crear una conexión por hilo
        if not hasattr(self.thread_local, "conexion"):
            self.thread_local.conexion = sqlite3.connect(':memory:', check_same_thread=False)
            self.crear_tablas()
        return self.thread_local.conexion
    
    def crear_tablas(self):
        # Crear tablas para almacenar conversaciones y mensajes
        with self.get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS conversaciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS mensajes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_conversacion INTEGER,
                    rol TEXT,
                    contenido TEXT,
                    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(id_conversacion) REFERENCES conversaciones(id)
                )
            ''')
    
    def iniciar_conversacion(self, titulo):
        # Iniciar una nueva conversación
        with self.get_connection() as conn:
            cursor = conn.execute('''
                INSERT INTO conversaciones (titulo) VALUES (?)
            ''', (titulo,))
            return cursor.lastrowid
    
    def guardar_mensaje(self, id_conversacion, rol, contenido):
        # Guardar un mensaje en la conversación
        with self.get_connection() as conn:
            conn.execute('''
                INSERT INTO mensajes (id_conversacion, rol, contenido) 
                VALUES (?, ?, ?)
            ''', (id_conversacion, rol, contenido))
    
    def obtener_historial(self, id_conversacion):
        # Obtener el historial de una conversación
        conn = self.get_connection()
        cursor = conn.execute('''
            SELECT rol, contenido, fecha_hora 
            FROM mensajes
            WHERE id_conversacion = ?
            ORDER BY fecha_hora
        ''', (id_conversacion,))
        return cursor.fetchall()
    
    def exportar_conversacion(self, id_conversacion, formato='txt'):
        # Exportar la conversación en un formato específico
        historial = self.obtener_historial(id_conversacion)
        if formato == 'txt':
            return self.exportar_como_txt(historial)
    
    def exportar_como_txt(self, historial):
        # Exportar como texto plano
        texto_exportado = ""
        for rol, contenido, fecha_hora in historial:
            texto_exportado += f"[{fecha_hora}] {rol}: {contenido}\n"
        return texto_exportado
    
    def eliminar_conversacion(self, id_conversacion):
        # Eliminar una conversación y sus mensajes
        with self.get_connection() as conn:
            conn.execute('''
                DELETE FROM mensajes 
                WHERE id_conversacion = ?
            ''', (id_conversacion,))
            conn.execute('''
                DELETE FROM conversaciones 
                WHERE id = ?
            ''', (id_conversacion,))
    
    def obtener_todas_conversaciones(self):
        # Obtener lista de todas las conversaciones
        cursor = self.get_connection().execute('''
            SELECT id, titulo, fecha_creacion 
            FROM conversaciones 
            ORDER BY fecha_creacion DESC
        ''')
        return cursor.fetchall()
    
    def buscar_en_conversaciones(self, texto_busqueda):
        # Buscar texto en las conversaciones
        cursor = self.get_connection().execute('''
            SELECT DISTINCT c.id, c.titulo, c.fecha_creacion
            FROM conversaciones c
            JOIN mensajes m ON c.id = m.id_conversacion
            WHERE m.contenido LIKE ?
            ORDER BY c.fecha_creacion DESC
        ''', (f'%{texto_busqueda}%',))
        return cursor.fetchall()