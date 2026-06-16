#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إدارة قاعدة البيانات
"""

import sqlite3
import json
from datetime import datetime
import config
from typing import List, Dict, Optional

class Database:
    """فئة إدارة قاعدة البيانات"""
    
    def __init__(self, db_path: str = config.DATABASE_PATH):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        """الحصول على اتصال بقاعدة البيانات"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """إنشاء جداول قاعدة البيانات"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # جدول المستخدمين
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                is_member BOOLEAN DEFAULT 0,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_admin BOOLEAN DEFAULT 0
            )
        ''')
        
        # جدول المحاضرات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS classes (
                class_id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                professor TEXT,
                day_of_week TEXT,
                start_time TEXT,
                end_time TEXT,
                room TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول التذكيرات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                reminder_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                class_id INTEGER,
                reminder_time TEXT,
                is_enabled BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (class_id) REFERENCES classes(class_id)
            )
        ''')
        
        # جدول الأسئلة
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                question_id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT,
                question TEXT NOT NULL,
                options TEXT,
                correct_answer TEXT,
                difficulty TEXT DEFAULT 'medium',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول نتائج المسابقات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quiz_results (
                result_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                subject TEXT,
                score INTEGER,
                total_questions INTEGER,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # جدول المعدل الدراسي
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS grades (
                grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                subject TEXT,
                grade REAL,
                credit_hours INTEGER,
                semester TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # ========== عمليات المستخدمين ==========
    def add_user(self, user_id: int, username: str, is_member: bool = False):
        """إضافة مستخدم جديد"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO users (user_id, username, is_member, is_admin)
            VALUES (?, ?, ?, ?)
        ''', (user_id, username, is_member, user_id in config.ADMIN_IDS))
        conn.commit()
        conn.close()
    
    def is_member(self, user_id: int) -> bool:
        """التحقق من عضوية المستخدم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT is_member FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else False
    
    def update_membership(self, user_id: int, is_member: bool):
        """تحديث حالة العضوية"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET is_member = ? WHERE user_id = ?', (is_member, user_id))
        conn.commit()
        conn.close()
    
    # ========== عمليات المحاضرات ==========
    def add_class(self, subject: str, professor: str, day: str, start_time: str, end_time: str, room: str):
        """إضافة محاضرة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO classes (subject, professor, day_of_week, start_time, end_time, room)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (subject, professor, day, start_time, end_time, room))
        conn.commit()
        class_id = cursor.lastrowid
        conn.close()
        return class_id
    
    def get_classes_by_day(self, day: str) -> List[Dict]:
        """الحصول على المحاضرات حسب اليوم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM classes WHERE day_of_week = ? ORDER BY start_time', (day,))
        classes = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return classes
    
    def get_all_classes(self) -> List[Dict]:
        """الحصول على جميع المحاضرات"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM classes ORDER BY day_of_week, start_time')
        classes = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return classes
    
    def delete_class(self, class_id: int):
        """حذف محاضرة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM classes WHERE class_id = ?', (class_id,))
        conn.commit()
        conn.close()
    
    # ========== عمليات التذكيرات ==========
    def add_reminder(self, user_id: int, class_id: int, reminder_time: str):
        """إضافة تذكير"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO reminders (user_id, class_id, reminder_time)
            VALUES (?, ?, ?)
        ''', (user_id, class_id, reminder_time))
        conn.commit()
        conn.close()
    
    def get_user_reminders(self, user_id: int) -> List[Dict]:
        """الحصول على تذكيرات المستخدم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT r.*, c.subject, c.start_time
            FROM reminders r
            JOIN classes c ON r.class_id = c.class_id
            WHERE r.user_id = ? AND r.is_enabled = 1
        ''', (user_id,))
        reminders = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return reminders
    
    # ========== عمليات الأسئلة والمسابقات ==========
    def add_question(self, subject: str, question: str, options: List[str], correct_answer: str, difficulty: str = 'medium'):
        """إضافة سؤال"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO questions (subject, question, options, correct_answer, difficulty)
            VALUES (?, ?, ?, ?, ?)
        ''', (subject, json.dumps(options), correct_answer, difficulty))
        conn.commit()
        conn.close()
    
    def get_questions_by_subject(self, subject: str, limit: int = 5) -> List[Dict]:
        """الحصول على أسئلة حسب المادة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM questions WHERE subject = ? ORDER BY RANDOM() LIMIT ?
        ''', (subject, limit))
        questions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return questions
    
    def save_quiz_result(self, user_id: int, subject: str, score: int, total: int):
        """حفظ نتيجة المسابقة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO quiz_results (user_id, subject, score, total_questions)
            VALUES (?, ?, ?, ?)
        ''', (user_id, subject, score, total))
        conn.commit()
        conn.close()
    
    # ========== عمليات المعدل ==========
    def add_grade(self, user_id: int, subject: str, grade: float, credit_hours: int, semester: str):
        """إضافة درجة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO grades (user_id, subject, grade, credit_hours, semester)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, subject, grade, credit_hours, semester))
        conn.commit()
        conn.close()
    
    def calculate_gpa(self, user_id: int, semester: str = None) -> float:
        """حساب المعدل GPA"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if semester:
            cursor.execute('''
                SELECT SUM(grade * credit_hours) as total_points,
                       SUM(credit_hours) as total_hours
                FROM grades
                WHERE user_id = ? AND semester = ?
            ''', (user_id, semester))
        else:
            cursor.execute('''
                SELECT SUM(grade * credit_hours) as total_points,
                       SUM(credit_hours) as total_hours
                FROM grades
                WHERE user_id = ?
            ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result and result[1]:
            return result[0] / result[1]
        return 0.0
    
    def get_user_grades(self, user_id: int) -> List[Dict]:
        """الحصول على درجات المستخدم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM grades WHERE user_id = ? ORDER BY semester DESC', (user_id,))
        grades = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return grades

# إنشاء كائن قاعدة البيانات العام
db = Database()
