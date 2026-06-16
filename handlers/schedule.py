#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
معالج الجدول الدراسي
"""

from telegram import Update
from telegram.ext import ContextTypes
from database import db

DAYS = {
    'saturday': 'السبت',
    'sunday': 'الأحد',
    'monday': 'الاثنين',
    'tuesday': 'الثلاثاء',
    'wednesday': 'الأربعاء',
    'thursday': 'الخميس',
    'friday': 'الجمعة'
}

async def show_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """عرض الجدول الدراسي"""
    classes = db.get_all_classes()
    
    if not classes:
        await update.message.reply_text(
            "❌ لا يوجد محاضرات مسجلة حالياً.",
            parse_mode="Markdown"
        )
        return
    
    schedule_text = "📅 **الجدول الدراسي**\n\n"
    
    current_day = None
    for class_info in classes:
        if class_info['day_of_week'] != current_day:
            current_day = class_info['day_of_week']
            schedule_text += f"\n**{DAYS.get(current_day, current_day)}**\n"
        
        schedule_text += (
            f"📚 {class_info['subject']}\n"
            f"   👨‍🏫 الأستاذ: {class_info['professor']}\n"
            f"   ⏰ {class_info['start_time']} - {class_info['end_time']}\n"
            f"   🏛️ القاعة: {class_info['room']}\n\n"
        )
    
    await update.message.reply_text(
        schedule_text,
        parse_mode="Markdown"
    )

